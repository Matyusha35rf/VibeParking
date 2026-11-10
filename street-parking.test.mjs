import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';

const sandbox = { window: {} };
vm.createContext(sandbox);
vm.runInContext(readFileSync(new URL('./street-parking.js', import.meta.url), 'utf8'), sandbox, { filename: 'street-parking.js' });
const { STREET_PARKING, streetParkingStatus } = sandbox.window;
const avenue = STREET_PARKING[0];

test('Dalnevostochny is one continuous curb rule', () => {
  assert.equal(avenue.id, 'dalnevostochny');
  assert.equal(avenue.ban.weekday, 'Sat');
  assert.equal(avenue.ban.from, 7 * 60);
  assert.equal(avenue.ban.to, 22 * 60);
  assert.ok(avenue.lines.length > 40);
  assert.equal(avenue.lines.filter(part => part.oneway).length > 40, true);
});

test('parking is banned only on Saturday from 07:00 to 22:00 Moscow', () => {
  const banned = streetParkingStatus(avenue, new Date('2026-11-14T04:00:00Z'));
  assert.equal(banned.allowed, false);
  assert.match(banned.text, /запрещена/);

  const before = streetParkingStatus(avenue, new Date('2026-11-14T03:59:00Z'));
  assert.equal(before.allowed, true);

  const after = streetParkingStatus(avenue, new Date('2026-11-14T19:00:00Z'));
  assert.equal(after.allowed, true);

  const friday = streetParkingStatus(avenue, new Date('2026-11-13T10:00:00+03:00'));
  assert.equal(friday.allowed, true);
});
