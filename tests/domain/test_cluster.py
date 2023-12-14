from src.domain.cluster import Cluster
import pytest

# 正しい型の引数を渡した場合にエラーにならないことを確認するテスト
def test_cluster_init():
    cluster = Cluster(1, ["a", "b", "c"])
    assert cluster.id == 1
    assert cluster.features == ["a", "b", "c"]
    assert cluster.size == 3

# 誤った型の引数を渡した場合にエラーになることを確認するテスト
def test_cluster_init_error1():
    with pytest.raises(TypeError):
        Cluster(1.0, ["a", "b", "c"])

    with pytest.raises(TypeError):
        Cluster(1, [1, 2, 3])

    with pytest.raises(TypeError):
        Cluster(1, ["a", "b", 1])