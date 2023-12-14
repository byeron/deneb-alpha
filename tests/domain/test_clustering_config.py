import pytest

from src.domain.clustering_config import ClusteringConfig


# 正しい型の引数を渡した場合にエラーにならないことを確認するテスト
def test_clustering_config_init():
    config = ClusteringConfig(0.5, 2, "single", "distance")
    assert config.cutoff == 0.5
    assert config.rank == 2
    assert config.method == "single"
    assert config.criterion == "distance"


# 誤った型の引数を渡した場合にエラーになることを確認するテスト
def test_clustering_config_init_error1():
    with pytest.raises(TypeError):
        ClusteringConfig(0.5, 2.0, "single", "distance")

    with pytest.raises(TypeError):
        ClusteringConfig(0.5, 2, 1, "distance")

    with pytest.raises(TypeError):
        ClusteringConfig(0.5, 2, "single", 1)

    with pytest.raises(ValueError):
        ClusteringConfig(0.0, 2, "single", "distance")

    with pytest.raises(ValueError):
        ClusteringConfig(1.0, 2, "single", "distance")

    with pytest.raises(ValueError):
        ClusteringConfig(0.5, 0, "single", "distance")

    with pytest.raises(ValueError):
        ClusteringConfig(0.5, -1, "single", "distance")
