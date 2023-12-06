from dataclasses import dataclass

from domain.cluster import Cluster


@dataclass
class Clusters:
    _clusters: list[Cluster]

    def max_size(self):
        return max([cluster.size for cluster in self._clusters])

    def max_clusters(self):
        return [
            cluster for cluster in self._clusters if cluster.size == self.max_size()
        ]

    def nth_largest(self, rank: int):
        sizes = [c.size for c in self._clusters]
        unique_sizes = sorted(list(set(sizes)), reverse=True)
        ranked_sizes = {n + 1: size for n, size in enumerate(unique_sizes)}
        if rank not in ranked_sizes:
            raise ValueError(f"count of cluster is less than {rank}")

        size = ranked_sizes[rank]

        size_features = {c.size: [] for c in self._clusters}
        for c in self._clusters:
            size_features[c.size].append(c.features)
        size_features = size_features[size]

        return (size, size_features)
