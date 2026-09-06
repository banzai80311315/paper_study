# A Hawkes Model Approach to Modeling Price Spikes in the Japanese Electricity Market

## 実行環境とデータ

環境構築・ライブラリの追加方法は[リポジトリのREADME](../README.md)を参照してください。Notebookのカーネルには、リポジトリ直下の `.venv` を選択します。

元データは全研究共通の `jepx-data-analytics/data/raw/` にあります。加工結果・特徴量・初期値は、この研究の `A_Hawkes_Model_Approach_to_Modeling_Price_Spikes_in_the_Japanese_Electricity_Market/data/` に保存します。Notebookでは最初のコードセルで設定する `RAW_DATA_DIR` と `PROJECT_DATA_DIR` を使用します。

[A Hawkes Model Approach to Modeling Price Spikes in the Japanese Electricity Market](https://share.google/UHuffuuGfEOrYFusC)

## モデル
### Hawkes I

$$
\lambda_d = \alpha \lambda_{d-1} + \beta + \gamma u_d
$$

$$
\alpha = \exp{\left(-\frac{1}{\tau}\right)}\ , \ \beta = \mu(1- \alpha)
$$

$$
\gamma : \text{スパイクが来た時のジャンプ量}
$$

### Hawkes II
強いショックは強い連鎖を生む

$$
\lambda_d = \alpha \lambda_{d-1} + \beta + \gamma_d u_d
$$

$$
\gamma_d = \gamma_0 (1 - \exp{\left( -\frac{x_d}{x_0}\right)})
$$

### Hawkes III
強いショックは長く尾を引く

$$
\lambda_d = \alpha_d \lambda_{d-1} + \beta + \gamma u_d
$$

$$
\tau_d = \tau_0 (1 - \exp{\left( -\frac{x_d}{x_0}\right)})
$$

## 論文の結論
Hawkes II が優位：「スパイクの強さが、その後の発生確率に効いてくる」
