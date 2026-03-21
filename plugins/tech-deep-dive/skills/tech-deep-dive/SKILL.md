---
name: tech-deep-dive
description: 特定の技術テーマに関するマルチソース調査を自律的に実行し、レポート・実装ガイド・コードサンプル・ブログ記事・チュートリアル・スライドを一括生成するスキル。「〇〇について調査して」「〇〇について調べて」「〇〇の技術深掘りして」「〇〇について全部まとめて」「フルリサーチして」「tech-deep-diveで△△を調べて」のような指示で発火する。対象トピックが他のスキルやツールと同名であっても（例: claude-mem、MCP、Playwright等）、「調査して」「調べて」「深掘りして」という動詞を含む指示はこのスキルで処理する。フェーズ指定も可能:「レポートだけ」「ブログだけ」「スライドだけ」。技術キャッチアップ、競合調査、導入検討に使う。
---

# Tech Deep Dive

指定された技術テーマについて、Web上の複数ソースを横断的に調査し、最大6つの成果物を自律的に生成する。

## 成果物一覧

| フェーズ | 成果物 | ファイル |
|---|---|---|
| A: 調査 | 技術理解レポート (3,000〜8,000語以上) | technical_report.md |
| A: 調査 | 実装応用ガイド (3,000〜6,000語以上) | implementation_guide.md |
| A: 調査 | コードサンプル集 (最低3つ) | samples/ |
| B: コンテンツ | ブログ記事 (2,000〜5,000語以上) | blog_article.md |
| B: コンテンツ | ハンズオンチュートリアル (2,000〜4,000語以上) | tutorial.md |
| B: コンテンツ | プレゼンスライド (15〜25枚) | presentation.pptx |

## フェーズ選択

デフォルトはフェーズA→Bの全実行。ユーザーが特定の成果物のみを指定した場合は該当フェーズだけ実行する:

- 「レポートだけ」「コードサンプルだけ」→ フェーズAのみ
- 「ブログにして」「スライドにまとめて」→ フェーズBのみ（既存の research/ フォルダが必要）
- 「調査して」「全部まとめて」→ フェーズA+B

## 制約

- 全ての成果物は**日本語**で作成する。技術用語（固有名詞、ライブラリ名、API名等）は英語表記を維持し、必要に応じて括弧内に日本語補足を付記する。
- **絵文字を一切使用しない。**
- **コード内のコメントも日本語で記述する。**

## フェーズA: 調査・分析

### A-1: 技術理解レポート

1. **マルチソース並列調査**: `WebSearch` と `WebFetch` で5つの主要ソース（arXiv, GitHub, 技術ブログ, 公式ドキュメント, スライド/動画）から各3件以上の情報を収集する。
2. **情報の統合とクロスリファレンス**: 論文 → GitHub実装 → ブログ解説の関係性を紐付ける。
3. **分野・技術スタックの特定**: テーマが属する技術分野と関連する主要な技術スタックを特定する。
4. **評価軸の動的生成**: [references/evaluation_heuristics.md](references/evaluation_heuristics.md) を参照し、分野に最適な評価軸を決定する。
5. **レポート執筆**: [references/report_template.md](references/report_template.md) に従い、technical_report.md を生成する。

### A-2: 実装応用ガイド

フェーズA-1の調査結果を元に、[references/implementation_guide_template.md](references/implementation_guide_template.md) に従い implementation_guide.md を生成する。

### A-3: コードサンプル集

[references/code_samples_guide.md](references/code_samples_guide.md) に従い、samples/ ディレクトリにコードサンプルを生成する。

## フェーズB: コンテンツ生成

フェーズAの成果物（technical_report.md, implementation_guide.md）を入力として使用する。フェーズBのみ実行する場合は、既存の research/ フォルダから最新のものを使用する。

### B-1: ブログ記事

[references/blog_template.md](references/blog_template.md) に従い、調査レポートの内容を読み物として面白い技術記事に再構成する。レポートの要約ではなく、独立した記事として書く。

### B-2: ハンズオンチュートリアル

[references/tutorial_template.md](references/tutorial_template.md) に従い、読者がゼロから手を動かして技術を体験できるチュートリアルを生成する。samples/ のコードサンプルがあれば活用する。

### B-3: プレゼンスライド

[references/slides_guide.md](references/slides_guide.md) に従い、自前の `scripts/html2pptx.js` を使用してスライドを生成する。外部スキル（`/pptx` 等）は使用しない。

手順:
1. research フォルダ内に `slides/` ディレクトリを作成
2. 各スライドを `slide_01.html` 〜 `slide_XX.html` として作成（1280x720px、自己完結型 HTML）
3. `node <このスキルのベースパス>/scripts/html2pptx.js slides/ presentation.pptx` を実行

## 出力先

```
research/{YYYY-MM-DD}_{テーマ名のケバブケース}/
  technical_report.md      # A-1
  implementation_guide.md  # A-2
  samples/                 # A-3
  blog_article.md          # B-1
  tutorial.md              # B-2
  slides/                  # B-3 (HTML ソース)
  presentation.pptx        # B-3
```

`research/` ディレクトリが存在しない場合は作成する。完了時に生成した成果物の一覧とフォルダパスをユーザーに提示する。
