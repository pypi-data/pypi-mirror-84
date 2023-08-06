from flask import Blueprint, request

from sitepipes.database.integrations import Device, Provider

integrations = Blueprint('integrations', __name__)


@integrations.route('/api/set_device')
def set_device():
    """ Registers a new device (ie. Apple Watch) for a user """
    r = request.get_json()
    Device(**r.params).save()


@integrations.route('/api/set_provider')
def set_provider():
    """ Registers a new provider (ie. Mayo Clinic) for a user """
    r = request.get_json()
    Provider(**r.params).save()
