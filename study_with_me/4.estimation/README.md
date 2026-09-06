# パラメータ推定の検討

## 実行環境とデータ

環境構築・ライブラリの追加方法は[リポジトリのREADME](../../README.md)を参照してください。Notebookのカーネルには、リポジトリ直下の `.venv` を選択します。

元データは全研究共通の `paper_study/data/raw/` にあります。加工結果・特徴量・初期値は、この研究の `study_with_me/data/` に保存します。Notebookでは最初のコードセルで設定する `RAW_DATA_DIR` と `PROJECT_DATA_DIR` を使用します。

## Notebook

- [sim_MCMC.ipynb](sim_MCMC.ipynb)：シミュレーションによるMCMCの検討。
- [MCMC.ipynb](MCMC.ipynb)：実データを用いた推定の検討。

`MCMC.ipynb` が参照する `study_with_me/data/process/electricity/df_tokyo.csv` は現在ありません。元の加工手順と必要な列を確認してから用意する必要があります。
