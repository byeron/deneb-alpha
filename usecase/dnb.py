from domain.interface.dnb import IDNB


class DNB(IDNB):
    def __init__(self, fluctuation, network):
        super().__init__(fluctuation, network)

    def run(self):
        self.fluctuation.run()
        self.network.run()
