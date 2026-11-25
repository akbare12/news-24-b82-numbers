#!/usr/bin/env python3
"""news-24 b82-numbers: front page, Tuesday 24 November 2026. PIL only, deterministic."""
import os
from PIL import Image, ImageDraw, ImageFont
W, H = 1024, 1024
PAPER = (247, 242, 231); INK = (17, 17, 17); RED = (179, 35, 27); NAVY = (27, 58, 92); GREY = (90, 88, 82)
LIGHT = (232, 226, 212); GOLD = (198, 142, 30); GREEN = (31, 110, 61); BLUE = (27, 90, 160); ORANGE = (196, 96, 16)
CHIP = {"CONFIRMED": (31, 110, 61), "OFFICIAL": (27, 90, 160), "REPORTED": (90, 88, 82), "CLAIM": (196, 96, 16)}
def F(p, s):
    try: return ImageFont.truetype(p, s)
    except Exception: return ImageFont.load_default()
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"; SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"; SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def sb(s): return F(SANSB, s)
def sr(s): return F(SERIF, s)
def sn(s): return F(SANS, s)
def wrap(d, t, f, w):
    out, cur = [], ""
    for wd in t.split(" "):
        t2 = (cur + " " + wd).strip()
        if d.textlength(t2, font=f) <= w: cur = t2
        else: out.append(cur) if cur else None; cur = wd
    if cur: out.append(cur)
    return out
def chip(d, x, y, label):
    c = CHIP[label]; f = sb(7); tw = d.textlength(label, font=f) + 8
    d.rounded_rectangle([x, y, x + tw, y + 11], 2, fill=c); d.text((x + 4, y + 1), label, font=f, fill=(255, 255, 255)); return tw
def txt(d, x, y, t, f, fill=INK, w=None, lh=None):
    if w is None: d.text((x, y), t, font=f, fill=fill); return y
    lines = wrap(d, t, f, w); lh = lh or int(f.size * 1.25)
    for i, ln in enumerate(lines): d.text((x, y + i * lh), ln, font=f, fill=fill)
    return y + len(lines) * lh
# Continent outlines as (lon, lat) vertices, equirectangular.
NA = [(-168, 66), (-165, 60), (-158, 58), (-152, 60), (-140, 60), (-135, 58), (-130, 54), (-125, 49), (-124, 42), (-120, 34), (-114, 29), (-110, 24), (-105, 20), (-97, 16), (-94, 17), (-90, 14), (-86, 12), (-83, 9), (-80, 8), (-79, 9), (-82, 12), (-84, 16), (-87, 21), (-90, 21), (-91, 19), (-96, 19), (-97, 26), (-93, 30), (-89, 30), (-84, 30), (-81, 25), (-80, 32), (-76, 35), (-74, 40), (-70, 42), (-68, 45), (-65, 44), (-60, 47), (-55, 52), (-60, 55), (-65, 58), (-68, 58), (-72, 62), (-78, 62), (-85, 66), (-92, 66), (-95, 69), (-110, 68), (-125, 70), (-140, 70), (-155, 71), (-165, 68), (-168, 66)]
GL = [(-58, 64), (-52, 60), (-43, 60), (-40, 64), (-32, 68), (-22, 70), (-25, 74), (-35, 76), (-50, 76), (-58, 74), (-58, 64)]
SA = [(-79, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12), (-72, -18), (-70, -23), (-70, -30), (-72, -37), (-73, -44), (-74, -50), (-70, -54), (-66, -55), (-65, -45), (-62, -41), (-58, -35), (-52, -32), (-48, -28), (-41, -23), (-39, -17), (-35, -9), (-35, -6), (-40, -3), (-44, -2), (-50, 0), (-53, 4), (-58, 6), (-62, 9), (-68, 11), (-72, 12), (-76, 10), (-79, 9)]
AF = [(-6, 35), (-10, 31), (-15, 27), (-17, 21), (-17, 15), (-15, 11), (-12, 8), (-8, 5), (-4, 5), (0, 6), (6, 4), (9, 4), (9, -1), (12, -5), (13, -10), (12, -17), (14, -22), (16, -28), (19, -34), (26, -34), (32, -29), (35, -24), (36, -18), (40, -15), (40, -10), (42, -4), (46, -1), (51, 2), (51, 11), (48, 11), (44, 11), (40, 15), (38, 18), (37, 22), (34, 27), (32, 31), (30, 31), (22, 33), (19, 33), (11, 34), (10, 37), (0, 36), (-6, 35)]
EU = [(-10, 36), (-9, 38), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (-2, 50), (0, 51), (3, 53), (5, 58), (8, 57), (10, 59), (5, 60), (10, 62), (12, 65), (18, 69), (25, 71), (30, 70), (35, 68), (40, 68), (45, 68), (50, 69), (55, 68), (60, 69), (65, 70), (70, 72), (75, 72), (80, 73), (85, 74), (90, 75), (95, 76), (100, 77), (105, 77), (110, 74), (115, 73), (120, 73), (130, 72), (140, 72), (150, 70), (158, 69), (162, 66), (170, 66), (178, 65), (180, 65), (178, 62), (170, 60), (162, 60), (158, 56), (156, 51), (150, 59), (142, 59), (142, 54), (140, 50), (138, 46), (135, 43), (132, 43), (128, 38), (127, 35), (126, 33), (122, 31), (120, 28), (118, 25), (112, 22), (108, 18), (105, 10), (104, 8), (100, 7), (98, 10), (95, 16), (92, 21), (90, 22), (88, 22), (86, 20), (82, 17), (80, 13), (77, 8), (76, 10), (73, 16), (70, 20), (66, 25), (62, 25), (58, 26), (56, 27), (52, 26), (50, 29), (48, 30), (44, 29), (42, 27), (40, 24), (39, 21), (38, 20), (35, 28), (34, 31), (36, 36), (30, 36), (27, 37), (26, 38), (23, 36), (22, 37), (19, 40), (15, 44), (12, 44), (8, 44), (3, 43), (0, 40), (-2, 37), (-6, 36), (-9, 37), (-10, 36)]
AU = [(114, -22), (113, -26), (115, -32), (118, -35), (124, -33), (129, -32), (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37), (153, -32), (153, -27), (150, -23), (146, -19), (142, -11), (141, -13), (136, -12), (132, -11), (130, -13), (126, -14), (122, -17), (118, -20), (114, -22)]
UK = [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51), (-5, 50)]; JP = [(130, 31), (132, 33), (135, 34), (137, 35), (139, 37), (140, 39), (141, 41), (143, 42), (145, 44), (142, 44), (140, 40), (138, 37), (136, 35), (133, 34), (130, 31)]; NZ = [(167, -45), (170, -43), (173, -41), (175, -38), (178, -38), (175, -41), (172, -43), (168, -46), (167, -45)]
CONTINENTS = [NA, GL, SA, AF, EU, AU, UK, JP, NZ]
# Pins: (number, lat, lon, dx, dy) offsets in px to separate overlaps.
PINS = [(1, 24.7, 46.7, 0, 0), (2, 31.2, 121.5, 0, 0), (3, 40.7, -74.0, 0, 0), (4, 47.8, 35.2, 0, 0), (5, 14.7, -17.4, 0, 0), (6, 26.5, 56.3, 0, 0), (7, 40.7, -74.0, 16, 10), (8, 47.7, -122.1, 0, 0), (9, 39.8, 30.5, 0, 0), (10, 10.4, -75.5, 0, 0), (11, 12.8, 45.0, 0, 0), (12, 13.0, 44.9, 18, -14), (13, 39.7, 98.5, 0, 0)]
LEGEND = ["1 Riyadh", "2 Shanghai", "3 New York", "4 Zaporizhzhia", "5 Dakar", "6 Hormuz", "7 New York", "8 Redmond", "9 Eskisehir", "10 Cartagena", "11 Aden", "12 Lahj", "13 Jiuquan"]

HEROES = [("1 RIYADH \u00b7 MIDDLE EAST", "CONFIRMED", "Houthi drone hits Riyadh's tallest tower again, 11 hurt", "A Houthi drone struck the PIF tower, the tallest in Riyadh, for the second time in a week. At least 11 people were hurt: 2 Saudis, 2 Indians, 3 Nepalis and 4 Egyptians.", "(Saudi officials \u00b7 wires)", "11", (16, 22, 48)), ("2 SHANGHAI \u00b7 ASIA", "OFFICIAL", "China probes Shanghai party chief Chen Jining", "Chen Jining, 62, faces a probe for \u201cserious violations\u201d. He is the fourth Politburo member to fall under investigation this year.", "(CCDI \u00b7 official)", "62", (128, 32, 32)), ("3 NEW YORK \u00b7 US / TECH", "CONFIRMED", "Huawei guilty on 10 of 12 counts", "A US federal jury found Huawei guilty on 10 of 12 counts, including trade-secret theft and bank fraud. It was cleared of racketeering.", "(US court \u00b7 wires)", "10/12", (32, 48, 80))]
CARDS = [("4 ZAPORIZHZHIA \u00b7 EUROPE / WAR", "REPORTED", "Russian attacks kill 9 across Ukraine in a day", "Russia launched 96 drones at Ukraine; 73 were shot down or jammed. Nine people were killed and 81 wounded in a day.", "(Ukrainian officials)", (30, 30, 60)), ("5 CAS \u00b7 AFRICA / SPORT", "OFFICIAL", "CAS hands Senegal back the AFCON title", "CAS restored Senegal as African champions after Morocco forfeited 3-0, turning the final into a 1-0 Senegal win.", "(CAS)", (31, 110, 61)), ("6 HORMUZ \u00b7 MIDDLE EAST", "REPORTED", "IRGC attacks container ship in Hormuz", "An IRGC attack hit a container ship in Hormuz at 18:58 UTC, shutting down its navigation near Khasab, Oman.", "(UKMTO \u00b7 wires)", (27, 90, 160)), ("7 NEW YORK \u00b7 MARKETS", "CONFIRMED", "Dow closes above 50,000 for the first time", "The Dow closed at 50,018, its first close above 50,000. The Taiex jumped a record 8.99% to 40,122.", "(Market close)", (198, 142, 30)), ("8 REDMOND \u00b7 TECH", "REPORTED", "Microsoft declares \u2018Code Red\u2019 after historic outage", "After a 24-hour outage, the worst in Exchange Online history, Microsoft set a one-hour global recovery target.", "(Reuters)", (179, 35, 27)), ("9 ESKISEHIR \u00b7 EUROPE", "REPORTED", "Turkish military helicopter crash kills 5", "A Turkish military AS-532 helicopter crashed in Eskisehir, killing all five people on board.", "(Turkish officials)", (90, 88, 82)), ("10 CARTAGENA \u00b7 AMERICAS", "REPORTED", "Supermarket hostages: 25 held in Cartagena", "Twenty-five people were held hostage in a Cartagena supermarket; five elderly women were freed and airport landings paused.", "(Colombian officials)", (27, 58, 92)), ("11 ADEN \u00b7 MIDDLE EAST", "REPORTED", "Houthis advance within 60 km of Aden", "Houthi forces advanced to within 60 km of Aden, Yemen, in their latest push south.", "(Wires)", (196, 96, 16)), ("12 LAHJ \u00b7 MIDDLE EAST", "REPORTED", "Saudi strikes kill 25, wound 6 in Yemen", "Saudi strikes on a bus and a truck in Wadi Maabaq, Lahj, killed or left missing 25 people and wounded six.", "(Yemeni officials)", (128, 32, 32)), ("13 JIUQUAN \u00b7 SPACE", "OFFICIAL", "China names first foreign astronaut for Tiangong", "China named the Shenzhou-24 crew: Tang Hongbo, Wu Yi and Muhammad Zeeshan Ali of Pakistan, the first foreigner on Tiangong.", "(CMSA)", (27, 90, 160))]
ALSO = [(14, "ANKARA", "Haftar visits Turkey first time", "REP"), (15, "LONDON", "UK sanctions Houthis, 4 officials", "OFF"), (16, "VILLAVICENCIO", "Car bomb injures 23", "REP"), (17, "GAZA", "Israel kills Hamas security chief", "REP"), (18, "BAGHDAD", "Iraq takes Kurdish oilfields", "OFF"), (19, "GAZA", "Meningitis alert: 272 cases Oct", "OFF"), (20, "DR CONGO", "Cessna missing; rebels claim hit", "CLM"), (21, "HANOI", "Hot-pot blast kills at least 6", "REP"), (22, "GULF OF FINLAND", "Ukraine hits Sparta II", "REP"), (23, "KUALA LUMPUR", "Migrants returned to Myanmar", "OFF"), (24, "ULLEUNGDO", "Korea shelter as jets enter ADIZ", "OFF"), (25, "DHAKA", "Hasina plans return 16 Dec", "REP"), (26, "THE HAGUE", "14 nations back ICJ ruling", "REP"), (27, "JAKARTA", "2 VP candidates nominated", "OFF"), (28, "BEIJING", "Official Ma sentenced to death", "OFF"), (29, "BRUSSELS", "NATO vows space defence", "OFF"), (30, "MEXICO CITY", "US drone aided El Chapo capture", "REP"), (31, "SAN SALVADOR", "Bukele names 3 soldiers killed", "OFF"), (32, "OTTAWA", "Only 41.9% of air fleet ready", "REP"), (33, "WASHINGTON", "Megaspeed on trade blacklist", "OFF"), (34, "KYIV", "Zelensky urges four-way talks", "REP"), (35, "RAS AL KHAIMAH", "Bus-truck crash kills 13", "REP"), (36, "LONDON", "Record 5,258 heat deaths 2026", "OFF"), (37, "KOUROU", "Ariane 6 lofts 36 satellites", "OFF"), (38, "CIKANDE", "Factory-fire toll rises to 26", "REP")]
ALSO_CHIP = {"OFF": (27, 90, 160), "REP": (90, 88, 82), "CLM": (196, 96, 16)}
NUMBERS = [("11", "hurt in Riyadh"), ("9", "killed in Ukraine"), ("50,018", "Dow first close"), ("+8.99%", "Taiex record"), ("25", "killed in Lahj"), ("26", "Cikande toll"), ("10/12", "Huawei guilty"), ("96", "drones at Ukraine")]
UTC = "02:15 NATO vows space defence  \u00b7  08:16 Hanoi blast  \u00b7  10:42 Saudi strikes Yemen  \u00b7  14:27 Riyadh tower hit  \u00b7  16:51 Houthis 60 km from Aden  \u00b7  18:58 Hormuz ship attack  \u00b7  20:41 Huawei guilty"
REGIONS = [("Europe", 9, (27, 90, 160)), ("Middle East", 8, (179, 35, 27)), ("Asia", 8, (198, 142, 30)), ("Africa", 2, (31, 110, 61)), ("Americas", 7, (27, 58, 92)), ("World / Space", 4, (90, 88, 82))]

def scene(d, x, y, w, h, kind, base):
    x, y, w, h = int(x), int(y), int(w), int(h); d.rectangle([x, y, x + w, y + h], fill=base)
    if kind == 0:  # Riyadh night skyline + PIF tower + smoke + drone
        d.rectangle([x, y + h - 26, x + w, y + h], fill=(12, 16, 34))
        for bx, bw, bh in [(0, 34, 52), (40, 26, 38), (70, 30, 62), (200, 34, 44), (240, 28, 58), (272, 30, 40)]:
            d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(24, 30, 56))
            for wy in range(y + h - bh + 6, y + h - 6, 10):
                for wx in range(x + bx + 5, x + bx + bw - 4, 9): d.rectangle([wx, wy, wx + 3, wy + 4], fill=(240, 200, 90))
        d.polygon([(x + 128, y + 6), (x + 152, y + 6), (x + 148, y + h), (x + 132, y + h)], fill=(52, 66, 110)); d.rectangle([x + 128, y + 6, x + 152, y + 14], fill=(240, 200, 90))
        for cx, cy, r in [(138, 22, 12), (150, 14, 15), (162, 24, 11)]: d.ellipse([x + cx - r, y + cy - r, x + cx + r, y + cy + r], fill=(150, 150, 150))
        d.ellipse([x + 240, y + 14, x + 252, y + 22], fill=(255, 80, 60)); d.line([x + 236, y + 18, x + 258, y + 18], fill=(255, 255, 255), width=1)
    elif kind == 1:  # Shanghai party gate + document
        d.rectangle([x, y + h - 30, x + w, y + h], fill=(60, 20, 20)); d.rectangle([x + 20, y + 26, x + w - 20, y + h - 6], fill=(128, 32, 32)); d.rectangle([x + 30, y + 34, x + w - 30, y + 44], fill=(198, 142, 30))
        for cx in range(x + 44, x + w - 40, 34): d.rectangle([cx, y + 52, cx + 18, y + h - 12], fill=(90, 20, 20))
        d.rectangle([x + w - 92, y + 12, x + w - 18, y + 52], fill=(255, 255, 255)); d.line([x + w - 84, y + 22, x + w - 26, y + 22], fill=RED, width=2)
        for ly in (30, 37, 44): d.line([x + w - 84, y + ly, x + w - 26, y + ly], fill=(120, 120, 120), width=1)
        d.ellipse([x + w - 52, y + 62, x + w - 30, y + 84], fill=RED)
    elif kind == 2:  # courthouse + gavel
        d.rectangle([x, y + h - 22, x + w, y + h], fill=(40, 40, 44)); d.polygon([(x + 30, y + 14), (x + w - 30, y + 14), (x + w - 8, y + 34), (x + 8, y + 34)], fill=(90, 88, 82))
        for cx in range(x + 36, x + w - 40, 44): d.rectangle([cx, y + 36, cx + 16, y + h - 8], fill=(220, 220, 220))
        d.rectangle([x + w - 78, y + 48, x + w - 30, y + 62], fill=(120, 70, 30)); d.rectangle([x + w - 58, y + 62, x + w - 50, y + 78], fill=(120, 70, 30))
    else:  # generic card mini-scene: sky band, ground, simple motif
        d.rectangle([x, y + h - 16, x + w, y + h], fill=(60, 60, 66)); d.ellipse([x + w - 34, y + 6, x + w - 10, y + 30], fill=(240, 200, 90))
        for bx in range(0, w - 20, 26): d.rectangle([x + bx, y + h - 34, x + bx + 18, y + h - 16], fill=(120, 120, 128))
def build():
    im = Image.new("RGB", (W, H), PAPER); d = ImageDraw.Draw(im); d.rectangle([0, 0, W, 7], fill=RED)
    d.text((16, 12), "THE WORLD ON ONE PAGE", font=sb(11), fill=RED); d.text((W - 16 - d.textlength("38 STORIES \u00b7 6 REGIONS \u00b7 13 FIELDS", font=sb(11)), 12), "38 STORIES \u00b7 6 REGIONS \u00b7 13 FIELDS", font=sb(11), fill=INK)
    d.text((16, 28), "Tuesday 24 November 2026", font=sr(33), fill=INK); d.text((16, 64), "Riyadh tower hit again  \u00b7  Shanghai party chief probed  \u00b7  Huawei guilty on 10 of 12 counts", font=sr(13), fill=RED)
    bx = 16
    for name, n, col in REGIONS:
        lab = f"{name} {n}"; f = sb(10); tw = d.textlength(lab, font=f) + 16
        d.rounded_rectangle([bx, 82, bx + tw, 100], 3, fill=col); d.text((bx + 8, 85), lab, font=f, fill=(255, 255, 255)); bx += tw + 6
    d.text((bx + 4, 85), "All from Tuesday 24 November 2026", font=sn(10), fill=GREY)
    cw = (W - 32 - 7 * 4) / 8
    for i, (num, lab) in enumerate(NUMBERS):
        x = 16 + i * (cw + 4); d.rectangle([x, 106, x + cw, 140], outline=NAVY, width=1, fill=(255, 255, 255)); nf = sb(21 if len(num) <= 6 else 17)
        d.text((x + cw / 2 - d.textlength(num, font=nf) / 2, 109), num, font=nf, fill=RED); d.text((x + cw / 2 - d.textlength(lab, font=sn(8)) / 2, 130), lab, font=sn(8), fill=GREY)
    d.text((16, 144), "THE DAY IN UTC", font=sb(9), fill=RED); d.text((104, 144), UTC, font=sn(9), fill=INK); d.line([16, 158, W - 16, 158], fill=INK, width=1)
    # Heroes: scene 100px tall, then text.
    hw = (W - 32 - 16) / 3
    for i, (kick, ch, head, deck, src, giant, base) in enumerate(HEROES):
        x = 16 + i * (hw + 8); y = 164; scene(d, x, y, hw, 100, i, base); gf = sb(54 if len(giant) <= 2 else 40); gw = d.textlength(giant, font=gf)
        d.text((x + hw - gw - 8, y + 100 - gf.size - 12), giant, font=gf, fill=(255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0))
        d.text((x, y + 106), kick, font=sb(10), fill=RED); chip(d, x + hw - 78, y + 104, ch); txt(d, x, y + 120, head, sr(15), w=hw, lh=17); txt(d, x, y + 154, deck, sn(9), w=hw, lh=12); d.text((x, y + 192), src, font=sn(9), fill=GREY)
    return im, d

def draw_cards(d):
    cw = (W - 32 - 24) / 5
    for r in range(2):
        y = 366 + r * 140
        for c in range(5):
            kick, ch, head, deck, src, base = CARDS[r * 5 + c]; x = 16 + c * (cw + 6)
            d.rectangle([x, y, x + cw, y + 136], outline=(200, 192, 172), width=1, fill=(255, 255, 255)); scene(d, x + 1, y + 1, cw - 2, 48, 3, base)
            d.text((x + 4, y + 52), kick, font=sb(8), fill=RED); chip(d, x + cw - 62, y + 51, ch)
            txt(d, x + 4, y + 66, head, sr(11), w=cw - 8, lh=13); txt(d, x + 4, y + 94, deck, sn(8), w=cw - 8, lh=10); d.text((x + 4, y + 126), src, font=sn(8), fill=GREY)
def draw_map(d):
    mx, my, mw, mh = 16, 648, 470, 170
    d.rectangle([mx, my, mx + mw, my + mh], fill=(210, 228, 240), outline=NAVY, width=1)
    def P(lon, lat): return (mx + (lon + 180) / 360 * mw, my + (84 - lat) / 142 * mh)
    for poly in CONTINENTS: d.polygon([P(lon, lat) for lon, lat in poly], fill=(120, 160, 110), outline=(70, 110, 70))
    d.text((mx + 6, my + 4), "WORLD MAP \u2014 13 ILLUSTRATED STORIES", font=sb(8), fill=NAVY)
    for n, lat, lon, dx, dy in PINS:
        px, py = P(lon, lat); qx, qy = px + dx, py + dy
        if dx or dy: d.line([px, py, qx, qy], fill=RED, width=1)
        d.ellipse([qx - 8, qy - 8, qx + 8, qy + 8], fill=RED, outline=(255, 255, 255), width=1); f = sb(8); t = str(n); d.text((qx - d.textlength(t, font=f) / 2, qy - 6), t, font=f, fill=(255, 255, 255))
    ly = my + mh + 8; d.text((mx, ly), "MAP KEY", font=sb(9), fill=RED)
    for i, lab in enumerate(LEGEND): d.text((mx + (i // 7) * 240, ly + 14 + (i % 7) * 10), lab, font=sn(9), fill=INK)
def draw_also(d):
    d.text((494, 648), "ALSO ON TUESDAY \u2014 25 MORE STORIES", font=sb(11), fill=RED)
    for i, (n, city, head, code) in enumerate(ALSO):
        col, row = i // 13, i % 13; x = 494 + col * 262; y = 670 + row * 17; f = sn(8); s = f"{n} {city} \u2014 {head}"; d.text((x, y), s, font=f, fill=INK)
        c = ALSO_CHIP[code]; cf = sb(7); tw = d.textlength(code, font=cf) + 6; cx = x + d.textlength(s, font=f) + 4
        d.rounded_rectangle([cx, y, cx + tw, y + 10], 2, fill=c); d.text((cx + 3, y + 1), code, font=cf, fill=(255, 255, 255))
def finish(im, d):
    draw_cards(d); draw_map(d); draw_also(d)
    d.rectangle([16, 914, W - 16, 948], outline=RED, width=2, fill=(255, 240, 238))
    d.text((24, 918), "DATE CHECK \u2014 Every story above happened or was first reported Tue 24 Nov 2026; wires to 23:00 UTC. LEFT OUT (not 24 Nov): Hormuz mine claims, Nvidia CEO return, EU sanctions 22 (23 Nov); COP31 no deal (22 Nov);", font=sn(8), fill=INK)
    d.text((24, 932), "El Chapo Isidro arrested Fri 20 Nov; Cikande fire began Sat 21 Nov. NOT YET: Shenzhou-24 launch Wed 25 Nov 00:18 UTC; Huawei sentencing Sep 2027; MPR vote 11 Dec; Hasina return 16 Dec.", font=sn(8), fill=INK)
    d.text((16, 954), "Sources: Saudi officials \u00b7 CCDI \u00b7 US court \u00b7 CAS \u00b7 UKMTO \u00b7 Reuters \u00b7 Ukrainian officials \u00b7 CMSA \u00b7 wires.  CONFIRMED = 2+ outlets \u00b7 OFFICIAL = on record \u00b7 REPORTED = one outlet \u00b7 CLAIM = one side\u2019s claim.", font=sn(9), fill=GREY)
    d.text((16, 970), "Scenes are drawn in code, not photographs. The world map uses real latitude and longitude. 38 stories, all from Tuesday 24 November 2026.", font=sn(9), fill=GREY)
    d.text((16, 986), "THE WORLD ON ONE PAGE \u00b7 TUESDAY 24 NOVEMBER 2026", font=sb(8), fill=GREY)
    out = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "out"), "entry.png")
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True); im.save(out, optimize=True)
if __name__ == "__main__":
    im, d = build(); finish(im, d)
