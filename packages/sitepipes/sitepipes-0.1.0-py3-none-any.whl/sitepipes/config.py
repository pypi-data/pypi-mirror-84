import io
import logging
import os
import sys

import yaml
from dotenv import load_dotenv
from flasgger import Swagger

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


def init_config(dir_name=None, filename='config.yml'):
    """  """
    if dir_name is None:
        dir_name = os.path.dirname(__file__)

    config_path = os.path.join(dir_name, filename)

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    return config


def init_log(name, log_level='DEBUG', std_level='INFO'):
    """
    Creates a logger that saves to log file and writes to the terminal

    Valid levels: DEBUG, INFO, WARNING, ERROR, CRITICAL

    :param name: str - The name of the logger
    :param log_level: str - The level for saving to a log file
    :param std_level: str - The level for writing to a Terminal
    :return logger: Logger - An object with logging methods
    """

    log_level = getattr(logging, log_level)
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    log.propagate = False

    log_format = '%(asctime)s %(levelname)s %(name)s %(module)s.%(funcName)s [L%(lineno)d] %(message)s'
    formatter = logging.Formatter(log_format)

    fh = logging.FileHandler('logs/debug.log')
    fh.setLevel(log_level)
    fh.setFormatter(formatter)

    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(std_level)
    sh.setFormatter(formatter)

    log.addHandler(fh)
    log.addHandler(sh)

    return log


class AppConfig:

    base_dir = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(os.path.join(base_dir, '.flaskenv'))

    FLASK_APP = os.environ.get('FLASK_APP', 'wsgi.py')
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
    SECRET_KEY = os.environ.get('SECRET_KEY', 'Ineedtosetasecretkeyindotenv')

    DEBUG = os.environ.get('DEBUG', config['app']['debug'])
    TESTING = os.environ.get('TESTING', config['app']['testing'])
    STATIC_FOLDER = 'static'
    STATIC_URL_PATH = ''
    TEMPLATES_FOLDER = 'templates'

    MONGODB_URI = 'mongodb://localhost:27017/myDatabase'

    SWAGGER = Swagger.DEFAULT_CONFIG
    SWAGGER['specs_route'] = '/api/docs'


if not os.path.exists('logs/'):
    os.makedirs('logs/')

flog = init_logger('api.front')
blog = init_logger('api.back')

# Disable werkzeug logs
werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.disabled = True

# Enable/disable print statements
if config['allow_print']:
    sys.stdout = sys.__stdout__
else:
    blog.warning('Suppressing print statements.')
    sys.stdout = io.StringIO()

home_dir_path = os.environ.get('USERPROFILE', '~')
config['lumena']['home_dir_path'] = home_dir_path
blog.info(f'Set home_dir_path = {home_dir_path}...')

paths = config['lumena']

for name, path in paths.items():
    config['lumena'][name] = os.path.join(home_dir_path, path)

log = build_log('log')