import logging
import model
import utils
from common import pre_check
from common import get_input
from common import get_required_input
from common import is_dept_admin
from error import NotDeptAdminError
from model import User
from utils import sql_result_to_json

log = logging.getLogger("cloudapi")


@pre_check
def list_user(req, db, context):
    depts = []
    dept_id = get_input(req, 'dept_id')

    if dept_id and dept_id!="":
        dept_id = int(dept_id)
        if is_dept_admin(context, dept_id) == False:
            raise NotDeptAdminError(dept_id)
        depts.append(dept_id)
    else:
        for d in context['depts']:        
            depts.append('%d' % d.id)

    users = db.query(User).filter(User.dept_id.in_(depts))
    return sql_result_to_json(users, 'users')
