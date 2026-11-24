#!/usr/bin/env python3
"""Build the pixel-art newspaper front page for Tuesday 24 November 2026.

Draws on a logical 512x512 grid with the Fusion Pixel Font 12px
(TakWolf/fusion-pixel-font, SIL OFL 1.1) at whole multiples of its
12px design size (12 / 24 / 36), then upscales x2 with NEAREST
neighbour to 1024x1024 and writes entry.png next to this script.

The font file lives OUTSIDE the repo (build-time only); pass its path
with the FUSION_FONT environment variable if it is not at the default.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = os.environ.get(
    "FUSION_FONT",
    "/tmp/fusionpixel/fusion-pixel-12px-proportional-latin.ttf",
)

W, H = 512, 512
MARGIN = 16
CONTENT_W = W - 2 * MARGIN  # 480

PAPER = (246, 241, 229)
INK = (20, 20, 20)
GREY = (90, 86, 76)
GREEN_DARK = (13, 43, 26)
GREEN = (23, 201, 100)
GREEN_DIM = (46, 160, 102)
RED = (178, 35, 27)
WHITE = (255, 255, 255)


def font(size):
    return ImageFont.truetype(FONT_PATH, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lead_visual(draw):
    """Pixel-art stock-chart strip for the lead story (Nvidia's leap)."""
    x0, y0, x1, y1 = MARGIN, 89, W - MARGIN, 145
    draw.rectangle([x0, y0, x1, y1], fill=GREEN_DARK)
    # dotted grid
    for gx in range(x0 + 8, x1, 16):
        for gy in range(y0 + 6, y1, 14):
            draw.point((gx, gy), fill=(28, 84, 54))
    # chip, left side
    cx, cy = x0 + 14, y0 + 12
    draw.rectangle([cx, cy, cx + 30, cy + 30], fill=(8, 26, 16),
                   outline=GREEN, width=2)
    for px in (cx + 6, cx + 15, cx + 24):
        draw.line([px, cy - 5, px, cy], fill=GREEN, width=2)
        draw.line([px, cy + 30, px, cy + 35], fill=GREEN, width=2)
    for py in (cy + 6, cy + 15, cy + 24):
        draw.line([cx - 5, py, cx, py], fill=GREEN, width=2)
        draw.line([cx + 30, py, cx + 35, py], fill=GREEN, width=2)
    draw.rectangle([cx + 9, cy + 9, cx + 21, cy + 21], fill=GREEN)
    draw.text((cx + 12, cy + 11), "N", font=font(12), fill=GREEN_DARK)
    # rising chart line
    pts = [(x0 + 62, y1 - 10), (x0 + 110, y1 - 26), (x0 + 150, y1 - 18),
           (x0 + 195, y1 - 34), (x0 + 240, y1 - 26), (x0 + 285, y1 - 44)]
    draw.line(pts, fill=GREEN, width=3, joint="curve")
    # arrowhead at the top of the climb
    ax, ay = pts[-1]
    draw.polygon([(ax, ay - 8), (ax + 10, ay + 2), (ax - 2, ay + 6)],
                 fill=GREEN)
    # labels, right side
    draw.text((x0 + 300, y0 + 6), "NVDA +~30%", font=font(24),
              fill=WHITE)
    draw.text((x0 + 300, y0 + 34), "NASDAQ +~6%", font=font(12),
              fill=(170, 230, 195))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # page frame
    d.rectangle([3, 3, W - 4, H - 4], outline=INK, width=2)

    # ---- masthead ----
    f36 = font(36)
    mast = "THE WORLD IN ONE DAY"
    d.text(((W - d.textlength(mast, font=f36)) / 2, 8), mast,
           font=f36, fill=INK)
    d.line([MARGIN, 50, W - MARGIN, 50], fill=INK, width=2)
    d.line([MARGIN, 54, W - MARGIN, 54], fill=INK, width=1)

    # ---- date band ----
    d.rectangle([MARGIN, 59, W - MARGIN, 85], fill=INK)
    f24 = font(24)
    date = "TUESDAY · 24 NOVEMBER 2026"
    d.text(((W - d.textlength(date, font=f24)) / 2, 61), date,
           font=f24, fill=WHITE)

    # ---- lead visual + lead story ----
    draw_lead_visual(d)

    f12 = font(12)
    lead_head = "HUANG IS BACK AT NVIDIA"
    d.text((MARGIN, 151), lead_head, font=f24, fill=INK)
    lead_deck = ("The board reinstated Jensen Huang ~11 days after he "
                 "resigned, under pressure from the Trump administration. "
                 "Nvidia shares leapt ~30%; the Nasdaq jumped ~6%.")
    y = 179
    for line in wrap(d, lead_deck, f12, CONTENT_W):
        d.text((MARGIN, y), line, font=f12, fill=INK)
        y += 15

    d.line([MARGIN, 213, W - MARGIN, 213], fill=INK, width=1)

    stories = [
        # Decks are each a single 12px line (must fit CONTENT_W); the
        # loop below asserts this so a wrap can never push the last
        # story into the ticker strip.
        ("KYIV: WE SANK TWO SHIPS",
         "Kyiv: its drones sank the corvette Merkury and hit the arms ship Angara."),
        ("RUSSIA WARNS ESTONIA",
         "Moscow: Tallinn's border closure brings both sides to the verge of open war."),
        ("NUCLEAR SATELLITE WARNING",
         "Allies warned of a Russian nuclear-armed satellite launch next month."),
        ("WORLD CUP 2031 HOSTS NAMED",
         "USA, Mexico, Costa Rica and Jamaica host 2031; the UK stages 2035."),
        ("GAZA STRIKES KILL THREE",
         "Israeli airstrikes killed at least three in Gaza, including a UNRWA worker."),
    ]
    y = 221
    for head, deck in stories:
        d.text((MARGIN, y), head, font=f24, fill=INK)
        y += 27
        lines = wrap(d, deck, f12, CONTENT_W)
        assert len(lines) == 1, f"deck wrapped to {len(lines)} lines: {deck!r}"
        d.text((MARGIN, y), lines[0], font=f12, fill=INK)
        y += 15
        y += 7  # gap between stories
    assert y <= 468, f"stories end at y={y}, colliding with the ticker"

    # ---- ticker ----
    d.line([MARGIN, 470, W - MARGIN, 470], fill=INK, width=2)
    tick1 = ("Trump halted Iowa plant detonation  •  "
             "Anthropic launched Claude Ship code tools")
    tick2 = ("5.6 quake hit Nepal near China border  •  "
             "N. Korean jet 'breached S. Korea airspace'")
    d.text((MARGIN, 476), tick1, font=f12, fill=INK)
    d.text((MARGIN, 491), tick2, font=f12, fill=INK)

    big = img.resize((1024, 1024), Image.NEAREST)
    out = os.path.join(HERE, "entry.png")
    big.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
