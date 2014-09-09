# -*- coding: UTF-8 -*-

import traceback
import datetime
import os
from os.path import getsize
import thread

import logging
from actions.common import get_input
from actions.common import get_required_input
from actions.common import handle_db_error
from actions.common import write_operation_log
from actions.common import is_sys_admin_or_dept_admin
from actions.common import pre_check
from actions.user import find_user
from utils import obj_array_to_json
from utils import obj_to_json
from model import Image 
from error import ImageNotFoundError
from error import UnsupportedOperationError
from error import UploadFolderNotSetError
from error import ImageUploadError
from actions.openstack.common import *

log = logging.getLogger("cloudapi")


@pre_check
@openstack_call
def list_image(req, db, context):
    images = db.query(Image).filter(Image.deleted==0).all()
    return obj_array_to_json(images, 'images')


def find_image(db, context, image_id):
    image = db.query(Image).filter(Image.deleted==0,
                                    Image.id==image_id).first()
    if image == None:
        raise ImageNotFoundError(image_id)
    return image


@pre_check
@openstack_call
def show_image(req, db, context, image_id):
    image = find_image(db, context, image_id)
    return obj_to_json(image, 'image')


@pre_check
@openstack_call
def create_image(req, db, context):
    if req.POST.imagefile is None:
        raise ImageUploadError('参数imagefile不存在')
        
    # image文件先保存在临时文件夹
    folder = conf.upload_files_path
    if os.path.exists(folder) == False:
        os.mkdir(folder)
    try:
        dest = '%s/%s' % (folder, req.POST.imagefile.filename)
        req.POST.imagefile.save(dest, overwrite=True)
    except (Exception) as e:
        raise ImageUploadError(e)

    data = { 'name': req.POST.name,
             'description': '',
             'source_type': 'file',
             'image_file': dest,
             'disk_format': 'qcow2',
             'architecture': '',
             'minimum_disk': 0,
             'minimum_ram': 0,
             'visibility': 'public',
             'protected': False }

    image = glance_client().images.create(container_format="bare",
                                          disk_format=data['disk_format'],
                                          visibility=data['visibility'],
                                          protected=data['protected'],
                                          min_disk=data['minimum_disk'],
                                          min_ram=data['minimum_ram'],
                                          name=data['name']);

    # 上传image文件内容
    thread.start_new_thread(image_upload,
                            (image.id, data['image_file']))

    item = Image(name = data['name'],
                 image_id = image.id,
                 status = 'creating',
                 created_at = datetime.datetime.now())
    db.add(item)
    db.commit()

    log.debug(item)
    return "{'success': {'image_id': %d}}" % item.id 


def image_upload(image_id, filename):
    size = getsize(filename)
    with open(filename, 'rb') as file:
        return glance_client().images.upload(image_id, file, size)


@pre_check
@openstack_call
def delete_image(req, db, context, image_id):
    image = find_image(db, context, image_id)
    image.status = 'deleting'
    db.add(image)
    db.commit()

    try: 
        glance_client().images.delete(image.image_id)
    except gl_ex.NotFound, e:
        image.deleted = 1
        image.deleted_at = datetime.datetime.now()
        db.add(image)
        db.commit()

    write_operation_log(db,
                        user_id = context['user'].id,
                        resource_type = 'image',
                        resource_id = image_id,
                        resource_uuid = image.image_id,
                        event = 'delete image')
    db.commit()
 

@pre_check
@openstack_call
def update_image(req, db, context, image_id):
    image = find_image(db, context, image_id)
    if image == None:
        raise ImageNotFoundError(image_id)

    name = get_input(req, 'name')
    if name:
        image.name = name

    db.add(image)
    db.commit()
