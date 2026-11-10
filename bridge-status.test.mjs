import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';

const sandbox = { window: {} };
vm.createContext(sandbox);
vm.runInContext(readFileSync(new URL('./bridges.js', import.meta.url), 'utf8'), sandbox, { filename: 'bridges.js' });

const { BRIDGES, getBridgeStatus } = sandbox.window;
const bridge = Object.fromEntries(BRIDGES.map(item => [item.id, item]));
const at = (id, iso) => getBridgeStatus(bridge[id], new Date(iso));

test('eighteen bridges, Birzhevoy has the night gap, Volodarsky reopens at 05:30', () => {
  assert.equal(BRIDGES.length, 18);
  assert.equal(JSON.stringify(bridge.birzhevoy.schedule), JSON.stringify([['02:00', '02:55'], ['03:35', '04:55']]));
  assert.equal(JSON.stringify(bridge.volodarsky.schedule), JSON.stringify([['02:00', '03:45'], ['04:15', '05:30']]));
  assert.equal(bridge.bolshoy_obukhovsky.type, 'fixed');
});

test('Birzhevoy is open for cars between the two draws', () => {
  const gap = at('birzhevoy', '2026-07-15T03:10:00+03:00');
  assert.equal(gap.isDrawn, false);
  assert.equal(gap.badgeClass, 'soon');
  assert.match(gap.subtext, /03:35/);

  const drawn = at('birzhevoy', '2026-07-14T23:10:00Z');
  assert.equal(drawn.isDrawn, true);
  assert.match(drawn.subtext, /02:55/);
});

test('Volodarsky is open again at 05:35 Moscow', () => {
  assert.equal(at('volodarsky', '2026-07-15T05:20:00+03:00').isDrawn, true);
  const reopened = at('volodarsky', '2026-07-15T05:35:00+03:00');
  assert.equal(reopened.isDrawn, false);
  assert.match(reopened.subtext, /02:00/);
});

test('season starts on the morning of 10 April and ends on the morning of 30 November', () => {
  assert.equal(at('dvortsovy', '2026-04-09T02:00:00+03:00').isDrawn, false);
  assert.equal(at('dvortsovy', '2026-04-10T02:00:00+03:00').isDrawn, true);
  assert.equal(at('dvortsovy', '2026-11-30T02:00:00+03:00').isDrawn, true);
  const winter = at('dvortsovy', '2026-12-01T02:00:00+03:00');
  assert.equal(winter.isDrawn, false);
  assert.match(winter.subtext, /10 апреля/);
});

test('holiday mornings stay closed and the next draw is announced', () => {
  for (const iso of ['2026-05-02T02:00:00+03:00', '2026-05-10T02:00:00+03:00', '2026-06-13T02:00:00+03:00', '2026-11-05T02:00:00+03:00']) {
    const result = at('dvortsovy', iso);
    assert.equal(result.isDrawn, false, iso);
    assert.match(result.subtext, /праздничн/);
  }
  const eve = at('dvortsovy', '2026-05-01T23:00:00+03:00');
  assert.match(eve.subtext, /3\.05/);
});

test('Bolshaya Nevka bridges are not shown as drawn, and only inside their season', () => {
  const summer = at('sampsonievsky', '2026-07-15T02:00:00+03:00');
  assert.equal(summer.isDrawn, false);
  assert.match(summer.subtext, /заявк/);
  assert.match(at('kantemirovsky', '2026-04-15T22:00:00+03:00').subtext, /20 апреля/);
  assert.match(at('grenadersky', '2026-11-15T22:00:00+03:00').subtext, /20 апреля/);
});

test('fixed bridges stay open', () => {
  const fixed = at('bolshoy_obukhovsky', '2026-07-15T02:00:00+03:00');
  assert.equal(fixed.isDrawn, false);
  assert.equal(fixed.badgeClass, 'fixed');
});
