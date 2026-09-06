# jepx-data-analytics

## Python環境の準備（Windows / PowerShell）

Python 3.11を使用します。リポジトリ直下で次を実行すると、仮想環境フォルダ `.venv` を作成し、`requirements.txt` のライブラリをインストールします。再実行時は既存の環境を使用します。

```powershell
powershell -ExecutionPolicy Bypass -File .\setup-env.ps1
```

Pythonの場所を指定する場合は `-Python "C:\path\to\python.exe"` を付けます。初回のライブラリ取得にはインターネット接続が必要です。

手動で作成する場合も、同じ一覧を使用できます。

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

すでに `.venv` を作成済みの場合や、`requirements.txt` にライブラリを追加した場合は、リポジトリ直下のPowerShellで次だけを実行してください。

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

このコマンドは今回の `.venv` にインストールします。すでに指定条件を満たしているライブラリはそのまま使用されます。Notebookで使用中のライブラリを追加・変更した後は、カーネルを再起動してください。

`requirements.txt` はNotebookとアプリの直接依存を用途別に記載しています。バージョン範囲を指定しており、将来の再インストールで完全に同じバージョンになることは保証しません。Meteostatは既存コードの `ms.daily` / `ms.interpolate` に対応する2系を使用します（[公式API](https://dev.meteostat.net/python/api/meteostat.interpolate)）。

## 実行方法

VS Codeでこのフォルダを開き、`Python: Select Interpreter` から `.venv\Scripts\python.exe` を選択します。Notebook右上のカーネル選択でも、同じ `.venv` のPythonを選択してください。既存の選択がある場合は手動で切り替える必要があります。

ブラウザでNotebookを実行する場合：

```powershell
.\.venv\Scripts\python.exe -m jupyterlab
```

作成スクリプトが登録するカーネル名は `Python (.venv - jepx-data-analytics)` です。手動作成の場合もJupyterLabの標準Pythonカーネルでこの環境を使用できます。

Pythonファイルを実行する場合：

```powershell
.\.venv\Scripts\python.exe path\to\script.py
```

必要なら `.\.venv\Scripts\Activate.ps1` で有効化すると、以降は `python` だけでこの環境を使用できます。有効化せずに上記のパスで実行することもできます。

`.venv` はGit管理対象外です。

## データの配置

元データはリポジトリ直下の `data/raw/` を全研究で共用します。加工データ・特徴量・モデル用データ・初期値は、各研究ディレクトリの `data/` に保存します。

```text
jepx-data-analytics/
├── .venv/
├── data/
│   └── raw/
│       ├── electricity/       # spot_summary_2005.csv ～ spot_summary_2026.csv
│       └── default_counts/    # M.csv, SP.csv
├── <研究ディレクトリ>/
│   ├── notebooks/
│   └── data/
│       ├── processed/
│       └── ...               # features, model, para, init_para など
└── study_with_me/
    └── data/
        ├── processed/
        ├── features/
        ├── model/
        └── para/
```

Notebookの最初のコードセルで、次の2つのパスを設定します。Notebookのあるフォルダ・研究フォルダ・リポジトリ直下から実行できます。

```python
RAW_DATA_DIR = REPO_ROOT / "data" / "raw"
PROJECT_DATA_DIR = PROJECT_DIR / "data"

# 共通の元データを読み込む
df = pd.read_csv(RAW_DATA_DIR / "electricity/spot_summary_2016.csv", encoding="cp932")

# 加工結果は自分の研究ディレクトリに保存する
output_path = PROJECT_DATA_DIR / "processed/result.csv"
output_path.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(output_path, index=False)
```

Merton研究の予備検討で使う初期値は、その研究の `data/pre/init_para/`、`data/pre/init_y/`、`data/pre/init_study/` に保存しています。再現実装の初期値 `data/init_para/` とは区別しています。

元データの `data/raw/` は `.gitignore` によりGit管理対象外です。別の環境ではリポジトリ直下に同じ `data/raw/` の配置を用意してください。研究間で同名の元データは内容一致を確認して共通化し、加工データは研究ごとに保持しています。

変更を反映するには、カーネルを再起動して最初のセルから実行してください。`.ipynb_checkpoints` 内の過去版は更新対象外です。

移動前から以下の2つのCSVは存在していません。該当Notebookの参照先も各研究の `data/` に設定していますが、実行には元の加工データの準備が必要です。`process` は元コードの表記で、既存の `processed` のデータと同一とは判断していません。

| Notebook | 不足するパス（リポジトリ直下から） |
| --- | --- |
| `study_with_me/3.model/04_price_forecasts_modelC.ipynb` | `study_with_me/data/process/electricity/weekly_base_after_2017.csv` |
| `study_with_me/4.estimation/MCMC.ipynb` | `study_with_me/data/process/electricity/df_tokyo.csv` |

読んだ論文とか考えたこととか
