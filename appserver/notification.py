# -*- coding: UTF-8 -*-

import logging
import threading
import datetime
from kombu.mixins import ConsumerMixin
from kombu import Connection
from kombu import Exchange, Queue
from model import NovaNotification
from model import CinderNotification
from model import GlanceNotification
from model import Server
from model import Volume
from model import Snapshot
from model import Image
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
import settings as conf
import novaclient.v1_1.client as nvclient
import cinderclient.v1.client as ciclient
import glanceclient as glclient


log = logging.getLogger("cloudapi")

nova_client = nvclient.Client(auth_url = conf.openstack_api['keystone_url'],
                              username = conf.openstack_api['user'],
                              api_key = conf.openstack_api['password'],
                              project_id = conf.openstack_api['tenant_name'])

cinder_client = ciclient.Client(auth_url = conf.openstack_api['keystone_url'],
                                username = conf.openstack_api['user'],
                                api_key = conf.openstack_api['password'],
                                project_id = conf.openstack_api['tenant_name'])

class Worker(ConsumerMixin):
    def __init__(self, connection, db_engine):
        self.connection = connection
        self.db_engine = db_engine


class NovaWorker(Worker):
    def get_consumers(self, Consumer, channel):
        exchange = Exchange('nova', type='topic', durable=False, 
                            auto_delete=False, internal=False)
        queues = [Queue('cloudapi_nova', exchange, 
                        routing_key='notifications.info',
                        no_ack=True)]
        return [Consumer(queues=queues,
                         accept=['json'],
                         callbacks=[self.process_task])]


    def process_task(self, body, message):
        Session = sessionmaker(self.db_engine)
        db = Session()
    
        # Save notification in database
        payload = body.get('payload')
        event_type = body.get('event_type', '')
        #log.debug(body);
        notification = NovaNotification(
                        message_id = body.get('message_id', ''),
                        occurred_at = body.get('timestamp', ''),
                        event_type = event_type,
                        instance_id = payload.get('instance_id', ''),
                        state = payload.get('state', ''),
                        old_state = payload.get('old_state', ''),
                        new_task_state = payload.get('new_task_state', ''),
                        old_task_state = payload.get('old_task_state', ''))
        db.add(notification)
        db.commit()

        if event_type == 'compute.instance.update':
            self.update_server_state(db, notification);
        elif event_type == 'compute.instance.delete.end':
            self.delete_server(db, notification);

        db.close()


    def update_server_state(self, db, notification):
        server = db.query(Server).filter(Server.instance_id==notification.instance_id).first()
        if server:
            # Update server state
            server.state = notification.state
            server.task_state = notification.new_task_state
            server.updated_at = datetime.datetime.now()

            if notification.state=='deleted':
                server.deleted = 1
                server.deleted_at = datetime.datetime.now()

            db.add(server)
            db.commit()

            try:
                instance = nova_client.servers.get(notification.instance_id).to_dict()
                if notification.state == 'active':
                    # Get server's IP
                    ips = []
                    for net in instance.get('addresses').values():
                        for n in net:
                            if n.get('addr'):
                                ips.append(n.get('addr'))
                    server.ip = ','.join(ips)

                if notification.state == 'error':
                    code = instance.get('fault')['code']
                    msg = instance.get('fault')['message']
                    server.fault = 'Error %d: %s' % (code, msg)

                db.add(server)
                db.commit()

            except Exception, e:
                log.info(e)

    
    def delete_server(self, db, notification):
        server = db.query(Server).filter(Server.instance_id==notification.instance_id).first()
        if server:
            # Update server state
            server.updated_at = datetime.datetime.now()
            server.deleted = 1
            server.deleted_at = datetime.datetime.now()

            db.add(server)
            db.commit()


class CinderWorker(Worker):
    def get_consumers(self, Consumer, channel):
        exchange = Exchange('cinder', type='topic', durable=False,
                            auto_delete=False, internal=False)
        queues = [Queue('cloudapi_cinder', exchange,
                        routing_key='notifications.info',
                        no_ack=True)]
        return [Consumer(queues=queues,
                         accept=['json'],
                         callbacks=[self.process_task])]

    def process_task(self, body, message):
        Session = sessionmaker(self.db_engine)
        db = Session()

        payload = body.get('payload')
        event_type = body.get('event_type', '')
        #log.debug(body)
        notification = CinderNotification(
                        message_id = body.get('message_id', ''),
                        occurred_at = body.get('timestamp', ''),
                        event_type = event_type,
                        volume_id = payload.get('volume_id', ''),
                        status = payload.get('status', ''))
        db.add(notification)
        db.commit()

        self.update_volume_status(db, notification)
        db.close()

    
    def update_volume_status(self, db, notification):
        volume = db.query(Volume).filter(Volume.volume_id==notification.volume_id).first()
        if volume:
            volume.status = notification.status
            volume.updated_at = datetime.datetime.now()
             
            if notification.event_type == 'volume.delete.end':
                volume.deleted = 1
                volume.deleted_at = datetime.datetime.now()

            if notification.event_type == 'volume.attach.end':
                attached_instance_id = ''
                try:
                    # notification中不包含attachments信息, 要重新从cinder取
                    ret = cinder_client.volumes.get(volume.volume_id)
                    if ret.attachments:
                        for att in ret.attachments:
                            if att['volume_id'] == volume.volume_id:
                                attached_instance_id = att['server_id']
                except Exception, e:
                    log.info(e)

                if attached_instance_id:
                    server = db.query(Server).filter(Server.instance_id==attached_instance_id).first()
                    if server:
                        volume.attached_to = server.id

            if notification.event_type == 'volume.detach.end': 
                if notification.status == 'available':
                    volume.attached_to = ''

            db.add(volume)
            db.commit()


class GlanceWorker(Worker):
    def get_consumers(self, Consumer, channel):
        exchange = Exchange('glance', type='topic', durable=False,
                            auto_delete=False, internal=False)
        queues = [Queue('cloudapi_glance', exchange,
                        routing_key='notifications.info',
                        no_ack=True)]
        return [Consumer(queues=queues,
                         accept=['json'],
                         callbacks=[self.process_task])]


    def process_task(self, body, message):
        Session = sessionmaker(self.db_engine)
        db = Session()

        payload = body.get('payload')
        event_type = body.get('event_type', '')
        log.debug(body)

        notification = GlanceNotification(
                        message_id = body.get('message_id', ''),
                        occurred_at = body.get('timestamp', ''),
                        event_type = event_type,
                        snapshot_id = payload.get('id', ''),
                        status = payload.get('status', ''))
        db.add(notification)
        db.commit()

        # notification里返回的可能是snapshot, 也可能是image
        self.update_snapshot_status(db, notification, payload)
        self.update_image_status(db, notification, payload)
        db.close


    def update_snapshot_status(self, db, notification, payload):
        snapshot = db.query(Snapshot).filter(Snapshot.snapshot_id==notification.snapshot_id).first()
        if snapshot:
            snapshot.status = notification.status
            snapshot.size = payload.get('size', 0)
            snapshot.updated_at = datetime.datetime.now()

            if snapshot.status == 'deleted':
                snapshot.deleted = 1
                snapshot.deleted_at = datetime.datetime.now()

            db.add(snapshot)
            db.commit()
   

    def update_image_status(self, db, notification, payload):
        image = db.query(Image).filter(Image.image_id==notification.snapshot_id).first()
        if image:
            image.status = notification.status
            image.size = payload.get('size', 0)
            image.updated_at = datetime.datetime.now()

            if image.status == 'deleted':
                image.deleted = 1
                image.deleted_at = datetime.datetime.now()

            db.add(image)
            db.commit()
   

class NotifyListener(threading.Thread):
    def __init__(self, db_engine):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.db_engine = db_engine


class NovaNotifyListener(NotifyListener):
    def run(self):
        mq = conf.openstack_message_queue
        url = "amqp://%s:%s@%s:%d//" % (mq['nova_user'],
                                        mq['nova_password'],
                                        mq['host'],
                                        mq['port'])
        with Connection(url) as conn:
            try:
                worker = NovaWorker(conn, self.db_engine)
                worker.run()
            except KeyboardInterrupt:
                pass


class CinderNotifyListener(NotifyListener):
    def run(self):
        mq = conf.openstack_message_queue
        url = "amqp://%s:%s@%s:%d//" % (mq['nova_user'],
                                        mq['nova_password'],
                                        mq['host'],
                                        mq['port'])
        with Connection(url) as conn:
            try:
                worker = CinderWorker(conn, self.db_engine)
                worker.run()
            except KeyboardInterrupt:
                pass


class GlanceNotifyListener(NotifyListener):
    def run(self):
        mq = conf.openstack_message_queue
        url = "amqp://%s:%s@%s:%d//" % (mq['nova_user'],
                                        mq['nova_password'],
                                        mq['host'],
                                        mq['port'])
        with Connection(url) as conn:
            try:
                worker = GlanceWorker(conn, self.db_engine)
                worker.run()
            except KeyboardInterrupt:
                pass
