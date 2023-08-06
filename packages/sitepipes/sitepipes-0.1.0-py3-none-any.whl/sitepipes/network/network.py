from sitepipes.network.abstract import Site
from sitepipes.util.helper import remove_id


class NetworkController(Site):
    """ A collection of sites with an agreed upon set of operations """

    def __init__(self, sites=None):
        super().__init__()
        if sites is None:
            sites = []
        self.sites = sites

    def add_site(self, site):
        self.sites.append(site)

    def remove_site(self, site):
        self.sites = remove_id(self.sites, site.id)

