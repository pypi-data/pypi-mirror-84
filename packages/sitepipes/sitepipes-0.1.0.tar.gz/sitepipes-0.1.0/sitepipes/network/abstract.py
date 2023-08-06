from sitepipes.util.helper import remove_id


class Site:
    """
    A machine with zero or more datasets and/or models

    :param host: str - The IP address of the host machine with data / models
    :param port: int - The port for inbound communication
    """

    def __init__(self, host=None, port=None):
        super().__init__()
        self.host = host
        self.port = port
        self.datasets = []
        self.models = []
        self.workers = []

    def add_dataset(self, dataset):
        self.datasets.append(dataset)

    def del_dataset(self, dataset):
        self.datasets = remove_id(self.datasets, dataset.id)

    def add_model(self, model):
        self.models.append(model)

    def del_model(self, model):
        self.models = remove_id(self.models, model.id)

    def add_worker(self, worker):
        self.workers.append(worker)

    def del_worker(self, worker):
        self.workers = remove_id(self.workers, worker.id)
