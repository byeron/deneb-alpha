import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial.distance import squareform

from domain.cluster import Cluster
from domain.clusters import Clusters
from domain.interface.clustering import IClustering


class Clustering(IClustering):
    def __init__(self, clustering_config):
        super().__init__(clustering_config)

    def run(self, dissimilarity_matrix: pd.DataFrame):
        rejected_feature = dissimilarity_matrix.columns
        d = squareform(dissimilarity_matrix.to_numpy())

        Z = linkage(d, method=self.config.method)
        ids = fcluster(Z, self.config.cutoff, criterion=self.config.criterion)

        ids_features = {}
        for _id, feature in zip(ids, rejected_feature):
            ids_features.setdefault(_id, []).append(feature)

        clusters = Clusters(
            [
                Cluster(
                    _id=_id,
                    _features=features,
                )
                for _id, features in ids_features.items()
            ]
        )

        return clusters.nth_largest(self.config.rank)
