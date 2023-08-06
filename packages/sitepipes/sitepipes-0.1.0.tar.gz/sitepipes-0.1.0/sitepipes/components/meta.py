from sitepipes.util.logger import logger


class MetaComponent(type):
    """ A type for pipeline components """

    def __new__(mcs, name, bases, class_dict):
        cls = super().__new__(mcs, name, bases, class_dict)
        cls = logger(cls)
        setattr(cls, 'pump_data', mcs.pump_data)
        return cls

    def __getattr__(self, item):
        err_msg = f'{type(self).__name__} has no attribute "{item}"...'
        print(err_msg)
        raise AttributeError(err_msg)

    def __setattr__(self, key, value):
        pass
