#!/usr/bin/env python3
"""Thursday 26 November 2026 — one-image world news front page.

Rebuilt from scratch for make.fun news-image-20261126. A dense 1024x1024
newspaper front page: masthead with a red DATE CHECK box, a five-cell KPI
strip, three illustrated lead stories, a numbered-pin world map, a UTC
timeline of the week's key space events, six region sections holding 39
stories, a stories-by-region bar and a sources footer. Every story carries
an OFFICIAL / REPORTED / CLAIM credibility tag. PIL only; no network, no
randomness, no timestamps beyond the fixed date.
"""

import os

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
PAPER = (250, 246, 236)
INK = (20, 20, 20)
ACCENT = (180, 32, 38)
NAVY = (24, 38, 66)
MUTED = (96, 94, 86)
BODY = (56, 54, 50)
WHITE = (255, 255, 255)
OCEAN = (176, 196, 212)
COAST = (72, 96, 122)
KPI_BG = (240, 235, 222)
MAP_BG = (233, 239, 245)
GREEN = (36, 122, 64)
BLUE = (34, 74, 148)
ORANGE = (198, 92, 22)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

MX = 40
CW = SIZE - 2 * MX

CRED_FILL = {"OFFICIAL": GREEN, "REPORTED": BLUE, "CLAIM": ORANGE}

_cache = {}


def load_font(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def wrap(draw, text, font, max_w):
    """Greedy word wrap; returns the lines that fit inside max_w."""
    out, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w or not cur:
            cur = trial
        else:
            out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def centred(draw, cx, y, text, font, fill=INK):
    draw.text((cx - draw.textlength(text, font=font) / 2, y), text,
              font=font, fill=fill)


def hline(draw, y, weight=1, fill=INK):
    draw.rectangle([MX, y, SIZE - MX, y + weight - 1], fill=fill)
    return y + weight


def cred_chip(draw, x, y, label, right=None):
    """Small coloured credibility tag. Returns its width."""
    f = load_font(SANS_B, 7)
    w = int(draw.textlength(label, font=f)) + 10
    if right is not None:
        x = right - w
    draw.rectangle([x, y, x + w - 1, y + 11], fill=CRED_FILL[label])
    draw.text((x + 5, y + 1), label, font=f, fill=WHITE)
    return w


# ---------------------------------------------------------------- art
def satellite_art(d, x0, y0, w, h):
    """Orbital satellite over a small Earth, drawn in the lead box."""
    cx, cy = x0 + w // 2, y0 + h // 2
    for sx, sy in ((x0 + 18, y0 + 10), (x0 + 44, y0 + 26), (x0 + w - 34, y0 + 12),
                   (x0 + w - 58, y0 + 40), (x0 + 66, y0 + 46)):
        d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=WHITE)
    # solar wings
    d.rectangle([cx - 66, cy - 8, cx - 20, cy + 8], fill=(62, 112, 164))
    d.rectangle([cx + 20, cy - 8, cx + 66, cy + 8], fill=(62, 112, 164))
    for gx in (cx - 51, cx - 36, cx + 36, cx + 51):
        d.line([gx, cy - 8, gx, cy + 8], fill=(30, 70, 110), width=1)
    # body
    d.rectangle([cx - 17, cy - 11, cx + 17, cy + 11], fill=NAVY)
    d.rectangle([cx - 17, cy - 3, cx + 17, cy + 3], fill=ACCENT)
    d.ellipse([cx - 4, cy - 5, cx + 4, cy + 3], fill=WHITE)
    # dish on top, with signal arcs
    d.arc([cx - 9, cy - 30, cx + 9, cy - 12], 180, 360, fill=NAVY, width=2)
    d.line([cx, cy - 11, cx, cy - 18], fill=NAVY, width=2)
    d.arc([cx - 16, cy - 40, cx + 16, cy - 8], 200, 340, fill=ACCENT, width=1)
    # small Earth, bottom right corner
    ex, ey = x0 + w - 26, y0 + h - 18
    d.ellipse([ex - 12, ey - 12, ex + 12, ey + 12], fill=OCEAN)
    d.ellipse([ex - 7, ey - 4, ex + 2, ey + 2], fill=WHITE)
    d.ellipse([ex + 2, ey + 3, ex + 8, ey + 8], fill=(120, 160, 190))


def mercury_art(d, x0, y0, w, h):
    """Cratered Mercury with a ring and a tiny approaching craft."""
    cx, cy = x0 + w // 2, y0 + h // 2 + 2
    for sx, sy in ((x0 + 16, y0 + 12), (x0 + 52, y0 + 8), (x0 + w - 40, y0 + 16),
                   (x0 + w - 18, y0 + 44), (x0 + 30, y0 + 48)):
        d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=WHITE)
    # ring behind the planet
    d.ellipse([cx - 38, cy - 11, cx + 38, cy + 11], outline=ACCENT, width=2)
    # planet
    d.ellipse([cx - 23, cy - 23, cx + 23, cy + 23], fill=(152, 146, 134))
    for ox, oy, r in ((-9, -8, 4), (7, -4, 3), (-3, 8, 5), (11, 9, 3),
                      (-12, 4, 2)):
        d.ellipse([cx + ox - r, cy + oy - r, cx + ox + r, cy + oy + r],
                  fill=(118, 112, 100))
    # front half of the ring, crossing the planet
    d.arc([cx - 38, cy - 11, cx + 38, cy + 11], 15, 165, fill=ACCENT, width=2)
    # approaching craft, top right, with a dotted path
    px, py = x0 + w - 34, y0 + 14
    for i in range(5):
        t = i / 4.0
        dx = px + (cx + 30 - px) * t
        dy = py + (cy - 14 - py) * t
        d.ellipse([dx - 1, dy - 1, dx + 1, dy + 1], fill=NAVY)
    d.polygon([(px, py - 6), (px + 5, py + 4), (px - 5, py + 4)], fill=NAVY)
    d.rectangle([px - 3, py + 4, px + 3, py + 9], fill=ACCENT)


def rocket_art(d, x0, y0, w, h):
    """Slim sounding rocket climbing past stars, flame below."""
    cx, cy = x0 + w // 2, y0 + h // 2 - 2
    for sx, sy in ((x0 + 18, y0 + 14), (x0 + 46, y0 + 8), (x0 + w - 44, y0 + 12),
                   (x0 + w - 20, y0 + 34), (x0 + 30, y0 + 44)):
        d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=WHITE)
    # fins
    d.polygon([(cx - 9, cy + 10), (cx - 24, cy + 26), (cx - 9, cy + 20)],
              fill=NAVY)
    d.polygon([(cx + 9, cy + 10), (cx + 24, cy + 26), (cx + 9, cy + 20)],
              fill=NAVY)
    # body and nose
    d.rectangle([cx - 9, cy - 26, cx + 9, cy + 12], fill=NAVY)
    d.polygon([(cx - 9, cy - 26), (cx + 9, cy - 26), (cx, cy - 42)],
              fill=ACCENT)
    d.rectangle([cx - 9, cy - 8, cx + 9, cy - 2], fill=WHITE)
    d.ellipse([cx - 4, cy + 1, cx + 4, cy + 9], fill=WHITE,
              outline=NAVY, width=1)
    # flame and smoke
    d.polygon([(cx - 7, cy + 12), (cx + 7, cy + 12), (cx, cy + 32)],
              fill=(230, 120, 30))
    d.polygon([(cx - 3, cy + 12), (cx + 3, cy + 12), (cx, cy + 24)],
              fill=(245, 200, 60))
    for sx, sy, r in ((cx - 18, cy + 30, 3), (cx + 16, cy + 34, 2),
                      (cx - 6, cy + 38, 2)):
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(200, 200, 200))


ART = {"satellite": satellite_art, "planet": mercury_art,
       "rocket": rocket_art}

# ---------------------------------------------------------------- data
LEADS = [
    {"tag": "SPACE  ·  NATO", "cred": "REPORTED", "art": "satellite",
     "wash": (244, 220, 218),
     "head": "RUSSIA'S NUCLEAR SATELLITE ALARMS NATO",
     "body": ("Western intel: Moscow's \u201cSputnik-S\u201d satellite, stored "
              "near Moscow for years, could launch in 60 days, possibly "
              "in December. NATO's Rutte vows to defend every inch, "
              "including space. Kremlin denies it."),
     "src": "Reuters / NDR-WDR-SZ, Nov 23"},
    {"tag": "SPACE  ·  MERCURY", "cred": "OFFICIAL", "art": "planet",
     "wash": (214, 230, 242),
     "head": "BEPICOLOMBO REACHES MERCURY AFTER 8 YEARS",
     "body": ("ESA/JAXA BepiColombo enters Mercury orbit on 21 Nov 2026 "
              "\u2014 only the second mission ever to do so after NASA's "
              "MESSENGER. Two orbiters separate 9\u201310 Dec; science "
              "begins April 2027."),
     "src": "AP / Washington Post"},
    {"tag": "SPACE  ·  CHINA", "cred": "OFFICIAL", "art": "rocket",
     "wash": (250, 232, 205),
     "head": "FIRST FOREIGNER ABOARD TIANGONG",
     "body": ("Shenzhou-24 docks 11:56 on 25 Nov; crew enters Tiangong "
              "the same day. Pakistani payload specialist Muhammad "
              "Zeeshan Ali is the first foreign astronaut on the "
              "station; returns on Shenzhou-23 in 5\u201310 days."),
     "src": "Xinhua / Reuters"},
]

KPIS = [
    ("60 DAYS", "SPUTNIK-S LAUNCH WINDOW"),
    ("8 YRS", "BEPICOLOMBO'S VOYAGE"),
    ("500,000", "RUSSIAN WAR DEAD (OWN FIGURES)"),
    ("+26%", "UK ENERGY BILLS FROM JAN"),
    ("36%", "BANGLADESH WAGE RISE"),
]

REGIONS = [
    ("ASIA", [
        ("XI PROBE ENSNARES SHANGHAI CHIEF CHEN", "REPORTED"),
        ("S. KOREA MINISTER QUITS OVER EXAM SCANDAL", "OFFICIAL"),
        ("AUSTRALIA FORCES PLATFORMS TO REMOVE HARMFUL CONTENT", "OFFICIAL"),
        ("AUSTRALIA-SOLOMON IS. SECURITY PACT", "OFFICIAL"),
        ("N. KOREA THREATENS SWISS OFFICE", "REPORTED"),
        ("VIETNAM PUSHES GREEN FARMING", "REPORTED"),
        ("S. KOREA TO BOOST EV INDUSTRY", "REPORTED"),
        ("INDIA SPACE ECONOMY $9BN TO $45BN", "REPORTED"),
        ("IITs ADD 6,000 TECH SEATS", "OFFICIAL"),
    ]),
    ("MIDDLE EAST", [
        ("IRAN BRACES FOR US BLOCKADE", "REPORTED"),
        ("ISRAEL: IRAN BUILDING CHEMICAL WEAPONS", "CLAIM"),
        ("SWIMMER CROSSES HORMUZ FOR OCEANS", "REPORTED"),
        ("EGYPT: SUEZ REVENUES RECOVERING", "REPORTED"),
        ("ETHIOPIA PUSHES HEALTH INDEPENDENCE", "REPORTED"),
        ("HOUTHI THREAT STILL LOOMS", "REPORTED"),
    ]),
    ("EUROPE", [
        ("EU UNVEILS 22ND RUSSIA SANCTIONS PACKAGE", "OFFICIAL"),
        ("RUSSIA'S OWN TOLL: NEARLY 500,000 DEAD", "REPORTED"),
        ("FRANCE EYES CRITICAL MINERALS FREEDOM", "REPORTED"),
        ("UK PROBES NUCLEAR TEST LEGACY", "REPORTED"),
        ("POLAND ALARMS OVER AIRSPACE VIOLATIONS", "REPORTED"),
        ("RUSSIA RAISES DEFENCE SPENDING", "REPORTED"),
        ("UKRAINE-HUNGARY SEEK ECONOMIC TIES", "REPORTED"),
        ("EU PLANS \u20ac50BN TECH FUND", "OFFICIAL"),
    ]),
    ("AMERICAS", [
        ("US CONSUMER CONFIDENCE NEAR 2-YEAR HIGH", "OFFICIAL"),
        ("CANADA HOLDS INFLATION STRATEGY", "OFFICIAL"),
        ("PETROBRAS UNVEILS $122BN PLAN", "OFFICIAL"),
        ("VENEZUELA DEBT: $237.5BN REVEALED", "REPORTED"),
        ("COLOMBIA: 10 YEARS SINCE PEACE DEAL", "REPORTED"),
        ("CARTAGENA HOSTAGES FREED AFTER 17 HRS", "REPORTED"),
        ("US READIES NEW GLOBAL TARIFF PLAN", "REPORTED"),
        ("ABREGO GARCIA LEAVES US FOR SPAIN", "REPORTED"),
    ]),
    ("AFRICA", [
        ("ZIMBABWE ARREST WARRANT FOR MUGABE'S SON", "REPORTED"),
        ("AFRICAN INSURGENTS TURN TO CHEAP DRONES", "REPORTED"),
        ("EGYPT'S SUEZ RECOVERY LIFTS AFRICA TRADE", "REPORTED"),
        ("ETHIOPIA'S HEALTH PUSH DRAWS PRAISE", "REPORTED"),
    ]),
    ("GLOBAL", [
        ("BARBADOS, INDIA PUSH AI GOVERNANCE", "REPORTED"),
        ("UN SEEKS GLOBAL AI SAFETY RULES", "REPORTED"),
        ("REAL MADRID THRASH PSV 5-1", "OFFICIAL"),
        ("ASTEROID CLOSE-UPS DUE FROM DART FOLLOW-UP", "REPORTED"),
    ]),
]

DIST = [("ASIA", 9, ACCENT), ("MIDDLE EAST", 6, (214, 110, 30)),
        ("EUROPE", 8, NAVY), ("AMERICAS", 8, (40, 110, 70)),
        ("AFRICA", 4, (120, 70, 140)), ("GLOBAL", 4, MUTED)]

# Rough continent shapes in a 900 x 100 map box.
LAND = [
    [(25, 25), (90, 8), (170, 10), (225, 20), (215, 40), (180, 45),
     (200, 60), (160, 75), (120, 88), (70, 80), (40, 60), (20, 40)],
    [(245, 5), (275, 3), (290, 12), (265, 22), (245, 14)],
    [(210, 65), (250, 62), (280, 70), (270, 92), (240, 97), (215, 82)],
    [(430, 12), (470, 6), (500, 14), (490, 30), (460, 34), (435, 26)],
    [(440, 38), (490, 34), (520, 46), (510, 72), (480, 88), (450, 76),
     (435, 54)],
    [(510, 8), (650, 4), (780, 12), (850, 26), (820, 52), (750, 64),
     (680, 58), (600, 50), (540, 32), (510, 20)],
    [(760, 76), (820, 72), (850, 80), (820, 92), (770, 90), (750, 84)],
]

PINS = [
    (0.48, 0.22, "BERLIN"),
    (0.56, 0.20, "MOSCOW"),
    (0.64, 0.52, "HORMUZ"),
    (0.81, 0.33, "JIUQUAN"),
    (0.24, 0.62, "CARTAGENA"),
    (0.36, 0.16, "MERCURY"),
]

TL_EVENTS = [
    ("21 NOV", "BEPICOLOMBO ENTERS MERCURY ORBIT", 0.08, True),
    ("00:18 UTC", "SHENZHOU-24 LIFTOFF (25 NOV)", 0.48, False),
    ("03:56 UTC", "SHENZHOU-24 DOCKS TIANGONG", 0.86, True),
]

# ---------------------------------------------------------------- page
def items_block(draw, x0, y, items, col_w, paint=True):
    """One region's story list. Returns the y below the block."""
    f = load_font(SANS, 10)
    chip_f = load_font(SANS_B, 7)
    for head, cred in items:
        cw = int(draw.textlength(cred, font=chip_f)) + 10
        if paint:
            draw.rectangle([x0, y, x0 + cw - 1, y + 11],
                           fill=CRED_FILL[cred])
            draw.text((x0 + 5, y + 1), cred, font=chip_f, fill=WHITE)
        tx = x0 + cw + 6
        for ln in wrap(draw, head, f, col_w - cw - 6):
            if paint:
                draw.text((tx, y), ln, font=f, fill=BODY)
            y += 12
        y += 2
    return y


def build():
    img = Image.new("RGB", (SIZE, SIZE), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([8, 8, SIZE - 9, SIZE - 9], outline=INK, width=2)

    # ---- masthead ----
    y = 20
    centred(d, 460, y, "THE WORLD IN ONE IMAGE",
            load_font(SERIF_B, 38))
    y += 50
    centred(d, 460, y, "T H U R S D A Y ,  2 6  N O V E M B E R  2 0 2 6",
            load_font(SANS_B, 14), fill=ACCENT)
    y += 22
    # red DATE CHECK box, top right
    bx0, by0, bw, bh = SIZE - MX - 184, 18, 184, 48
    d.rectangle([bx0, by0, bx0 + bw, by0 + bh], outline=ACCENT, width=2)
    d.rectangle([bx0, by0, bx0 + bw, by0 + 20], fill=ACCENT)
    centred(d, bx0 + bw // 2, by0 + 3, "DATE CHECK",
            load_font(SANS_B, 13), fill=WHITE)
    centred(d, bx0 + bw // 2, by0 + 25, "THU 26 NOV 2026 \u00b7 UTC",
            load_font(SANS_B, 11), fill=ACCENT)
    y = hline(d, y, weight=3)
    y += 8

    # ---- KPI strip ----
    kpi_h = 40
    d.rectangle([MX, y, SIZE - MX, y + kpi_h], fill=KPI_BG, outline=INK,
                width=1)
    cell = CW // 5
    for i, (num, label) in enumerate(KPIS):
        cx = MX + cell * i + cell // 2
        if i:
            d.line([MX + cell * i, y + 6, MX + cell * i, y + kpi_h - 6],
                   fill=MUTED, width=1)
        centred(d, cx, y + 4, num, load_font(SANS_B, 17), fill=ACCENT)
        centred(d, cx, y + 24, label, load_font(SANS_B, 9), fill=BODY)
    y += kpi_h + 8

    # ---- three leads ----
    gap = 14
    lw = (CW - 2 * gap) // 3
    art_h = 62
    lead_bottom = y
    for i, lead in enumerate(LEADS):
        x0 = MX + i * (lw + gap)
        d.rectangle([x0, y, x0 + lw, y + art_h], fill=lead["wash"],
                    outline=INK, width=1)
        ART[lead["art"]](d, x0, y, lw, art_h)
        ty = y + art_h + 6
        d.text((x0, ty), lead["tag"], font=load_font(SANS_B, 11),
               fill=ACCENT)
        cred_chip(d, x0, ty, lead["cred"], right=x0 + lw)
        ty += 16
        for ln in wrap(d, lead["head"], load_font(SERIF_B, 18), lw):
            d.text((x0, ty), ln, font=load_font(SERIF_B, 18), fill=INK)
            ty += 21
        ty += 3
        for ln in wrap(d, lead["body"], load_font(SERIF, 11), lw):
            d.text((x0, ty), ln, font=load_font(SERIF, 11), fill=BODY)
            ty += 14
        ty += 3
        d.text((x0, ty), lead["src"], font=load_font(SANS, 9), fill=MUTED)
        lead_bottom = max(lead_bottom, ty + 12)
    y = lead_bottom + 8
    y = hline(d, y, weight=1)
    y += 7

    # ---- world map ----
    d.text((MX, y), "THE WORLD TODAY", font=load_font(SANS_B, 12),
           fill=NAVY)
    right = "6 REGIONS \u00b7 39 STORIES + 3 LEADS"
    d.text((SIZE - MX - d.textlength(right, font=load_font(SANS_B, 11)), y),
           right, font=load_font(SANS_B, 11), fill=ACCENT)
    y += 18
    map_h = 92
    d.rectangle([MX, y, MX + CW, y + map_h], fill=MAP_BG, outline=INK,
                width=1)
    sx, sy = CW / 900.0, map_h / 100.0
    for poly in LAND:
        d.polygon([(MX + px * sx, y + py * sy) for px, py in poly],
                  fill=OCEAN, outline=COAST)
    for idx, (fx, fy, name) in enumerate(PINS, start=1):
        px, py = MX + fx * CW, y + fy * map_h
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=ACCENT,
                  outline=WHITE, width=1)
        centred(d, px, py - 5, str(idx), load_font(SANS_B, 9), fill=WHITE)
        lf = load_font(SANS_B, 9)
        lwdt = d.textlength(name, font=lf)
        lx = min(max(px - lwdt / 2, MX + 2), MX + CW - lwdt - 2)
        d.text((lx, py - 19), name, font=lf, fill=ACCENT)
    y += map_h + 8

    # ---- UTC timeline ----
    d.text((MX, y), "UTC TIMELINE \u2014 KEY EVENTS (21\u201326 NOVEMBER 2026)",
           font=load_font(SANS_B, 12), fill=NAVY)
    y += 18
    tl_y = y + 28
    d.line([MX, tl_y, SIZE - MX, tl_y], fill=INK, width=2)
    for frac, lab in ((0.08, "21 NOV"), (0.50, "25 NOV 00:00"),
                      (0.92, "26 NOV 00:00")):
        tx = MX + frac * CW
        d.line([tx, tl_y - 4, tx, tl_y + 4], fill=INK, width=1)
        centred(d, tx, tl_y + 8, lab, load_font(SANS, 9), fill=MUTED)
    for stamp, text, frac, above in TL_EVENTS:
        ex = MX + frac * CW
        d.ellipse([ex - 4, tl_y - 4, ex + 4, tl_y + 4], fill=ACCENT)
        lab = stamp + " \u2014 " + text
        lf = load_font(SANS_B, 9)
        lwdt = d.textlength(lab, font=lf)
        lx = min(max(ex - lwdt / 2, MX), SIZE - MX - lwdt)
        ly = tl_y - 26 if above else tl_y + 22
        d.text((lx, ly), lab, font=lf, fill=ACCENT)
    y = tl_y + 38

    # ---- region grid ----
    col_w = (CW - 2 * gap) // 3
    for row in (REGIONS[0:3], REGIONS[3:6]):
        row_h = 0
        for name, items in row:
            row_h = max(row_h, items_block(d, 0, 0, items, col_w,
                                           paint=False))
        for c, (name, items) in enumerate(row):
            x0 = MX + c * (col_w + gap)
            d.rectangle([x0, y, x0 + col_w, y + 20], fill=NAVY)
            d.text((x0 + 6, y + 4), name, font=load_font(SANS_B, 11),
                   fill=WHITE)
            cnt = f"{len(items)} STORIES"
            d.text((x0 + col_w - 6 - d.textlength(
                cnt, font=load_font(SANS_B, 10)), y + 4), cnt,
                font=load_font(SANS_B, 10), fill=WHITE)
            items_block(d, x0, y + 24, items, col_w)
        y += 20 + row_h + 8
    y += 2

    # ---- distribution bar ----
    d.text((MX, y), "STORIES BY REGION (39 GRID STORIES)",
           font=load_font(SANS_B, 11), fill=NAVY)
    y += 16
    total = sum(n for _, n, _ in DIST)
    x = MX
    for k, (name, n, color) in enumerate(DIST):
        end = MX + round(CW * sum(m for _, m, _ in DIST[:k + 1]) / total)
        d.rectangle([x, y, end - 1, y + 15], fill=color)
        centred(d, (x + end) // 2, y + 2, str(n),
                load_font(SANS_B, 10), fill=WHITE)
        x = end
    y += 15 + 6
    lx = MX
    for name, n, color in DIST:
        d.rectangle([lx, y, lx + 10, y + 10], fill=color)
        lab = f"{name} {n}"
        d.text((lx + 13, y), lab, font=load_font(SANS_B, 9), fill=BODY)
        lx += 13 + d.textlength(lab, font=load_font(SANS_B, 9)) + 16
    y += 18

    # ---- footer ----
    y = hline(d, y, weight=1)
    y += 6
    centred(d, SIZE // 2, y,
            "Sources: Reuters \u00b7 AP \u00b7 Xinhua \u00b7 NYT \u00b7 CNN "
            "\u00b7 SCMP \u00b7 Washington Post",
            load_font(SANS, 10), fill=MUTED)
    y += 14
    centred(d, SIZE // 2, y,
            "Compiled from the day's reporting  \u00b7  "
            "Thursday 26 November 2026",
            load_font(SANS, 10), fill=MUTED)
    y += 14

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    img.save(out)
    print(f"saved {out} (1024, 1024); bottom y = {y}")
    return out


if __name__ == "__main__":
    build()
