from sitepipes.util.helper import gen_id


class Worker:
    """ Executes jobs for a site """

    def __init__(self):
        self.id = gen_id()
