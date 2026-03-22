# tech-deep-dive

技術テーマのマルチソース調査から、レポート・実装ガイド・コードサンプル・ブログ記事・チュートリアル・スライドまで一括生成する統合スキル。

## Requirements（必要環境）

- **Python**: 3.9以上
- **Node.js**: 18.0以上
- **npm**: 9.0以上
- **Claude Code**: 最新版

## インストール

### 前提条件の確認

```bash
# Python バージョンの確認
python --version  # 3.9以上であることを確認

# Node.js バージョンの確認
node --version    # 18.0以上であることを確認
npm --version     # 9.0以上であることを確認
```

### Claude Code マーケットプレイス経由でのインストール

```bash
/plugin marketplace add <owner>/<repo>
/plugin install tech-deep-dive@deep-dive-lab
```

### ローカルからのインストール

```bash
cd /path/to/agi-lab-skills-marketplace
/plugin install ./plugins/tech-deep-dive
```

## 使い方

### 基本的な使い方

| やりたいこと | 言い方の例 |
|---|---|
| 調査から資料まで全部 | 「〇〇について調査して」「フルリサーチして」 |
| レポート系だけ | 「レポートだけ欲しい」「コードサンプルだけ」 |
| 既存調査からコンテンツ生成 | 「調査結果をブログにして」「スライドにまとめて」 |

### プロンプトに含めるとよい情報（任意）

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

## セットアップ

### 自動セットアップ

初回実行時に依存モジュール（Playwright、requests、beautifulsoup4など）が自動的にインストールされます。手動セットアップは不要です。

### 手動セットアップ（オプション）

依存関係を明示的にインストールしたい場合：

```bash
# Python依存のインストール
python scripts/install_deps.py

# または個別にインストール
pip install -r scripts/requirements.txt

# Node.js依存のインストール
npm install --prefix scripts/
```

### インストール後の確認

```bash
# セットアップが完了したか確認
python scripts/verify_samples.py
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

## トラブルシューティング

### 依存関係がインストールできない

```bash
# キャッシュをクリアしてリトライ
pip cache purge
npm cache clean --force

# 再度セットアップを実行
python scripts/install_deps.py
```

### Python バージョンエラー

```bash
# 複数の Python がインストールされている場合は明示的にバージョンを指定
python3.9 -m pip install -r scripts/requirements.txt
```

### Playwright のインストール失敗

```bash
# Playwright のブラウザをインストール
playwright install
```

## Development

このプロジェクトに貢献したい場合：

1. リポジトリを Fork する
2. 機能ブランチを作成: `git checkout -b feature/amazing-feature`
3. 変更をコミット: `git commit -m 'Add amazing feature'`
4. ブランチに Push: `git push origin feature/amazing-feature`
5. Pull Request を作成する

### 開発環境の構築

```bash
# 開発用依存関係をインストール
pip install -e .
npm install --prefix scripts/

# テストを実行
python scripts/verify_samples.py
```

## License

MIT

## Support

問題が発生した場合は、[GitHub Issues](https://github.com/<owner>/<repo>/issues) で報告してください。
