from dataclasses import dataclass


@dataclass
class Cluster:
    _id: int
    _features: list[str]

    def __post_init__(self):
        if not isinstance(self._id, int):
            raise TypeError("id must be int type")

        if not isinstance(self._features, list):
            raise TypeError("features must be list type")

        for feature in self._features:
            if not isinstance(feature, str):
                raise TypeError("feature must be str type")

    @property
    def id(self):
        return self._id

    @property
    def features(self):
        return self._features

    @property
    def size(self):
        return self._features.__len__()
