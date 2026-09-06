# データ加工

## 実行環境とデータ

環境構築・ライブラリの追加方法は[リポジトリのREADME](../../README.md)を参照してください。Notebookのカーネルには、リポジトリ直下の `.venv` を選択します。

元データは全研究共通の `jepx-data-analytics/data/raw/` にあります。加工結果・特徴量・初期値は、この研究の `study_with_me/data/` に保存します。Notebookでは最初のコードセルで設定する `RAW_DATA_DIR` と `PROJECT_DATA_DIR` を使用します。

## Notebook

- [01_jepx_data.ipynb](01_jepx_data.ipynb)：共通の電力価格CSVから価格系列・週次系列を作成します。
- [02_temp_data.ipynb](02_temp_data.ipynb)：気温データを取得・加工します。取得にはネットワーク接続が必要です。

加工結果は `study_with_me/data/processed/electricity/` に保存します。
