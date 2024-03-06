from domain.interface.dnb_score import IDNBScore
from domain.interface.fluctuation import IFluctuation
from domain.interface.dissimilarity import IDissimilarity
from domain.interface.clustering import IClustering
from domain.interface.multiple_correction import IMultipleCorrection
from domain.interface.feature_data import IFeatureData
from injector import inject


class DNBScore(IDNBScore):
    @inject
    def __init__(
            self,
            fluctuation: IFluctuation,
            correction: IMultipleCorrection,
            dissimilarity: IDissimilarity,
            clustering: IClustering
    ):
        # super().__init__(fluctuation, network)
        self.fluctuation = fluctuation
        self.dissimilarity = dissimilarity
        self.clustering = clustering

    def run(self, feature_data: IFeatureData):
        pvals, rejects = self.fluctuation.run(feature_data)
        """
        if correction_input["multipletest"]:
            pvals_corrected, rejects = correction_hander.run(pvals)
        """
        feature_data.fluctuation = rejects
        d = self.dissimilarity.run(feature_data)
        clusters = self.clustering.run(d)
