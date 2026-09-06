# 価格予測モデル

## Base model

以下はモデル候補の定義です。$t$ は観測時点、$S_t>0$ は電力価格（円/kWh）、$x_t$ は説明変数ベクトル、$\mu_t$ は対数価格の条件付き平均部分です。$\eta_t$ は誤差、$I_t\in\{0,1\}$ はジャンプ指標、$J_t$ は対数価格上のジャンプ幅、$p_t$ はジャンプ確率です。Student-t分布の $\sigma^2$ はスケールの二乗であり、分散そのものではありません（$\nu>2$ で分散は $\nu\sigma^2/(\nu-2)$）。


## 実行環境とデータ

環境構築・ライブラリの追加方法は[リポジトリのREADME](../../README.md)を参照してください。Notebookのカーネルには、リポジトリ直下の `.venv` を選択します。

元データは全研究共通の `paper_study/data/raw/` にあります。加工結果・特徴量・初期値は、この研究の `study_with_me/data/` に保存します。Notebookでは最初のコードセルで設定する `RAW_DATA_DIR` と `PROJECT_DATA_DIR` を使用します。

$$
\log S_t = c + \sum_{j = 1}^p \alpha_j \log S_{t-j} + \beta^T x_t = \mu_t
$$

## Model A: Student-t Error Model

$$
\log S_t=\mu_t+\eta_t
$$

$$
\eta_t \sim t_\nu(0, \sigma^2)
$$

## Model B: Jump Model

$$
\log S_t = \mu_t + \eta_t+I_t J_t
$$

$$
\eta_t \sim N(0, \sigma^2)
$$

$$
I_t \sim \mathrm{Bernoulli}(p_t)
$$

## Model C: Student-t + Jump Model

$$
\log S_t=\mu_t+\eta_t
+
I_t J_t
$$

$$
\eta_t \sim t_\nu(0, \sigma^2)
$$

$$
I_t \sim \mathrm{Bernoulli}(p_t)
$$

## 現在のNotebook

- [01_price_forecasts_modelA.ipynb](01_price_forecasts_modelA.ipynb)
- [02_jump_forecasts.ipynb](02_jump_forecasts.ipynb)
- [03_price_forecasts_modelB.ipynb](03_price_forecasts_modelB.ipynb)
- [04_price_forecasts_modelC.ipynb](04_price_forecasts_modelC.ipynb)

以下の数式はモデル候補の定義です。ファイル名だけで、すべてのモデルが完成しているとは判断しないでください。Model Cが参照する `study_with_me/data/process/electricity/weekly_base_after_2017.csv` は現在ありません。

モデル用データと推定パラメータは `study_with_me/data/model/`、`study_with_me/data/para/` に保存します。
