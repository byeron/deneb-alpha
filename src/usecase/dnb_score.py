from domain.interface.dnb_score import IDNBScore


class DNBScore(IDNBScore):
    def __init__(self, fluctuation, network):
        super().__init__(fluctuation, network)

    def run(self):
        self.fluctuation.run()
        self.network.run()
