from src.domain.ftest_config import FtestConfig
import pytest

@pytest.fixture
def ftest_config():
    return FtestConfig(
        control="control",
        experiment="experiment",
        alpha=0.05,
    )

# コンストラクタに与えられる引数の型が誤っている場合
# controlがstr型でない場合
def test_control_type_error():
    with pytest.raises(TypeError):
        FtestConfig(
            control=1,
            experiment="experiment",
            alpha=0.05,
        )

# experimentがstr型でない場合
def test_experiment_type_error():
    with pytest.raises(TypeError):
        FtestConfig(
            control="control",
            experiment=1,
            alpha=0.05,
        )

# alphaがfloat型でない場合
def test_alpha_type_error():
    with pytest.raises(TypeError):
        FtestConfig(
            control="control",
            experiment="experiment",
            alpha="0.05",
        )

# 有意水準は0より大きく1より小さい値でなければならない
def test_alpha_value_error():
    # alphaが0より小さい場合
    with pytest.raises(ValueError):
        FtestConfig(
            control="control",
            experiment="experiment",
            alpha=-0.05,
        )

    # alphaが1より大きい場合
    with pytest.raises(ValueError):
        FtestConfig(
            control="control",
            experiment="experiment",
            alpha=1.05,
        )