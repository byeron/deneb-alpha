## $deneb
denebは2段階方によるDNB解析を行うためのCLIツールです。

揺らぐ変数や、それらのネットワークを手軽に抽出することを目的としています。

## 実行環境
- Python 3.10
- poetry

## かんたんな実行例
```bash
docker pull byeron/poetry

# カレントディレクトリをマウントしてコンテナを起動
docker run -it --rm -v $(pwd):/workspace byeron/poetry bash

# コンテナ内で以下のコマンドを実行
cd workspace
poetry install

# ヘルプの表示
poetry run python src/serve.py --help

# テストデータを登録
poetry run python src/serve.py file add testdata/test_table.csv
FILE_ID=c1b64a70
CTRL=control
EXPR=experiment

# 揺らぐ変数の抽出
poetry run python src/serve.py fluctuation $FILE_ID ftest --control $CTRL --experiment $EXPR

# 揺らぐ変数間の非類似度、階層型クラスタリングの計算
poetry run python src/serve.py network $FILE_ID correlation --control $CTRL --experiment $EXPR
poetry run python src/serve.py network $FILE_ID clustering --control $CTRL --experiment $EXPR

# DNBスコアの計算
poetry run python src/serve.py dnb $FILE_ID score --control $CTRL --experiment $EXPR

# 樹形図、相関ヒートマップ、DNBスコアの可視化
poetry run python src/serve.py visualize $FILE_ID dendrogram
poetry run python src/serve.py visualize $FILE_ID heatmap
poetry run python src/serve.py visualize $FILE_ID score --state label1 --state label2 --state label3
```

## コマンド体系
```bash
 deneb-alpha
 ├── dnb
 │   └── score
 ├── file
 │   ├── add
 │   ├── delete
 │   └── get
 ├── fluctuation
 │   ├── ftest
 │   ├── inner-var
 │   ├── levene
 │   └── var-ratio
 ├── network
 │   ├── clustering
 │   └── correlation
 └── visualize
     ├── dendrogram
     ├── heatmap
     └── score
```

## 想定しているファイル形式
以下のようなテーブル構造をもつCSVファイルを想定しています。

|       | feat1 | feat2 | feat3 | ... | featN |
|-------|-------|-------|-------|-----|-------|
|label1 |       |       |       |     |       |
|label1 |       |       |       |     |       |
|label1 |       |       |       |     |       |
|label2 |       |       |       |     |       |
|label2 |       |       |       |     |       |
|label3 |       |       |       |     |       |

pandas.read_csv(index_col=0, header=0)によって、DataFrame.indexにサンプルID、DataFrame.columnsに変数名が格納されます。

具体的な例は`testdata`ディレクトリにサンプルデータを格納しています。

## 出力例
![dendrogram](./docs/images/dendrogram.png)
![heatmap](./docs/images/heatmap_1.png)
![score](./docs/images/score_0.png)
