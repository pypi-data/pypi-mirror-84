import inspect
import uuid


def remove_id(iterable, obj_id):
    """
    Removes any entry from iterable with matching ID

    :param iterable: list - A collection of objects (ie. Dataset, Model)
    :param obj_id: int - The ID matching the objects contained in iterable
    :return: The iterable without an entry for the filter ID
    """
    return [x for x in iterable if x.id != obj_id]


def gen_id():
    """ Generates a unique ID """
    return uuid.uuid4()


def obj_to_module_name(obj):
    """
    Extracts the module name (ie. the file name) of any instance of a class

    Useful for automatically detecting which libraries and frameworks are being
    used and changing logic accordingly. Such as to detect that the model being
    used is a Keras model and can be saved with the Keras internal API

    :param obj: object - An instance of any class
    :return: str - The module name that an object belongs to

    >>> model = Model(...)
        model_type = obj_to_module_name(model)
    """

    module = inspect.getmodule(obj)
    base, _sep, _stem = module.__name__.partition('.')

    return base
