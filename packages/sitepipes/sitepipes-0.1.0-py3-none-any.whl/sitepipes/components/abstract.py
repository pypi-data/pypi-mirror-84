from sitepipes.components.meta import MetaComponent
from sitepipes.util.exceptions import ProtectedDatasetError


class Component(metaclass=MetaComponent):
    """
    Performs an operation on either a Dataset or Model

    :param inlets: list - Objects that send data to the component
    :param outlets: list - Objects that receive data from the component
    """

    inlets = []
    outlets = []

    def __init__(self, host=None, port=None, inlets=None, outlets=None):
        self.host = host
        self.port = port
        self.inlets = inlets
        self.outlets = outlets

    def __call__(self):

        return self.flow()

    def push_outlets(self, comp, outlets=None):
        """
        Pushes data to all outlets

        :param comp: CompositeDataset - With one or more datasets
        :param outlets:
        :return:
        """
        if outlets is None:
            outlets = self.outlets

        if len(outlets) < 1:
            raise ValueError(f'"{outlets}" must be greater than length 1,'
                             f'found length = {len(outlets)}')

        for outlet in outlets:
            comp.send(outlet)


class Connector:
    """ A component for connecting to an external environment """

    def __init__(self, inlets=None, outlets=None):
        super().__init__(inlets, outlets)


class DatabaseConnector(Connector):
    """ A component for connecting to a database """

    def __init__(self, inlets=None, outlets=None):
        super().__init__(inlets, outlets)


class Pipe(Component):
    """
    A component for moving data from Point A to Point B

    :param point_a: str - Path for the data source
    :param point_b: str - Path for the data destination
    """

    def __init__(self, point_a, point_b, inlets=None, outlets=None):
        super().__init__(inlets, outlets)
        self.point_a = point_a
        self.point_b = point_b

    def check_integrity(self):
        """ Checks the data integrity of a data flow """


class Fitting(Component):
    """
    A component for connecting two or more pipes into one or more flows. Will
    randomly split data flowing out into "pipes_out" pieces

    :param pipes_in: int - The number of pipes coming in
    :param pipes_out: int - The number of pipes coming out
    """

    def __init__(self, pipes_in, pipes_out=1, inlets=None, outlets=None):
        super().__init__(inlets, outlets)
        self.pipes_in = pipes_in
        self.pipes_out = pipes_out


class Valve(Component):
    """ A component for controlling the flow of data """

    def __init__(self, inlets=None, outlets=None):
        super().__init__(inlets, outlets)


class Queue(Valve):
    """ A component for queueing a data flow"""

    def __init__(self, inlets=None, outlets=None):
        super().__init__(inlets, outlets)


class Filter(Component):
    """ A component for removing data from the pipeline """

    def __init__(self, inlets=None, outlets=None):
        super().__init__(inlets, outlets)


class Reservoir(Component):
    """ A component for storing data on disk (long-term) """

    def __init__(self, inlets=None, outlets=None):
        super().__init__(inlets, outlets)


class Tank(Component):
    """
    A component for storing data in-memory (short-term)

    The contents of each tank are cleared when memory loses power. DO NOT store
    any data that cannot be lost here
    """

    def __init__(self, inlets=None, outlets=None):
        super().__init__(inlets, outlets)

    def __call__(self):
        pass

    def pump_data(self, dataset_id, location):
        """
        Selects a dataset by ID and sends it to a location.

        :param dataset_id: int - ID of the dataset
        :param location: str - Path to the data receiver
        """

        if self.dataset_id in self.protected_ids:
            raise ProtectedDatasetError


class ProtectedTank(Tank):
    """
    A tank with data that cannot leave the tank

    :param protected_ids: list - Datasets that cannot be sent
    """

    def __init__(self, protected_ids):
        super().__init__()
        self.protected_ids = protected_ids

    def __call__(self):
        pass

    def pump_data(self, dataset_id, location):
        """
        Selects a dataset by ID and sends it to a location.

        :param dataset_id: int - ID of the dataset
        :param location: str - Path to the data receiver
        """

        if self.dataset_id in self.protected_ids:
            raise ProtectedDatasetError


class DataTank(Tank):
    """ A type of tank used to store Dataset instances in short-term memory """

    def __init__(self, inlets=None, outlets=None):
        super().__init__(inlets, outlets)


class ProtectedDataTank(DataTank, ProtectedTank):
    """ A type of tank with Dataset instances that cannot leave the tank """

    def __init__(self, inlets=None, outlets=None):
        super().__init__(inlets, outlets)


class ModelTank(DataTank):
    """ A type of tank used to store Model instances in-memory """

    def __init__(self, inlets=None, outlets=None):
        super().__init__(inlets, outlets)


class ProtectedModelTank(ModelTank, ProtectedDataTank):
    """ A type of tank with Model instances that cannot leave the tank """

    def __init__(self, inlets=None, outlets=None):
        super().__init__(inlets, outlets)


class Screen(Component):
    """ A component for viewing the state of another component """

    def __init__(self, inlets=None, outlets=None):
        super().__init__(inlets, outlets)


class Hose(Component):
    """ A component for portable and flexible data moving """

    def __init__(self, inlets=None, outlets=None):
        super().__init__(inlets, outlets)


class Processor(Component):
    """ A component for running computations on data """

    def __init__(self, inlets=None, outlets=None):
        super().__init__(inlets, outlets)


class Controller(Component):
    """ A component for controlling a collection of components """

    def __init__(self, inlets=None, outlets=None):
        super().__init__(inlets, outlets)


class MainController(Controller):
    """
    A component for controlling a federated network """

    def __init__(self, inlets=None, outlets=None):
        super().__init__(inlets, outlets)

    def add_host(self, host):
        self.hosts.append(host)





class TrainingPlan:
    pass
