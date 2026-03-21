# 検証ガイド

コードサンプル（samples/）と実装応用ガイド（implementation_guide.md）の品質を、実際に実行して検証する手順。

## 検証対象

### 1. コードサンプル（samples/）

samples/ 内の各サブディレクトリについて:

1. 依存関係のインストール（requirements.txt または package.json）
2. メインファイル（main.py, main.ts 等）の実行
3. 実行結果と期待される出力の照合

### 2. 実装ガイドのコードブロック（implementation_guide.md）

implementation_guide.md 内の実行可能なコードブロック（```python, ```typescript 等）について:

1. コードブロックを一時ファイルに抽出
2. 依存関係の推定とインストール
3. 実行と結果の確認

以下のコードブロックは検証対象外:
- インストールコマンドのみ（`pip install ...`, `npm install ...`）
- シェルコマンド例（`$` で始まる行のみ）
- 1行以下のスニペット
- 設定ファイル（yaml, json, toml 等）
- 擬似コード・概念説明のブロック

## 検証スクリプトの使い方

`scripts/verify_samples.py` を使用する。

```bash
# コードサンプルの検証
python scripts/verify_samples.py <research-dir>/samples/

# 実装ガイドのコードブロック検証
python scripts/verify_samples.py --extract-md <research-dir>/implementation_guide.md

# JSON形式で結果取得（プログラム的に判定する場合）
python scripts/verify_samples.py --json <research-dir>/samples/
```

## エラーの分類と対応

### 環境変数エラー（無視）

API キー、トークン等の環境変数が未設定であることに起因するエラーは**無視する**。スクリプトはデフォルトでこれらを自動検出してスキップする。

判定パターン: API_KEY, SECRET, TOKEN, AuthenticationError 等のキーワードを含むエラー。

### 修正が必要なエラー

以下は実際のコード品質問題として修正する:

- **SyntaxError**: 構文エラー。コードの記述ミス。
- **ImportError / ModuleNotFoundError**: 依存関係の記載漏れ。requirements.txt または package.json に追記する。
- **NameError**: 未定義変数。コード内の参照ミス。
- **TypeError / ValueError**: 型・値の不整合。ロジックエラー。
- **FileNotFoundError**: 存在しないファイルへの参照。パスの修正またはファイル生成ロジックの追加。
- **IndentationError**: インデントの崩れ（Markdown変換時に頻発）。

### 修正手順

1. エラーの原因を特定する
2. 該当するソースファイル（samples/ 内）または implementation_guide.md のコードブロックを修正する
3. 修正後に再度検証スクリプトを実行して確認する
4. 全てのエラーが解消（または環境変数エラーのみ）になるまで繰り返す

## 検証レポート

検証スクリプトは `verification_report.md` を自動生成する。レポートには:

- 各サンプル/コードブロックの実行結果（成功/失敗/環境変数エラー）
- 失敗時のエラー詳細
- サマリー（合計、成功数、失敗数）

このレポートは成果物の一部として出力ディレクトリに含める。
