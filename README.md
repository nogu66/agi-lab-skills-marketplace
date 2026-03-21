# tech-deep-dive

技術テーマのマルチソース調査・分析・コンテンツ生成を行う 3 スキルセット（`tech-deep-dive` / `tech-content-gen` / `tech-research-suite`）。単体でも組み合わせでも使用できます。

## 使い方（概要）

| やりたいこと | 使うスキル | 目安 |
|--------------|------------|------|
| 調査だけ先に済ませたい（レポート・実装ガイド・サンプルコードまで） | `tech-deep-dive` | テーマを一文で指定すれば開始できる |
| 既にある調査結果を記事・チュートリアル・スライドにしたい | `tech-content-gen` | 対象の `research/...` フォルダが必要 |
| 調査から外向きの資料まで一気に欲しい | `tech-research-suite` | 時間・トークンは最大になる |

**プロンプトに含めるとよいこと（任意だが精度が上がる）**

- **テーマ**: 何について知りたいか（例: 「Rust の async ランタイム比較」）
- **目的**: キャッチアップ / 導入判断 / 勉強会資料 など
- **範囲**: 含めたい・除外したいもの（例: 「プロダクション運用の観点は必須、歴史背景は短く」）
- **コンテンツ系のみ**: 想定読者（初心者向け／社内エンジニア向け 等）

**出力フォルダの規則**

- すべて `research/{YYYY-MM-DD}_{テーマ名のケバブケース}/` にまとまります（日付は実行日、`{テーマ名}` は英語のケバブケースが目安）。
- `tech-content-gen` は **同じフォルダに追記**します。フォルダを指定しない場合は **最新の `research/` 配下**が使われます。意図した調査結果で記事化したいときは、**パスを明示**してください（例: `research/2025-03-21_rust-async-runtimes/`）。

**スライド（`presentation.pptx`）について**

- `tech-content-gen` / `tech-research-suite` は、環境に **pptx 生成スキル**（`/pptx` 等）がある前提でスライドを作成します。**利用できない場合はスライドはスキップ**され、その旨が伝わる想定です。ブログ・チュートリアルは通常どおり生成されます。

詳細なワークフロー・テンプレートは `plugins/tech-deep-dive/skills/*/SKILL.md` および各 `references/` を参照してください。

## スキル一覧

### tech-deep-dive（調査・分析）

出力先: `research/{YYYY-MM-DD}_{テーマ名}/`（`research/` が無ければ作成）

成果物:

| ファイル | 内容 |
|----------|------|
| `technical_report.md` | 技術理解レポート（3,000〜8,000 語以上を目安） |
| `implementation_guide.md` | 実装応用ガイド（3,000〜6,000 語以上を目安） |
| `samples/` | コードサンプル集（最低 3 つの動作するサンプル） |

特定の技術テーマに関するマルチソース（arXiv、GitHub、技術ブログ、公式ドキュメント等）調査を自律的に実行し、技術理解レポート・実装応用ガイド・コードサンプル集を生成します。「〇〇について調査して」「〇〇の技術深掘りして」「tech-deep-dive で △△ を調べて」のような指示で発火します。技術キャッチアップ、競合調査、導入検討に使います。

**処理の流れ（要約）**: Web 上の複数ソースを調査 → `technical_report.md` → `implementation_guide.md` → `samples/`（最低 3 サンプル）。完了時に出力フォルダのパスと概要が示されます。

### tech-content-gen（コンテンツ生成）

`tech-deep-dive` の調査結果を元に、ブログ記事・ハンズオンチュートリアル・プレゼンスライドを生成します。「調査結果をブログにして」「チュートリアルを作って」「スライドにまとめて」「tech-content-gen で共有資料を作って」のような指示で発火します。調査結果の共有・発信に使います。

前提: 対象の `research/` 配下フォルダを特定する。未指定なら最新の `research/` を使用。`technical_report.md` と `implementation_guide.md` を入力とする。

成果物:

| ファイル | 内容 |
|----------|------|
| `blog_article.md` | Qiita / Zenn レベルの技術記事（2,000〜5,000 語以上を目安） |
| `tutorial.md` | ステップバイステップのハンズオン（2,000〜4,000 語以上を目安） |
| `presentation.pptx` | 社内共有・勉強会用スライド（15〜25 枚を目安） |

出力先: 上記と同じ `research/{YYYY-MM-DD}_{テーマ名}/` に追記

**処理の流れ（要約）**: 指定フォルダの `technical_report.md` と `implementation_guide.md` を読む → `blog_article.md` → `tutorial.md`（`samples/` があれば活用）→ `presentation.pptx`（pptx スキル不可時はスキップの可能性あり）。

### tech-research-suite（一括実行）

技術テーマの調査から共有資料の作成まで一括で実行するオーケストレーションです。`tech-deep-dive` と `tech-content-gen` を順に実行し、レポート・実装ガイド・コードサンプル・ブログ記事・チュートリアル・スライドの 6 成果物を一度に生成します。「〇〇について全部まとめて」「フルリサーチして」「tech-research-suite で △△ を調査して」のような指示で発火します。

**処理の流れ（要約）**: まず `tech-deep-dive` と同じ成果物を同一フォルダに生成 → 続けて `tech-content-gen` で同フォルダに 3 ファイルを追記。途中で止めたい場合は、代わりにスキルを分けて実行してください。

最終出力（同一フォルダ）:

```
research/{YYYY-MM-DD}_{テーマ名}/
  technical_report.md
  implementation_guide.md
  samples/
  blog_article.md
  tutorial.md
  presentation.pptx
```

## 共通の制約（各スキル）

- 成果物は**日本語**（技術用語・固有名詞等は英語表記を維持し、必要なら括弧で補足）
- **絵文字は使わない**
- コード内コメントは**日本語**

## Claude Code でのインストールと起動例

marketplace 名は **agi-lab-skills** です。`<owner>/<repo>` はホストしているリポジトリに読み替えてください。

```bash
/plugin marketplace add <owner>/<repo>
/plugin install tech-deep-dive@agi-lab-skills
```

インストール後、通常のチャットで **スキル名ややりたいことを自然文で書く**と、該当スキルの説明（`description`）にマッチして利用されます。次のような言い方がそのまま使えます。

**調査のみ（`tech-deep-dive`）**

- 「PostgreSQL の論理レプリケーションとストリーミング複製の違いを tech-deep-dive で調べて。導入判断に使う。」
- 「〇〇の技術深掘りして。公式ドキュメントと実装例を重視して。」

**調査済みフォルダから記事化（`tech-content-gen`）**

- 「`research/2025-03-21_postgresql-replication/` の結果を元に、tech-content-gen でブログとチュートリアルとスライドを作って。」
- パス省略時は **最新の `research/`** が選ばれるため、複数テーマがある場合は **必ずフォルダを指定**する。

**一括（`tech-research-suite`）**

- 「GraphQL の N+1 と DataLoader についてフルリサーチして。社内勉強会用の資料まで欲しい。」

**Cursor 等の別クライアント**

- プラグインではなく **リポジトリの `plugins/tech-deep-dive/skills/` をエージェントのスキルとして読み込む**運用の場合も、上記と同様にテーマ・目的・（任意で）出力フォルダを指示してください。

## ディレクトリ構成（本 plugin）

```text
plugins/tech-deep-dive/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    ├── tech-deep-dive/
    │   ├── SKILL.md
    │   └── references/
    ├── tech-content-gen/
    │   ├── SKILL.md
    │   └── references/
    └── tech-research-suite/
        └── SKILL.md
```

## License

MIT
