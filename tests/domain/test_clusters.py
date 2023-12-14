from src.domain.clusters import Clusters
from src.domain.cluster import Cluster
import pytest

@pytest.fixture
def clusters():
    return Clusters(
        [
            Cluster(
                _id=1,
                _features=["a", "b", "c"],
            ),
            Cluster(
                _id=2,
                _features=["d", "e", "f", "g"],
            ),
            Cluster(
                _id=3,
                _features=["h", "i"],
            ),
            Cluster(
                _id=4,
                _features=["j", "k", "l", "m"],
            ),
        ]
    )

# 誤った型の引数を渡した場合にエラーになることを確認するテスト
def test_clusters_init_error1():
    with pytest.raises(TypeError):
        Clusters(
            [
                Cluster(
                    _id=1.0,
                    _features=["a", "b", "c"],
                ),
                Cluster(
                    _id=2,
                    _features=["d", "e", "f"],
                ),
                Cluster(
                    _id=3,
                    _features=["g", "h", "i"],
                ),
            ]
        )

    with pytest.raises(TypeError):
        Clusters(
            [
                Cluster(
                    _id=1,
                    _features=[1, 2, 3],
                ),
                Cluster(
                    _id=2,
                    _features=["d", "e", "f"],
                ),
                Cluster(
                    _id=3,
                    _features=["g", "h", "i"],
                ),
            ]
        )

    with pytest.raises(TypeError):
        Clusters(
            [
                Cluster(
                    _id=1,
                    _features=["a", "b", "c"],
                ),
                Cluster(
                    _id=2,
                    _features=["d", "e", "f"],
                ),
                Cluster(
                    _id=3,
                    _features=[1, 2, 3],
                ),
            ]
        )

# max_size()のテスト
def test_max_size(clusters):
    assert clusters.max_size() == 4

# max_clusters()のテスト
def test_max_clusters(clusters):
    assert clusters.max_clusters() == [
        Cluster(
            _id=2,
            _features=["d", "e", "f", "g"],
        ),
        Cluster(
            _id=4,
            _features=["j", "k", "l", "m"],
        ),
    ]

# rankが存在しない場合にエラーになることを確認するテスト
def test_nth_largest_error1(clusters):
    with pytest.raises(ValueError):
        clusters.nth_largest(5)

# rankが存在する場合に正しい値を返すことを確認するテスト
def test_nth_largest_error2(clusters):
    assert clusters.nth_largest(1) == (4, [["d", "e", "f", "g"], ["j", "k", "l", "m"]])
    assert clusters.nth_largest(2) == (3, [["a", "b", "c"]])
    assert clusters.nth_largest(3) == (2, [["h", "i"]])