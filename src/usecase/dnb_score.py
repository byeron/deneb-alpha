from domain.interface.dnb_score import IDNBScore
from domain.interface.fluctuation import IFluctuation
from domain.interface.dissimilarity import IDissimilarity
from domain.interface.clustering import IClustering
from domain.interface.multiple_correction import IMultipleCorrection
from domain.interface.feature_data import IFeatureData
from injector import inject
import numpy as np


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
        self.correction = correction
        self.dissimilarity = dissimilarity
        self.clustering = clustering

    def run(self, feature_data: IFeatureData):
        pvals, rejects = self.fluctuation.run(feature_data)

        if self.correction.is_apply():
            pvals_corrected, rejects = self.correction.run(pvals)
        feature_data.fluctuation = rejects

        d = self.dissimilarity.run(feature_data)
        clusters = self.clustering.run(d)

        candidates = feature_data.matrix.loc[:, clusters[1][0]]
        ave_standard_devs = {}
        ave_corr_strengths = {}
        dnb_scores = {}
        for t, d in candidates.groupby(level=0):
            ave_sd = d.std(axis="index", ddof=1).mean()
            ave_standard_devs[t] = ave_sd

            dof = len(d.columns)
            corr = abs(d.corr())
            tri_corr = np.tril(corr.to_numpy(), k=-1)
            ave_cs = 2.0 * np.sum(tri_corr) / (dof * (dof - 1))
            ave_corr_strengths[t] = ave_cs

            dnb_scores[t] = ave_sd * ave_cs
        return {
            "std_deviation": ave_standard_devs,
            "corr_strength": ave_corr_strengths,
            "dnb_score": dnb_scores,
        }
