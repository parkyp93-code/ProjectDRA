const { chromium } = require(require('child_process').execSync('npm root -g').toString().trim() + '/playwright');
const SP = require('os').tmpdir() + '/';
const URL = 'file:///home/user/ProjectDRA/drachma_trpg/site/index.html';
const TABS = ['map', 'timeline', 'people', 'org', 'strategic', 'damocles', 'session'];
(async () => {
  const browser = await chromium.launch();
  const results = [];
  for (const preset of [null, 'C', 'A']) {
    for (const w of [1440, 390]) {
      const ctx = await browser.newContext({ viewport: { width: w, height: 900 } });
      if (preset) await ctx.addInitScript(p => { try { localStorage.setItem('drachma.branch', JSON.stringify(p)); } catch (e) {} }, preset);
      const page = await ctx.newPage();
      const errs = [];
      page.on('pageerror', e => errs.push('pageerror: ' + e.message));
      page.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text()); });
      for (const t of TABS) {
        errs.length = 0;
        await page.goto(URL + '#' + t);
        await page.waitForTimeout(250);
        const info = await page.evaluate(() => ({
          ov: document.documentElement.scrollWidth - innerWidth,
          hash: location.hash,
          vis: [...document.querySelectorAll('section.view')].filter(s => !s.hidden).map(s => s.id),
          branchBtns: [...document.querySelectorAll('#branchSwitch button')].map(b => b.textContent),
          stored: localStorage.getItem('drachma.branch'),
        }));
        results.push({ preset, w, t, errs: [...errs], ...info });
        if (!preset && w === 1440 && ['map', 'org', 'strategic', 'session', 'people', 'timeline'].includes(t))
          await page.screenshot({ path: SP + `shot_${t}_${w}.png`, fullPage: t !== 'map' });
        if (!preset && w === 390 && ['map', 'strategic', 'org'].includes(t))
          await page.screenshot({ path: SP + `shot_${t}_${w}.png`, fullPage: true });
      }
      await ctx.close();
    }
  }
  for (const r of results) console.log(JSON.stringify(r));
  const bad = results.filter(r => r.errs.length || r.ov !== 0);
  console.log('BAD', bad.length);
  await browser.close();
})();
