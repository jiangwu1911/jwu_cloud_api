import logging
import threading
from kombu.mixins import ConsumerMixin
from kombu import Connection
from kombu import Exchange, Queue
import settings as conf

log = logging.getLogger("cloudapi")

class Worker(ConsumerMixin):
    def __init__(self, connection):
        self.connection = connection


class NovaWorker(Worker):
    def get_consumers(self, Consumer, channel):
        exchange = Exchange('nova', type='topic', durable=False, 
                            auto_delete=False, internal=False)
        queues = [Queue('cloudapi_nova', exchange, 
                        routing_key='notifications.info')]
        return [Consumer(queues=queues,
                         accept=['json'],
                         callbacks=[self.process_task])]

    def process_task(self, body, message):
        log.debug("Got nova notification: %s" % body)


class NotifyListener(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.setDaemon(True)


class NovaNotifyListener(NotifyListener):
    def run(self):
        mq = conf.openstack_message_queue
        url = "amqp://%s:%s@%s:%d//" % (mq['nova_user'],
                                        mq['nova_password'],
                                        mq['host'],
                                        mq['port'])
        with Connection(url) as conn:
            try:
                worker = NovaWorker(conn)
                worker.run()
            except KeyboardInterrupt:
                pass
