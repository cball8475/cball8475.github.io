// shoot.cjs — screenshot site pages at phone and desktop width for visual review.
//
// Usage (from the repo root):
//   node .claude/skills/frontend-design/shoot.cjs about.html pricing.html [--out DIR]
//
// Serves the repo root on a throwaway localhost port so root-absolute paths
// (/fsc-brand.css, /images/...) resolve the way GitHub Pages resolves them.
// Analytics and call-tracking requests are blocked so a review never registers
// as a visit and CallRail never swaps the phone number in the shot. Google
// Fonts are allowed; the script lists the web-font families that actually
// loaded, so a shot rendered in a fallback face is caught.
//
// Read-only: it writes PNGs to --out (default: $TMPDIR or /tmp) and nothing else.
// CommonJS on purpose: the preinstalled Playwright is found through NODE_PATH,
// which require() honors and ESM import does not.
const { createServer } = require('node:http');
const { readFile } = require('node:fs/promises');
const { extname, join, normalize, resolve } = require('node:path');
const { chromium } = require('playwright');

const ROOT = process.cwd();
const args = process.argv.slice(2);
const outIdx = args.indexOf('--out');
const OUT = outIdx >= 0 ? resolve(args.splice(outIdx, 2)[1]) : (process.env.TMPDIR || '/tmp');
const pages = args.length ? args : ['index.html'];

const TYPES = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.svg': 'image/svg+xml',
  '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.ico': 'image/x-icon' };
const BLOCK = /googletagmanager|google-analytics|callrail|cdn-cgi|clarity\.ms|facebook/;
const WIDTHS = [{ name: 'phone', width: 390, height: 844 }, { name: 'desktop', width: 1280, height: 800 }];

const server = createServer(async (req, res) => {
  let p = decodeURIComponent(new URL(req.url, 'http://x').pathname);
  if (p.endsWith('/')) p += 'index.html';
  const file = normalize(join(ROOT, p));
  if (!file.startsWith(ROOT)) { res.writeHead(403).end(); return; }
  try {
    const body = await readFile(file);
    res.writeHead(200, { 'content-type': TYPES[extname(file)] || 'application/octet-stream' }).end(body);
  } catch { res.writeHead(404).end(); }
});
(async () => {
await new Promise(r => server.listen(0, '127.0.0.1', r));
const base = `http://127.0.0.1:${server.address().port}`;

const browser = await chromium.launch();
try {
  for (const page of pages) {
    for (const vp of WIDTHS) {
      const ctx = await browser.newContext({ viewport: { width: vp.width, height: vp.height } });
      const tab = await ctx.newPage();
      await tab.route('**/*', r => BLOCK.test(r.request().url()) ? r.abort() : r.continue());
      const missing = [];
      tab.on('response', r => { if (r.url().startsWith(base) && r.status() === 404) missing.push(r.url().slice(base.length)); });
      await tab.goto(`${base}/${page}`, { waitUntil: 'networkidle', timeout: 20000 }).catch(() => {});
      // document.fonts.check() returns true when no @font-face matches at all,
      // so list loaded families instead of trusting it.
      const fonts = await tab.evaluate(() => [...new Set([...document.fonts]
        .filter(f => f.status === 'loaded').map(f => f.family.replace(/["']/g, '')))]).catch(() => []);
      const overflow = await tab.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
      const png = join(OUT, `${page.replace(/[\/.]/g, '_')}-${vp.name}.png`);
      await tab.screenshot({ path: png, fullPage: true });
      console.log([png,
        fonts.length ? `fonts: ${fonts.join(', ')}` : 'fonts: NONE loaded (fallback face in shot)',
        overflow > 0 ? `HORIZONTAL OVERFLOW ${overflow}px` : 'no horizontal overflow',
        missing.length ? `404s: ${missing.join(', ')}` : 'no local 404s'].join(' | '));
      await ctx.close();
    }
  }
} finally {
  await browser.close();
  server.close();
}
})();
