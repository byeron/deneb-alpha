import pytest
from src.usecase.abslinear import AbsLinear
from src.domain.dissimilarity_config import DissimilarityConfig
from src.domain.feature_data import FeatureData
from src.usecase.ftest import Ftest
from src.domain.ftest_config import FtestConfig
from src.usecase.multipletest import Multipletest
from src.domain.multipletest_config import MultipletestConfig

@pytest.fixture
def abslinear():
    dissimilarity_config = DissimilarityConfig("experiment", "pearson", "abslinear")
    return AbsLinear(dissimilarity_config)

# 揺らぐ変数が0のためにデータが空になる場合、エラーを返す
def test_no_fluctuating_vars(abslinear):
    # Test-specific setup
    feature_data = FeatureData.from_new("./testdata/test_table_uniform.csv")

    # Common setup
    ftest_config = FtestConfig("control", "experiment", 0.05)
    pvals, rejects = Ftest(ftest_config).run(feature_data)
    multipletest_config = MultipletestConfig("fdr_bh", 0.05)
    pvals_corrected, rejects_corrected = Multipletest(multipletest_config).run(pvals)
    feature_data.fluctuation = rejects_corrected

    with pytest.raises(ValueError):
        abslinear.run(feature_data)

# 指定したexperimentがindexに存在しない場合、エラーを返す
def test_experiment_not_found():
    # Common setup
    feature_data = FeatureData.from_new("./testdata/test_table.csv")
    ftest_config = FtestConfig("control", "experiment", 0.05)
    pvals, rejects = Ftest(ftest_config).run(feature_data)
    multipletest_config = MultipletestConfig("fdr_bh", 0.05)
    pvals_corrected, rejects_corrected = Multipletest(multipletest_config).run(pvals)
    feature_data.fluctuation = rejects_corrected

    invalid_experiment = "invalid_experiment" # Test-specific setup: 存在しないexperiment
    config = DissimilarityConfig(invalid_experiment, "pearson", "abslinear")
    abslinear = AbsLinear(config)

    with pytest.raises(ValueError):
        abslinear.run(feature_data)