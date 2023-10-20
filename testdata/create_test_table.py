import numpy as np
import pandas as pd

if __name__ == "__main__":
    # 60 x 30 の乱数行列を生成
    np.random.seed(12345)
    a = np.random.randint(0, 100, (20, 30))
    b = np.random.randint(0, 100, (20, 30))
    # bの指定した列にランダムな値を加算 or 減算する
    b[:, 0:20] = b[:, 0:20] + np.random.randint(-90, 90, (20, 20))

    # aとbを結合
    c = np.concatenate([a, b], axis=0)
    df = pd.DataFrame(c)
    l1 = ["control"] * 20
    l2 = ["experiment"] * 20
    l = l1 + l2
    df.index = l
    print(df)
    df.to_csv("test_table.csv")
