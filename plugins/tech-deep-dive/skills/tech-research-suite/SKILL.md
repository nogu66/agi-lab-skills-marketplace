---
name: tech-research-suite
description: 技術テーマの調査から共有資料の作成まで全てを一括実行するオーケストレーションスキル。tech-deep-dive（調査・分析）と tech-content-gen（コンテンツ生成）を順番に実行し、レポート・実装ガイド・コードサンプル・ブログ記事・チュートリアル・スライドの6成果物を一度に生成する。「〇〇について全部まとめて」「フルリサーチして」「tech-research-suiteで△△を調査して」のような指示で発火する。
---

# Tech Research Suite

tech-deep-dive と tech-content-gen を連続実行し、1つの技術テーマについて6つの成果物を一括生成するオーケストレーター。

## 実行フロー

```
ユーザー指示（テーマ指定）
  |
  v
[tech-deep-dive]
  -> technical_report.md
  -> implementation_guide.md
  -> samples/
  |
  v
[tech-content-gen]（上記の出力を入力として使用）
  -> blog_article.md
  -> tutorial.md
  -> presentation.pptx
  |
  v
完了報告
```

## 手順

1. ユーザーからテーマを受け取る。
2. **tech-deep-dive を実行する。** research/{YYYY-MM-DD}_{テーマ名}/ フォルダに technical_report.md, implementation_guide.md, samples/ を生成する。
3. **tech-content-gen を実行する。** 同じフォルダに blog_article.md, tutorial.md, presentation.pptx を追加生成する。入力として手順2で生成された成果物を使用する。
4. 全成果物の一覧とフォルダパスをユーザーに提示する。

## 最終出力

```
research/{YYYY-MM-DD}_{テーマ名}/
  technical_report.md      # 技術理解レポート
  implementation_guide.md  # 実装応用ガイド
  samples/                 # コードサンプル集
  blog_article.md          # ブログ記事
  tutorial.md              # ハンズオンチュートリアル
  presentation.pptx        # プレゼンスライド
```
