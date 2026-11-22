#!/usr/bin/env python3
"""Render 'The World Today' front page for 22 November 2026 (news-image-20261122).

Deterministic: no randomness, no timestamps, no network. All text is drawn
with PIL + DejaVu so no generated image carries text that could be garbled.
Reads the four panel images from ../ni22-assets/ (outside the repo) and
writes entry.png (1024x1024) next to this script.
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.abspath(os.path.join(HERE, "..", "..", "ni22-assets"))

CREAM = (247, 243, 234)
NAVY = (20, 33, 61)
GOLD = (201, 162, 39)
BLACK = (20, 20, 20)
GREY = (90, 90, 90)
MAROON = (128, 30, 30)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


BOLD = lambda s: font("DejaVuSans-Bold.ttf", s)      # noqa: E731
REG = lambda s: font("DejaVuSans.ttf", s)            # noqa: E731


def center_crop(im, tw, th):
    """Crop image to the target aspect ratio, centred, then resize."""
    w, h = im.size
    ta = tw / th
    a = w / h
    if a > ta:  # too wide: trim sides
        nw = int(h * ta)
        x0 = (w - nw) // 2
        im = im.crop((x0, 0, x0 + nw, h))
    else:       # too tall: trim top/bottom
        nh = int(w / ta)
        y0 = (h - nh) // 2
        im = im.crop((0, y0, w, y0 + nh))
    return im.resize((tw, th), Image.LANCZOS)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap to a pixel width; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_centered(draw, cx, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size


def main():
    img = Image.new("RGB", (1024, 1024), CREAM)
    d = ImageDraw.Draw(img)

    # ---- Masthead y0-112, navy band ----
    d.rectangle([0, 0, 1024, 112], fill=NAVY)
    draw_centered(d, 512, 22, "THE WORLD TODAY", BOLD(62), (255, 255, 255))
    draw_centered(d, 512, 82, "SUNDAY, 22 NOVEMBER 2026", BOLD(26), GOLD)
    d.line([(0, 110), (1024, 110)], fill=GOLD, width=2)

    # ---- Lead y122-560: tanker photo 1024x300 ----
    lead = Image.open(os.path.join(
        ASSETS, "media-generation-gulf-tanker-fire-0-1f721f82-b81b-43b4-9578-a240d8d0e654.webp"))
    lead = center_crop(lead.convert("RGB"), 1024, 300)
    img.paste(lead, (0, 122))
    draw_centered(d, 512, 432, "GULF IN FLAMES", BOLD(46), BLACK)
    draw_centered(d, 512, 488, "Iran hits Bahrain and US bases; tankers burn near Hormuz",
                  REG(25), BLACK)
    d.line([(16, 552), (1008, 552)], fill=GREY, width=1)

    # ---- Secondary y570-840, three columns ----
    cols = [
        ("media-generation-cop31-summit-hall-0-98e72095-d58a-41f2-a343-159af7542f18.webp",
         "COP31 IN OVERTIME",
         "Antalya talks stall on fossil fuels and funding",
         "cop31"),
        ("media-generation-riyadh-interception-0-02fa306f-e6b2-4ada-a872-89ab6778d537.webp",
         "MISSILES OVER RIYADH",
         "Saudi defences stop Houthi strike on the capital",
         "plain"),
        ("media-generation-baltic-ship-fire-0-6868ffeb-9261-4891-8139-87efbd1a3c79.webp",
         "SHIP ABLAZE IN THE BALTIC",
         "Russian cargo ship hit; crew evacuated",
         "plain"),
    ]
    xs = [16, 352, 688]
    for x, (fname, head, cap, kind) in zip(xs, cols):
        im = Image.open(os.path.join(ASSETS, fname)).convert("RGB")
        if kind == "cop31":
            # DEFECT FIX: the source image's screen reads "CLIMATE SUMMIT 2025 -
            # COP30 / NOV 2025" (wrong year/event). Keep only the delegates band
            # (bottom ~52%), which shows nameplates and no screen.
            w, h = im.size
            im = im.crop((0, int(h * 0.48), w, h))
        im = center_crop(im, 320, 150)
        img.paste(im, (x, 570))
        y = 728
        for line in wrap(d, head, BOLD(22), 320)[:2]:
            d.text((x, y), line, font=BOLD(22), fill=BLACK)
            y += 27
        y = max(y, 782)
        for line in wrap(d, cap, REG(19), 320)[:2]:
            d.text((x, y), line, font=REG(19), fill=BLACK)
            y += 23

    d.line([(16, 848), (1008, 848)], fill=GREY, width=1)

    # ---- In brief y850-1000 ----
    d.text((16, 858), "IN BRIEF", font=BOLD(20), fill=MAROON)
    briefs = [
        "Peru quake 6.7 injures 15 in the Andes",
        "Florida floods break a 73-year record",
        "S&P's worst week since April; Fed hike looms",
    ]
    y = 890
    for b in briefs:
        d.text((16, y), "\u2022  " + b, font=REG(20), fill=BLACK)
        y += 32

    # ---- Footer ----
    d.line([(16, 996), (1008, 996)], fill=GREY, width=1)
    draw_centered(d, 512, 1004, "The World Today \u2014 22 November 2026",
                  REG(14), GREY)

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
