# -*- coding: UTF-8 -*-

import traceback
import datetime
import os
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
    pass


def find_image(db, context, image_id):
    pass


@pre_check
@openstack_call
def show_image(req, db, context, image_id):
    pass


@pre_check
@openstack_call
def create_image(req, db, context):
    folder = conf.upload_folder
    if os.path.exists(folder) == False:
        os.mkdir(folder)

    if req.POST.imagefile is None:
        raise ImageUploadError('参数imagefile不存在')
        
    try:
        dest = '%s/%s' % (folder, req.POST.imagefile.filename)
        req.POST.imagefile.save(dest, overwrite=True)
    except (Exception) as e:
        raise ImageUploadError(e)

    image = glance_client().images.create(name=req.POST.name)
    data = { 'image_file': dest }
    thread.start_new_thread(image_update,
                            (image.id,),
                            {'data': data})

    image = Image(name = req.POST.name,
                  image_id = image.id,
                  status = 'creating',
                  created_at = datetime.datetime.now())
    db.add(image)
    return 'success'


def image_update(image_id, **kwargs):
    return  glance_client().images.update(image_id, None, **kwargs)


@pre_check
@openstack_call
def delete_image(req, db, context, id):
    pass


@pre_check
@openstack_call
def update_image(req, db, context, id):
    pass
