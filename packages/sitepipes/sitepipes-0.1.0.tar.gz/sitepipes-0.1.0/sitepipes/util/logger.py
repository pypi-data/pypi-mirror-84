import inspect
import logging
from functools import wraps
from types import MethodType

from sitepipes import config


def logger(obj):
    """ Automatically detects whether a function or class  """


def func_logger(obj, do_log=config['do_log']):
    """ Decorator to automatically log function calls and results """

    @wraps(obj)
    def inner(*args, **kwargs):
        result = obj(*args, **kwargs)

        if do_log:
            log.info(f'\nDEBUG Called object = {obj.__qualname__}')
            print(f'DEBUG args = {args}')
            print(f'DEBUG kwargs = {kwargs}')
            print(f'DEBUG result = {result}\n')

        return result

    return inner


def class_logger(cls, autolog=config['autolog'],
                 decorate_static=config['decorate_static'],
                 decorate_class=config['decorate_class'],
                 decorate_property=config['decorate_property'],
                 decorate_routine=config['decorate_routine']):
    """
    A class decorator for automatic logging of various methods

    :param cls: object - The class definition to decorate
    :param autolog: bool - Whether to automatically log method calls
    :param decorate_static: bool - Whether to decorate static methods
    :param decorate_class: bool - Whether to decorate class methods
    :param decorate_property: bool - Whether to decorate properties
    :param decorate_routine: bool - Whether to decorate all other routines
    """

    if not autolog:
        return cls

    logging.info(f'Creating loggers for methods of {type(cls).__name__}...')

    for name, obj in vars(cls).items():

        if decorate_static and isinstance(obj, staticmethod):
            decorated_fn = func_logger(obj.__func__)
            setattr(obj, name, staticmethod(decorated_fn))

        elif decorate_class and isinstance(obj, classmethod):
            decorated_fn = func_logger(obj.__func__)
            setattr(obj, name, classmethod(decorated_fn))

        elif decorate_property and isinstance(obj, property):
            if obj.fget:
                obj = obj.getter(func_logger(obj.fget))
            if obj.fget:
                obj = obj.setter(func_logger(obj.fset))
            if obj.fget:
                obj = obj.deleter(func_logger(obj.fdel))
            setattr(cls, name, obj)

        elif decorate_routine and inspect.isroutine(obj):
            setattr(cls, name, func_logger(obj))

    return cls


class Logger:
    """
    Decorator class for automatic logging of function calls

    :param fn: object -
    """

    def __init__(self, fn):
        self.fn = fn

    def __call__(self, *args, **kwargs):

        result = self.fn(*args, **kwargs)
        logging.info(f'Ran {self.fn.__qualname__}(args={args}, kwargs={kwargs}) = {result}...')

        return result

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return MethodType(self, instance)
