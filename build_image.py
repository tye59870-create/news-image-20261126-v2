#!/usr/bin/env python3
"""Front page for Thursday 26 November 2026 (make.fun news-image-20261126).

A dense newspaper front page: masthead, KPI bar, three illustrated leads,
a world map, a UTC timeline, six region sections totalling 39 stories, a
region distribution bar and a source footer. 1024x1024, PIL only,
deterministic: no network, no randomness, no timestamps inside the image
beyond the fixed date.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (251, 247, 238)
INK = (18, 18, 18)
RED = (176, 30, 40)
NAVY = (22, 35, 63)
GREY = (92, 90, 84)
BODY = (54, 52, 48)
WHITE = (255, 255, 255)
SEA = (178, 198, 214)
SEA_EDGE = (70, 95, 120)
KPI_FILL = (240, 235, 224)

F_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
F_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

MARGIN = 44
INNER = W - 2 * MARGIN
GAP = 12


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(d, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_center(d, cx, y, text, fnt, fill=INK):
    w = d.textlength(text, font=fnt)
    d.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size


def rule(d, y, x0=MARGIN, x1=W - MARGIN, weight=1, fill=INK):
    d.rectangle([x0, y, x1, y + weight - 1], fill=fill)
    return y + weight


def draw_satellite(d, x, y, s):
    """A small satellite: body, panels, dish."""
    d.rectangle([x + s * 0.38, y + s * 0.35, x + s * 0.62, y + s * 0.65],
                fill=NAVY)
    d.rectangle([x + s * 0.05, y + s * 0.42, x + s * 0.32, y + s * 0.58],
                fill=RED)
    d.rectangle([x + s * 0.68, y + s * 0.42, x + s * 0.95, y + s * 0.58],
                fill=RED)
    d.ellipse([x + s * 0.44, y + s * 0.42, x + s * 0.56, y + s * 0.58],
              fill=WHITE)
    d.line([x + s * 0.5, y + s * 0.35, x + s * 0.72, y + s * 0.12],
           fill=NAVY, width=2)
    d.ellipse([x + s * 0.66, y + s * 0.06, x + s * 0.78, y + s * 0.18],
              outline=NAVY, width=2)


def draw_planet(d, x, y, s):
    """A ringed planet."""
    d.ellipse([x + s * 0.2, y + s * 0.18, x + s * 0.8, y + s * 0.82],
              fill=(120, 140, 170))
    d.ellipse([x + s * 0.32, y + s * 0.3, x + s * 0.68, y + s * 0.7],
              fill=(150, 170, 195))
    d.ellipse([x + s * 0.05, y + s * 0.42, x + s * 0.95, y + s * 0.58],
              outline=RED, width=3)
    d.ellipse([x + s * 0.42, y + s * 0.4, x + s * 0.5, y + s * 0.48],
              fill=WHITE)


def draw_rocket(d, x, y, s):
    """A small rocket with a flame."""
    d.polygon([(x + s * 0.5, y + s * 0.05), (x + s * 0.7, y + s * 0.4),
               (x + s * 0.3, y + s * 0.4)], fill=NAVY)
    d.rectangle([x + s * 0.32, y + s * 0.38, x + s * 0.68, y + s * 0.72],
                fill=NAVY)
    d.polygon([(x + s * 0.32, y + s * 0.72), (x + s * 0.14, y + s * 0.88),
               (x + s * 0.32, y + s * 0.82)], fill=NAVY)
    d.polygon([(x + s * 0.68, y + s * 0.72), (x + s * 0.86, y + s * 0.88),
               (x + s * 0.68, y + s * 0.82)], fill=NAVY)
    d.polygon([(x + s * 0.42, y + s * 0.72), (x + s * 0.58, y + s * 0.72),
               (x + s * 0.5, y + s * 0.98)], fill=RED)
    d.ellipse([x + s * 0.42, y + s * 0.44, x + s * 0.58, y + s * 0.6],
              fill=WHITE)


ICONS = {"satellite": draw_satellite, "planet": draw_planet,
         "rocket": draw_rocket}

LEADS = [
    {"kicker": "SPACE  ·  NATO",
     "headline": "RUSSIA'S NUCLEAR SATELLITE ALARMS NATO",
     "deck": ("Western intel: Moscow's \u201cSputnik-S\u201d satellite, stored "
              "near Moscow for years, could launch in 60 days, possibly "
              "in December. NATO's Rutte vows to defend every inch, "
              "including space. Kremlin denies it."),
     "icon": "satellite", "tint": (244, 220, 218),
     "source": "Reuters / NDR-WDR-SZ, Nov 23"},
    {"kicker": "SPACE  ·  MERCURY",
     "headline": "BEPICOLOMBO REACHES MERCURY AFTER 8 YEARS",
     "deck": ("ESA/JAXA BepiColombo enters Mercury orbit on 21 Nov 2026 "
              "\u2014 only the second mission ever to do so after NASA's "
              "MESSENGER. Two orbiters separate 9\u201310 Dec; science "
              "begins April 2027."),
     "icon": "planet", "tint": (214, 230, 242),
     "source": "AP / Washington Post"},
    {"kicker": "SPACE  ·  CHINA",
     "headline": "FIRST FOREIGNER ABOARD TIANGONG",
     "deck": ("Shenzhou-24 docks 11:56 on 25 Nov; crew enters Tiangong "
              "the same day. Pakistani payload specialist Muhammad "
              "Zeeshan Ali is the first foreign astronaut on the "
              "station; returns on Shenzhou-23 in 5\u201310 days."),
     "icon": "rocket", "tint": (250, 232, 205),
     "source": "Xinhua / Reuters"},
]

KPIS = [
    ("60 DAYS", "SPUTNIK-S LAUNCH WINDOW"),
    ("8 YRS", "BEPICOLOMBO'S VOYAGE"),
    ("500,000", "RUSSIAN WAR DEAD (OWN FIGURES)"),
    ("+26%", "UK ENERGY BILLS FROM JAN"),
    ("36%", "BANGLADESH WAGE RISE"),
]

REGIONS = [
    ("ASIA", 9, [
        "XI PROBE ENSNARES SHANGHAI CHIEF CHEN",
        "S. KOREA MINISTER QUITS OVER EXAM SCANDAL",
        "AUSTRALIA FORCES PLATFORMS TO REMOVE HARMFUL CONTENT",
        "AUSTRALIA-SOLOMON IS. SECURITY PACT",
        "N. KOREA THREATENS SWISS OFFICE",
        "VIETNAM PUSHES GREEN FARMING",
        "S. KOREA TO BOOST EV INDUSTRY",
        "INDIA SPACE ECONOMY $9BN TO $45BN",
        "IITs ADD 6,000 TECH SEATS",
    ]),
    ("MIDDLE EAST", 6, [
        "IRAN BRACES FOR US BLOCKADE",
        "ISRAEL: IRAN BUILDING CHEMICAL WEAPONS",
        "SWIMMER CROSSES HORMUZ FOR OCEANS",
        "EGYPT: SUEZ REVENUES RECOVERING",
        "ETHIOPIA PUSHES HEALTH INDEPENDENCE",
        "HOUTHI THREAT STILL LOOMS",
    ]),
    ("EUROPE", 8, [
        "EU UNVEILS 22ND RUSSIA SANCTIONS PACKAGE",
        "RUSSIA'S OWN TOLL: NEARLY 500,000 DEAD",
        "FRANCE EYES CRITICAL MINERALS FREEDOM",
        "UK PROBES NUCLEAR TEST LEGACY",
        "POLAND ALARMS OVER AIRSPACE VIOLATIONS",
        "RUSSIA RAISES DEFENCE SPENDING",
        "UKRAINE-HUNGARY SEEK ECONOMIC TIES",
        "EU PLANS \u20ac50BN TECH FUND",
    ]),
    ("AMERICAS", 8, [
        "US CONSUMER CONFIDENCE NEAR 2-YEAR HIGH",
        "CANADA HOLDS INFLATION STRATEGY",
        "PETROBRAS UNVEILS $122BN PLAN",
        "VENEZUELA DEBT: $237.5BN REVEALED",
        "COLOMBIA: 10 YEARS SINCE PEACE DEAL",
        "CARTAGENA HOSTAGES FREED AFTER 17 HRS",
        "US READIES NEW GLOBAL TARIFF PLAN",
        "ABREGO GARCIA LEAVES US FOR SPAIN",
    ]),
    ("AFRICA", 4, [
        "ZIMBABWE ARREST WARRANT FOR MUGABE'S SON",
        "AFRICAN INSURGENTS TURN TO CHEAP DRONES",
        "EGYPT'S SUEZ RECOVERY LIFTS AFRICA TRADE",
        "ETHIOPIA'S HEALTH PUSH DRAWS PRAISE",
    ]),
    ("GLOBAL", 4, [
        "BARBADOS, INDIA PUSH AI GOVERNANCE",
        "UN SEEKS GLOBAL AI SAFETY RULES",
        "REAL MADRID THRASH PSV 5-1",
        "ASTEROID CLOSE-UPS DUE FROM DART FOLLOW-UP",
    ]),
]

DIST = [("ASIA", 9, RED), ("MIDDLE EAST", 6, (214, 110, 30)),
        ("EUROPE", 8, NAVY), ("AMERICAS", 8, (40, 110, 70)),
        ("AFRICA", 4, (120, 70, 140)), ("GLOBAL", 4, GREY)]

# Simplified continent outlines, in a 900x100 map box.
CONTINENTS = [
    [(30, 20), (110, 8), (190, 14), (220, 28), (200, 52), (160, 64),
     (130, 86), (85, 90), (45, 62), (25, 36)],
    [(240, 6), (270, 4), (285, 12), (262, 20), (242, 12)],
    [(200, 66), (240, 62), (270, 70), (260, 92), (232, 96),
     (208, 82)],
    [(420, 14), (460, 8), (490, 16), (480, 32), (450, 36), (430, 28)],
    [(430, 40), (480, 36), (510, 48), (500, 74), (470, 90),
     (442, 78), (426, 56)],
    [(500, 10), (640, 5), (770, 14), (840, 28), (810, 54), (740, 66),
     (670, 60), (590, 52), (530, 34), (500, 22)],
    [(750, 78), (810, 74), (840, 82), (810, 94), (762, 92),
     (742, 86)],
]
# Marker positions are fractions of the 900x100 map box.
MARKERS = [
    (0.42, 0.30, "BERLIN"), (0.56, 0.28, "MOSCOW"),
    (0.64, 0.52, "HORMUZ"), (0.80, 0.34, "JIUQUAN"),
    (0.17, 0.62, "CARTAGENA"), (0.36, 0.22, "MERCURY"),
]

TIMELINE = [
    ("21 NOV", "BEPICOLOMBO ENTERS MERCURY ORBIT"),
    ("00:18 UTC", "SHENZHOU-24 LIFTOFF (25 NOV)"),
    ("03:56 UTC", "SHENZHOU-24 DOCKS TIANGONG"),
]


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([6, 6, W - 7, H - 7], outline=INK, width=2)
    y = 22

    # ---- masthead ----
    # Title is centred left of the DATE CHECK box so the two never touch.
    title_f = font(F_SERIF_B, 38)
    draw_center(d, 460, y, "THE WORLD IN ONE IMAGE", title_f)
    y += 52
    date_f = font(F_SANS_B, 15)
    draw_center(d, W // 2, y, "T H U R S D A Y ,  2 6  N O V E M B E R  2 0 2 6",
                date_f, fill=RED)
    y += 24
    # red DATE CHECK box, top right
    box_w, box_h = 200, 46
    bx0, by0 = W - MARGIN - box_w, 20
    d.rectangle([bx0, by0, bx0 + box_w, by0 + box_h], outline=RED, width=2)
    d.rectangle([bx0, by0, bx0 + box_w, by0 + 20], fill=RED)
    dc_f = font(F_SANS_B, 13)
    draw_center(d, bx0 + box_w // 2, by0 + 3, "DATE CHECK", dc_f, fill=WHITE)
    dc2_f = font(F_SANS_B, 11)
    draw_center(d, bx0 + box_w // 2, by0 + 25, "THU 26 NOV 2026 \u00b7 UTC",
                dc2_f, fill=RED)
    y = rule(d, y, weight=3)
    y += 8

    # ---- KPI bar ----
    kpi_h = 44
    d.rectangle([MARGIN, y, W - MARGIN, y + kpi_h], fill=KPI_FILL,
                outline=INK, width=1)
    cell_w = INNER // 5
    for i, (num, label) in enumerate(KPIS):
        cx = MARGIN + cell_w * i + cell_w // 2
        if i:
            d.line([MARGIN + cell_w * i, y + 6,
                    MARGIN + cell_w * i, y + kpi_h - 6], fill=GREY, width=1)
        d.text((cx - d.textlength(num, font=font(F_SANS_B, 17)) / 2, y + 4),
               num, font=font(F_SANS_B, 17), fill=RED)
        d.text((cx - d.textlength(label, font=font(F_SANS_B, 9)) / 2, y + 26),
               label, font=font(F_SANS_B, 9), fill=BODY)
    y += kpi_h + 10

    # ---- three leads ----
    lead_w = (INNER - 2 * GAP) // 3
    lead_top = y
    icon_h = 74
    for i, lead in enumerate(LEADS):
        x0 = MARGIN + i * (lead_w + GAP)
        d.rectangle([x0, y, x0 + lead_w, y + icon_h], fill=lead["tint"],
                    outline=INK, width=1)
        ICONS[lead["icon"]](d, x0 + lead_w // 2 - 26, y + 10, 52)
        d.text((x0 + 6, y + icon_h - 16), lead["source"],
               font=font(F_SANS, 9), fill=GREY)
        ty = y + icon_h + 8
        d.text((x0, ty), lead["kicker"], font=font(F_SANS_B, 11), fill=RED)
        ty += 16
        head_lines = wrap_text(d, lead["headline"], font(F_SERIF_B, 19),
                               lead_w)
        for line in head_lines:
            d.text((x0, ty), line, font=font(F_SERIF_B, 19), fill=INK)
            ty += 22
        ty += 2
        for line in wrap_text(d, lead["deck"], font(F_SERIF, 12), lead_w):
            d.text((x0, ty), line, font=font(F_SERIF, 12), fill=BODY)
            ty += 15
    # leads block height: icon 74 + kicker 16 + headline ~44 + deck ~75
    y = lead_top + icon_h + 8 + 16 + 44 + 2 + 75 + 6
    y = rule(d, y, weight=1)
    y += 6

    # ---- world map ----
    map_h = 96
    d.text((MARGIN, y), "THE WORLD TODAY", font=font(F_SANS_B, 12), fill=NAVY)
    d.text((W - MARGIN - d.textlength("6 REGIONS \u00b7 39 STORIES + 3 LEADS",
                                      font=font(F_SANS_B, 11)), y),
           "6 REGIONS \u00b7 39 STORIES + 3 LEADS",
           font=font(F_SANS_B, 11), fill=RED)
    y += 18
    map_x0, map_y0 = MARGIN, y
    d.rectangle([map_x0, map_y0, map_x0 + INNER, map_y0 + map_h],
                fill=(232, 238, 244), outline=INK, width=1)
    scale_x = INNER / 900.0
    scale_y = map_h / 100.0
    for poly in CONTINENTS:
        pts = [(map_x0 + px * scale_x, map_y0 + py * scale_y)
               for px, py in poly]
        d.polygon(pts, fill=SEA, outline=SEA_EDGE)
    for fx, fy, name in MARKERS:
        mx = map_x0 + fx * INNER
        my = map_y0 + fy * map_h
        d.ellipse([mx - 4, my - 4, mx + 4, my + 4], fill=RED,
                  outline=WHITE, width=1)
        label_f = font(F_SANS_B, 9)
        lw = d.textlength(name, font=label_f)
        lx = min(max(mx - lw / 2, map_x0 + 2), map_x0 + INNER - lw - 2)
        d.text((lx, my - 16), name, font=label_f, fill=RED)
    y += map_h + 10

    # ---- UTC timeline ----
    d.text((MARGIN, y), "UTC TIMELINE \u2014 KEY EVENTS (21\u201326 NOVEMBER 2026)",
           font=font(F_SANS_B, 12), fill=NAVY)
    y += 18
    # Leave room above the line for the two raised event labels.
    tl_y = y + 30
    d.line([MARGIN, tl_y, W - MARGIN, tl_y], fill=INK, width=2)
    slots = [(0.08, "21 NOV"), (0.5, "25 NOV 00:00"), (0.92, "26 NOV 00:00")]
    for frac, lab in slots:
        tx = MARGIN + frac * INNER
        d.line([tx, tl_y - 4, tx, tl_y + 4], fill=INK, width=1)
        d.text((tx - d.textlength(lab, font=font(F_SANS, 9)) / 2, tl_y + 8),
               lab, font=font(F_SANS, 9), fill=GREY)
    events = [(0.10, 0), (0.46, 1), (0.82, 2)]
    for frac, idx in events:
        ex = MARGIN + frac * INNER
        d.ellipse([ex - 4, tl_y - 4, ex + 4, tl_y + 4], fill=RED)
        lab = TIMELINE[idx][0] + " \u2014 " + TIMELINE[idx][1]
        lab_f = font(F_SANS_B, 9)
        lw = d.textlength(lab, font=lab_f)
        lx = min(max(ex - lw / 2, MARGIN), W - MARGIN - lw)
        # stagger: first and third above, middle below
        ly = tl_y - 26 if idx != 1 else tl_y + 22
        d.text((lx, ly), lab, font=lab_f, fill=RED)
    y = tl_y + 40

    # ---- region grid ----
    col_w = (INNER - 2 * GAP) // 3
    rows = [REGIONS[0:3], REGIONS[3:6]]
    for r, row in enumerate(rows):
        row_h = 0
        for c, (name, count, items) in enumerate(row):
            x0 = MARGIN + c * (col_w + GAP)
            hdr_h = 20
            d.rectangle([x0, y, x0 + col_w, y + hdr_h], fill=NAVY)
            d.text((x0 + 6, y + 4), name, font=font(F_SANS_B, 11),
                   fill=WHITE)
            cnt = f"{count} STORIES"
            d.text((x0 + col_w - 6 - d.textlength(cnt, font=font(F_SANS_B, 10)),
                    y + 4), cnt, font=font(F_SANS_B, 10), fill=WHITE)
            iy = y + hdr_h + 4
            for item in items:
                lines = wrap_text(d, item, font(F_SANS, 10), col_w - 4)
                for line in lines:
                    d.text((x0 + 2, iy), line, font=font(F_SANS, 10),
                           fill=BODY)
                    iy += 13
            row_h = max(row_h, iy - y)
        y += row_h + 8
    y += 2

    # ---- distribution bar ----
    d.text((MARGIN, y), "STORIES BY REGION (39 GRID STORIES)",
           font=font(F_SANS_B, 11), fill=NAVY)
    y += 16
    bar_h = 16
    total = sum(n for _, n, _ in DIST)
    bx = MARGIN
    for name, n, color in DIST:
        seg = INNER * n // total
        d.rectangle([bx, y, bx + seg - 1, y + bar_h], fill=color)
        lab = str(n)
        d.text((bx + seg // 2 - d.textlength(lab, font=font(F_SANS_B, 10)) / 2,
                y + 2), lab, font=font(F_SANS_B, 10), fill=WHITE)
        bx += seg
    y += bar_h + 6
    lx = MARGIN
    for name, n, color in DIST:
        d.rectangle([lx, y, lx + 10, y + 10], fill=color)
        lab = f"{name} {n}"
        d.text((lx + 13, y), lab, font=font(F_SANS_B, 9), fill=BODY)
        lx += 13 + d.textlength(lab, font=font(F_SANS_B, 9)) + 14
    y += 18

    # ---- footer ----
    y = rule(d, y, weight=1)
    y += 6
    foot_f = font(F_SANS, 10)
    draw_center(d, W // 2, y,
                "Sources: Reuters \u00b7 AP \u00b7 Xinhua \u00b7 NYT \u00b7 CNN "
                "\u00b7 SCMP \u00b7 Washington Post", foot_f, fill=GREY)
    y += 14
    draw_center(d, W // 2, y,
                "Compiled from the day's reporting  \u00b7  Thursday 26 November 2026",
                foot_f, fill=GREY)

    img.save("entry.png")
    print("saved entry.png (1024, 1024)")


if __name__ == "__main__":
    build()
