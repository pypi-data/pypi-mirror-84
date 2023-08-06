from flask import Blueprint, request


workflows = Blueprint('workflows', __name__)


@workflows.route('/api/run_')
def run_():
    r = request.get_json()
    return r
