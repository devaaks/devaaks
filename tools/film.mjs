// node film.mjs <svg> <out.png> [--times 0,1.4,2.5] [--width 830] [--bg #fff] [--scale 2]
import { chromium } from 'playwright-core';
import fs from 'fs';
const [svgPath, out, ...rest] = process.argv.slice(2);
const opt = Object.fromEntries(rest.reduce((a, v, i, arr) => (v.startsWith('--') && a.push([v.slice(2), arr[i + 1]]), a), []));
const times = (opt.times || '0').split(',').map(Number);
const width = +(opt.width || 830), bg = opt.bg || '#ffffff', scale = +(opt.scale || 2);
const svg = fs.readFileSync(svgPath, 'utf8');
const browser = await chromium.launch({ executablePath: process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' });
const page = await browser.newPage({ deviceScaleFactor: scale, viewport: { width: width + 32, height: 900 } });
await page.setContent(`<html><body style="margin:0;padding:16px;background:${bg}"><div id="w" style="width:${width}px">${svg}</div><style>#w svg{width:100%;height:auto;display:block}</style></body></html>`);
await page.evaluate(() => document.fonts.ready);
const shots = [];
for (const t of times) {
  await page.evaluate((ms) => document.getAnimations().forEach(a => { a.pause(); a.currentTime = ms; }), t * 1000);
  await page.waitForTimeout(30);
  const b = await page.locator('#w').screenshot();
  shots.push({ t, b64: b.toString('base64') });
}
if (shots.length === 1) fs.writeFileSync(out, Buffer.from(shots[0].b64, 'base64'));
else {
  const cols = +(opt.cols || 2);
  const p2 = await browser.newPage({ deviceScaleFactor: 1, viewport: { width: cols * (width + 16) + 16, height: 800 } });
  await p2.setContent(`<body style="margin:0;padding:8px;background:#888;font:12px system-ui;display:grid;grid-template-columns:repeat(${cols},${width}px);gap:8px">${shots.map(s => `<div><div style="color:#fff">t=${s.t}s</div><img style="width:${width}px" src="data:image/png;base64,${s.b64}"></div>`).join('')}</body>`);
  await p2.screenshot({ path: out, fullPage: true });
}
await browser.close();
console.log('wrote', out);
