import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';

const sandbox = { window: {} };
vm.createContext(sandbox);
vm.runInContext(readFileSync(new URL('./street-parking.js', import.meta.url), 'utf8'), sandbox, { filename: 'street-parking.js' });
const { STREET_PARKING, STREET_PARKING_SOURCE, streetParkingStatus } = sandbox.window;

const byId = Object.fromEntries(STREET_PARKING.map(item => [item.id, item]));

test('right-bank Nevsky list comes from the Avtopark 7 sign schedule', () => {
  assert.equal(STREET_PARKING_SOURCE.area, 'Невский район, правый берег');
  assert.match(STREET_PARKING_SOURCE.url, /Знаки-3\.27-Невский-правый-берег/);
  assert.ok(STREET_PARKING.length >= 80);
  for (const item of STREET_PARKING) {
    assert.ok(item.line.length >= 2);
    assert.ok(item.ban.from < item.ban.to);
    assert.match(item.side, /сторона/);
    for (const [lat, lon] of item.line) {
      assert.ok(lat > 59.86 && lat < 59.95);
      assert.ok(lon > 30.40 && lon < 30.52);
    }
  }
});

test('Dalnevostochny is split by side and is not a Saturday 07:00–22:00 ban', () => {
  const parts = STREET_PARKING.filter(item => item.name === 'Дальневосточный проспект');
  assert.ok(parts.length >= 3);
  assert.equal(parts.some(item => item.ban.weekday === 'Sat' && item.ban.from === 7 * 60 && item.ban.to === 22 * 60), false);
  const saturdayNight = byId.n17;
  assert.equal(saturdayNight.side, 'нечётная сторона');
  assert.equal(saturdayNight.ban.weekday, 'Sat');
  assert.equal(saturdayNight.ban.from, 0);
  assert.equal(saturdayNight.ban.to, 7 * 60);
});

test('a sign is active only inside its weekday and hours, Moscow time', () => {
  const night = streetParkingStatus(byId.n17, new Date('2026-11-14T01:30:00+03:00'));
  assert.equal(night.active, true);
  assert.match(night.text, /запрещена/);

  const morning = streetParkingStatus(byId.n17, new Date('2026-11-14T07:00:00+03:00'));
  assert.equal(morning.active, false);
  assert.match(morning.text, /не действует/);

  const friday = streetParkingStatus(byId.n17, new Date('2026-11-13T02:00:00+03:00'));
  assert.equal(friday.active, false);

  const wednesday = streetParkingStatus(byId.n15, new Date('2026-11-11T10:00:00+03:00'));
  assert.equal(wednesday.active, true);
  assert.equal(byId.n15.ban.weekday, 'Wed');
  assert.equal(byId.n15.ban.from, 9 * 60);
});
