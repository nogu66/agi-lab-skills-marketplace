# プレゼンスライド 生成ガイド

## 目次

1. [概要](#概要)
2. [依存パッケージ](#依存パッケージ)
3. [生成プロセス](#生成プロセス)
4. [言語要件](#言語要件)
5. [品質基準](#品質基準)

## 概要

自前の `scripts/html2pptx.js` を使用して、HTML スライドから PPTX を生成する。外部スキル（`/pptx` 等）には依存しない。

## 依存パッケージ

以下がグローバルまたはローカルにインストールされていること（スクリプトが自動解決する）:

- `playwright` (Chromium ブラウザ同梱)
- `pptxgenjs`

## 生成プロセス

### 1. スライド内容の構成

tech-deep-dive の成果物（technical_report.md, implementation_guide.md）から、以下の構成で **15〜25枚** のスライドを設計する:

- 表紙（テーマ名、調査日）
- 目次
- エグゼクティブサマリー（1〜2枚）
- 背景と課題（2〜3枚）
- コア技術の解説（3〜5枚、図解を含む）
- 主要アプローチの比較（2〜3枚、比較表を含む）
- 実装方法の概要（2〜3枚）
- デモ/コードサンプルの紹介（1〜2枚）
- 採用事例・ユースケース（1〜2枚）
- まとめと次のアクション（1〜2枚）
- 参考文献（1枚）

### 2. HTML スライドの作成

research フォルダ内に `slides/` ディレクトリを作成し、各スライドを個別の HTML ファイルとして書く:

```
slides/
  slide_01.html
  slide_02.html
  ...
  slide_20.html
```

各 HTML ファイルの要件:

- ビューポート: **1280×720px**（16:9 標準）
- 自己完結型: CSS はインライン or `<style>` タグで記述
- フォント: Web セーフフォント（Arial, Helvetica, Verdana, Georgia 等）を使用
- 外部リソース不要: 画像は Base64 data URI またはローカル絶対パスで埋め込む

HTML テンプレート例:

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { width: 1280px; height: 720px; overflow: hidden; font-family: Arial, sans-serif; }
  .slide { width: 100%; height: 100%; padding: 60px; display: flex; flex-direction: column; justify-content: center; }
  h1 { font-size: 44px; margin-bottom: 24px; }
  p { font-size: 24px; line-height: 1.6; }
  ul { font-size: 22px; line-height: 1.8; margin-left: 32px; }
</style>
</head>
<body>
<div class="slide" style="background: #1a1a2e; color: #eee;">
  <h1>スライドタイトル</h1>
  <ul>
    <li>ポイント1</li>
    <li>ポイント2</li>
    <li>ポイント3</li>
  </ul>
</div>
</body>
</html>
```

### 3. PPTX の生成

自前スクリプトを実行する:

```bash
node <skill-base>/scripts/html2pptx.js slides/ presentation.pptx
```

`<skill-base>` はこのスキルの SKILL.md があるディレクトリのパス。

スクリプトの動作:
1. `slides/` 内の `slide_*.html` を番号順にソート
2. Playwright (headless Chromium) で各 HTML をレンダリング
3. スクリーンショットを撮影し PptxGenJS でスライド画像として追加
4. `presentation.pptx` として保存

## 言語要件

スライドの全コンテンツを日本語で作成すること:
- スライドタイトル、見出し・小見出し、本文・箇条書き
- 図表のキャプション・ラベル

技術用語（固有名詞、ライブラリ名、API名、コード等）のみ英語表記を維持する。

## 品質基準

- 1枚のスライドに詰め込みすぎず、**1スライド1メッセージ**を原則とする。
- 箇条書きは1スライドあたり最大5〜6項目に抑える。
- 配色に一貫性を持たせる（ダーク系/ライト系のどちらかに統一）。
- コードスニペットは `<pre><code>` で等幅フォント表示する。
- 図解が必要な場合は HTML/CSS で描画する（SVG も可）。
