# -*- coding: UTF-8 -*-

import logging
from sqlalchemy import or_

from model import Dept
from model import User
import utils
from common import pre_check
from common import get_user_by_token
from common import get_all_depts
from utils import sql_results_to_json

log = logging.getLogger("cloudapi")


@pre_check
def list_dept(req, db):
    """Return all dept and sub depts"""
    user = get_user_by_token(req, db)
    depts = get_all_depts(db, user)
    print depts
    return sql_results_to_json(depts, 'depts')
