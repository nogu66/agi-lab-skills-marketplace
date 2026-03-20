# コードサンプル集 生成ガイド

## サンプルの種類（最低3つ以上作成）

1. **基本サンプル（basic_example）**: 最小限のコードで技術の基本動作を示す
2. **実践サンプル（practical_example）**: 実際のユースケースに近い、やや複雑な実装
3. **応用サンプル（advanced_example）**: 複数の技術を組み合わせた発展的な実装

テーマに応じて追加のサンプルを作成してよい（ベンチマーク用、テスト用、統合例など）。

## 各サンプルの要件

- **即座に実行可能**であること。依存関係のインストール手順を含む。
- ファイル冒頭に以下を日本語コメントで記載:
  - サンプルの概要（何を示すか）
  - 実行方法（コマンド）
  - 前提条件（必要なライブラリ、環境変数等）
  - 期待される出力
- コード内の重要な箇所に**日本語コメント**で解説を付与する。
- **README.md** を `samples/` ディレクトリに作成し、全サンプルの一覧と説明、実行方法をまとめる。

## ディレクトリ構成例

```
samples/
  README.md                    # サンプル一覧と使い方
  basic_example/
    main.py (or .ts, .js等)    # 基本サンプル
    requirements.txt           # 依存関係（該当する場合）
  practical_example/
    main.py
    config.yaml                # 設定ファイル（該当する場合）
    requirements.txt
  advanced_example/
    main.py
    requirements.txt
```

使用言語はテーマに最も適した言語を選択する（Python, TypeScript, Go等）。
