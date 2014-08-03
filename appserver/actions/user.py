import logging
from bottle import request
import model
import utils

log = logging.getLogger("cloudapi")

def list_user(request, db):
    results = db.query(model.User)
    return utils.sql_results_to_json(results, 'users') 
