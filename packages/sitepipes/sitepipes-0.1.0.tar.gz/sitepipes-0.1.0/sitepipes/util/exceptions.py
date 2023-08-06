import json
import logging
from datetime import datetime
from http import HTTPStatus


class AppException(Exception):
    """ Base app exception """

    http_status = HTTPStatus.INTERNAL_SERVER_ERROR
    internal_err_msg = 'App exception occurred'
    user_err_msg = 'We are sorry! Something happened on our end.'

    def __init__(self, *args, user_err_msg=None):
        if args:
            self.internal_err_msg = args[0]
            super().__init__(*args)
        else:
            super().__init__(self.internal_err_msg)

        if user_err_msg is not None:
            self.user_err_msg = user_err_msg

    def to_json(self):
        err = {'http_status': self.http_status, 'user_err_msg': self.user_err_msg}

        return json.dumps(err)

    def log_exception(self):

        exception = {
            'type': type(self).__name__,
            'http_status': self.http_status,
            'message': self.args[0] if self.args else self.internal_err_msg,
            'args': self.args[1:]
        }

        logging.info(f'EXCEPTION - {datetime.now()}: {exception}')


class ProtectedDatasetError(AppException):
    """ An exception for a forbidden action on a protected component """

    def __init__(self, dataset_name=None, dataset_id=None, message=None):
        super().__init__(message)

        self.internal_err_msg = f'Dataset {dataset_name} cannot be sent!'


class ModelNotFoundError(AppException):
    """ An exception for a forbidden action on a protected component """

    def __init__(self, message=None, model_name=None, model_id=None):
        super().__init__(message)
        self.internal_err_msg = f'Model {model_name} {model_id} could not be found!'


if __name__ == '__main__':

    raise ProtectedDatasetError('Dataset cannot be sent!')
