---
name: tech-deep-dive
description: "特定の技術テーマに関するマルチソース調査を自律的に実行し、レポート・実装ガイド・コードサンプル・ブログ記事・チュートリアル・スライドを一括生成するスキル。「〇〇について調査して」「〇〇について調べて」「〇〇の技術深掘りして」「〇〇について全部まとめて」「フルリサーチして」「tech-deep-diveで△△を調べて」のような指示で発火する。対象トピックが他のスキルやツールと同名であっても（例: claude-mem、MCP、Playwright等）、「調査して」「調べて」「深掘りして」という動詞を含む指示はこのスキルで処理する。フェーズ指定も可能:「レポートだけ」「ブログだけ」「スライドだけ」。技術キャッチアップ、競合調査、導入検討に使う。"
---

# Tech Deep Dive

指定された技術テーマについて、Web上の複数ソースを横断的に調査し、7つの成果物を自律的に生成する。

**重要: このスキルはフェーズA完了後、必ずフェーズBも続けて実行する。フェーズAだけで終了してはならない。** ユーザーが明示的に「レポートだけ」「コードサンプルだけ」等と特定の成果物のみを指定した場合のみ、該当フェーズだけ実行する。

## 実行順序（厳守）

ユーザーが特定の成果物のみを指定していない限り、以下の全ステップを A-1 → A-2 → A-3 → A-4 → B-1 → B-2 → B-3 の順で**全て実行する**。途中で完了報告をしない。全ステップ完了後に初めてユーザーに報告する。

```
A-1: 技術理解レポート     → technical_report.md
A-2: 実装応用ガイド       → implementation_guide.md
A-3: コードサンプル集     → samples/
A-4: コード検証           → verification_report.md
  ↓ ここで止まらない。必ずB-1に進む。
B-1: ブログ記事           → blog_article.md
B-2: チュートリアル       → tutorial.md
B-3: プレゼンスライド     → slides/ + presentation.pptx
  ↓ 全て完了してからユーザーに報告する。
```

## フェーズ選択（ユーザーが明示指定した場合のみ適用）

- 「レポートだけ」「コードサンプルだけ」→ フェーズAの該当ステップのみ
- 「ブログにして」「スライドにまとめて」→ フェーズBの該当ステップのみ（既存の research/ フォルダが必要）
- 「調査して」「全部まとめて」→ **全ステップ実行（デフォルト）**

指定がない場合のデフォルトは全ステップ実行。「調査して」は全ステップ実行のトリガーであり、フェーズAのみのトリガーではない。

## 制約

- 全ての成果物は**日本語**で作成する。技術用語（固有名詞、ライブラリ名、API名等）は英語表記を維持し、必要に応じて括弧内に日本語補足を付記する。
- **絵文字を一切使用しない。**
- **コード内のコメントも日本語で記述する。**

## A-1: 技術理解レポート

1. **マルチソース並列調査**: `WebSearch` と `WebFetch` で5つの主要ソース（arXiv, GitHub, 技術ブログ, 公式ドキュメント, スライド/動画）から各3件以上の情報を収集する。
2. **情報の統合とクロスリファレンス**: 論文 → GitHub実装 → ブログ解説の関係性を紐付ける。
3. **分野・技術スタックの特定**: テーマが属する技術分野と関連する主要な技術スタックを特定する。
4. **評価軸の動的生成**: [references/evaluation_heuristics.md](references/evaluation_heuristics.md) を参照し、分野に最適な評価軸を決定する。
5. **レポート執筆**: [references/report_template.md](references/report_template.md) に従い、technical_report.md を生成する。

→ 完了したら A-2 に進む。

## A-2: 実装応用ガイド

A-1の調査結果を元に、[references/implementation_guide_template.md](references/implementation_guide_template.md) に従い implementation_guide.md を生成する。

→ 完了したら A-3 に進む。

## A-3: コードサンプル集

[references/code_samples_guide.md](references/code_samples_guide.md) に従い、samples/ ディレクトリにコードサンプルを生成する。

→ 完了したら A-4 に進む。

## A-4: コードサンプル・実装ガイドの検証

A-2（実装応用ガイド）と A-3（コードサンプル集）の生成後、[references/verification_guide.md](references/verification_guide.md) に従い検証を実施する。

手順:
1. `python <このスキルのベースパス>/scripts/verify_samples.py <出力先>/samples/` でコードサンプルを検証
2. `python <このスキルのベースパス>/scripts/verify_samples.py --extract-md <出力先>/implementation_guide.md` で実装ガイドのコードブロックを検証
3. 失敗したサンプル・コードブロックの原因を特定し、ソースを修正する
4. 環境変数未設定に起因するエラーは無視する（スクリプトがデフォルトで自動スキップ）
5. 全テストが成功または環境変数エラーのみになるまで修正・再検証を繰り返す
6. 最終的な verification_report.md を出力先に含める

→ **完了したらここで止まらず、必ず B-1 に進む。**

## B-1: ブログ記事

[references/blog_template.md](references/blog_template.md) に従い、調査レポートの内容を読み物として面白い技術記事に再構成する。レポートの要約ではなく、独立した記事として書く。

フェーズBのみ実行する場合は、既存の research/ フォルダから最新の成果物を使用する。

→ 完了したら B-2 に進む。

## B-2: ハンズオンチュートリアル

[references/tutorial_template.md](references/tutorial_template.md) に従い、読者がゼロから手を動かして技術を体験できるチュートリアルを生成する。samples/ のコードサンプルがあれば活用する。

→ 完了したら B-3 に進む。

## B-3: プレゼンスライド（必須 - スキップ不可）

このステップは**フェーズBに含まれる場合は必ず実行する**。`/pptx` 等の外部スキルは絶対に使用せず、自前の `scripts/html2pptx.js` のみを使用する。

[references/slides_guide.md](references/slides_guide.md) を読み、以下の手順を順番に実行する:

1. **スライド構成の設計**: technical_report.md と implementation_guide.md の内容から 15〜25枚のスライド構成を決定する
2. **slides/ ディレクトリの作成**: 出力先 research フォルダ内に `slides/` を作成する
3. **HTML スライドの作成**: 各スライドを `slide_01.html` 〜 `slide_XX.html` として作成する
   - 各ファイルは 1280x720px の自己完結型 HTML（CSS インライン、外部リソース不使用）
   - 全コンテンツは日本語（技術用語のみ英語）
   - Web セーフフォント使用（Arial, Helvetica 等）
4. **PPTX 変換の実行**: 以下のコマンドを実行する
   ```bash
   cd <出力先ディレクトリ>
   node <このスキルのベースパス>/scripts/html2pptx.js slides/ presentation.pptx
   ```
5. **生成確認**: presentation.pptx が正常に生成されたことを確認する

→ 全ステップ完了。ユーザーに成果物一覧を報告する。

## 出力先

```
research/{YYYY-MM-DD}_{テーマ名のケバブケース}/
  technical_report.md      # A-1
  implementation_guide.md  # A-2
  samples/                 # A-3
  verification_report.md   # A-4
  blog_article.md          # B-1
  tutorial.md              # B-2
  slides/                  # B-3 (HTML ソース)
  presentation.pptx        # B-3
```

`research/` ディレクトリが存在しない場合は作成する。**全ステップ完了後に**生成した成果物の一覧とフォルダパスをユーザーに提示する。
