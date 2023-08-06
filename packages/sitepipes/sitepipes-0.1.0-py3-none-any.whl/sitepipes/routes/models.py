from flask import Blueprint, request

from sitepipes import db
from sitepipes.util.exceptions import ModelNotFoundError

models = Blueprint('models', __name__)


class Model(db.Document):
    """ A machine learning model """
    model_id = db.PrimaryKey()
    model_name = db.StringField()
    model_path = db.StringField()

    def to_json(self):
        return {'model_name': self.model_name, 'model_path': self.model_path}


@models.route('/api/create_model', methods=['POST'])
def create_model():
    """ Updates a model """
    data = request.get_json()
    params = data.get('params', {'model_id': 1})
    entry = Model(**params)
    entry.save()
    return entry.to_json()


@models.route('/api/read_model', methods=['GET'])
def read_model():
    """ Updates a model """
    data = request.get_json()
    params = data.get('params', {'model_id': 1})
    entry = Model.objects(model_id=params.model_id).first()
    if not entry:
        return {'error': ModelNotFoundError()}
    return entry.to_json()


@models.route('/api/update_model', methods=['PUT'])
def update_model():
    """ Updates a model """
    data = request.get_json()
    params = data.get('params', {'model_id': 1})
    entry = Model.objects(model_id=params.model_id).first()
    if not entry:
        return {'error': ModelNotFoundError()}
    entry.update(**params)
    return entry.to_json()


@models.route('/api/delete_model', methods=['DELETE'])
def delete_model():
    """ Updates a model """
    data = request.get_json()
    params = data.get('params', {'model_id': 1})
    entry = Model.objects(model_id=params.model_id).first()
    if not entry:
        return {'error': ModelNotFoundError()}
    entry.delete(params.model_id)
    return entry.to_json()
