from sitepipes.network.abstract import Site


class MobileSite(Site):
    def __init__(self, host=None, port=None):
        super().__init__()
        self.host = host
        self.port = port


class ServerSite(Site):
    def __init__(self, host=None, port=None):
        super().__init__()
        self.host = host
        self.port = port


class SwiftSite(MobileSite):
    pass


class KotlinSite(MobileSite):
    pass
