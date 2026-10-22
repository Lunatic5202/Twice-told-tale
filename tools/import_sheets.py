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
    python3 tools/import_sheets.py --install --only echo   # only the named sets

--only takes a comma-separated list of tags (e.g. `--only echo` or
`--only echo,nahida`) so a change to one character's sheet never rewrites the
others.
"""
import argparse
import os
import tempfile
from collections import deque
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

SRC_DIR = os.path.expanduser("~/Downloads/sprite_clean/sprite")
OUT_DIR = "game/images/sprites"
STAGE_DIR = os.path.join(tempfile.gettempdir(), "opencode", "sheet_staging")

CANVAS = (700, 1120)

# cols/rows = grid; names = row-major expression mapping.  Gaps between cells
# are found from the alpha projection; cell boundaries fall on gap midpoints.
SHEETS = {
    "wanderer": dict(file="wanderer.png", cols=3, rows=2,
                     names=[["neutral", "smug", "soft"],
                            ["flustered", "hurt", "tired"]]),
    # echo arrives as two labelled strips (echo.png then echo1.png), each read
    # left-to-right.  Both come from white-background JPEGs, so the flat bg is
    # knocked out automatically.
    "echo": dict(sheets=[
        dict(file="echo.png", cols=4, rows=1,
             names=[["amused", "smile", "cold", "sneer"]]),
        dict(file="echo1.png", cols=3, rows=1,
             names=[["grieving", "startled", "shy"]]),
    ]),
    "nahida": dict(file="nahida.png", cols=2, rows=2,
                   names=[["gentle", "serious"],
                          ["mischievous", "sad"]]),
    "dottore": dict(file="dottore.png", cols=2, rows=2,
                    names=[["cold", "pleasant"],
                           ["fascinated", "delighted"]]),
    "ei": dict(file="ei.png", cols=2, rows=2,
               names=[["neutral", "sad"],
                      ["serious", "soft"]]),
    "yae": dict(file="yae.png", cols=2, rows=2,
                names=[["neutral", "amused"],
                       ["smug", "serious"]]),
    "tighnari": dict(file="tighnari.png", cols=2, rows=1,
                     names=[["neutral", "sly"]]),
    # cyno comes as a flat white-background JPEG (cut=True -> knock out the bg).
    "cyno": dict(file=os.path.expanduser("~/Downloads/cyno.jpeg"), cols=2, rows=1,
                 cut=True, names=[["neutral", "grinning"]]),
}

TARGET_H = {
    "wanderer": 950, "echo": 945, "nahida": 770, "dottore": 955,
    "tighnari": 940, "cyno": 950, "ei": 960, "yae": 900,
}

# Expressions absent from the sheets -> duplicate the nearest pose.
COPIES = {
    # the new wanderer sheet trades "guarded" for a real "soft" pose, so the
    # four guarded beats reuse the aloof smug pose.
    "wanderer_guarded": "wanderer_smug",
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


def flood_exterior(mask):
    """Flood-fill from the border through True pixels (background-ish)."""
    h, w = mask.shape
    ext = np.zeros((h, w), bool)
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if mask[y, x] and not ext[y, x]:
                ext[y, x] = True
                q.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if mask[y, x] and not ext[y, x]:
                ext[y, x] = True
                q.append((y, x))
    while q:
        cy, cx = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = cy + dy, cx + dx
            if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not ext[ny, nx]:
                ext[ny, nx] = True
                q.append((ny, nx))
    return ext


def remove_flat_bg(rgb, thr=42, enc_thr=30):
    """Knock out a uniform light background (used for the flat JPEG sheets)."""
    rgb = rgb.astype(np.float32)
    border = np.concatenate([rgb[0], rgb[-1], rgb[:, 0], rgb[:, -1]])
    bg = np.median(border, axis=0)
    dist = np.sqrt(((rgb - bg) ** 2).sum(-1))
    ext = flood_exterior(dist < thr)
    # Background caught in pockets the border flood can't reach (the gap between
    # an arm and the body, under a hat brim, between fingers) still reads as
    # white.  Knock out any such enclosed pixels that sit close to the bg colour
    # so no white gaps survive around the figure.
    enclosed = (dist < enc_thr) & ~ext
    alpha = np.where(ext | enclosed, 0, 255).astype(np.uint8)
    # erode 1px to cut the white-blended rim, then soften for anti-aliasing
    a_im = Image.fromarray(alpha, "L").filter(ImageFilter.MinFilter(3))
    a_im = a_im.filter(ImageFilter.GaussianBlur(0.6))
    return np.dstack([rgb.astype(np.uint8), np.array(a_im)])


def fit(rgba, target_h):
    # Resize in premultiplied alpha so transparent-black doesn't bleed into the
    # figure edge (avoids a dark fringe).  Deliberately no unsharp mask: it
    # exaggerates the cut edge and reads as a halo around the sprite.
    src = rgba.astype(np.float32)
    alpha = src[..., 3:4] / 255.0
    prem = src[..., :3] * alpha
    h, w = src.shape[:2]
    scale = target_h / h
    nw, nh = max(1, round(w * scale)), target_h
    if nw > CANVAS[0]:
        nh = max(1, round(nh * CANVAS[0] / nw))
        nw = CANVAS[0]
    prem_i = Image.fromarray(np.clip(prem, 0, 255).astype(np.uint8), "RGB").resize((nw, nh), Image.LANCZOS)
    a_i = Image.fromarray((alpha[..., 0] * 255).astype(np.uint8), "L").resize((nw, nh), Image.LANCZOS)
    rgb = np.asarray(prem_i).astype(np.float32) / np.maximum(np.asarray(a_i).astype(np.float32) / 255.0, 1e-3)[..., None]
    im = Image.fromarray(np.dstack([np.clip(rgb, 0, 255), np.asarray(a_i)[..., None]]).astype(np.uint8), "RGBA")
    canvas = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    canvas.alpha_composite(im, ((CANVAS[0] - im.width) // 2, CANVAS[1] - im.height - 8))
    return canvas


def slice_sheet(arr, cfg, tag, out_dir):
    """Cut a grid of expression cells out of one sheet and write each to a
    standard sprite.  Returns the list of written paths."""
    written = []
    colproj = arr[..., 3].astype(float).mean(0) / 255.0
    rowproj = arr[..., 3].astype(float).mean(1) / 255.0
    xb = cell_bounds(cfg["cols"], colproj)
    yb = cell_bounds(cfg["rows"], rowproj)
    for r in range(cfg["rows"]):
        for c in range(cfg["cols"]):
            name = cfg["names"][r][c]
            if name is None:  # spare pose with no in-game expression
                continue
            cell = arr[yb[r][0]:yb[r][1], xb[c][0]:xb[c][1]]
            cut = strip_labels(cell[..., 3])[1]
            if cut:
                cell = cell[cut:, :]
            rgba = trim(cell)
            sprite = fit(rgba, TARGET_H[tag])
            stem = "%s_%s" % (tag, name)
            outp = os.path.join(out_dir, stem + ".png")
            sprite.save(outp, optimize=True)
            written.append(outp)
            print("  %s  (cell %dx%d)" % (stem, r, c))
    return written


def copy_variants(out_dir, only=None):
    """Fill expressions absent from the sheets by copying the nearest pose."""
    written = []
    for dst, src in COPIES.items():
        if only is not None and dst.split("_")[0] not in only:
            continue
        s = os.path.join(out_dir, src + ".png")
        d = os.path.join(out_dir, dst + ".png")
        Image.open(s).save(d, optimize=True)
        written.append(d)
        print("  %s  (copy of %s)" % (dst, src))
    return written


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--install", action="store_true")
    ap.add_argument("--preview", action="store_true")
    ap.add_argument("--only", default="",
                    help="comma-separated character tags to (re)generate; "
                         "everything else is left untouched")
    args = ap.parse_args()
    out_dir = OUT_DIR if args.install else STAGE_DIR
    os.makedirs(out_dir, exist_ok=True)
    only = {t.strip() for t in args.only.split(",") if t.strip()} or None

    written = []
    for tag, cfg in SHEETS.items():
        if only is not None and tag not in only:
            continue
        for sc in cfg.get("sheets", [cfg]):
            path = sc["file"] if os.path.isabs(sc["file"]) else os.path.join(SRC_DIR, sc["file"])
            img = Image.open(path)
            rgba = np.array(img.convert("RGBA"))
            if sc.get("cut") or rgba[..., 3].min() > 250:
                # flat/opaque background (white JPEG/PNG sheets) -> knock it out
                arr = remove_flat_bg(np.array(img.convert("RGB")))
            else:
                arr = rgba
            written += slice_sheet(arr, sc, tag, out_dir)
    written += copy_variants(out_dir, only)

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
    mont_path = os.path.join(tempfile.gettempdir(), "opencode", "sheet_montage.png")
    os.makedirs(os.path.dirname(mont_path), exist_ok=True)
    mont.save(mont_path)
    print("wrote", len(written), "sprites ->", out_dir)
    print("montage ->", mont_path)


if __name__ == "__main__":
    main()
