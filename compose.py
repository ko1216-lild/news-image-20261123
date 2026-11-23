#!/usr/bin/env python3
"""Compose the news poster for Monday 23 November 2026.

Builds a front-page style poster, 1024x1024, out of Pillow drawing
primitives and saves it as entry.png next to this file. The drawing uses
no randomness, clocks or external data, so every run writes the same
bytes.

Stories (all reported under 23 November 2026 datelines):
- Hero: Bahrain demands UN action after an Iranian attack on a civilian
  facility (Arab News front page, Monday 23 November 2026).
- Indonesia factory fire, three dead and 36 missing (AFP via The Manila
  Times, 23 November 2026).
- South Korea's education chief quits amid AI cheating (AFP via The
  Manila Times, 23 November 2026).
- Kim Jong Un: North Korea seeks security, not supremacy (Philippine
  Daily Inquirer, 23 November 2026).
- Myanmar to eliminate graft in military recruitment (The Manila Times,
  23 November 2026).
- China slams US ban on telecom companies (The Manila Times,
  23 November 2026).
- Thousands protest closure of pro-opposition Turkish media outlets
  (Philippine Daily Inquirer, 23 November 2026).
"""
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
PAPER = (247, 243, 233)
PANEL_BG = (253, 251, 245)
INK = (18, 20, 24)
BODY = (50, 52, 56)
RULE = (188, 180, 162)
RED = (178, 30, 43)
BLUE = (28, 76, 136)
GOLD = (172, 128, 24)
GREEN = (32, 106, 60)
GREY = (100, 100, 100)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split():
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


def centered(d, cx, y, text, fnt, fill=INK):
    d.text((cx - d.textlength(text, font=fnt) / 2, y), text, font=fnt, fill=fill)


def star(d, cx, cy, r_out, r_in, points, fill):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = -math.pi / 2 + i * math.pi / points
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=fill)


# --- panel icons (drawn around a centre point) ---

def icon_flame(d, cx, cy):
    d.polygon([(cx, cy - 26), (cx + 10, cy - 4), (cx + 15, cy + 9),
               (cx + 9, cy + 22), (cx - 9, cy + 22), (cx - 15, cy + 9),
               (cx - 10, cy - 4)], fill=RED)
    d.polygon([(cx, cy - 7), (cx + 6, cy + 6), (cx + 7, cy + 15),
               (cx + 4, cy + 22), (cx - 4, cy + 22), (cx - 7, cy + 15),
               (cx - 6, cy + 6)], fill=GOLD)
    d.rectangle([cx - 20, cy + 24, cx + 20, cy + 28], fill=INK)


def icon_book(d, cx, cy):
    d.polygon([(cx, cy - 22), (cx - 30, cy - 28), (cx - 30, cy + 24),
               (cx, cy + 18)], fill=BLUE)
    d.polygon([(cx, cy - 22), (cx + 30, cy - 28), (cx + 30, cy + 24),
               (cx, cy + 18)], fill=(70, 120, 180))
    d.line([(cx, cy - 22), (cx, cy + 18)], fill=INK, width=3)
    for dy in (-12, 0, 12):
        d.line([(cx - 24, cy + dy - 4), (cx - 5, cy + dy - 8)], fill=(230, 236, 244), width=3)
        d.line([(cx + 5, cy + dy - 8), (cx + 24, cy + dy - 4)], fill=(230, 236, 244), width=3)
    star(d, cx, cy - 34, 9, 4, 5, GOLD)


def icon_star_badge(d, cx, cy):
    d.ellipse([cx - 27, cy - 27, cx + 27, cy + 27], outline=RED, width=4)
    star(d, cx, cy, 19, 8, 5, RED)


def icon_shield(d, cx, cy):
    d.polygon([(cx, cy - 30), (cx + 24, cy - 20), (cx + 24, cy + 6),
               (cx + 14, cy + 24), (cx, cy + 32), (cx - 14, cy + 24),
               (cx - 24, cy + 6), (cx - 24, cy - 20)], outline=GREEN, width=4)
    d.line([(cx - 11, cy + 2), (cx - 3, cy + 11), (cx + 13, cy - 9)],
           fill=GREEN, width=5, joint="curve")


def icon_tower(d, cx, cy):
    d.line([(cx - 16, cy + 32), (cx, cy - 26), (cx + 16, cy + 32)], fill=INK, width=4)
    d.line([(cx - 10, cy + 10), (cx + 10, cy + 10)], fill=INK, width=3)
    d.line([(cx - 13, cy + 21), (cx + 13, cy + 21)], fill=INK, width=3)
    for r in (10, 18, 26):
        d.arc([cx - r, cy - 26 - r, cx + r, cy - 26 + r], -60, 60, fill=RED, width=3)
        d.arc([cx - r, cy - 26 - r, cx + r, cy - 26 + r], 120, 240, fill=RED, width=3)
    d.ellipse([cx - 4, cy - 30, cx + 4, cy - 22], fill=RED)


def icon_megaphone(d, cx, cy):
    d.polygon([(cx - 26, cy - 8), (cx + 16, cy - 24), (cx + 16, cy + 24),
               (cx - 26, cy + 8)], fill=GOLD)
    d.rectangle([cx - 30, cy - 9, cx - 24, cy + 9], fill=INK)
    d.line([(cx - 14, cy + 8), (cx - 8, cy + 28)], fill=INK, width=5)
    d.line([(cx + 24, cy - 12), (cx + 32, cy - 18)], fill=RED, width=3)
    d.line([(cx + 26, cy), (cx + 35, cy)], fill=RED, width=3)
    d.line([(cx + 24, cy + 12), (cx + 32, cy + 18)], fill=RED, width=3)


def icon_skyline_burst(d, x, y, w, h):
    base = y + h
    towers = [(0.02, 0.52), (0.14, 0.78), (0.27, 0.60), (0.38, 0.88),
              (0.52, 0.66), (0.63, 0.80), (0.76, 0.55), (0.87, 0.72)]
    for fx, fh in towers:
        tx = x + w * fx
        tw = w * 0.11
        d.rectangle([tx, base - h * fh, tx + tw, base], fill=(64, 70, 82))
        for wy in range(3):
            for wx in range(2):
                d.rectangle([tx + 6 + wx * (tw / 2), base - h * fh + 8 + wy * 16,
                             tx + 6 + wx * (tw / 2) + 7, base - h * fh + 16 + wy * 16],
                            fill=(240, 214, 120))
    star(d, x + w * 0.44, y + h * 0.16, 34, 14, 10, RED)
    star(d, x + w * 0.44, y + h * 0.16, 17, 7, 10, GOLD)
    d.line([(x, base), (x + w, base)], fill=INK, width=3)


def panel(d, x, y, w, h, place, color, headline, body, icon):
    d.rectangle([x, y, x + w, y + h], fill=PANEL_BG, outline=INK, width=2)
    d.rectangle([x, y, x + w, y + 8], fill=color)
    icon(d, x + 38, y + 48)
    d.text((x + 82, y + 28), place, font=F(SANS_B, 19), fill=color)
    hy = y + 78
    for line in wrap(d, headline, F(SERIF_B, 23), w - 24):
        d.text((x + 12, hy), line, font=F(SERIF_B, 23), fill=INK)
        hy += 28
    d.line([(x + 12, hy + 1), (x + w - 12, hy + 1)], fill=RULE, width=2)
    by = hy + 9
    for line in wrap(d, body, F(SANS, 16), w - 24):
        d.text((x + 12, by), line, font=F(SANS, 16), fill=BODY)
        by += 21


def main():
    img = Image.new("RGB", (SIZE, SIZE), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    d.line([(36, 26), (988, 26)], fill=INK, width=3)
    centered(d, 512, 38, "THE WORLD IN A DAY", F(SERIF_B, 62))
    d.line([(36, 116), (988, 116)], fill=INK, width=3)
    d.rectangle([36, 126, 988, 168], fill=INK)
    centered(d, 512, 133, "MONDAY · 23 NOVEMBER 2026", F(SANS_B, 30),
             fill=(255, 255, 255))

    # Hero: Bahrain / Iran
    hx, hy, hw, hh = 36, 184, 952, 308
    d.rectangle([hx, hy, hx + hw, hy + hh], fill=PANEL_BG, outline=INK, width=3)
    d.rectangle([hx, hy, hx + hw, hy + 10], fill=RED)
    d.text((hx + 20, hy + 22), "MIDDLE EAST", font=F(SANS_B, 20), fill=RED)
    d.text((hx + 20, hy + 48), "BAHRAIN DEMANDS UN ACTION", font=F(SERIF_B, 47), fill=INK)
    d.text((hx + 20, hy + 102), "AFTER IRAN ATTACK", font=F(SERIF_B, 47), fill=INK)
    icon_skyline_burst(d, hx + 24, hy + 168, 430, 104)
    sx = hx + 500
    sy = hy + 162
    for line in wrap(d, "Iran strikes a civilian facility in Bahrain. Manama demands "
                        "UN action, Saudi Arabia declares solidarity, and Houthi "
                        "drones are intercepted over the Gulf.",
                     F(SANS, 18), 420):
        d.text((sx, sy), line, font=F(SANS, 18), fill=BODY)
        sy += 25

    # Panels
    pw, gap = 309, 12
    xs = [36, 36 + pw + gap, 36 + 2 * (pw + gap)]
    row1 = [
        ("INDONESIA", RED, "FACTORY FIRE KILLS THREE, 36 MISSING",
         "Blaze at a confectionery factory in Serang, Banten; rescuers "
         "search the ruins for the missing.", icon_flame),
        ("SOUTH KOREA", BLUE, "EDUCATION CHIEF QUITS OVER AI CHEATING",
         "Minister resigns amid an AI cheating scandal over admission "
         "tests.", icon_book),
        ("NORTH KOREA", GOLD, "KIM: SECURITY, NOT SUPREMACY",
         "Kim Jong Un says his country seeks security, not supremacy.",
         icon_star_badge),
    ]
    row2 = [
        ("MYANMAR", GREEN, "JUNTA VOWS TO END RECRUITMENT GRAFT",
         "The military says it will eliminate graft in its recruitment "
         "of soldiers.", icon_shield),
        ("CHINA - U.S.", RED, "BEIJING SLAMS U.S. TELECOM BAN",
         "China condemns Washington's ban on Chinese telecom companies.",
         icon_tower),
        ("TURKEY", BLUE, "THOUSANDS PROTEST MEDIA CLOSURES",
         "Crowds rally against the closure of pro-opposition Turkish "
         "media outlets.", icon_megaphone),
    ]
    for x, args in zip(xs, row1):
        panel(d, x, 504, pw, 216, *args)
    for x, args in zip(xs, row2):
        panel(d, x, 732, pw, 216, *args)

    # Footer ticker
    d.rectangle([36, 964, 988, 1000], fill=INK)
    centered(d, 512, 973,
             "ALSO: Saudi crown prince meets Bulgaria's PM  ·  "
             "Lebanon holds 3 with 264 kg of explosives  ·  Trump meme-coin gala",
             F(SANS_B, 16), fill=(255, 255, 255))

    out = Path(__file__).with_name("entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, out.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
