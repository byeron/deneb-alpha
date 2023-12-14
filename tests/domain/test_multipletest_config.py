import pytest

from src.domain.multipletest_config import MultipletestConfig


# 正しい型の引数を渡した場合にエラーにならないことを確認するテスト
def test_multipletest_config_init():
    config = MultipletestConfig("bonferroni", 0.05)
    assert config.method == "bonferroni"
    assert config.alpha == 0.05


# 誤った型の引数を渡した場合にエラーになることを確認するテスト
def test_multipletest_config_init_error1():
    with pytest.raises(TypeError):
        MultipletestConfig(1, 0.05)

    with pytest.raises(ValueError):
        MultipletestConfig("bonferroni", 0.0)

    with pytest.raises(ValueError):
        MultipletestConfig("bonferroni", 1.0)

    with pytest.raises(TypeError):
        MultipletestConfig("bonferroni", "0.05")

    with pytest.raises(TypeError):
        MultipletestConfig("bonferroni", None)

    with pytest.raises(TypeError):
        MultipletestConfig(None, 0.05)
