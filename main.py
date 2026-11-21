#!/usr/bin/env python3
"""News image entry: sum up Saturday 21 November 2026 in one image.

Draws a newspaper front page (1024x1024 PNG) with pure Python stdlib:
a masthead naming the day, one lead story, four illustrated story
panels and a ticker strip with three more stories. No network, no
external files, no randomness: two runs write byte-identical output.

Output: $MAKEFUN_OUTPUT_DIR/entry.png, or /output/entry.png.
"""

import math
import os
import struct
import zlib

WIDTH = 1024
HEIGHT = 1024

# ---------------------------------------------------------------- palette
PAPER = (247, 243, 232)
INK = (26, 26, 26)
WHITE = (255, 255, 255)
NAVY = (22, 38, 76)
RED = (176, 58, 46)
GOLD = (212, 175, 55)
DARK_LINE = (60, 60, 60)
TEAL = (31, 111, 107)
BROWN = (138, 90, 0)
BLUE_UA = (0, 87, 184)
YELLOW_UA = (255, 213, 0)
RED_PL = (220, 20, 60)
BLUE_EU = (0, 51, 153)
BLUE_UK = (1, 33, 105)
RED_UK = (200, 16, 46)
GREEN = (34, 120, 60)

# ------------------------------------------------------------- 5x7 font
# Each glyph: 7 rows, 5 bits each, most significant bit on the left.
FONT = {
    "A": (0b01110, 0b10001, 0b10001, 0b11111, 0b10001, 0b10001, 0b10001),
    "B": (0b11110, 0b10001, 0b10001, 0b11110, 0b10001, 0b10001, 0b11110),
    "C": (0b01110, 0b10001, 0b10000, 0b10000, 0b10000, 0b10001, 0b01110),
    "D": (0b11110, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b11110),
    "E": (0b11111, 0b10000, 0b10000, 0b11110, 0b10000, 0b10000, 0b11111),
    "F": (0b11111, 0b10000, 0b10000, 0b11110, 0b10000, 0b10000, 0b10000),
    "G": (0b01110, 0b10001, 0b10000, 0b10111, 0b10001, 0b10001, 0b01111),
    "H": (0b10001, 0b10001, 0b10001, 0b11111, 0b10001, 0b10001, 0b10001),
    "I": (0b01110, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b01110),
    "J": (0b00111, 0b00010, 0b00010, 0b00010, 0b00010, 0b10010, 0b01100),
    "K": (0b10001, 0b10010, 0b10100, 0b11000, 0b10100, 0b10010, 0b10001),
    "L": (0b10000, 0b10000, 0b10000, 0b10000, 0b10000, 0b10000, 0b11111),
    "M": (0b10001, 0b11011, 0b10101, 0b10101, 0b10001, 0b10001, 0b10001),
    "N": (0b10001, 0b11001, 0b10101, 0b10011, 0b10001, 0b10001, 0b10001),
    "O": (0b01110, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01110),
    "P": (0b11110, 0b10001, 0b10001, 0b11110, 0b10000, 0b10000, 0b10000),
    "Q": (0b01110, 0b10001, 0b10001, 0b10001, 0b10101, 0b10010, 0b01101),
    "R": (0b11110, 0b10001, 0b10001, 0b11110, 0b10100, 0b10010, 0b10001),
    "S": (0b01111, 0b10000, 0b10000, 0b01110, 0b00001, 0b00001, 0b11110),
    "T": (0b11111, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100),
    "U": (0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01110),
    "V": (0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01010, 0b00100),
    "W": (0b10001, 0b10001, 0b10001, 0b10101, 0b10101, 0b11011, 0b10001),
    "X": (0b10001, 0b10001, 0b01010, 0b00100, 0b01010, 0b10001, 0b10001),
    "Y": (0b10001, 0b10001, 0b01010, 0b00100, 0b00100, 0b00100, 0b00100),
    "Z": (0b11111, 0b00001, 0b00010, 0b00100, 0b01000, 0b10000, 0b11111),
    "0": (0b01110, 0b10001, 0b10011, 0b10101, 0b11001, 0b10001, 0b01110),
    "1": (0b00100, 0b01100, 0b00100, 0b00100, 0b00100, 0b00100, 0b01110),
    "2": (0b01110, 0b10001, 0b00001, 0b00110, 0b01000, 0b10000, 0b11111),
    "3": (0b11111, 0b00010, 0b00100, 0b00010, 0b00001, 0b10001, 0b01110),
    "4": (0b00010, 0b00110, 0b01010, 0b10010, 0b11111, 0b00010, 0b00010),
    "5": (0b11111, 0b10000, 0b11110, 0b00001, 0b00001, 0b10001, 0b01110),
    "6": (0b00110, 0b01000, 0b10000, 0b11110, 0b10001, 0b10001, 0b01110),
    "7": (0b11111, 0b00001, 0b00010, 0b00100, 0b01000, 0b01000, 0b01000),
    "8": (0b01110, 0b10001, 0b10001, 0b01110, 0b10001, 0b10001, 0b01110),
    "9": (0b01110, 0b10001, 0b10001, 0b01111, 0b00001, 0b00010, 0b01100),
    " ": (0, 0, 0, 0, 0, 0, 0),
    ".": (0, 0, 0, 0, 0, 0b01100, 0b01100),
    ",": (0, 0, 0, 0, 0b01100, 0b00100, 0b01000),
    ":": (0, 0b01100, 0b01100, 0, 0b01100, 0b01100, 0),
    ";": (0, 0b01100, 0b01100, 0, 0b01100, 0b00100, 0b01000),
    "-": (0, 0, 0, 0b01110, 0, 0, 0),
    "!": (0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0, 0b00100),
    "?": (0b01110, 0b10001, 0b00001, 0b00010, 0b00100, 0, 0b00100),
    "(": (0b00010, 0b00100, 0b01000, 0b01000, 0b01000, 0b00100, 0b00010),
    ")": (0b01000, 0b00100, 0b00010, 0b00010, 0b00010, 0b00100, 0b01000),
    "/": (0b00001, 0b00010, 0b00010, 0b00100, 0b01000, 0b01000, 0b10000),
    "%": (0b11001, 0b11010, 0b00010, 0b00100, 0b01000, 0b01011, 0b10011),
    "&": (0b01100, 0b10010, 0b10100, 0b01000, 0b10101, 0b10010, 0b01101),
    "+": (0, 0b00100, 0b00100, 0b11111, 0b00100, 0b00100, 0),
    "=": (0, 0, 0b11111, 0, 0b11111, 0, 0),
    "'": (0b00100, 0b00100, 0b01000, 0, 0, 0, 0),
    '"': (0b01010, 0b01010, 0, 0, 0, 0, 0),
    "$": (0b00100, 0b01111, 0b10100, 0b01110, 0b00101, 0b11110, 0b00100),
}


def text_width(text, scale):
    """Pixel width of text at the given scale (6 units per glyph)."""
    return len(text) * 6 * scale


def wrap(text, max_chars):
    """Greedy word wrap; returns a list of lines of at most max_chars."""
    lines = []
    for word in text.split(" "):
        if not lines or len(lines[-1]) + 1 + len(word) > max_chars:
            lines.append(word)
        else:
            lines[-1] += " " + word
    return lines


# ----------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, width, height, background):
        self.width = width
        self.height = height
        self.pixels = bytearray(width * height * 3)
        self.fill_rect(0, 0, width, height, background)

    def set_pixel(self, x, y, color):
        if 0 <= x < self.width and 0 <= y < self.height:
            i = (y * self.width + x) * 3
            self.pixels[i] = color[0]
            self.pixels[i + 1] = color[1]
            self.pixels[i + 2] = color[2]

    def fill_rect(self, x, y, w, h, color):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.width, x + w)
        y1 = min(self.height, y + h)
        r, g, b = color
        for yy in range(y0, y1):
            base = (yy * self.width + x0) * 3
            for xx in range(x0, x1):
                i = base + (xx - x0) * 3
                self.pixels[i] = r
                self.pixels[i + 1] = g
                self.pixels[i + 2] = b

    def border(self, x, y, w, h, color, thickness=2):
        self.fill_rect(x, y, w, thickness, color)
        self.fill_rect(x, y + h - thickness, w, thickness, color)
        self.fill_rect(x, y, thickness, h, color)
        self.fill_rect(x + w - thickness, y, thickness, h, color)

    def line(self, x0, y0, x1, y1, color):
        """Bresenham line, 1 px thick."""
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            self.set_pixel(x0, y0, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def thick_line(self, x0, y0, x1, y1, color, thickness):
        """Thick line: draw the line shifted over a small disc of offsets."""
        half = thickness // 2
        for ox in range(-half, half + 1):
            for oy in range(-half, half + 1):
                if ox * ox + oy * oy <= half * half + 1:
                    self.line(x0 + ox, y0 + oy, x1 + ox, y1 + oy, color)

    def filled_circle(self, cx, cy, r, color):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) * (xx - cx) + (yy - cy) * (yy - cy) <= r * r:
                    self.set_pixel(xx, yy, color)

    def draw_text(self, text, x, y, scale, color):
        """Draw uppercase text; unknown chars render as blank."""
        cx = x
        for ch in text:
            glyph = FONT.get(ch, FONT[" "])
            for row in range(7):
                bits = glyph[row]
                for col in range(5):
                    if bits & (1 << (4 - col)):
                        self.fill_rect(
                            cx + col * scale, y + row * scale,
                            scale, scale, color,
                        )
            cx += 6 * scale

    def draw_text_centered(self, text, cx, y, scale, color):
        self.draw_text(text, cx - text_width(text, scale) // 2, y, scale, color)


# ------------------------------------------------------------------- icons
def draw_flag_ukraine(c, x, y, w, h):
    c.fill_rect(x, y, w, h // 2, BLUE_UA)
    c.fill_rect(x, y + h // 2, w, h - h // 2, YELLOW_UA)
    c.border(x, y, w, h, DARK_LINE, 1)


def draw_flag_poland(c, x, y, w, h):
    c.fill_rect(x, y, w, h // 2, WHITE)
    c.fill_rect(x, y + h // 2, w, h - h // 2, RED_PL)
    c.border(x, y, w, h, DARK_LINE, 1)


def draw_flag_eu(c, x, y, w, h):
    c.fill_rect(x, y, w, h, BLUE_EU)
    cx, cy = x + w // 2, y + h // 2
    radius = min(w, h) // 2 - 8
    for i in range(12):
        ang = 2 * math.pi * i / 12 - math.pi / 2
        sx = int(cx + radius * math.cos(ang))
        sy = int(cy + radius * math.sin(ang))
        c.filled_circle(sx, sy, 3, GOLD)
    c.border(x, y, w, h, DARK_LINE, 1)


def draw_flag_uk(c, x, y, w, h):
    c.fill_rect(x, y, w, h, BLUE_UK)
    # White saltire (diagonals), then white cross, then red cross.
    c.thick_line(x, y, x + w, y + h, WHITE, 10)
    c.thick_line(x + w, y, x, y + h, WHITE, 10)
    c.fill_rect(x + w // 2 - 8, y, 16, h, WHITE)
    c.fill_rect(x, y + h // 2 - 8, w, 16, WHITE)
    c.fill_rect(x + w // 2 - 4, y, 8, h, RED_UK)
    c.fill_rect(x, y + h // 2 - 4, w, 8, RED_UK)
    c.border(x, y, w, h, DARK_LINE, 1)


def draw_chart(c, cx, top, bottom):
    """Falling market line with axes and a red arrowhead."""
    x0, x1 = cx - 90, cx + 90
    y0, y1 = top + 8, bottom - 8
    c.line(x0, y0, x0, y1, INK)
    c.line(x0, y1, x1, y1, INK)
    pts = [
        (x0 + 4, y0 + 8), (x0 + 30, y0 + 14), (x0 + 48, y0 + 30),
        (x0 + 66, y0 + 26), (x0 + 92, y0 + 44), (x0 + 118, y0 + 42),
        (x0 + 142, y0 + 58), (x0 + 168, y0 + 62),
    ]
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        c.thick_line(ax, ay, bx, by, RED, 3)
    ex, ey = pts[-1]
    c.thick_line(ex, ey, ex - 12, ey - 2, RED, 3)
    c.thick_line(ex, ey, ex - 2, ey - 12, RED, 3)


def draw_scales(c, cx, top, bottom):
    """Scales of justice."""
    mid_y = bottom - 6
    top_y = top + 6
    post_x = cx
    c.thick_line(post_x, top_y, post_x, mid_y, INK, 3)
    c.line(post_x - 14, mid_y, post_x + 14, mid_y, INK)
    c.thick_line(post_x - 52, top_y + 10, post_x + 52, top_y + 10, INK, 3)
    c.filled_circle(post_x, top_y, 4, GOLD)
    for sign in (-1, 1):
        px = post_x + sign * 52
        pan_y = top_y + 34
        c.line(px, top_y + 10, px - 16, pan_y, INK)
        c.line(px, top_y + 10, px + 16, pan_y, INK)
        c.thick_line(px - 18, pan_y, px + 18, pan_y, GOLD, 3)
        c.filled_circle(px, pan_y + 2, 7, GOLD)


def draw_quake(c, cx, top, bottom):
    """Cracked ground with shaking buildings."""
    ground_y = bottom - 14
    c.thick_line(cx - 95, ground_y, cx + 95, ground_y, INK, 3)
    # Buildings, slightly askew silhouettes.
    c.fill_rect(cx - 88, ground_y - 52, 44, 52, BROWN)
    c.fill_rect(cx - 30, ground_y - 68, 52, 68, INK)
    c.fill_rect(cx + 34, ground_y - 40, 40, 40, BROWN)
    # Windows.
    for bx, by in ((cx - 78, ground_y - 44), (cx - 56, ground_y - 44),
                   (cx - 20, ground_y - 58), (cx + 2, ground_y - 58),
                   (cx + 42, ground_y - 32)):
        c.fill_rect(bx, by, 10, 10, GOLD)
    # Zigzag crack through the ground.
    crack = [(cx - 60, ground_y), (cx - 44, ground_y + 6),
             (cx - 28, ground_y - 2), (cx - 10, ground_y + 6),
             (cx + 8, ground_y - 2), (cx + 26, ground_y + 6),
             (cx + 44, ground_y - 2), (cx + 62, ground_y + 4)]
    for (ax, ay), (bx, by) in zip(crack, crack[1:]):
        c.thick_line(ax, ay, bx, by, RED, 2)
    # Motion dashes beside the tall building.
    for dy in (0, 14, 28):
        c.line(cx - 38, ground_y - 60 + dy, cx - 46, ground_y - 60 + dy, RED)


# -------------------------------------------------------------------- png
def chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    return out


def encode_png(canvas):
    raw = bytearray()
    stride = canvas.width * 3
    for y in range(canvas.height):
        raw.append(0)  # filter: none
        start = y * stride
        raw += canvas.pixels[start:start + stride]
    body = zlib.compress(bytes(raw), 9)
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", canvas.width,
                                      canvas.height, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", body)
    png += chunk(b"IEND", b"")
    return png


# ------------------------------------------------------------------ layout
def draw_panel(c, x, y, w, h, strip_color, label, icon, headline, body):
    c.fill_rect(x, y, w, h, WHITE)
    c.border(x, y, w, h, DARK_LINE, 2)
    c.fill_rect(x, y, w, 32, strip_color)
    c.draw_text(label, x + 14, y + 9, 2, WHITE)
    icon(c, x + w // 2, y + 40, y + 120)
    hy = y + 128
    for i, line in enumerate(headline):
        c.draw_text(line, x + 14, hy + i * 18, 2, INK)
    by = y + 172
    for i, line in enumerate(wrap(body, 38)):
        c.draw_text(line, x + 14, by + i * 18, 2, INK)


def build_image():
    c = Canvas(WIDTH, HEIGHT, PAPER)

    # Masthead.
    c.fill_rect(16, 16, 992, 104, NAVY)
    c.fill_rect(16, 116, 992, 4, GOLD)
    c.draw_text_centered("THE WORLD IN ONE IMAGE", 512, 34, 2, WHITE)
    c.draw_text_centered("SATURDAY 21 NOVEMBER 2026", 512, 62, 4, WHITE)

    # Lead story: Russia strikes Ukraine, missiles land in Poland.
    lx, ly, lw, lh = 16, 132, 992, 216
    c.fill_rect(lx, ly, lw, lh, WHITE)
    c.border(lx, ly, lw, lh, DARK_LINE, 2)
    c.draw_text("WAR IN EUROPE", lx + 14, ly + 12, 2, RED)
    c.draw_text("RUSSIA'S BIGGEST STRIKES", lx + 14, ly + 38, 3, INK)
    c.draw_text("HIT UKRAINE; MISSILES LAND IN POLAND", lx + 14, ly + 68, 3, INK)
    c.draw_text(
        "MORE THAN 400 DRONES AND 110 MISSILES RAINED ON UKRAINE OVERNIGHT,",
        lx + 14, ly + 108, 2, INK)
    c.draw_text(
        "KILLING AT LEAST EIGHT PEOPLE IN KYIV. TWO RUSSIAN MISSILES AND A",
        lx + 14, ly + 130, 2, INK)
    c.draw_text(
        "SUSPECTED DRONE CAME DOWN IN POLAND. PRIME MINISTER TUSK CALLED IT",
        lx + 14, ly + 152, 2, INK)
    c.draw_text("A DELIBERATE PROVOCATION.", lx + 14, ly + 174, 2, INK)
    # Flags of Ukraine and Poland at the right of the lead panel.
    fx, fy = 836, ly + 14
    draw_flag_ukraine(c, fx, fy, 76, 46)
    draw_flag_poland(c, fx + 86, fy, 76, 46)
    c.draw_text("KYIV - WARSAW", fx + 3, fy + 56, 2, INK)

    # Four story panels, 2 x 2.
    draw_panel(
        c, 16, 360, 488, 260, RED, "MARKETS", draw_chart,
        ["AI SELL-OFF DRAGS WALL STREET", "INTO CORRECTION"],
        "S&P 500 FELL 3.7%, NASDAQ 5.3%, WIPING OUT ITS 2026 GAINS. "
        "NVIDIA SLID 14% AS THE SEC OPENED AN ACCOUNTING PROBE.")
    draw_panel(
        c, 520, 360, 488, 260, NAVY, "JUSTICE", draw_scales,
        ["COURT: MYANMAR COMMITTED", "GENOCIDE"],
        "THE WORLD COURT RULED 9-6 THAT MYANMAR COMMITTED GENOCIDE "
        "AGAINST THE ROHINGYA, THE FIRST TIME IT HELD A STATE RESPONSIBLE.")
    draw_panel(
        c, 16, 632, 488, 260, BROWN, "DISASTER",
        draw_quake,
        ["6.8 QUAKE SHAKES PERU"],
        "A MAGNITUDE 6.8 QUAKE STRUCK THE ANDEAN REGION OF JUNIN. "
        "TREMORS WERE FELT IN LIMA, 320 KM AWAY.")
    draw_panel(
        c, 520, 632, 488, 260, TEAL, "EUROPE",
        lambda cv, cx, top, bottom: (
            draw_flag_eu(cv, cx - 108, top + 6, 96, 58),
            draw_flag_uk(cv, cx + 12, top + 6, 96, 58),
        ),
        ["UK AND EU SEAL POST-BREXIT", "DEALS"],
        "BRUSSELS AGREED TO SCRAP MOST FOOD TRADE CHECKS, LINK CARBON "
        "MARKETS AND OPEN A YOUTH MOBILITY SCHEME FOR 100,000 PEOPLE.")

    # Ticker strip: three more stories of the day.
    tx, ty, tw, th = 16, 904, 992, 104
    c.fill_rect(tx, ty, tw, th, INK)
    c.draw_text(
        "ALSO TODAY: SAUDI DEFENCES STOP HOUTHI MISSILES AIMED AT RIYADH",
        tx + 14, ty + 14, 2, WHITE)
    c.draw_text(
        "PANCREATIC CANCER PILL MAKES TUMOURS UNDETECTABLE IN 1 IN 12 PATIENTS",
        tx + 14, ty + 38, 2, WHITE)
    c.draw_text(
        "COP31 CLIMATE TALKS MISS DEADLINE - CYCLONE AKVAN HITS INDIA'S EAST COAST",
        tx + 14, ty + 62, 2, WHITE)

    return c


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    png = encode_png(build_image())
    path = os.path.join(out_dir, "entry.png")
    with open(path, "wb") as fh:
        fh.write(png)
    print("wrote {} ({} bytes)".format(path, len(png)))


if __name__ == "__main__":
    main()
