#!/usr/bin/env node
/**
 * html2pptx.js - HTML スライドから PPTX を生成する自前スクリプト
 *
 * 使い方: node html2pptx.js <slides-dir> <output.pptx>
 *
 * slides-dir 内の slide_*.html を番号順に読み込み、
 * Playwright でレンダリング → スクリーンショット → PptxGenJS でスライド化する。
 *
 * 依存: playwright, pptxgenjs (グローバルまたはローカルインストール)
 */

const path = require('path');
const fs = require('fs');

// 依存モジュール自動インストール
function ensureDependencies() {
  const { execSync } = require('child_process');
  const packageJsonPath = path.join(__dirname, 'package.json');

  if (fs.existsSync(packageJsonPath)) {
    try {
      const nodeModulesPath = path.join(__dirname, 'node_modules');
      if (!fs.existsSync(nodeModulesPath)) {
        console.log('依存モジュールをインストール中...');
        execSync('npm install --quiet', { cwd: __dirname, stdio: 'pipe' });
        console.log('✓ 依存モジュールをインストールしました');
      }
    } catch (error) {
      console.error('警告: 依存モジュールのインストールに失敗しました');
      // インストール失敗時も続行（グローバルインストールが存在するかもしれない）
    }
  }
}

ensureDependencies();

// グローバルインストールのモジュールも解決できるようにする
function requireModule(name) {
  // まずローカルパッケージを試す
  try {
    return require(name);
  } catch (e) {
    // ローカルが失敗したら、スクリプトディレクトリの node_modules を試す
    try {
      return require(path.join(__dirname, 'node_modules', name));
    } catch {
      // それでも失敗したらグローバルを試す
      try {
        const { execSync } = require('child_process');
        const globalRoot = execSync('npm root -g', { encoding: 'utf8' }).trim();
        return require(path.join(globalRoot, name));
      } catch (globalError) {
        throw new Error(`モジュール '${name}' が見つかりません。以下を実行してください:\npython ${path.join(__dirname, 'install_deps.py')}`);
      }
    }
  }
}

// 16:9 標準レイアウト (13.33" x 7.5")
const VIEWPORT_W = 1280;
const VIEWPORT_H = 720;
const PPTX_W = 13.33;
const PPTX_H = 7.5;

async function main() {
  const [,, slidesDir, outputPath] = process.argv;

  if (!slidesDir || !outputPath) {
    console.error('使い方: node html2pptx.js <slides-dir> <output.pptx>');
    process.exit(1);
  }

  const absSlidesDir = path.resolve(slidesDir);
  if (!fs.existsSync(absSlidesDir)) {
    console.error(`エラー: スライドディレクトリが見つかりません: ${absSlidesDir}`);
    process.exit(1);
  }

  // 出力先ディレクトリの作成確認
  const absOutput = path.resolve(outputPath);
  const outputDir = path.dirname(absOutput);
  if (!fs.existsSync(outputDir)) {
    try {
      fs.mkdirSync(outputDir, { recursive: true });
      console.log(`出力ディレクトリを作成しました: ${outputDir}`);
    } catch (err) {
      console.error(`エラー: 出力ディレクトリを作成できません: ${err.message}`);
      process.exit(1);
    }
  }

  // HTML スライドファイルを番号順に取得
  const slideFiles = fs.readdirSync(absSlidesDir)
    .filter(f => {
      const match = /^slide[_-]?(\d+)\.html$/i.test(f);
      return match;
    })
    .sort((a, b) => {
      const matchA = a.match(/(\d+)/);
      const matchB = b.match(/(\d+)/);
      const numA = matchA ? parseInt(matchA[1], 10) : 0;
      const numB = matchB ? parseInt(matchB[1], 10) : 0;
      return numA - numB;
    });

  if (slideFiles.length === 0) {
    console.error('slide_*.html ファイルが見つかりません');
    process.exit(1);
  }

  console.log(`${slideFiles.length} 枚の HTML スライドを検出`);

  // モジュール読み込み
  const playwright = requireModule('playwright');
  const { chromium } = playwright;
  const PptxGenJS = requireModule('pptxgenjs');

  // Playwright ブラウザのインストール確認（初回実行時）
  try {
    console.log('Playwright ブラウザをチェック中...');
    await playwright.chromium.executablePath();
  } catch {
    console.log('Playwright ブラウザをインストール中...');
    await chromium.downloadBrowserIfNeeded?.();
  }

  // Playwright 起動
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: VIEWPORT_W, height: VIEWPORT_H },
  });

  // PptxGenJS セットアップ
  const pptx = new PptxGenJS();
  pptx.defineLayout({ name: 'WIDE_16x9', width: PPTX_W, height: PPTX_H });
  pptx.layout = 'WIDE_16x9';

  for (let i = 0; i < slideFiles.length; i++) {
    const file = slideFiles[i];
    console.log(`スライド ${i + 1}/${slideFiles.length} を変換中: ${file}`);

    const page = await context.newPage();
    const htmlPath = path.join(absSlidesDir, file);
    try {
      await page.goto(`file://${htmlPath}`, { waitUntil: 'load', timeout: 30000 });
    } catch (err) {
      console.error(`エラー: ${file} の読み込みに失敗: ${err.message}`);
      await page.close();
      throw err;
    }

    // スクリーンショットを Base64 で取得
    const buf = await page.screenshot({ type: 'png' });
    const b64 = buf.toString('base64');

    // スライドに画像として追加
    const slide = pptx.addSlide();
    slide.addImage({
      data: `image/png;base64,${b64}`,
      x: 0, y: 0, w: PPTX_W, h: PPTX_H,
    });

    await page.close();
  }

  await browser.close();

  // 保存
  try {
    // PptxGenJS のバージョン互換性対応
    if (typeof pptx.writeFile === 'function') {
      await pptx.writeFile({ fileName: absOutput });
    } else if (typeof pptx.save === 'function') {
      await pptx.save({ fileName: absOutput });
    } else {
      throw new Error('PptxGenJS の保存メソッドが見つかりません');
    }

    // ファイルが実際に生成されたか確認
    if (fs.existsSync(absOutput)) {
      const stats = fs.statSync(absOutput);
      console.log(`生成完了: ${absOutput} (${stats.size} バイト)`);
    } else {
      throw new Error(`ファイルが生成されませんでした: ${absOutput}`);
    }
  } catch (err) {
    console.error(`エラー: PPTX ファイルの生成に失敗: ${err.message}`);
    throw err;
  }
}

main().catch(err => {
  console.error('\n❌ PPTX 生成に失敗しました');
  console.error('エラー:', err.message);

  // スタックトレースは詳細には出力しない（ただし DEBUG=1 の場合は出力）
  if (process.env.DEBUG === '1') {
    console.error('\nスタックトレース:');
    console.error(err.stack);
  }

  console.error('\n対処方法:');
  console.error('1. 依存モジュールをインストール: python scripts/install_deps.py');
  console.error('2. スライドディレクトリが存在することを確認');
  console.error('3. slide_*.html ファイルが存在することを確認');

  process.exit(1);
});
