#!/usr/bin/env python3
"""Render the 17 November 2026 world-news front page to entry.png.

Run locally (needs Pillow + DejaVu fonts, both present on the build box):
    python3 render.py
Writes entry.png (1024x1024, < 1 MiB) next to this file.
The entry program main.py only copies that PNG to /output/entry.png,
so the graded run is deterministic and needs no network.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (20, 20, 20)
RED = (179, 38, 30)
NAVY = (27, 58, 92)
TEAL = (14, 107, 107)
GOLD = (176, 124, 22)
GREY = (90, 86, 78)
CARD = (255, 253, 247)
RULE = (200, 192, 172)

F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to pixel width; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, xy, text, fnt, fill, width, leading=None):
    x, y = xy
    leading = leading or int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def chip(draw, xy, text, fnt, bg, fg):
    x, y = xy
    pad_x, pad_y = 10, 5
    w = int(draw.textlength(text, font=fnt)) + 2 * pad_x
    h = fnt.size + 2 * pad_y
    draw.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, fill=bg)
    draw.text((x + pad_x, y + pad_y - 1), text, font=fnt, fill=fg)
    return x + w


def draw_tanker_scene(draw, box):
    """Simple Gulf scene: dusk sea, tanker, smoke plume, drone dots."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(23, 52, 84))
    # sun / glow, top-left of the scene
    draw.ellipse([x0 + 18, y0 + 16, x0 + 66, y0 + 64], fill=(232, 164, 62))
    # sea
    draw.rectangle([x0, y0 + 150, x1, y1], fill=(16, 42, 66))
    for i, yy in enumerate(range(y0 + 158, y1 - 6, 14)):
        draw.line([x0 + 12 + (i % 3) * 30, yy, x0 + 70 + (i % 3) * 30, yy],
                  fill=(52, 96, 128), width=2)
    # tanker hull + containers
    draw.rectangle([x0 + 24, y0 + 118, x0 + 250, y0 + 150], fill=(40, 40, 40))
    draw.rectangle([x0 + 24, y0 + 118, x0 + 250, y0 + 128], fill=(179, 38, 30))
    for i, c in enumerate([(232, 164, 62), (14, 107, 107), (200, 200, 190)]):
        draw.rectangle([x0 + 40 + i * 52, y0 + 92, x0 + 84 + i * 52, y0 + 118],
                       fill=c)
    draw.rectangle([x0 + 208, y0 + 84, x0 + 244, y0 + 118], fill=(230, 230, 220))
    # smoke plume from a stricken tanker, far right
    for cx, cy, r in [(x1 - 108, y0 + 92, 22), (x1 - 84, y0 + 66, 28),
                      (x1 - 58, y0 + 44, 20)]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 116, 108))
    draw.ellipse([x1 - 116, y0 + 104, x1 - 82, y0 + 128], fill=(232, 120, 40))
    # drone dots
    for dx, dy in [(x0 + 110, y0 + 30), (x0 + 142, y0 + 46), (x0 + 178, y0 + 28)]:
        draw.ellipse([dx - 4, dy - 4, dx + 4, dy + 4], fill=(255, 255, 255))
        draw.line([dx - 9, dy, dx + 9, dy], fill=(255, 255, 255), width=1)
        draw.line([dx, dy - 9, dx, dy + 9], fill=(255, 255, 255), width=1)


def story_card(draw, box, accent, kicker, headline, body, stat=None,
               hsize=25, bsize=18):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=10, fill=CARD, outline=RULE, width=1)
    draw.rounded_rectangle([x0, y0, x1, y0 + 8], radius=4, fill=accent)
    draw.rectangle([x0, y0 + 4, x1, y0 + 8], fill=accent)
    x, y = x0 + 18, y0 + 22
    draw.text((x, y), kicker, font=font(F_BOLD, 16), fill=accent)
    y += 28
    y = para(draw, (x, y), headline, font(F_BOLD, hsize), INK, x1 - x0 - 36,
             leading=hsize + 5)
    y += 5
    y = para(draw, (x, y), body, font(F_SANS, bsize), (60, 58, 52),
             x1 - x0 - 36, leading=bsize + 5)
    if stat and y + 26 <= y1 - 8:
        draw.text((x, y + 4), stat, font=font(F_BOLD, 17), fill=accent)
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 28  # margin

    # ---- masthead ----
    d.line([M, 30, W - M, 30], fill=INK, width=3)
    d.text((M, 42), "T H E   W O R L D   I N   O N E   P A G E",
           font=font(F_BOLD, 20), fill=RED)
    d.text((W - M - d.textlength("No. 321  •  17 NOV 2026", font=font(F_BOLD, 20)),
            42), "No. 321  •  17 NOV 2026", font=font(F_BOLD, 20), fill=GREY)
    d.text((M, 68), "Tuesday, 17 November 2026",
           font=font(F_SERIF, 46), fill=INK)
    d.text((M, 122),
           "The day's world news in one picture — every story below happened "
           "or broke on 17 November 2026.",
           font=font(F_SANS, 19), fill=GREY)
    d.line([M, 152, W - M, 152], fill=INK, width=2)

    # ---- lead story: Gulf / US-Iran ----
    L0, L1 = 166, 478
    d.rounded_rectangle([M, L0, W - M, L1], radius=12, fill=NAVY)
    draw_tanker_scene(d, (W - 330, L0 + 14, W - M - 14, L1 - 14))
    lx = M + 22
    lead_w = W - 330 - lx - 24
    d.text((lx, L0 + 16), "LEAD  •  THE GULF  •  WAR AT SEA",
           font=font(F_BOLD, 19), fill=(232, 164, 62))
    d.text((lx, L0 + 48), "GULF ON THE BRINK",
           font=font(F_BOLD, 50), fill=(255, 255, 255))
    y = para(d, (lx, L0 + 122),
             "Iranian drones strike a U.S. radar site in Bahrain — "
             "intercepted, no damage. Hours later U.S. jets hit a "
             "missile site on Iran's Qeshm Island.",
             font(F_SANS, 20), (225, 232, 240), lead_w, leading=26)
    y = para(d, (lx, y + 8),
             "A fourth tanker is mined in the Strait of Hormuz in 24 hours — "
             "1 crew missing, 11 hurt.",
             font(F_BOLD, 20), (255, 255, 255), lead_w, leading=26)
    cx = lx
    cx = chip(d, (cx, L1 - 44), "4 TANKERS HIT IN 24 H", font(F_BOLD, 16),
              (179, 38, 30), (255, 255, 255)) + 10
    cx = chip(d, (cx, L1 - 44), "BRENT $91.62", font(F_BOLD, 16),
              (255, 255, 255), NAVY)

    # ---- middle row: Ukraine / Gaza / Summit ----
    R0, R1 = 494, 744
    cw = (W - 2 * M - 2 * 16) // 3
    story_card(d, (M, R0, M + cw, R1), RED, "UKRAINE  •  WAR",
               "Strike on Zaporizhzhia kills 40",
               "Russia hits a city and an aid centre; Kyiv hits back — "
               "the Kerch bridge to Crimea is shut.",
               stat="40 KILLED")
    story_card(d, (M + cw + 16, R0, M + 2 * cw + 16, R1), TEAL,
               "GAZA  •  AID",
               "West urges Israel: open the crossings",
               "UK, Australia, Canada and Italy call it catastrophic; "
               "the UN warns of a winter emergency.",
               stat="1.7M STILL DISPLACED")
    story_card(d, (M + 2 * cw + 32, R0, W - M, R1), GOLD,
               "SHENZHEN  •  SUMMIT",
               "Trump, Xi & Putin to meet Thursday",
               "A first-ever trilateral of the U.S., Chinese and Russian "
               "leaders, at APEC in Shenzhen.",
               stat="THU 19 NOV")

    # ---- bottom row: COP31 / France / Japan ----
    B0, B1 = 756, 940
    story_card(d, (M, B0, M + cw, B1), (46, 110, 46), "CLIMATE  •  COP31",
               "COP31: quit fossil fuels faster",
               "Antalya draft seeks $120bn a year in climate finance by 2035.",
               stat=None, hsize=22, bsize=17)
    story_card(d, (M + cw + 16, B0, M + 2 * cw + 16, B1), (110, 60, 140),
               "FRANCE  •  COURT",
               "Depardieu pleads guilty",
               "The French film star admits a sexual assault charge "
               "in a Paris court.",
               stat=None, hsize=22, bsize=17)
    story_card(d, (M + 2 * cw + 32, B0, W - M, B1), (120, 70, 20),
               "JAPAN  •  AIRSPACE",
               "Jets scrambled over Russian planes",
               "Tokyo protests after two Russian aircraft "
               "violate its airspace.",
               stat=None, hsize=22, bsize=17)

    # ---- footer ticker ----
    d.line([M, 952, W - M, 952], fill=INK, width=2)
    d.text((M, 962),
           "ALSO:  Houthis advance in Yemen  •  U.S. loses measles-free "
           "status  •  India edge Pakistan in U19 Asia Cup final",
           font=font(F_SANS, 16), fill=GREY)
    d.text((M, 986),
           "Sources: Reuters, Al Jazeera, AFP  •  All events 17 November 2026",
           font=font(F_SANS, 15), fill=GREY)

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
