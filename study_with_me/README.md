# 潜在状態付き時系列モデル（Latent State Time Series Model）

## 実行環境とデータ

環境構築・ライブラリの追加方法は[リポジトリのREADME](../README.md)を参照してください。Notebookのカーネルには、リポジトリ直下の `.venv` を選択します。

元データは全研究共通の `paper_study/data/raw/` にあります。加工結果・特徴量・初期値は、この研究の `study_with_me/data/` に保存します。Notebookでは最初のコードセルで設定する `RAW_DATA_DIR` と `PROJECT_DATA_DIR` を使用します。

## 将来のライブラリ構成案

以下の `powerlib` は構成案です。現在の `src/` には `load_csv.py`、`make_dataset.py`、`util_plot.py`、`__init__.py` があり、この構成はまだ実装されていません。
```
src/
  powerlib/
    __init__.py

    io/ # 外部ファイルを読むだけ
      jepx_csv.py          # JEPX CSV読み込み
      schema.py            # 列名定義・標準カラム名

    preprocessing/ # 生データを分析可能な形に整える
      datetime.py          # 受渡日 + 時刻コード → datetime
      cleaning.py          # 数値変換、欠損処理、型変換
      scaling.py           # 休日・曜日補正

    features/ # 分析・モデルに使う列を作る
      time_features.py     # 時刻、曜日、休日、slot特徴量
      spike_features.py    # spike indicator, excess magnitude

    analysis/ # モデルではない集計分析
      summary.py           # 平均、分位点、基本統計
      distribution.py      # ヒストグラム用集計、分布分析
      time_profile.py      # 30分単位平均、時間帯別分析

    models/ # 予測・推定モデル
      hawkes.py            # Hawkesモデル
      threshold.py         # 閾値ベースモデル
      baseline.py          # persistenceなどベースライン

    metrics/ # 結果評価
      classification.py    # accuracy, precision, recall, F1, MCC
      forecasting.py       # MAE, WACCなど

    visualization/ # 図を作る
      timeseries.py        # plot用関数
      distribution.py      # histogram用関数
      spike.py             # spike可視化

    config.py              # 共通定数
    exceptions.py          # 独自例外
```

対応をするために、このプロジェクトディレクトリの責務も以下を意識する
```
io : 0.data_input
preprocessing : 1.data_processing
features , analysis : 2.feature_extraction
models : 3.model
estimation : 4.estimation
metrics : 5.evaluation
```

# スパイク確率モデリング

以下はモデル候補の理論メモです。$t$ は観測期間、$X_t$ は指標または期間内イベント数、$y_t$ は無次元の潜在状態です。$p_t$ は確率、$\lambda_t,\mu_t$ は期間内の期待件数、$r>0$ はNBの形状パラメータです。$\phi$ は推定対象のパラメータを表します。

## 1. 観測モデル（Observation Model）

$$
X_t \mid y_t \sim p(X_t \mid y_t, \phi)
$$

### ベルヌーイ

$$
X_t \sim \text{Bernoulli}(p_t), \quad
p_t = \frac{1}{1 + e^{-y_t}}
$$

### ポアソン

$$
X_t \sim \text{Poisson}(\lambda_t), \quad
\log \lambda_t = y_t
$$

### 負の二項分布

$$
X_t \sim \text{NB}(\mu_t, r), \quad \log \mu_t = y_t
$$

## 2. 潜在状態モデル（State Model）

$$
y_t = \beta + \theta y_{t-1} + \boldsymbol{\omega}^\top \mathbf{z}_{t-1} + \sigma \varepsilon_t
$$

$$
\varepsilon_t \sim \mathcal{N}(0,1)
$$

## 3. 対数事後分布（Log Posterior）

$$
\phi = (\beta, \theta, \boldsymbol{\omega}, \sigma)
$$

$$
p(\phi, y \mid X) \propto p(X \mid y)\, p(y \mid \phi)\, p(\phi)
$$

$$
\log p(y \mid \phi)=- \frac{1}{2\sigma^2}\sum_{t=2}^T(y_t - \beta - \theta y_{t-1} - \boldsymbol{\omega}^\top \mathbf{z}_{t-1})^2- (T-1)\log \sigma + C
$$

## 4. 観測尤度の違い

### Bernoulli
$$
\log p(X_{1:T} \mid y_{1:T}) = \sum_t \left[X_t y_t - \log(1+e^{y_t})\right]
$$

### Poisson

以下は観測値だけに依存する項 $-\sum_t\log(X_t!)$ を省いた対数尤度です。

$$
\log p(X_{1:T} \mid y_{1:T}) = \sum_t \left[X_t y_t - e^{y_t}\right]
$$

### Negative Binomial

以下は $r$ を固定したときの、$y_t$ に依存する対数尤度の部分です。$r$ も推定する場合は、ガンマ関数などの $r$ に依存する項も含める必要があります。

$$
\log p(X_{1:T} \mid y_{1:T}) = \sum_t \left[X_t y_t - (X_t+r)\log(r+e^{y_t})\right]
$$

## 5. 推論手法

### 5.1 MCMC（NUTS）

$$
(\phi^{(s)}, y^{(s)}) \sim p(\phi, y \mid X)
$$

- 高精度（漸近的に真の事後分布に収束）
- 計算コスト大
- フルベイズ推定（不確実性を保持）

#### ハミルトニアンの定義

未知パラメータと潜在変数をまとめて

$$
q = (\phi, y)
$$

とおく。

補助変数として運動量

$$
p \sim \mathcal{N}(0, M)
$$

を導入し、拡張空間 $(q,p)$ を考える。

ハミルトニアンは

$$
H(q,p) = U(q) + K(p)
$$

で定義される。

#### ポテンシャルエネルギー

$$
U(q) = -\log p(q \mid X)
$$

（正規化定数は不要）

#### 運動エネルギー

$$
K(p) = \frac{1}{2} p^\top M^{-1} p
$$

#### 同時分布

$$
p(q,p \mid X) \propto \exp\{-H(q,p)\}
$$

### ハミルトン方程式

$$
\frac{dq}{dt} = M^{-1}p
$$

$$
\frac{dp}{dt} = \nabla \log p(q \mid X)
$$

#### 性質

- エネルギー保存
- 体積保存（Liouvilleの定理）
- 可逆性（reversibility）

### リープフロッグ法（離散化）

ステップサイズ $\epsilon$ を用いて：

$$
p \leftarrow p + \frac{\epsilon}{2} \nabla \log p(q \mid X)
$$

$$
q \leftarrow q + \epsilon M^{-1} p
$$

$$
p \leftarrow p + \frac{\epsilon}{2} \nabla \log p(q \mid X)
$$

これを $L$ 回繰り返す。

### Metropolis補正

$$
\alpha = \min\left(1,\exp\left(-H(q^{new},p^{new}) + H(q,p)\right)\right)
$$

により採択判定を行う。

### NUTS（No-U-Turn Sampler）

HMCのハイパーパラメータ

- $\epsilon$（ステップサイズ）
- $L$（軌道長）
- $M$（質量行列）

を自動調整する。

#### 各要素の扱い

- $\epsilon$：dual averaging により適応的に更新  
- $M$：サンプル共分散から推定  
- $L$：Uターン条件により動的決定  

#### Uターン条件

$$
(q_t - q_0)^\top p_t < 0
$$

となった時点で軌道の拡張を停止する。

## 本モデルへの適用

本研究のモデル

$$
\lambda_t = \beta \exp(\alpha y_t)
$$

$$
y_t = \theta y_{t-1} + \xi_t
$$

に対して、ポテンシャルエネルギーは

$$
U(q)=- \sum_{t=1}^T \left[x_t(\log \beta + \alpha y_t)- \beta e^{\alpha y_t}\right]+ \frac{1}{2\sigma^2}\sum_{t=2}^T (y_t - \theta y_{t-1})^2- \log p(\phi)
$$

となる。

### 理論的利点

- 勾配情報を利用した効率的探索
- ランダムウォークの回避
- 数値積分によるエネルギー誤差をMetropolis補正で扱う。受理率はステップサイズなどに依存する
- 詳細釣り合いに基づく正当性
### 5.2 変分推論（Variational Inference）

$$
q(\phi, y) \approx p(\phi, y \mid X)
$$

$$
\mathrm{KL}(q || p) を最小化
$$

- 高速
- スケーラブル
- 近似誤差あり

## 6. モデル評価（Model Evaluation）

### 6.1 LFO（Leave-Future-Out）

逐次予測性能：

$$
\log p(X_{t+1} \mid X_{1:t})
$$

$$
=\log \mathbb{E}_{p(\phi,y|X_{1:t})}\left[p(X_{t+1}|\phi,y)\right]
$$

全期間で：

$$
\sum_{t} \log p(X_{t+1} \mid X_{1:t})
$$

### 特徴

- 時系列に適した交差検証
- 各時点で学習データだけを使って前処理・初期値推定・事前分布設定を行う必要がある
- モデル比較に最適

## 7. モデル解釈

- $y_t$：潜在状態（市場の内部状態）
- $\theta$：持続性
- $\boldsymbol{\omega}$：外生影響

## 8. 一般化

線形AR(1)モデル

$$
y_t = \beta + \theta y_{t-1} + \boldsymbol{\omega}^\top z_{t-1} + \sigma \varepsilon_t
$$

は、より一般に

$$
y_t = f(y_{t-1}, z_{t-1}) + \sigma \varepsilon_t
$$

と書ける。

## 9. ガウス過程拡張

この一般化に対して、潜在状態そのもの、あるいは状態遷移関数 $f$ を
ガウス過程でモデル化することができる。

### 9.1 潜在状態そのものをガウス過程とみなす方法

離散時点 $t = 1, \dots, T$ における潜在状態ベクトル

$$
\mathbf{y} = (y_1, \dots, y_T)^\top
$$

に対して、

$$
\mathbf{y} \sim \mathcal{N}(\mathbf{m}, K)
$$

と仮定する。

ここで

- $\mathbf{m}$：平均ベクトル
- $K$：共分散行列

である。たとえば平均関数を一定とすれば

$$
m_t = \beta
$$

より

$$
\mathbf{m} = \beta \mathbf{1}
$$

となる。

また、共分散行列はカーネル関数 $k(t,s)$ を用いて

$$
K_{ts} = k(t,s)
$$

と定義する。

したがって、

$$
\mathbf{y} \sim \mathcal{N}(\beta \mathbf{1}, K)
$$

となる。

### 9.2 代表的なカーネル

#### 指数カーネル

$$
k(t,s) = \alpha^2 \exp\left(-\frac{|t-s|}{\ell}\right)
$$

- $\alpha^2$：潜在状態の分散スケール
- $\ell$：相関の減衰速度を決める長さ尺度

このとき

$$
\text{Cov}(y_t, y_s) = \alpha^2 \exp\left(-\frac{|t-s|}{\ell}\right)
$$

であり、時点が近いほど強く相関する。

このカーネルは連続時間OU過程や離散時間AR(1)と近い構造を持つ。

#### 二乗指数カーネル

$$
k(t,s) = \alpha^2 \exp\left(-\frac{(t-s)^2}{2\ell^2}\right)
$$

指数カーネルよりも滑らかな潜在軌道を与える。

#### 周期カーネル

電力価格のように日周期・週周期が重要な場合には、

$$
k(t,s)=\alpha^2\exp\left(-\frac{2\sin^2\left(\pi |t-s| / p\right)}{\ell^2}\right)
$$

のような周期カーネルも考えられる。

- $p$：周期長
- $\ell$：周期内での滑らかさ

### 9.3 GP潜在状態モデルの全体構造

たとえば Bernoulli 観測なら、

$$
X_t \mid y_t \sim \text{Bernoulli}(p_t)
$$

$$
p_t = \frac{1}{1+e^{-y_t}}
$$

$$
\mathbf{y} \sim \mathcal{N}(\beta \mathbf{1}, K)
$$

となる。

同様に Poisson 観測では

$$
X_t \mid y_t \sim \text{Poisson}(\lambda_t), \quad\lambda_t = e^{y_t}
$$

とすればよい。

このように、**観測モデルはそのままに、潜在状態の事前分布だけをAR(1)からGPへ置き換える**ことができる。

### 9.4 GP化したときの対数事前分布

潜在状態 $\mathbf{y}$ の事前分布が

$$
\mathbf{y} \sim \mathcal{N}(\beta \mathbf{1}, K)
$$

なら、その対数事前分布は

$$
\log p(\mathbf{y} \mid \beta, K)=-\frac{1}{2}(\mathbf{y} - \beta \mathbf{1})^\top K^{-1} (\mathbf{y} - \beta \mathbf{1})-\frac{1}{2}\log |K|+ C
$$

である。

したがって、Bernoulli観測のときの対数事後分布は

$$
\log p(\phi, \mathbf{y} \mid X)=\sum_{t=1}^T\left[X_t y_t - \log(1+e^{y_t})\right]
$$

$$
\quad-\frac{1}{2}(\mathbf{y} - \beta \mathbf{1})^\top K^{-1} (\mathbf{y} - \beta \mathbf{1})-\frac{1}{2}\log |K|+ \log p(\phi)+ C
$$

となる。

ここで $\phi$ は、たとえば

$$
\phi = (\beta, \alpha, \ell)
$$

のように、平均とカーネルパラメータをまとめたものである。

Poisson観測なら第1項だけが

$$
\sum_{t=1}^T (X_t y_t - e^{y_t})
$$

に置き換わる。

### 9.5 AR(1)モデルとの関係

AR(1)状態モデル

$$
y_t = \beta + \theta y_{t-1} + \sigma \varepsilon_t
$$

は、局所的な一次マルコフ構造を持つ。

一方、GPモデルでは

$$
\mathbf{y} \sim \mathcal{N}(\beta \mathbf{1}, K)
$$

とまとめて表すため、

- より一般の相関構造を導入できる
- 周期性や長期依存を自然に組み込める
- 外生変数なしでも柔軟な時系列依存を表現できる

という利点がある。

ただし、

- $K^{-1}$ や $\log|K|$ の計算が必要
- 計算量が大きい
- 長系列では近似が必要

という欠点もある。

### 9.6 遷移関数そのものをガウス過程化する方法

もう一つの拡張として、状態遷移を

$$
y_t = f(y_{t-1}, \mathbf{z}_{t-1}) + \sigma \varepsilon_t
$$

と書き、この関数 $f$ 自体に対して

$$
f \sim \mathrm{GP}(m, k)
$$

を仮定する方法がある。

この場合、GPの対象は潜在状態列 $\mathbf{y}$ そのものではなく、  
**「1期前の状態と外生変数から次の状態を生成する関数」** である。

この拡張により、

- 非線形な自己回帰
- 外生変数との非線形相互作用
- 線形AR(1)では表せない複雑な遷移

を記述できる。

ただし、この形式はモデルも推論もかなり重くなるため、  
まずは

1. AR(1)状態モデル  
2. 潜在状態GPモデル  

の順で考える方が実装上は自然である。

### 9.7 この研究における位置づけ

重要なのは、潜在状態 $y_t$ を

- AR(1)で置くか
- ガウス過程で置くか

を比較することである。

すなわち、

- AR(1)：簡潔で計算しやすい
- GP：柔軟で多様な依存構造を表現できる

という対比になる。

したがって、本モデルにおけるガウス過程拡張とは、  
基本的には

> 潜在状態の事前分布を AR(1) から GP に置き換えること

を意味する。

# 価格予測モデリング
スパイク確率モデリングを使って価格予測モデリングを行う。

これを踏まえて以下のモデルを考える
## Model A: Student-t Error Model

$$
\log S_t=c+\alpha \log S_{t-1}+\beta x_t+\eta_t
$$

$$
\eta_t \sim t_\nu(0, \sigma^2)
$$

## Model B: Jump Model

$$
\log S_t=c+\alpha \log S_{t-1}+\beta x_t+\eta_t+I_t J_t
$$

$$
\eta_t \sim N(0, \sigma^2)
$$

$$
I_t \sim \mathrm{Bernoulli}(p_t)
$$

## Model C: Student-t + Jump Model

$$
\log S_t=c+\alpha \log S_{t-1}+\beta x_t+\eta_t
+
I_t J_t
$$

$$
\eta_t \sim t_\nu(0, \sigma^2)
$$

$$
I_t \sim \mathrm{Bernoulli}(p_t)
$$

## モデル評価
1. 対数尤度
2. AIC / BIC
3. シミュレーションでの最大値分布
4. スパイク発生回数
5. スパイクタイミング一致率
6. 価格系列のMSE / MAE
7. LFO

## 現在の実行順

1. `0.data_input/data_input.ipynb`：共通の元データの取得。既存ファイルの上書きに注意してください。
2. [1.data_processing](1.data_processing/README.md)：価格・気温データの加工。
3. [2.feature_extraction](2.feature_extraction/README.md)：特徴量の検討と保存。
4. [3.model](3.model/README.md)：価格・ジャンプモデルの検討。
5. [4.estimation](4.estimation/README.md)：推定方法の検討。
6. [5.evaluation](5.evaluation/README.md)：評価項目の計画。

`app/` はStreamlitアプリ、`6.app/streamlit.ipynb` はアプリ用データの試行Notebookです。
