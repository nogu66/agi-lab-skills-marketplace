---
name: tech-content-gen
description: tech-deep-diveの調査結果を元に、ブログ記事・ハンズオンチュートリアル・プレゼンスライドを生成するスキル。「調査結果をブログにして」「チュートリアルを作って」「スライドにまとめて」「tech-content-genで共有資料を作って」のような指示で発火する。調査結果の共有・発信に使う。
---

# Tech Content Gen

tech-deep-dive が生成した調査結果（research/ 配下のフォルダ）を入力として、以下の3つのコンテンツを生成する。

- **ブログ記事** (blog_article.md) -- Qiita/Zennレベルの技術記事、2,000〜5,000語以上
- **ハンズオンチュートリアル** (tutorial.md) -- ステップバイステップ教材、2,000〜4,000語以上
- **プレゼンスライド** (presentation.pptx) -- 社内共有・勉強会用、15〜25枚

## 制約

- 全ての成果物は**日本語**で作成する。技術用語（固有名詞、ライブラリ名、API名等）は英語表記を維持し、必要に応じて括弧内に日本語補足を付記する。
- **絵文字を一切使用しない。**
- **コード内のコメントも日本語で記述する。**

## 前提

実行前に、対象となる research/ 配下のフォルダを特定する。ユーザーが指定しない場合は、最新の research/ フォルダを使用する。フォルダ内の technical_report.md と implementation_guide.md を読み込んで入力情報とする。

## ワークフロー

### フェーズ1: ブログ記事生成

[references/blog_template.md](references/blog_template.md) に従い、調査レポートの内容を読み物として面白い技術記事に再構成する。レポートの要約ではなく、独立した記事として書く。

### フェーズ2: ハンズオンチュートリアル生成

[references/tutorial_template.md](references/tutorial_template.md) に従い、読者がゼロから手を動かして技術を体験できるチュートリアルを生成する。samples/ のコードサンプルがあれば活用する。

### フェーズ3: プレゼンスライド生成

[references/slides_guide.md](references/slides_guide.md) に従い、`/pptx` スキルを使用してスライドを生成する。`/pptx` スキルが利用不可の場合はスキップし、その旨をユーザーに通知する。

## 出力先

既存の research/ フォルダに追記する:

```
research/{YYYY-MM-DD}_{テーマ名}/
  blog_article.md        # 新規追加
  tutorial.md            # 新規追加
  presentation.pptx      # 新規追加
```

完了時に生成した成果物の一覧をユーザーに提示する。
