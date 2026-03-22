# tech-deep-dive

技術テーマのマルチソース調査から、レポート・実装ガイド・コードサンプル・ブログ記事・チュートリアル・スライドまで一括生成する統合スキル。

## 使い方

| やりたいこと | 言い方の例 |
|---|---|
| 調査から資料まで全部 | 「〇〇について調査して」「フルリサーチして」 |
| レポート系だけ | 「レポートだけ欲しい」「コードサンプルだけ」 |
| 既存調査からコンテンツ生成 | 「調査結果をブログにして」「スライドにまとめて」 |

**プロンプトに含めるとよいこと（任意）**

- **テーマ**: 何について知りたいか（例: 「Rust の async ランタイム比較」）
- **目的**: キャッチアップ / 導入判断 / 勉強会資料 など
- **範囲**: 含めたい・除外したいもの（例: 「プロダクション運用の観点は必須」）
- **想定読者**: 初心者向け／社内エンジニア向け 等

## 成果物

すべて `research/{YYYY-MM-DD}_{テーマ名}/` に出力されます。

| フェーズ | ファイル | 内容 |
|---|---|---|
| A: 調査 | `technical_report.md` | 技術理解レポート (3,000〜8,000語) |
| A: 調査 | `implementation_guide.md` | 実装応用ガイド (3,000〜6,000語) |
| A: 調査 | `samples/` | コードサンプル集 (最低3つ) |
| B: コンテンツ | `blog_article.md` | ブログ記事 (2,000〜5,000語) |
| B: コンテンツ | `tutorial.md` | チュートリアル (2,000〜4,000語) |
| B: コンテンツ | `presentation.pptx` | スライド (15〜25枚) |

## インストール

```bash
/plugin marketplace add <owner>/<repo>
/plugin install tech-deep-dive@deep-dive-lab
```

## セットアップ

初回実行時に依存モジュール（Playwright、requests、beautifulsoup4など）が自動的にインストールされます。手動セットアップは不要です。

**手動インストール（オプション）:**
```bash
python scripts/install_deps.py       # Python依存をインストール
npm install --prefix scripts/         # Node.js依存をインストール
```

## ディレクトリ構成

```text
plugins/tech-deep-dive/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── tech-deep-dive/
        ├── SKILL.md
        ├── scripts/
        │   ├── install_deps.py        # 依存管理スクリプト
        │   ├── requirements.txt       # Python依存定義
        │   ├── package.json          # Node.js依存定義
        │   ├── html2pptx.js          # スライド生成スクリプト
        │   └── verify_samples.py     # コード検証スクリプト
        └── references/
            ├── report_template.md
            ├── implementation_guide_template.md
            ├── code_samples_guide.md
            ├── evaluation_heuristics.md
            ├── blog_template.md
            ├── tutorial_template.md
            ├── slides_guide.md
            └── verification_guide.md
```

## License

MIT
