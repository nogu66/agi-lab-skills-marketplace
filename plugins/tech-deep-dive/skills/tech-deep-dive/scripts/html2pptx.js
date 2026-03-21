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

// グローバルインストールのモジュールも解決できるようにする
function requireModule(name) {
  try {
    return require(name);
  } catch {
    const globalRoot = require('child_process')
      .execSync('npm root -g', { encoding: 'utf8' }).trim();
    return require(path.join(globalRoot, name));
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
    console.error(`ディレクトリが見つかりません: ${absSlidesDir}`);
    process.exit(1);
  }

  // HTML スライドファイルを番号順に取得
  const slideFiles = fs.readdirSync(absSlidesDir)
    .filter(f => /^slide[_-]?\d+\.html$/i.test(f))
    .sort((a, b) => {
      const numA = parseInt(a.match(/\d+/)[0], 10);
      const numB = parseInt(b.match(/\d+/)[0], 10);
      return numA - numB;
    });

  if (slideFiles.length === 0) {
    console.error('slide_*.html ファイルが見つかりません');
    process.exit(1);
  }

  console.log(`${slideFiles.length} 枚の HTML スライドを検出`);

  // モジュール読み込み
  const { chromium } = requireModule('playwright');
  const PptxGenJS = requireModule('pptxgenjs');

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
    await page.goto(`file://${htmlPath}`, { waitUntil: 'networkidle', timeout: 30000 });

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
  const absOutput = path.resolve(outputPath);
  await pptx.writeFile({ fileName: absOutput });
  console.log(`生成完了: ${absOutput}`);
}

main().catch(err => {
  console.error('エラー:', err.message);
  process.exit(1);
});
