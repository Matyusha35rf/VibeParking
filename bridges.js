// График разводки мостов Санкт-Петербурга на 2026 год (СПб ГБУ «Мостотрест»).
// Регулярные мосты Невы, Большой и Малой Невы: ночи с 10 апреля по 30 ноября.
// Большая Невка: по заявке, с 20 апреля по 15 ноября.
// В ночь на 2 мая, 10 мая, 13 июня и 5 ноября регулярной разводки нет.
window.BRIDGES = [
  {
    id: "dvortsovy",
    name: "Дворцовый мост",
    shortName: "Дворцовый",
    lat: 59.941177,
    lon: 30.308100,
    line: [[59.942034, 30.306534], [59.940357, 30.309613]],
    type: "regular",
    schedule: [["01:10", "02:50"], ["03:10", "04:55"]],
    scheduleText: "01:10–02:50 и 03:10–04:55",
    connects: "Стрелка Васильевского острова и Дворцовая площадь",
    draws: true
  },
  {
    id: "blagoveshchensky",
    name: "Благовещенский мост",
    shortName: "Благовещенский",
    lat: 59.934812,
    lon: 30.289736,
    line: [[59.933467, 30.291025], [59.936157, 30.288447]],
    type: "regular",
    schedule: [["01:25", "02:45"], ["03:10", "05:00"]],
    scheduleText: "01:25–02:45 и 03:10–05:00",
    connects: "Васильевский остров и площадь Труда",
    draws: true
  },
  {
    id: "troitsky",
    name: "Троицкий мост",
    shortName: "Троицкий",
    lat: 59.948892,
    lon: 30.327350,
    line: [[59.950997, 30.325335], [59.946508, 30.329600]],
    type: "regular",
    schedule: [["01:20", "04:50"]],
    scheduleText: "01:20–04:50",
    connects: "Петроградская сторона и Дворцовая набережная",
    draws: true
  },
  {
    id: "liteyny",
    name: "Литейный мост",
    shortName: "Литейный",
    lat: 59.951940,
    lon: 30.349516,
    line: [[59.950105, 30.349000], [59.953619, 30.350326]],
    type: "regular",
    schedule: [["01:40", "04:45"]],
    scheduleText: "01:40–04:45",
    connects: "Литейный проспект и Выборгская сторона",
    draws: true
  },
  {
    id: "bolsheokhtinsky",
    name: "Большеохтинский мост",
    shortName: "Большеохтинский",
    lat: 59.942700,
    lon: 30.401214,
    line: [[59.942612, 30.398185], [59.942787, 30.404244]],
    type: "regular",
    schedule: [["02:00", "05:00"]],
    scheduleText: "02:00–05:00",
    connects: "Смольная набережная и Малая Охта",
    draws: true
  },
  {
    id: "alexander_nevsky",
    name: "Мост Александра Невского",
    shortName: "Александра Невского",
    lat: 59.925715,
    lon: 30.395628,
    line: [[59.924511, 30.390370], [59.926939, 30.401044]],
    type: "regular",
    schedule: [["02:20", "05:10"]],
    scheduleText: "02:20–05:10",
    connects: "Площадь Александра Невского и Заневский проспект",
    draws: true
  },
  {
    id: "volodarsky",
    name: "Володарский мост",
    shortName: "Володарский",
    lat: 59.877725,
    lon: 30.453225,
    line: [[59.876715, 30.449693], [59.879321, 30.459290]],
    type: "regular",
    schedule: [["02:00", "03:45"], ["04:15", "05:30"]],
    scheduleText: "02:00–03:45 и 04:15–05:30",
    connects: "Ивановская улица и Народная улица",
    draws: true
  },
  {
    id: "birzhevoy",
    name: "Биржевой мост",
    shortName: "Биржевой",
    lat: 59.946282,
    lon: 30.303373,
    line: [[59.945226, 30.302990], [59.947347, 30.303756]],
    type: "regular",
    schedule: [["02:00", "02:55"], ["03:35", "04:55"]],
    scheduleText: "02:00–02:55 и 03:35–04:55",
    connects: "Петроградская сторона и стрелка Васильевского острова",
    draws: true
  },
  {
    id: "tuchkov",
    name: "Тучков мост",
    shortName: "Тучков",
    lat: 59.948949,
    lon: 30.285506,
    line: [[59.948241, 30.284149], [59.949675, 30.286901]],
    type: "regular",
    schedule: [["02:00", "02:55"], ["03:35", "04:55"]],
    scheduleText: "02:00–02:55 и 03:35–04:55",
    connects: "Петроградская сторона и Васильевский остров",
    draws: true
  },
  {
    id: "sampsonievsky",
    name: "Сампсониевский мост",
    shortName: "Сампсониевский",
    lat: 59.957962,
    lon: 30.337314,
    line: [[59.958123, 30.335431], [59.957843, 30.339315]],
    type: "on_demand",
    schedule: [["01:30", "04:30"]],
    scheduleText: "01:30–04:30 по заявке за 2 суток",
    connects: "Петроградская сторона и Выборгская сторона",
    draws: true
  },
  {
    id: "grenadersky",
    name: "Гренадерский мост",
    shortName: "Гренадерский",
    lat: 59.967957,
    lon: 30.334605,
    line: [[59.967800, 30.332912], [59.968112, 30.336294]],
    type: "on_demand",
    schedule: [["01:30", "04:30"]],
    scheduleText: "01:30–04:30 по заявке за 2 суток",
    connects: "Аптекарский остров и Выборгская сторона",
    draws: true
  },
  {
    id: "kantemirovsky",
    name: "Кантемировский мост",
    shortName: "Кантемировский",
    lat: 59.978499,
    lon: 30.321814,
    line: [[59.977589, 30.319693], [59.979412, 30.323957]],
    type: "on_demand",
    schedule: [["01:30", "04:30"]],
    scheduleText: "01:30–04:30 по заявке за 2 суток",
    connects: "Аптекарский остров и Выборгская сторона",
    draws: true
  },
  {
    id: "bolshoy_obukhovsky",
    name: "Большой Обуховский мост",
    shortName: "Вантовый",
    lat: 59.853725,
    lon: 30.492316,
    line: [[59.85105, 30.4866], [59.85645, 30.4980]],
    type: "fixed",
    schedule: [],
    scheduleText: "Круглосуточно",
    connects: "Проспект Обуховской Обороны и Октябрьская набережная. Единственный неразводной мост через Неву",
    draws: false
  },
  {
    id: "betancourt",
    name: "Мост Бетанкура",
    shortName: "Бетанкура",
    lat: 59.956689,
    lon: 30.265020,
    line: [[59.953282, 30.266229], [59.959923, 30.270601]],
    type: "fixed",
    schedule: [],
    scheduleText: "Круглосуточно",
    connects: "Петровский остров и Васильевский остров",
    draws: false
  },
  {
    id: "ushakovsky",
    name: "Ушаковский мост",
    shortName: "Ушаковский",
    lat: 59.982585,
    lon: 30.300209,
    line: [[59.981655, 30.299656], [59.983516, 30.300753]],
    type: "fixed",
    schedule: [],
    scheduleText: "Круглосуточно",
    connects: "Каменный остров и Приморский район",
    draws: false
  },
  {
    id: "kamennoostrovsky",
    name: "Каменноостровский мост",
    shortName: "Каменноостровский",
    lat: 59.977504,
    lon: 30.301392,
    line: [[59.978063, 30.300276], [59.976957, 30.302491]],
    type: "fixed",
    schedule: [],
    scheduleText: "Круглосуточно",
    connects: "Аптекарский остров и Каменный остров",
    draws: false
  },
  {
    id: "lazarevsky",
    name: "Лазаревский мост",
    shortName: "Лазаревский",
    lat: 59.965025,
    lon: 30.273722,
    line: [[59.965537, 30.273372], [59.964514, 30.274071]],
    type: "fixed",
    schedule: [],
    scheduleText: "Круглосуточно",
    connects: "Петроградский остров и Крестовский остров",
    draws: false
  },
  {
    id: "bolshoy_krestovsky",
    name: "Большой Крестовский мост",
    shortName: "Б. Крестовский",
    lat: 59.967040,
    lon: 30.280382,
    line: [[59.967437, 30.279266], [59.966675, 30.281428]],
    type: "fixed",
    schedule: [],
    scheduleText: "Круглосуточно",
    connects: "Петроградский остров и Крестовский остров",
    draws: false
  }
];

const HOLIDAY_MORNINGS = [[5, 2], [5, 10], [6, 13], [11, 5]];

function formatMins(total) {
  const h = Math.floor(total / 60);
  const min = total % 60;
  if (h > 0 && min > 0) return h + " ч " + min + " мин";
  if (h > 0) return h + " ч";
  return min + " мин";
}

function clockMinutes(hhmm) {
  const parts = hhmm.split(":");
  return Number(parts[0]) * 60 + Number(parts[1]);
}

function moscowParts(date) {
  const fmt = new Intl.DateTimeFormat("en-GB", {
    timeZone: "Europe/Moscow",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    hourCycle: "h23"
  });
  const bag = {};
  fmt.formatToParts(date).forEach(part => { bag[part.type] = part.value; });
  return {
    year: Number(bag.year),
    month: Number(bag.month),
    day: Number(bag.day),
    minutes: Number(bag.hour) * 60 + Number(bag.minute)
  };
}

function shiftDays(year, month, day, delta) {
  const next = new Date(Date.UTC(year, month - 1, day + delta));
  return { year: next.getUTCFullYear(), month: next.getUTCMonth() + 1, day: next.getUTCDate() };
}

function seasonOf(bridge) {
  if (bridge.type === "on_demand") return { start: 420, end: 1115, opens: "20 апреля" };
  return { start: 410, end: 1130, opens: "10 апреля" };
}

function monthDayKey(month, day) {
  return month * 100 + day;
}

function inSeason(bridge, month, day) {
  const key = monthDayKey(month, day);
  const season = seasonOf(bridge);
  return key >= season.start && key <= season.end;
}

function isHolidayMorning(month, day) {
  return HOLIDAY_MORNINGS.some(pair => pair[0] === month && pair[1] === day);
}

function drawsOnMorning(bridge, month, day) {
  return bridge.type === "regular" && inSeason(bridge, month, day) && !isHolidayMorning(month, day);
}

function status(text, subtext, badgeClass, isDrawn) {
  return { isOpenForCars: !isDrawn, isDrawn: !!isDrawn, text, subtext, badgeClass };
}

window.getBridgeStatus = function getBridgeStatus(bridge, now) {
  const clock = moscowParts(now || new Date());
  const today = { year: clock.year, month: clock.month, day: clock.day };

  if (bridge.type === "fixed" || !bridge.schedule || bridge.schedule.length === 0) {
    return status("Открыт круглосуточно", "Мост не разводится", "fixed", false);
  }

  const upcoming = clock.minutes >= 12 * 60 ? shiftDays(today.year, today.month, today.day, 1) : today;
  if (bridge.type === "on_demand") {
    const nightIsOpen = inSeason(bridge, upcoming.month, upcoming.day);
    if (!nightIsOpen) {
      return status("Сведён", "Навигация по Большой Невке закрыта до " + seasonOf(bridge).opens, "open", false);
    }
    return status(
      "Обычно открыт",
      "Разводят только по заявке судна за двое суток, окно " + bridge.scheduleText,
      "on-demand",
      false
    );
  }

  if (drawsOnMorning(bridge, today.month, today.day)) {
    for (let i = 0; i < bridge.schedule.length; i++) {
      const startMins = clockMinutes(bridge.schedule[i][0]);
      const endMins = clockMinutes(bridge.schedule[i][1]);
      if (clock.minutes >= startMins && clock.minutes < endMins) {
        return status(
          "Разведён",
          "Проезд закрыт до " + bridge.schedule[i][1] + ", ещё " + formatMins(endMins - clock.minutes),
          "drawn",
          true
        );
      }
    }
  }

  let next = null;
  if (drawsOnMorning(bridge, today.month, today.day)) {
    bridge.schedule.forEach(slot => {
      const startMins = clockMinutes(slot[0]);
      const diff = startMins - clock.minutes;
      if (diff > 0 && (!next || diff < next.diff)) next = { diff, start: slot[0], when: today };
    });
  }

  if (!next) {
    let cursor = shiftDays(today.year, today.month, today.day, 1);
    for (let i = 1; i <= 220; i++) {
      if (drawsOnMorning(bridge, cursor.month, cursor.day)) {
        const start = bridge.schedule[0][0];
        next = {
          diff: i * 24 * 60 + clockMinutes(start) - clock.minutes,
          start,
          when: cursor
        };
        break;
      }
      cursor = shiftDays(cursor.year, cursor.month, cursor.day, 1);
    }
  }

  if (!next) return status("Сведён", "Навигация закрыта", "open", false);

  const season = seasonOf(bridge);
  if (next.diff > 36 * 60) {
    return status("Сведён", "Навигация закрыта до " + season.opens, "open", false);
  }

  const sameNight = next.when.year === upcoming.year && next.when.month === upcoming.month && next.when.day === upcoming.day;
  const when = next.when.day + "." + String(next.when.month).padStart(2, "0");
  let subtext = sameNight
    ? "Разводка в " + next.start + ", через " + formatMins(next.diff)
    : "Разводка " + when + " в " + next.start + ", через " + formatMins(next.diff);
  if (inSeason(bridge, upcoming.month, upcoming.day) && isHolidayMorning(upcoming.month, upcoming.day)) {
    subtext = "В праздничную ночь разводки нет. " + subtext;
  }
  return status(next.diff <= 60 ? "Скоро разводка" : "Сведён", subtext, next.diff <= 60 ? "soon" : "open", false);
};
