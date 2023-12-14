import pytest

from src.domain.feature_data import FeatureData


@pytest.fixture
def feature_data():
    return FeatureData.from_new("./testdata/test_table.csv")


# 存在しないファイルを指定した場合
def test_from_new_not_found():
    with pytest.raises(FileNotFoundError):
        FeatureData.from_new("tests/data/feature_data/not_found.csv")
