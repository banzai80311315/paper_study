# 価格予測とジャンプ予測のための特徴量の考察

## 実行環境とデータ

環境構築・ライブラリの追加方法は[リポジトリのREADME](../../README.md)を参照してください。Notebookのカーネルには、リポジトリ直下の `.venv` を選択します。

元データは全研究共通の `jepx-data-analytics/data/raw/` にあります。加工結果・特徴量・初期値は、この研究の `study_with_me/data/` に保存します。Notebookでは最初のコードセルで設定する `RAW_DATA_DIR` と `PROJECT_DATA_DIR` を使用します。

このフォルダのNotebookで、価格予測・ジャンプ予測に用いる説明変数の候補を考察します。

# 価格予測に有用な変数の特徴

> point :  需給の平均状態を表す変数

# ジャンプ予測に有用な変数の特徴

> point :  需給の平均状態からの急変を表す変数

# 確認すべき図
## 散布図
線形な関係があるかを確認するために散布図を描く。

## LOWESS曲線付き散布図
非線形な関係があるかを確認するために散布図にLOWESS曲線を重ねる。

## 箱ひげ図

## ヒストグラム

## KDEプロット

## Notebookと保存先

- [01_jepx_acf.ipynb](01_jepx_acf.ipynb)：価格系列と自己相関の分析。
- [02_temp_feature.ipynb](02_temp_feature.ipynb)：気温に関する特徴量の作成。

`data/processed/electricity/` の加工結果を読み込み、特徴量を `study_with_me/data/features/electricity/` に保存します。
