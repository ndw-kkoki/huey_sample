
# Huey Task Synchronization Examples

PythonのHuey（SqliteHuey）を使用した複数タスクの同期処理サンプル集です。

## Hueyについて

Hueyは軽量で使いやすいPythonタスクキューライブラリです：

- **軽量**: 最小限の設定で動作
- **柔軟**: SQLite、Redis、PostgreSQLなど複数のバックエンドをサポート
- **シンプル**: 直感的なAPI
- **機能豊富**: リトライ、スケジューリング、結果保存などをサポート

## ディレクトリ構成

```
huey_sample/
├── app/
│   ├── __init__.py          # Pythonパッケージ化
│   └── tasks.py             # タスク定義
├── main.py                  # メインプロセス起動スクリプト
├── run_worker.py            # Hueyワーカー起動スクリプト
├── requirements.txt         # 依存関係
├── README.md                # このファイル
└── huey.db                  # SQLiteデータベース（自動生成）
```

## セットアップ

### 1. **Python環境の準備:**
```bash
# 仮想環境の作成（推奨）
python -m venv venv

# 仮想環境の有効化
# Windows (PowerShell)
venv\Scripts\Activate.ps1
# Windows (Command Prompt)
venv\Scripts\activate.bat
# Linux/Mac
source venv/bin/activate
```

### 2. **依存関係のインストール:**
```bash
# pipの更新(必要に応じて)
pip install --upgrade pip
# 依存関係のインストール
pip install -r requirements.txt
```

### 3. **Hueyワーカーの起動（別のターミナルで実行）:**

#### 方法1: Pythonスクリプトを使用
```bash
python run_worker.py
```

#### 方法2: huey_consumerコマンドを使用
```bash
# マルチスレッド（2ワーカー）
huey_consumer app.tasks.huey -k thread -w 2
# マルチプロセス（2ワーカー）
huey_consumer app.tasks.huey -k process -w 2
# 単一スレッド
huey_consumer app.tasks.huey
```

### 4. **メインプロセスの実行:**
#### 基本的な同期処理
```bash
python main.py
```

### 5. **期待される出力**
   ```
   Starting main process...
   Running task_a with 1
   Running task_b with 2
   task_c waiting for task_a and task_b to finish...
   Received: A1, B2
   Final result: Combined: A1 + B2
   ```

## トラブルシューティング

### よくある問題と解決方法

1. **タスクが実行されない**
   - ワーカーが起動していることを確認
   - `huey.db` ファイルの権限を確認
   - ワーカーとメインプロセスが同じHueyインスタンスを使用していることを確認

2. **ワーカーが見つからない**
   ```bash
   # Hueyがインストールされていることを確認
   pip list | grep huey
   
   # 再インストール
   pip install --upgrade huey
   ```

3. **パフォーマンスの最適化**
   - CPUバウンドなタスク: プロセスワーカー (`-k process`)
   - I/Oバウンドなタスク: スレッドワーカー (`-k thread`)
   - ワーカー数はCPUコア数に合わせて調整

## 注意事項

- ワーカーが起動していない場合、タスクはキューに蓄積されるだけで実行されません
- `blocking=True` を使用すると、タスクが完了するまでメインスレッドがブロックされます
- SQLiteデータベース（`huey.db`）はタスクキューとして使用されます
- Hueyではタスクを直接呼び出すとResultオブジェクトが返され、`.get()` メソッドで実際の結果を取得します
- タスク間の依存関係は、結果を明示的に受け渡しすることで実現します
- 本番環境では、RedisやPostgreSQLなどのより堅牢なバックエンドの使用を推奨