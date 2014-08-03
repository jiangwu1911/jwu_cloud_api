import logging
from bottle import request
import model
import utils
from common import pre_check

log = logging.getLogger("cloudapi")


@pre_check
def list_user(request, db):
    results = db.query(model.User)
    return utils.sql_results_to_json(results, 'users') 
