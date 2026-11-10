#!/usr/bin/env python3
"""Build street-parking.js from the Avtopark 7 sign list and OSM ways.

The list is the July 2024 PDF linked from spectrans7.ru for the right bank
of Nevsky district. Geometry comes from /tmp/nevsky/ways.json (Overpass).
House samples used only to tell even and odd curbs apart come from Nominatim.
"""

import json
import math
import re
import time
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WAYS = json.loads(Path("/tmp/nevsky/ways.json").read_text())["elements"]
HOUSE_CACHE = Path("/tmp/nevsky/houses.json")
PDF = Path("/home/ubuntu/.cursor/projects/agent-repos-VibeParking/agent-tools/9245bc49-5d98-433e-ae4d-f81411118626.txt")
OUT = ROOT / "street-parking.js"
SOURCE_URL = "http://spectrans7.ru/wp-content/uploads/2024/07/Знаки-3.27-Невский-правый-берег-район.pdf"

WEEK = {
    "понедельник": "Mon",
    "вторник": "Tue",
    "среда": "Wed",
    "четверг": "Thu",
    "пятница": "Fri",
    "суббота": "Sat",
    "воскресенье": "Sun",
}
WEEK_RU = {
    "Mon": "понедельникам",
    "Tue": "вторникам",
    "Wed": "средам",
    "Thu": "четвергам",
    "Fri": "пятницам",
    "Sat": "субботам",
    "Sun": "воскресеньям",
}
STEM = {
    "антонова-овсеенко": "улица Антонова-Овсеенко",
    "бадаева": "улица Бадаева",
    "белышева": "улица Белышева",
    "большевиков": "проспект Большевиков",
    "воркутинская": "Воркутинская улица",
    "ворошилова": "улица Ворошилова",
    "дальневосточного": "Дальневосточный проспект",
    "дальневосточный": "Дальневосточный проспект",
    "джона рида": "улица Джона Рида",
    "дыбенко": "улица Дыбенко",
    "евдокима огнева": "улица Евдокима Огнева",
    "искровского": "Искровский проспект",
    "искровский": "Искровский проспект",
    "клочков": "Клочков переулок",
    "коллонтай": "улица Коллонтай",
    "кржижановского": "улица Кржижановского",
    "крыленко": "улица Крыленко",
    "кудровский": "Кудровский проезд",
    "латышских стрелков": "улица Латышских Стрелков",
    "лопатина": "улица Лопатина",
    "народной": "Народная улица",
    "народная": "Народная улица",
    "нерчинской": "Нерчинская улица",
    "нерчинская": "Нерчинская улица",
    "новоселов": "улица Новосёлов",
    "октябрьской": "Октябрьская набережная",
    "октябрьская": "Октябрьская набережная",
    "паткановская": "Паткановская улица",
    "подвойского": "улица Подвойского",
    "пятилеток": "проспект Пятилеток",
    "российского": "Российский проспект",
    "российский": "Российский проспект",
    "солидарности": "проспект Солидарности",
    "тельмана": "улица Тельмана",
    "товарищеского": "Товарищеский проспект",
    "товарищеский": "Товарищеский проспект",
    "чудновского": "улица Чудновского",
    "шотмана": "улица Шотмана",
    "зольной": "Зольная улица",
    "зольная": "Зольная улица",
    "якутской": "Якутская улица",
    "якутская": "Якутская улица",
}


def meters(a, b):
    return math.hypot((a[0] - b[0]) * 111320, (a[1] - b[1]) * 111320 * math.cos(math.radians(a[0])))


def key_of(p):
    return (round(p[0], 5), round(p[1], 5))


def stem_name(text):
    t = text.lower().replace("ё", "е")
    t = t.replace("пр-зд", " ").replace("наб.", " ").replace("ул.", " ").replace("пр.", " ").replace("пер.", " ")
    t = re.sub(r"[^а-я0-9\- ]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    for stem, osm in sorted(STEM.items(), key=lambda kv: -len(kv[0])):
        if stem in t:
            return osm
    return None


def road_name(raw):
    raw_l = raw.lower().replace("ё", "е")
    if "якут" in raw_l:
        return "Якутская улица"
    if "боковой" in raw_l and "товарищ" in raw_l:
        return "Товарищеский проспект"
    name = stem_name(raw)
    if not name:
        raise SystemExit(f"unknown road {raw}")
    return name


def parse_rules():
    rules = []
    for line in PDF.read_text().splitlines():
        if "Автопарк" not in line or line.count("|") < 6:
            continue
        cols = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cols) < 7 or not cols[1].isdigit():
            continue
        num, road, _district, section, side, day, clock = cols[1:8]
        a, b = clock.split("-")
        fh, fm = map(int, a.split(":"))
        th, tm = map(int, b.split(":"))
        sec = section.lower().replace("ё", "е")
        kind = "main"
        if "съезд" in sec or "заезд" in sec and "володар" in sec:
            kind = "ramp"
        elif "автобус" in sec:
            kind = "bus"
        elif "газона и сторона домов" in sec or "сторона газона и сторона домов" in sec:
            kind = "side"
        elif "сторона газона" in sec:
            kind = "side_lawn"
        elif "сторона домов" in sec:
            kind = "side_houses"
        elif "боков" in sec:
            kind = "side"
        if "товарищеский пр. боковой" in road.lower() or "боковой" in road.lower():
            kind = "side"
        rules.append({
            "n": int(num),
            "name": road_name(road),
            "pdf_road": road,
            "section": section,
            "side": "odd" if side.startswith("неч") else "even",
            "kind": kind,
            "weekday": WEEK[day],
            "from": fh * 60 + fm,
            "to": th * 60 + tm,
        })
    # The PDF repeats numbers 59 and 60. Keep file order and unique ids.
    seen = defaultdict(int)
    for rule in rules:
        seen[rule["n"]] += 1
        rule["id"] = f"n{rule['n']:02d}" if seen[rule["n"]] == 1 else f"n{rule['n']:02d}b"
    return rules


def load_ways():
    by = defaultdict(list)
    for el in WAYS:
        tags = el.get("tags") or {}
        name = tags.get("name")
        geom = [(g["lat"], g["lon"]) for g in el.get("geometry") or []]
        if not name or len(geom) < 2:
            continue
        hw = tags.get("highway") or ""
        if hw in {"footway", "cycleway", "path", "steps", "pedestrian", "corridor"}:
            continue
        by[name].append({"id": el["id"], "highway": hw, "geom": geom})
    return by


BY = load_ways()


def way_length(way):
    return sum(meters(way["geom"][i], way["geom"][i + 1]) for i in range(len(way["geom"]) - 1))


def is_side_way(way):
    return way["highway"] in {"residential", "living_street", "service", "unclassified"} and way_length(way) > 40


def is_main_way(way):
    return way["highway"] in {"primary", "secondary", "tertiary", "unclassified", "residential", "living_street"} and not (
        way["highway"] in {"residential", "living_street", "service"} and way_length(way) > 40 and way["highway"] != "unclassified"
    )


def select_ways(name, kind):
    ways = BY.get(name, [])
    side = [w for w in ways if w["highway"] in {"residential", "living_street", "service"} and way_length(w) > 40]
    main = [w for w in ways if w["highway"] in {"primary", "secondary", "tertiary", "unclassified"}]
    if not main:
        main = [w for w in ways if w["highway"] not in {"service", "track"}]
    if kind == "main":
        return main or ways, False
    if kind in {"side", "side_lawn", "side_houses"}:
        if side:
            return side, False
        return main or ways, True
    if kind == "ramp":
        bridge = (59.877725, 30.453225)
        near = [w for w in ways if min(meters(p, bridge) for p in w["geom"]) < 400]
        return near or main, True
    if kind == "bus":
        return main or ways, True
    return main or ways, True


def closest_point_on_ways(ways, point):
    best = None
    for way in ways:
        geom = way["geom"]
        for i in range(len(geom) - 1):
            a, b = geom[i], geom[i + 1]
            ax, ay = a[1], a[0]
            bx, by = b[1], b[0]
            px, py = point[1], point[0]
            abx, aby = bx - ax, by - ay
            denom = abx * abx + aby * aby
            t = 0 if denom == 0 else max(0, min(1, ((px - ax) * abx + (py - ay) * aby) / denom))
            q = (ay + (by - ay) * t, ax + (bx - ax) * t)
            d = meters(q, point)
            if best is None or d < best[0]:
                best = (d, q, way)
    return best


def intersection_point(street_ways, cross_name):
    cross = BY.get(cross_name, [])
    best = None
    for sw in street_ways:
        for cw in cross:
            for p in sw["geom"][::2]:
                hit = closest_point_on_ways([cw], p)
                if hit and (best is None or hit[0] < best[0]):
                    best = (hit[0], p)
    if best and best[0] < 45:
        return best[1]
    return None


def graph_from(ways, link_m=8):
    nodes = {}
    edges = defaultdict(list)

    def add_edge(a, b, poly):
        if a == b:
            return
        edges[a].append((b, meters(a, b), poly))
        edges[b].append((a, meters(a, b), list(reversed(poly))))

    ends = []
    for way in ways:
        geom = way["geom"]
        keys = [key_of(p) for p in geom]
        nodes[keys[0]] = geom[0]
        for i in range(len(geom) - 1):
            nodes[keys[i + 1]] = geom[i + 1]
            add_edge(keys[i], keys[i + 1], [geom[i], geom[i + 1]])
        ends.append(keys[0])
        ends.append(keys[-1])
    for i, a in enumerate(ends):
        for b in ends[i + 1:]:
            if a != b and meters(nodes[a], nodes[b]) <= link_m:
                add_edge(a, b, [nodes[a], nodes[b]])
    return nodes, edges


def nearest_node(nodes, point, limit=70):
    best = None
    for k, p in nodes.items():
        d = meters(p, point)
        if d <= limit and (best is None or d < best[0]):
            best = (d, k)
    return best


def route_keys(nodes, edges, sk, ek):
    import heapq
    if sk == ek:
        return [nodes[sk]]
    dist = {sk: 0}
    prev = {}
    heap = [(0, sk)]
    while heap:
        d, u = heapq.heappop(heap)
        if d != dist.get(u):
            continue
        if u == ek:
            break
        for v, w, poly in edges[u]:
            nd = d + w
            if nd < dist.get(v, 1e18):
                dist[v] = nd
                prev[v] = (u, poly)
                heapq.heappush(heap, (nd, v))
    if ek not in dist:
        return None
    poly = []
    cur = ek
    while cur != sk:
        u, part = prev[cur]
        poly = part[:-1] + poly
        cur = u
    poly.append(nodes[ek])
    return poly


def components(nodes, edges):
    seen = set()
    groups = []
    for start in nodes:
        if start in seen:
            continue
        stack = [start]
        group = set()
        while stack:
            u = stack.pop()
            if u in group:
                continue
            group.add(u)
            for v, _, _ in edges[u]:
                if v not in group:
                    stack.append(v)
        seen |= group
        groups.append(group)
    return groups


def route(nodes, edges, start, end):
    groups = components(nodes, edges)
    direct = meters(start, end)
    best = None
    for group in groups:
        local = {k: nodes[k] for k in group}
        s = nearest_node(local, start, 80)
        e = nearest_node(local, end, 80)
        if not s or not e:
            continue
        poly = route_keys(nodes, edges, s[1], e[1])
        if not poly:
            continue
        length = polyline_length(poly)
        # A path that reaches the other anchor the long way around is the wrong carriageway.
        if direct > 40 and length > direct * 1.75:
            continue
        if best is None or length < best[0]:
            best = (length, poly)
    return None if best is None else best[1]


def polyline_length(line):
    return sum(meters(line[i], line[i + 1]) for i in range(len(line) - 1))


def simplify(line, tol=12):
    if len(line) < 3:
        return line

    def dp(pts):
        if len(pts) < 3:
            return pts
        a, b = pts[0], pts[-1]
        ax, ay = 0, 0
        bx = (b[1] - a[1]) * 111320 * math.cos(math.radians(a[0]))
        by = (b[0] - a[0]) * 111320
        best_i, best_d = 0, -1
        for i in range(1, len(pts) - 1):
            px = (pts[i][1] - a[1]) * 111320 * math.cos(math.radians(a[0]))
            py = (pts[i][0] - a[0]) * 111320
            abx, aby = bx - ax, by - ay
            denom = abx * abx + aby * aby or 1
            t = max(0, min(1, ((px - ax) * abx + (py - ay) * aby) / denom))
            d = math.hypot(px - ax - abx * t, py - ay - aby * t)
            if d > best_d:
                best_i, best_d = i, d
        if best_d <= tol:
            return [pts[0], pts[-1]]
        left, right = dp(pts[: best_i + 1]), dp(pts[best_i:])
        return left[:-1] + right

    return dp(line)


def shift(line, signed_m):
    if len(line) < 2 or abs(signed_m) < 0.5:
        return line
    dirs = []
    for i in range(len(line) - 1):
        north = (line[i + 1][0] - line[i][0]) * 111320
        east = (line[i + 1][1] - line[i][1]) * 111320 * math.cos(math.radians(line[i][0]))
        length = math.hypot(east, north) or 1
        dirs.append((east / length, north / length))
    out = []
    for i, point in enumerate(line):
        a = dirs[max(0, i - 1)]
        b = dirs[min(len(dirs) - 1, i)]
        east, north = a[0] + b[0], a[1] + b[1]
        length = math.hypot(east, north) or 1
        east, north = east / length, north / length
        # left of travel is -east, +north when signed_m > 0
        out.append((
            round(point[0] + (-east * signed_m) / 111320, 5),
            round(point[1] + (north * signed_m) / (111320 * math.cos(math.radians(point[0]))), 5),
        ))
    return out


def cross_sign(a, b, p):
    east = (b[1] - a[1]) * math.cos(math.radians(a[0]))
    north = b[0] - a[0]
    pe = (p[1] - a[1]) * math.cos(math.radians(a[0]))
    pn = p[0] - a[0]
    return east * pn - north * pe


def side_of_line(line, point):
    best = None
    for i in range(len(line) - 1):
        d = meters(line[i], point)
        if best is None or d < best[0]:
            best = (d, cross_sign(line[i], line[i + 1], point))
    if not best:
        return 0
    return 1 if best[1] >= 0 else -1


def nominatim(street, number):
    cache = {}
    if HOUSE_CACHE.exists():
        cache = json.loads(HOUSE_CACHE.read_text())
    token = f"{street}|{number}"
    if token in cache:
        return cache[token]
    url = "https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode({
        "format": "jsonv2",
        "limit": 1,
        "countrycodes": "ru",
        "addressdetails": 1,
        "street": f"{number} {street}",
        "city": "Санкт-Петербург",
    })
    req = urllib.request.Request(url, headers={"User-Agent": "VibeParking/nevsky-signs (geometry build)"})
    try:
        with urllib.request.urlopen(req, timeout=30) as res:
            data = json.load(res)
    except Exception:
        data = []
    found = None
    if data:
        hn = str((data[0].get("address") or {}).get("house_number") or "")
        hn_norm = hn.lower().replace(" ", "")
        if re.match(rf"^{number}(\D|$)", hn_norm):
            point = (float(data[0]["lat"]), float(data[0]["lon"]))
            ways = BY.get(street, [])
            hit = closest_point_on_ways(ways, point) if ways else None
            if hit and hit[0] < 400:
                found = {"lat": point[0], "lon": point[1], "hn": hn}
    cache[token] = found
    HOUSE_CACHE.write_text(json.dumps(cache, ensure_ascii=False))
    time.sleep(1.05)
    return found


def houses_for(street):
    found = []
    for number in (1, 2, 3, 4, 5, 6, 8, 10, 11, 12, 14, 15, 20, 30):
        hit = nominatim(street, number)
        if not hit:
            continue
        parity = "odd" if int(number) % 2 else "even"
        found.append((parity, (hit["lat"], hit["lon"])))
        odds = sum(1 for p, _ in found if p == "odd")
        evens = sum(1 for p, _ in found if p == "even")
        if odds >= 2 and evens >= 2:
            break
    return found


def anchor_for(rule, ways, which):
    section = rule["section"].lower().replace("ё", "е")
    if " до " not in section:
        hits = []
        for stem in STEM:
            i = section.find(stem)
            if i >= 0:
                hits.append((i, stem))
        hits.sort()
        picked = []
        for i, stem in hits:
            if picked and i < picked[-1][0] + len(picked[-1][1]):
                continue
            picked.append((i, stem))
        if len(picked) >= 2:
            cut = picked[1][0]
            section = section[:cut] + "до " + section[cut:]
    if " до " not in section:
        idx = section.rfind(" от ")
        if idx > 0:
            section = section[:idx] + " до " + section[idx + 4:]
    # Pull the from/to phrase. House numbers win over street names in the same clause.
    if which == "from":
        m = re.search(r"от\s+(.+?)\s+до\s+", section)
        phrase = m.group(1) if m else ""
    else:
        m = re.search(r"\sдо\s+(.+)$", section)
        phrase = m.group(1) if m else ""
    hm = re.search(r"д\.?\s*(\d+)", phrase)
    if hm and "клочкова моста" not in phrase:
        hit = nominatim(rule["name"], hm.group(1))
        if hit:
            return (hit["lat"], hit["lon"]), False
    if "клочкова моста" in phrase or (rule["kind"] == "bus" and which == "to"):
        return None, True
    if "володар" in phrase:
        return (59.877725, 30.453225), True
    osm = stem_name(phrase)
    if osm and osm != rule["name"]:
        point = intersection_point(ways, osm)
        if point:
            return point, False
    return None, False


def clip_between(ways, start, end):
    nodes, edges = graph_from(ways)
    path = route(nodes, edges, start, end)
    if path and polyline_length(path) > 25:
        return path
    nodes, edges = graph_from(ways, link_m=22)
    path = route(nodes, edges, start, end)
    if path and polyline_length(path) > 25:
        return path
    return None


def bbox_clip(ways, start, end):
    south, north = sorted((start[0], end[0]))
    west, east = sorted((start[1], end[1]))
    pad_lat, pad_lon = 0.0015, 0.002
    parts = []
    for way in ways:
        keep = [p for p in way["geom"] if south - pad_lat <= p[0] <= north + pad_lat and west - pad_lon <= p[1] <= east + pad_lon]
        if len(keep) >= 2 and polyline_length(keep) > 40:
            parts.append(keep)
    if not parts:
        return None
    parts.sort(key=polyline_length, reverse=True)
    return parts[0]


def filter_parity(ways, houses, side):
    if not houses:
        return ways, True
    wanted = [p for parity, p in houses if parity == side]
    other = [p for parity, p in houses if parity != side]
    if len(wanted) < 1:
        return ways, True
    scored = []
    for way in ways:
        dw = min(min(meters(p, q) for q in way["geom"]) for p in wanted)
        do = min((min(meters(p, q) for q in way["geom"]) for p in other), default=1e9)
        scored.append((dw, do, way))
    close = [way for dw, do, way in scored if dw < 55 and dw + 8 < do]
    if len(close) >= 1 and sum(way_length(w) for w in close) > 80:
        return close, False
    return ways, True


def offset_toward(line, houses, side):
    wanted = [p for parity, p in houses if parity == side]
    if len(line) < 2 or not wanted:
        return line, True
    signs = [side_of_line(line, p) for p in wanted]
    # Move toward the majority side. side_of_line +1 is left of the drawn direction.
    left = sum(1 for s in signs if s > 0)
    right = len(signs) - left
    signed = 8 if left >= right else -8
    return shift(line, signed), False


def far_end(ways, other):
    points = [p for w in ways for p in (w["geom"][0], w["geom"][-1])]
    if not points or not other:
        return None
    return max(points, key=lambda p: meters(p, other))


def build():
    rules = parse_rules()
    streets = sorted({r["name"] for r in rules})
    print(f"rules {len(rules)} streets {len(streets)}")
    house_book = {name: houses_for(name) for name in streets}
    for name, houses in house_book.items():
        print(f"  houses {name}: {len(houses)}")

    features = []
    for rule in rules:
        houses = house_book.get(rule["name"], [])
        pref_ways, pref_approx = select_ways(rule["name"], rule["kind"])
        everything = [w for w in BY.get(rule["name"], []) if w["highway"] != "track"]
        sets = [(pref_ways, pref_approx)]
        if everything != pref_ways:
            sets.append((everything, True))
        line = None
        approx = True
        for ways, kind_approx in sets:
            if not ways:
                continue
            start, start_special = anchor_for(rule, ways, "from")
            end, end_special = anchor_for(rule, ways, "to")
            approx = kind_approx
            if start_special and end and not start:
                start = far_end(ways, end)
                approx = True
            if end_special and start and not end:
                end = far_end(ways, start)
                approx = True
            if not start or not end:
                continue
            line = clip_between(ways, start, end)
            if not line:
                line = bbox_clip(ways, start, end)
                approx = True
            elif polyline_length(line) > max(80, meters(start, end) * 2.4):
                alt = bbox_clip(ways, start, end)
                if alt and polyline_length(alt) > polyline_length(line) * 0.5:
                    line = alt
                approx = True
            if rule["kind"] == "bus" and line:
                trimmed = [line[0]]
                walked = 0
                for i in range(1, len(line)):
                    step = meters(line[i - 1], line[i])
                    if walked + step >= 400:
                        break
                    trimmed.append(line[i])
                    walked += step
                if len(trimmed) >= 2:
                    line = trimmed
                approx = True
            if line and kind_approx and rule["kind"] not in {"main", "bus", "ramp"} and polyline_length(line) > 1200:
                line = None
                continue
            if line and polyline_length(line) >= 30:
                break
            line = None
        if not line or polyline_length(line) < 30:
            print(f"MISS {rule['id']} {rule['name']} | {rule['section']}")
            continue
        line, off_approx = offset_toward(line, houses, rule["side"])
        line = [(p[0], p[1]) for p in simplify(line, 14)]
        if off_approx:
            approx = True
        side_text = "нечётная сторона" if rule["side"] == "odd" else "чётная сторона"
        hh = lambda m: f"{m // 60:02d}:{m % 60:02d}"
        when = f"по {WEEK_RU[rule['weekday']]} с {hh(rule['from'])} до {hh(rule['to'])}"
        features.append({
            "id": rule["id"],
            "name": rule["name"],
            "side": side_text,
            "section": rule["section"],
            "when": when,
            "approx": approx,
            "ban": {"weekday": rule["weekday"], "from": rule["from"], "to": rule["to"]},
            "line": line,
            "meters": round(polyline_length(line)),
        })
        print(f"OK {rule['id']} {rule['meters'] if False else features[-1]['meters']:5}m approx={approx} {rule['name']} | {rule['section']}")

    payload = {
        "area": "Невский район, правый берег",
        "publisher": "АО «Автопарк №7 Спецтранс»",
        "url": SOURCE_URL,
        "published": "2024-07",
        "covers": "Знаки 3.27 «Остановка запрещена» с табличкой времени. Левый берег Невского района в этот перечень не входит.",
    }
    lines = [
        "// Знаки 3.27 на правом берегу Невского района.",
        "// Источник: АО «Автопарк №7 Спецтранс», перечень июля 2024.",
        f"// {SOURCE_URL}",
        "// Линия — бордюр указанной стороны на участке из перечня, по геометрии OpenStreetMap.",
        "// Вне указанного окна этот знак не действует. Другие знаки перечень не отменяет.",
        "window.STREET_PARKING_SOURCE = " + json.dumps(payload, ensure_ascii=False, indent=2) + ";",
        "",
        "window.STREET_PARKING = " + json.dumps([
            {k: f[k] for k in ("id", "name", "side", "section", "when", "approx", "ban", "line")}
            for f in features
        ], ensure_ascii=False, separators=(",", ":")) + ";",
        "",
        """window.streetParkingStatus = function (item, now) {
  const fmt = new Intl.DateTimeFormat("en-US", {
    timeZone: "Europe/Moscow",
    weekday: "short",
    hour: "2-digit",
    minute: "2-digit",
    hourCycle: "h23"
  });
  const bag = {};
  fmt.formatToParts(now || new Date()).forEach(part => { bag[part.type] = part.value; });
  const minutes = Number(bag.hour) * 60 + Number(bag.minute);
  const ban = item.ban;
  const active = !!(ban && bag.weekday === ban.weekday && minutes >= ban.from && minutes < ban.to);
  const endH = String(Math.floor(ban.to / 60)).padStart(2, "0");
  const endM = String(ban.to % 60).padStart(2, "0");
  const place = item.side + (item.section ? ", " + item.section : "");
  if (active) {
    return {
      active: true,
      text: "Сейчас остановка запрещена",
      detail: "Знак 3.27, " + place + ". " + item.when + ", до " + endH + ":" + endM + "."
    };
  }
  return {
    active: false,
    text: "Сейчас этот запрет не действует",
    detail: "Знак 3.27, " + place + ". " + item.when + "."
  };
};
""",
    ]
    OUT.write_text("\n".join(lines))
    print(f"wrote {len(features)} / {len(rules)} -> {OUT}")


if __name__ == "__main__":
    build()
