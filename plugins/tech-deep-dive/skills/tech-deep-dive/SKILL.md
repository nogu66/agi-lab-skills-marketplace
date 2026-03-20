---
name: tech-deep-dive
description: 特定の技術テーマに関するマルチソース（arXiv、GitHub、技術ブログ、公式ドキュメント等）調査を自律的に実行し、技術理解レポート・実装応用ガイド・コードサンプル集を生成するスキル。「〇〇について調査して」「〇〇の技術深掘りして」「tech-deep-diveで△△を調べて」のような指示で発火する。技術キャッチアップ、競合調査、導入検討に使う。
---

# Tech Deep Dive

指定された技術テーマについて、Web上の複数ソースを横断的に調査し、以下の3つの成果物を自律的に生成する。

- **技術理解レポート** (technical_report.md) -- 3,000〜8,000語以上の本格的な技術分析
- **実装応用ガイド** (implementation_guide.md) -- 3,000〜6,000語以上の実践ガイド
- **コードサンプル集** (samples/) -- 最低3つの動作するコードサンプル

## 制約

- 全ての成果物は**日本語**で作成する。技術用語（固有名詞、ライブラリ名、API名等）は英語表記を維持し、必要に応じて括弧内に日本語補足を付記する。
- **絵文字を一切使用しない。**
- **コード内のコメントも日本語で記述する。**

## ワークフロー

### フェーズ1: 技術理解レポート生成

1. **マルチソース並列調査**: `WebSearch` と `WebFetch` で5つの主要ソース（arXiv, GitHub, 技術ブログ, 公式ドキュメント, スライド/動画）から各3件以上の情報を収集する。
2. **情報の統合とクロスリファレンス**: 論文 → GitHub実装 → ブログ解説の関係性を紐付ける。
3. **分野・技術スタックの特定**: テーマが属する技術分野と関連する主要な技術スタックを特定する。
4. **評価軸の動的生成**: [references/evaluation_heuristics.md](references/evaluation_heuristics.md) を参照し、分野に最適な評価軸を決定する。
5. **レポート執筆**: [references/report_template.md](references/report_template.md) のテンプレートに従い、technical_report.md を生成する。

### フェーズ2: 実装応用ガイド作成

フェーズ1の調査結果を元に、[references/implementation_guide_template.md](references/implementation_guide_template.md) に従い implementation_guide.md を生成する。

### フェーズ3: コードサンプル集の生成

[references/code_samples_guide.md](references/code_samples_guide.md) に従い、samples/ ディレクトリにコードサンプルを生成する。

## 出力先

```
research/{YYYY-MM-DD}_{テーマ名のケバブケース}/
  technical_report.md
  implementation_guide.md
  samples/
    README.md
    basic_example/
    practical_example/
    advanced_example/
```

`research/` ディレクトリが存在しない場合は作成する。完了時にフォルダパスと各成果物の概要をユーザーに提示する。
