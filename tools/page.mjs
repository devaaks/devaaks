import { chromium } from 'playwright-core'; import fs from 'fs'; import { marked } from 'marked';
const md = marked.parse(fs.readFileSync('README.md','utf8'));
const css = (f) => fs.readFileSync(`tools/node_modules/github-markdown-css/${f}`,'utf8');
const doc = (theme) => `<html><head><base href="file://${process.cwd()}/"><style>${css(theme==='dark'?'github-markdown-dark.css':'github-markdown-light.css')}</style></head>
<body style="margin:0;background:${theme==='dark'?'#0d1117':'#fff'}"><div style="width:830px;padding:24px;border:1px solid ${theme==='dark'?'#30363d':'#d0d7de'};margin:16px;border-radius:6px"><div style="font:12px ui-monospace;color:#7d8590;margin-bottom:12px">devaaks / README.md</div><article class="markdown-body">${md}</article></div></body></html>`;
const b = await chromium.launch({ executablePath: process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' });
for (const t of ['light','dark']) {
  const p = await b.newPage({ deviceScaleFactor: 1.5, viewport: { width: 900, height: 900 } });
  fs.writeFileSync(`tools/shots/page-${t}.html`, doc(t));
  await p.goto(`file://${process.cwd()}/tools/shots/page-${t}.html`); await p.waitForTimeout(700);
  await p.screenshot({ path: `tools/shots/page-${t}.png`, fullPage: true });
}
await b.close();
