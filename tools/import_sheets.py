#!/usr/bin/env python3
"""
import_sheets.py - slice character expression sheets into game sprites.

Source: sprite_clean/sprite/<tag>.png - one PNG per character, already
transparent, containing a grid of expressions (rows x cols).  Each cell is
cropped, trimmed to its alpha bbox, scaled to the character's target height,
and placed on the standard 700x1120 canvas (feet anchored at the bottom).

Usage:
    python3 tools/import_sheets.py --preview      # write to /tmp staging + montage
    python3 tools/import_sheets.py --install       # write into game/images/sprites
"""
import argparse
import os
from collections import deque
from PIL import Image, ImageDraw
import numpy as np

SRC_DIR = os.path.expanduser("~/Downloads/sprite_clean/sprite")
OUT_DIR = "game/images/sprites"
STAGE_DIR = "/tmp/opencode/sheet_staging"

CANVAS = (700, 1120)

# cols/rows = grid; names = row-major expression mapping.  Gaps between cells
# are found from the alpha projection; cell boundaries fall on gap midpoints.
SHEETS = {
    "wanderer": dict(file="wanderer.png", cols=3, rows=2,
                     names=[["neutral", "guarded", "smug"],
                            ["flustered", "hurt", "tired"]]),
    "echo": dict(file="echo.png", cols=3, rows=2,
                 names=[["cold", "amused", "startled"],
                        ["grieving", "shy", "smile"]]),
    "nahida": dict(file="nahida.png", cols=2, rows=2,
                   names=[["gentle", "serious"],
                          ["mischievous", "sad"]]),
    "dottore": dict(file="dottore.png", cols=2, rows=2,
                    names=[["pleasant", "delighted"],
                           ["cold", "fascinated"]]),
    "ei": dict(file="ei.png", cols=2, rows=2,
               names=[["neutral", "sad"],
                      ["serious", "soft"]]),
    "yae": dict(file="yae.png", cols=2, rows=2,
                names=[["neutral", "amused"],
                       ["smug", "serious"]]),
    "tighnari": dict(file="tighnari.png", cols=2, rows=1,
                     names=[["neutral", "sly"]]),
    "cyno": dict(file="cyno.png", cols=2, rows=1,
                 names=[["neutral", "grinning"]]),
}

TARGET_H = {
    "wanderer": 950, "echo": 945, "nahida": 770, "dottore": 955,
    "tighnari": 940, "cyno": 950, "ei": 960, "yae": 900,
}

# Expressions absent from the sheets -> duplicate the nearest pose.
COPIES = {
    "wanderer_soft": "wanderer_neutral",
    "echo_sneer": "echo_cold",
}


def interior_gaps(proj, thr=0.06):
    """Midpoints of interior low-alpha runs (excluding runs touching a border)."""
    n = len(proj)
    below = proj < thr
    runs = []
    i = 0
    while i < n:
        if below[i]:
            j = i
            while j + 1 < n and below[j + 1]:
                j += 1
            runs.append((i, j))
            i = j + 1
        else:
            i += 1
    mids = [ (a + b) / 2.0 for a, b in runs if a > 2 and b < n - 3 ]
    return mids


def cell_bounds(n_cells, proj):
    """Split [0, len(proj)) into n_cells slices, preferring gap midpoints."""
    mids = interior_gaps(proj)
    if len(mids) == n_cells - 1:
        edges = [0.0] + mids + [float(len(proj))]
        return [ (round(edges[i]), round(edges[i + 1])) for i in range(n_cells) ]
    return [ (round(len(proj) * i / n_cells), round(len(proj) * (i + 1) / n_cells))
             for i in range(n_cells) ]


def _components(mask):
    h, w = mask.shape
    seen = np.zeros((h, w), bool)
    out = []
    for y in range(h):
        for x in np.nonzero(mask[y] & ~seen[y])[0]:
            if seen[y, x] or not mask[y, x]:
                continue
            q = deque([(y, x)])
            seen[y, x] = True
            ys = []
            xs = []
            while q:
                cy, cx = q.popleft()
                ys.append(cy)
                xs.append(cx)
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ny, nx = cy + dy, cx + dx
                    if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True
                        q.append((ny, nx))
            out.append((len(ys), min(ys), max(ys), min(xs), max(xs)))
    out.sort(reverse=True)
    return out


def strip_labels(alpha, t=96):
    """The sheets carry text labels above each head.  At alpha>96 the glyphs
    separate from the figure; drop small components that sit above the figure
    and crop the cell to start below them.  Returns (cropped_alpha, rows_cut)."""
    h, w = alpha.shape
    comps = _components(alpha > t)
    if not comps:
        return alpha, 0
    fa, fy0, fy1, fx0, fx1 = comps[0]
    tb = -1
    for area, y0, y1, x0, x1 in comps[1:]:
        if y1 < fy0 and area < 0.08 * fa and y0 < 0.25 * h:
            tb = max(tb, y1)
    if tb < 0:
        return alpha, 0
    return alpha[tb + 1:, :], tb + 1


def trim(rgba, athr=8):
    a = rgba[..., 3]
    ys, xs = np.where(a > athr)
    if len(xs) == 0:
        return rgba
    return rgba[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def fit(rgba, target_h):
    im = Image.fromarray(rgba, "RGBA")
    w, h = im.size
    scale = target_h / h
    nw, nh = max(1, round(w * scale)), max(1, round(h * scale))
    im = im.resize((nw, nh), Image.LANCZOS)
    if nw > CANVAS[0]:
        im = im.resize((CANVAS[0], max(1, round(nh * CANVAS[0] / nw))), Image.LANCZOS)
    canvas = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    x = (CANVAS[0] - im.width) // 2
    y = CANVAS[1] - im.height - 8
    canvas.alpha_composite(im, (x, y))
    return canvas


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--install", action="store_true")
    ap.add_argument("--preview", action="store_true")
    args = ap.parse_args()
    out_dir = OUT_DIR if args.install else STAGE_DIR
    os.makedirs(out_dir, exist_ok=True)

    written = []
    for tag, cfg in SHEETS.items():
        path = os.path.join(SRC_DIR, cfg["file"])
        sheet = Image.open(path).convert("RGBA")
        arr = np.array(sheet)
        H, W = arr.shape[:2]
        colproj = arr[..., 3].astype(float).mean(0) / 255.0
        rowproj = arr[..., 3].astype(float).mean(1) / 255.0
        xb = cell_bounds(cfg["cols"], colproj)
        yb = cell_bounds(cfg["rows"], rowproj)
        for r in range(cfg["rows"]):
            for c in range(cfg["cols"]):
                name = cfg["names"][r][c]
                cell = arr[yb[r][0]:yb[r][1], xb[c][0]:xb[c][1]]
                cut = strip_labels(cell[..., 3])[1]
                if cut:
                    cell = cell[cut:, :]
                rgba = trim(cell)
                sprite = fit(rgba, TARGET_H[tag])
                outp = os.path.join(out_dir, "%s_%s.png" % (tag, name))
                sprite.save(outp, optimize=True)
                written.append(outp)
                print("  %s_%s  (cell %dx%d)" % (tag, name, r, c))

    for dst, src in COPIES.items():
        s = os.path.join(out_dir, src + ".png")
        d = os.path.join(out_dir, dst + ".png")
        Image.open(s).save(d, optimize=True)
        written.append(d)
        print("  %s  (copy of %s)" % (dst, src))

    # montage for visual review
    cols = 6
    rows = (len(written) + cols - 1) // cols
    cw, ch = 220, 372
    mont = Image.new("RGBA", (cols * cw, rows * ch), (60, 60, 68, 255))
    draw = ImageDraw.Draw(mont)
    sq = 16
    for yy in range(0, mont.height, sq):
        for xx in range(0, mont.width, sq):
            if (xx // sq + yy // sq) % 2:
                draw.rectangle([xx, yy, xx + sq, yy + sq], fill=(92, 92, 102, 255))
    for i, f in enumerate(written):
        im = Image.open(f).convert("RGBA").resize((cw, 352), Image.LANCZOS)
        ox, oy = (i % cols) * cw, (i // cols) * ch
        mont.alpha_composite(im, (ox, oy))
        name = os.path.splitext(os.path.basename(f))[0]
        draw.text((ox + 4, oy + 356), name, fill=(255, 235, 120, 255))
    mont_path = "/tmp/opencode/sheet_montage.png"
    mont.save(mont_path)
    print("wrote", len(written), "sprites ->", out_dir)
    print("montage ->", mont_path)


if __name__ == "__main__":
    main()
