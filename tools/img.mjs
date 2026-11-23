// real <img> render on GitHub light + dark grounds, after N ms of real playback
import { chromium } from 'playwright-core';
const [file, out, ms='600', width='830'] = process.argv.slice(2);
const b = await chromium.launch({ executablePath: process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', args:['--allow-file-access-from-files'] });
const p = await b.newPage({ deviceScaleFactor: 2, viewport: { width: +width*2+96, height: 700 } });
const img = `<img src="file://${process.cwd()}/${file}" style="width:${width}px;display:block">`;
await p.goto(`file://${process.cwd()}/tools/shots/blank.html`);
await p.setContent(`<body style="margin:0;display:flex"><div style="background:#fff;padding:24px">${img}</div><div style="background:#0d1117;padding:24px">${img}</div></body>`);
await p.waitForTimeout(+ms);
await p.screenshot({ path: out, fullPage: true }); await b.close(); console.log('wrote', out);
