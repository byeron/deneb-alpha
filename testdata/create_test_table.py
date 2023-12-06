import numpy as np
import pandas as pd

if __name__ == "__main__":
    # 乱数のシードを設定
    np.random.seed(12345)
    matrix = np.random.rand(90, 30)

    # 後半の0から20列の相関を高くする
    # 例: 0から20列間の相関係数を0.8に設定
    correlation_value = 0.8
    correlation_matrix = np.ones((21, 21)) * correlation_value  # 相関係数行列の初期化
    np.fill_diagonal(correlation_matrix, 1.0)  # 対角成分は1に設定
    matrix[30:60, :21] = np.random.multivariate_normal(
        mean=np.zeros(21), cov=correlation_matrix, size=30
    )
    matrix[30:60, :] += np.random.rand(30, 30)

    print(matrix.shape)
    df = pd.DataFrame(matrix)
    # indexを設定
    # 0から29行目までをcontrol、30から59行目までをexperiment, 60から89行目までをotherとする

    df.index = (
        ["control" for i in range(30)]
        + ["experiment" for i in range(30)]
        + ["other" for i in range(30)]
    )

    df.to_csv("testdata/test_table.csv")

    # 一様乱数の行列を作成
    matrix = np.random.rand(90, 30)
    df = pd.DataFrame(matrix)
    # indexを設定
    # 0から29行目までをcontrol、30から59行目までをexperiment, 60から89行目までをotherとする
    df.index = (
        ["control" for i in range(30)]
        + ["experiment" for i in range(30)]
        + ["other" for i in range(30)]
    )

    df.to_csv("testdata/test_table_uniform.csv")
