from src.domain.dissimilarity_config import DissimilarityConfig
import pytest

# コンストラクタに与えられる引数の型が誤っている場合

# experimentがstr型でない場合

def test_experiment_type_error():
    with pytest.raises(TypeError):
        DissimilarityConfig(
            experiment=1,
            corr_method="pearson",
            dissimilarity="abslinear",
        )

# corr_methodがstr型でない場合

def test_corr_method_type_error():

    with pytest.raises(TypeError):
        DissimilarityConfig(
            experiment="experiment",
            corr_method=1,
            dissimilarity="abslinear",
        )

# dissimilarityがstr型でない場合
def test_dissimilarity_type_error():
    with pytest.raises(TypeError):
        DissimilarityConfig(
            experiment="experiment",
            corr_method="pearson",
            dissimilarity=1,
        )

# corr_methodが"pearson"でも"spearman"でもない場合
def test_corr_method_value_error():
    with pytest.raises(ValueError):
        DissimilarityConfig(
            experiment="experiment",
            corr_method="pear",
            dissimilarity="abslinear",
        )

# dissimilarityが"abslinear"でもない場合
def test_dissimilarity_value_error():
        with pytest.raises(ValueError):
            DissimilarityConfig(
                experiment="experiment",
                corr_method="pearson",
                dissimilarity="abs",
            )