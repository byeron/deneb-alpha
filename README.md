# deneb-alpha
- このCLIは、2段階法によるDNBスコアの計算を行うためのものです

# 実行環境
- Python 3.10
- poetry

# 想定しているファイル形式
以下の情報が格納されているcsvファイル
行方向: サンプル(1列目はサンプルIDやラベルなどの情報)
列方向: 特徴量(0行目は変数名が示されたヘッダー行)
pandas.read_csv(index_col=0, header=0)によって、DataFrame.indexにサンプルID、DataFrame.columnsに変数名が格納されることを想定しています。
`testdata`ディレクトリにサンプルデータを格納していますので、参考にしてください。

# セットアップ(docker)
```bash
docker pull byeron/poetry

# カレントディレクトリをマウントしてコンテナを起動
docker run -it --rm -v $(pwd):/workspace byeron/poetry bash

# コンテナ内で以下のコマンドを実行
cd workspace
poetry install
poetry run python src/serve.py --help
```

# コマンド体系
このCLIは以下のコマンドによって構成されています。
詳細は各コマンドのヘルプを参照してください。
- dnb
    - 2段階法によって得られた変数によるDNBスコアの計算
- file
    - 解析対象のcsvファイルの登録、削除、一覧表示
- fluctuation
    - 2段階法における1段階目の揺らぐ変数の抽出
- network
    - 2段階法における2段階目のネットワーク構築
- visualize
    - 樹形図、相関ヒートマップ、DNBスコアの可視化

# 一般的な操作処理フロー
1. 解析対象のcsvファイルを登録する
```bash
# ファイルの登録
PATH_TO_CSV=testdata/test_table.csv
$ poetry run python src/serve.py file add $PATH_TO_CSV

File ID: c1b64a70

# ファイル登録後はファイル一覧から、ファイルのIDを取得できます
$ poetry run python src/serve.py file get

ID: c1b64a70
        Name: test_table
        Created at: 2024-08-20 05:35:44

FILE_ID=99b7a34e
```
2. 2段階法における1段階目の揺らぐ変数の抽出を行う
```bash
# CLI上で揺らぐ変数の抽出を行う
# サブコマンドのOptions(最新の情報は--helpで確認してください)
# --control: コントロール群のラベル(default: control)
# --experiment: 実験群のラベル(default: experiment)
# --alpha: 有意水準(default: 0.05)
# --robust / --no-robust: ロバストな統計量を用いるかどうか(default: no-robust)

# 基本的には以下のコマンドを実行する
# 対象群と実験群を指定する
$ poetry run python src/serve.py fluctuation $FILE_ID ftest --control hoge --experiment fuga

id: c1b64a70
method: ftest, robust: False
control: control, experiment: experiment, alpha: 0.05
   features      p_values  p_values_corrected  reject
0         0  2.229330e-08        3.934112e-08    True
1         1  2.952568e-12        8.857704e-11    True
2         2  9.717656e-06        1.388237e-05    True
3         3  3.214649e-08        5.075761e-08    True
4         4  2.138766e-11        2.138766e-10    True
5         5  1.623690e-11        2.138766e-10    True
6         6  7.081714e-08        1.062257e-07    True
7         7  9.807160e-10        2.263191e-09    True
8         8  3.201163e-08        5.075761e-08    True
9         9  3.612371e-11        2.709278e-10    True
10       10  2.817644e-10        1.056617e-09    True
11       11  3.746532e-10        1.248844e-09    True
...

# デフォルトオプションを省略しない場合は
# poetry run python src/serve.py fluctuation --multipletest --method fdr_bh $FILE_ID ttest --control hoge --experiment fuga --alpha 0.05 --no-robust
```
3. 2段階法における2段階目のネットワーク構築を行う
```bash
# CLI上で距離行列の計算を行う
# サブコマンドのOptions(最新の情報は--helpで確認してください)
# --control: コントロール群のラベル(default: control)
# --experiment: 実験群のラベル(default: experiment)
# --corr-method: 相関係数の計算方法(default: pearson)
# --dissimilarity: 距離行列の計算方法(default: abslinear, 1 - |correlation|)

# 対象群と実験群を指定する
poetry run python src/serve.py network $FILE_ID correlation --control hoge --experiment fuga

id: c1b64a70
fluctuation method: ftest
alpha: 0.05
multipletest method: fdr_bh
           0         1         2         3         4         5         6  ...        22        23        24        25        26        27        28
0   0.000000  0.328601  0.434678  0.280079  0.260438  0.274593  0.224016  ...  0.712254  0.942098  0.950110  0.846269  0.753495  0.967428  0.689523
1   0.328601  0.000000  0.251945  0.325435  0.278216  0.281435  0.333197  ...  0.891082  0.917270  0.823752  0.685138  0.891852  0.876375  0.671373
2   0.434678  0.251945  0.000000  0.318165  0.299083  0.344560  0.448543  ...  0.977057  0.975467  0.864782  0.641638  0.735182  0.831317  0.609826
3   0.280079  0.325435  0.318165  0.000000  0.283194  0.215163  0.398815  ...  0.823960  0.964219  0.911583  0.481593  0.629666  0.957121  0.584318
4   0.260438  0.278216  0.299083  0.283194  0.000000  0.200466  0.177195  ...  0.928089  0.990752  0.999827  0.678836  0.822985  0.846650  0.661775

# デフォルトオプションを省略しない場合は
# poetry run python src/serve.py network --alpha 0.05 --fluctuation-method ftest --fluctuation-threshold 2.0 --no-multiple-correction --multipletest-method fdr_bh $FILE_ID correlation --control hoge --experiment fuga --corr-method pearson --dissimilarity abslinear
```
```bash

# CLI上で距離行列をもとにした階層型クラスタリングを行う
# サブコマンドのOptions(最新の情報は--helpで確認してください)
# --control: コントロール群のラベル(default: control)
# --experiment: 実験群のラベル(default: experiment)
# --corr-method: 相関係数の計算方法(default: pearson)
# --dissimilarity: 距離行列の計算方法(default: abslinear, 1 - |correlation|)
# --cutoff: クラスタリングのカットオフ(default: 0.5)
# --rank: 大きい方から何番目のクラスタを表示するか(default: 1)
# --linkage-method: クラスタリングの手法(default: average)
# --criterion: クラスタリングの基準(default: distance)

# 対象群と実験群を指定する
$ poetry run python src/serve.py network $FILE_ID clustering --control hoge --experiment fuga

(21, [['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']])

# デフォルトオプションを省略しない場合は
# poetry run python src/serve.py network --alpha 0.05 --fluctuation-method ftest --fluctuation-threshold 2.0 --no-multiple-correction --multipletest-method fdr_bh $FILE_ID clustering --control hoge --experiment fuga --corr-method pearson --dissimilarity abslinear --cutoff 0.5 --rank 1 --linkage-method average --criterion distance
```

4. DNBスコアの計算を行う
```bash
# CLI上でDNBスコアの計算を行う
# サブコマンドのOptions(最新の情報は--helpで確認してください)
# --control: コントロール群のラベル(default: control)
# --experiment: 実験群のラベル(default: experiment)

# 対象群と実験群を指定する
$ poetry run python src/serve.py dnb $FILE_ID score --control hoge --experiment fuga

id: c1b64a70
multipletest: True, method: fdr_bh
#1
                control experiment     other
dnb_score      0.045898   0.694127  0.042062
std_deviation  0.286546   0.984691  0.285541
corr_strength  0.160178   0.704919  0.147305

# デフォルトオプションを省略しない場合は
# poetry run python src/serve.py dnb --alpha 0.05 --threshold 2.0 --fluctuation-method ftest --fluctuation-threshold 2.0 --no-multiple-correction --multipletest-method fdr_bh --dissimilarity-method pearson --dissimilarity-metric abslinear --clustering-cutoff 0.5 --clustering-rank 1 --clustering-linkage-mathod average --clustering criterion distance $FILE_ID score --control hoge --experiment fuga
```

5. 樹形図、相関ヒートマップ、DNBスコアの可視化を行う
2, 3, 4ステップの計算結果をもとに可視化を行うため、エラーが発生する場合はまずそれらのステップを再度実行してください。
```bash
# CLI上で可視化を行う
# サブコマンドのOptions(最新の情報は--helpで確認してください)
# --cutoff: クラスタリングのカットオフ(default: 0.5)
# --method: クラスタリングの手法(default: average)

# デンドログラムを出力
poetry run python src/serve.py visualize $FILE_ID dendrogram

# 相関ヒートマップを出力
poetry run python src/serve.py visualize $FILE_ID heatmap

# DNBスコアを出力
# --state: データの並び順を任意に設定できる
poetry run python src/serve.py visualize $FILE_ID score --state label1 --state label2 --state label3
```

# 注意
- 統一されていないオプション名などは、今後修正される可能性があります。最新の情報はメインコマンド、サブコマンドの--helpで確認してください。
