import pytest

from src.domain.feature_data import FeatureData
from src.usecase.ftest import Ftest
from src.domain.ftest_config import FtestConfig

# 指定したcontrolがindexに存在しない場合、エラーを返す
def test_control_not_found():
    feature_data = FeatureData.from_new("./testdata/test_table.csv")
    ftest_config = FtestConfig("invalid_control", "experiment", 0.05)
    ftest = Ftest(ftest_config)

    with pytest.raises(ValueError):
        ftest.run(feature_data)

# 指定したexperimentがindexに存在しない場合、エラーを返す
def test_experiment_not_found():
    feature_data = FeatureData.from_new("./testdata/test_table.csv")
    ftest_config = FtestConfig("control", "invalid_experiment", 0.05)
    ftest = Ftest(ftest_config)

    with pytest.raises(ValueError):
        ftest.run(feature_data)

# control群の変数に分散が0のものが含まれている場合、エラーを返す
@pytest.mark.skip(reason="分散が0の変数が含まれている場合のテストデータが準備されていないため")
def test_control_has_zero_variance():
    feature_data = FeatureData.from_new("./testdata/test_table.csv")
    ftest_config = FtestConfig("control", "experiment", 0.05)
    ftest = Ftest(ftest_config)

    with pytest.raises(ValueError):
        ftest.run(feature_data)