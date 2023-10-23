from dataclasses import dataclass


@dataclass
class Cluster:
    _id: int
    _features: list[str]
    _size: int

    @property
    def id(self):
        return self._id

    @property
    def features(self):
        return self._features

    @property
    def size(self):
        return self._size
