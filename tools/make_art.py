#!/usr/bin/env python3
################################################################################
## Twice-Told Tale - Procedural Art Generator
################################################################################
##
## Generates every background, CG, and character sprite for the game in a
## cohesive "ink & paper" style. All output is original, deterministic, and
## copyright-free: layered painterly washes, silhouettes, atmosphere, and
## paper grain.
##
## Usage:
##     python3 tools/make_art.py                # generate everything
##     python3 tools/make_art.py --only annex_night bg_shrine
##     python3 tools/make_art.py --montage      # contact sheet of all art
##
## Output:
##     game/images/bg/<key>.png
##     game/images/cg/<key>.png
##     game/images/sprites/<tag>_<expr>.png

import os
import sys
import math
import random
import hashlib
import argparse

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
IMAGES = os.path.join(ROOT, "game", "images")

W, H = 1280, 720
SS = 2  # supersample factor for shape layers

# ----------------------------------------------------------------------------
# Palette
# ----------------------------------------------------------------------------

def hx(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


INK = hx("#14141f")
PAPER = hx("#ece4d2")
GOLD = hx("#c9a44a")
VIOLET = hx("#7d5fb2")
TEAL = hx("#3f8a83")
CRIMSON = hx("#b23a3a")
EMBER = hx("#d9773a")
SILHOUETTE = "#181423"


# ----------------------------------------------------------------------------
# Low-level helpers
# ----------------------------------------------------------------------------

def lerp(a, b, t):
    return a + (b - a) * t


def hseed(s):
    """Stable integer seed from any value (unlike hash(), stable across runs)."""
    return int.from_bytes(hashlib.sha256(str(s).encode()).digest()[:4], "big")


def vgrad(w, h, stops):
    """Vertical gradient. stops: [(pos 0..1, (r,g,b)), ...]"""
    ys = np.linspace(0.0, 1.0, h)
    pos = [s[0] for s in stops]
    cols = np.array([s[1] for s in stops], dtype=float)
    arr = np.zeros((h, 3))
    for ch in range(3):
        arr[:, ch] = np.interp(ys, pos, cols[:, ch])
    return np.repeat(arr[:, None, :], w, axis=1)


def radial(w, h, cx, cy, rx, ry, falloff=2.0):
    yy, xx = np.mgrid[0:h, 0:w]
    d = np.sqrt(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2)
    return np.clip(1.0 - d, 0.0, 1.0) ** falloff


def add_glow(arr, cx, cy, radius, color, strength=1.0, falloff=2.0):
    g = radial(arr.shape[1], arr.shape[0], cx, cy, radius, radius, falloff)
    for ch in range(3):
        arr[:, :, ch] += g * color[ch] * strength
    return arr


def composite(arr, layer):
    """Alpha-composite an RGBA PIL image onto an (h,w,3) float array."""
    base = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB").convert("RGBA")
    out = Image.alpha_composite(base, layer)
    return np.asarray(out.convert("RGB"), dtype=float).copy()


def new_layer():
    return Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))


def down(layer):
    return layer.resize((W, H), Image.LANCZOS)


def blur(layer, r):
    return layer.filter(ImageFilter.GaussianBlur(r * SS))


def shape(fn, fill, bl=0.0):
    """Draw shapes on a supersampled transparent layer."""
    lay = new_layer()
    d = ImageDraw.Draw(lay)
    fn(d)
    if bl:
        lay = blur(lay, bl)
    return down(lay)


def S(seq):
    seq = list(seq)
    if seq and not isinstance(seq[0], (tuple, list)):
        return [int(v * SS) for v in seq]
    return [(int(x * SS), int(y * SS)) for x, y in seq]


# ----------------------------------------------------------------------------
# Painterly layers
# ----------------------------------------------------------------------------

def ridge_layer(base_y, amp, color, seed=0, points=10, bl=1.5):
    rnd = random.Random(seed)
    pts = [(0, base_y + (rnd.random() - 0.5) * amp)]
    for i in range(1, points):
        x = W * i / (points - 1)
        y = base_y + (rnd.random() - 0.5) * amp * 2
        pts.append((x, y))
    pts += [(W, H), (0, H)]
    return shape(lambda d: d.polygon(S(pts), fill=color), color, bl)


def skyline_layer(base_y, color, seed=0, density=18, max_h=260, bl=1.2):
    rnd = random.Random(seed)
    rects = []
    x = -40.0
    while x < W + 40:
        w = rnd.uniform(50, 150)
        h = rnd.uniform(60, max_h)
        rects.append((x, base_y - h, x + w, base_y + 40))
        x += w + rnd.uniform(-10, 24)
    return shape(lambda d: [d.rectangle(S(r), fill=color) for r in rects], color, bl)


def forest_layer(base_y, color, seed=0, count=26, bl=1.4):
    rnd = random.Random(seed)
    trees = []
    for i in range(count):
        x = W * i / (count - 1) + rnd.uniform(-18, 18)
        h = rnd.uniform(120, 300)
        w = h * rnd.uniform(0.22, 0.4)
        trees.append([(x, base_y - h), (x - w, base_y), (x + w, base_y)])
    return shape(lambda d: [d.polygon(S(t), fill=color) for t in trees], color, bl)


def window_layer(box, glow_color, glow=0.9, bar=True):
    x0, y0, x1, y1 = box
    lay = shape(lambda d: d.rectangle(S(box), fill=glow_color), glow_color)
    if bar:
        m = (x1 - x0) / 2
        n = (y1 - y0) / 3
        d = ImageDraw.Draw(lay)
        for k in range(1, 3):
            d.rectangle(S((x0 + m - 3, y0, x0 + m + 3, y1)), fill=(0, 0, 0, 120))
        for k in range(1, 3):
            d.rectangle(S((x0, y0 + n * k - 3, x1, y0 + n * k + 3)), fill=(0, 0, 0, 120))
    return lay


def fog_band(arr, y, height, color, strength=0.5):
    yy = np.arange(H)[:, None]
    band = np.exp(-((yy - y) ** 2) / (2 * height ** 2))
    for ch in range(3):
        arr[:, :, ch] = arr[:, :, ch] * (1 - band * strength) + color[ch] * band * strength
    return arr


def light_shaft(arr, x, width, color, strength=0.35, tilt=0.0):
    yy, xx = np.mgrid[0:H, 0:W]
    cx = x + (yy - H / 2) * tilt
    beam = np.exp(-((xx - cx) ** 2) / (2 * width ** 2))
    beam *= np.clip(1 - yy / H, 0.15, 1.0)
    for ch in range(3):
        arr[:, :, ch] += beam * color[ch] * strength
    return arr


def particles(layer, count, seed, kind="dust", color=(255, 255, 255), size=3.0):
    rnd = random.Random(seed)
    d = ImageDraw.Draw(layer)
    for _ in range(count):
        x = rnd.uniform(0, W) * SS
        y = rnd.uniform(0, H) * SS
        s = rnd.uniform(size * 0.4, size) * SS
        a = rnd.randint(40, 130)
        if kind == "rain":
            ln = rnd.uniform(14, 34) * SS
            d.line([(x, y), (x - 5 * SS, y + ln)], fill=color + (a,), width=max(1, int(SS * 0.7)))
        elif kind == "snow":
            d.ellipse([x, y, x + s, y + s], fill=color + (a,))
        elif kind == "ash":
            d.ellipse([x, y, x + s * 0.7, y + s * 0.7], fill=color + (a,))
        else:
            d.ellipse([x, y, x + s * 0.5, y + s * 0.5], fill=color + (a,))
    return layer


def vignette(arr, strength=0.55):
    yy, xx = np.mgrid[0:H, 0:W]
    d = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
    v = np.clip(d - 0.45, 0, 1) ** 1.6
    return arr * (1 - v[..., None] * strength)


def grain(arr, amount=8.0, seed=1):
    rnd = np.random.default_rng(seed)
    n = rnd.normal(0, amount, (H, W, 1))
    light = np.mean(arr, axis=2, keepdims=True)
    mod = 1.0 + n / 255.0
    return np.clip(arr * mod, 0, 255)


def paper_finish(arr, strength=0.18, seed=7):
    """Warm paper wash blended over the whole image."""
    yy, xx = np.mgrid[0:H, 0:W]
    rnd = np.random.default_rng(seed)
    fiber = rnd.normal(0, 1, (H, W, 1))
    fiber = np.asarray(Image.fromarray(((fiber[..., 0] * 30) + 128).clip(0, 255).astype(np.uint8))
                       .filter(ImageFilter.GaussianBlur(1.2)), dtype=float)[..., None]
    fiber = (fiber - 128) / 128.0
    for ch in range(3):
        arr[:, :, ch] = arr[:, :, ch] * (1 - strength) + PAPER[ch] * strength
    arr += fiber * 4.0
    return arr


def finish(arr, vig=0.5, gr=6.0, pf=0.14, seed=1):
    arr = vignette(arr, vig)
    arr = paper_finish(arr, pf, seed + 3)
    arr = grain(arr, gr, seed + 9)
    return np.clip(arr, 0, 255)


def ink_frame(arr, margin=26, color=(20, 18, 26), a=120, bl=0.0):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    m = margin
    d.rectangle([m, m, W - m, H - m], outline=color + (a,), width=2)
    d.rectangle([m - 5, m - 5, W - m + 5, H - m + 5], outline=color + (a // 3,), width=1)
    return composite(arr, lay)


# ----------------------------------------------------------------------------
# Figures (character sprites and in-scene silhouettes)
# ----------------------------------------------------------------------------

SPRITE_SPECS = {
    "wanderer": dict(skin="#f0d8c0", hair="#1d2c4d", hair_style="short",
                     coat="#33506e", coat_dark="#22384f", accent="#6fd0d8",
                     trim="#eae6da", eyes="#3f7fc4", hair2="#4a6fa5",
                     hat="kasa", height=950),
    "echo": dict(skin="#f0d8c0", hair="#2a2050", hair_style="bob",
                 coat="#6a2440", coat_dark="#471830", accent="#9a6bc0",
                 trim="#e8e2d0", eyes="#8465cf", hair2="#523088",
                 hat="veiled", height=945),
    "nahida": dict(skin="#f7e4cf", hair="#dfeccf", hair_style="long",
                   coat="#f2f6e8", coat_dark="#bcd8a4", accent="#6fa843",
                   trim="#8fc15e", hat=None, height=770, head_ratio=0.25,
                   leaf=True, eyes="#5ea23f", hair2="#a9cf82", eye_scale=1.2),
    "dottore": dict(skin="#e8d3c3", hair="#8fbcd8", hair_style="spiky",
                    coat="#dfe4ea", coat_dark="#c2cad4", accent="#3a5570",
                    trim="#3a5570", eyes="#a83840", hair2="#cfe6f4",
                    hat=None, height=955, mask=True),
    "tighnari": dict(skin="#ecd2b4", hair="#6f7f3e", hair_style="short",
                     coat="#4a5e2e", coat_dark="#33421f", accent="#c9b070",
                     trim="#c9b070", eyes="#9bbf3a", hair2="#93a852",
                     hat=None, ears="fox", height=940),
    "cyno": dict(skin="#dcbd97", hair="#1c1c26", hair_style="short",
                 coat="#2a2a34", coat_dark="#1a1a22", accent="#c9a44a",
                 trim="#c9a44a", eyes="#cfa03a", hair2="#3a3a4a",
                 hat=None, ears="jackal", height=950),
    "ei": dict(skin="#f2ddca", hair="#6a5a9a", hair_style="long",
               coat="#4a3a6a", coat_dark="#352a52", accent="#c9a44a",
               trim="#dcd8ea", eyes="#8a6cd0", hair2="#9a86c8",
               hat=None, height=955),
    "yae": dict(skin="#f6e3cf", hair="#eec2d6", hair_style="long",
                coat="#f0eee8", coat_dark="#d8d0c8", accent="#b03040",
                trim="#b03040", eyes="#d06a9a", hair2="#f6d6e6",
                hat=None, ears="fox", height=940),
}

EXPR = {
    "neutral":   ("flat", "open", "flat"),
    "guarded":   ("flat", "narrow", "flat"),
    "smug":      ("oneup", "narrow", "smirk"),
    "flustered": ("inner", "wide", "small", True),
    "hurt":      ("inner", "droop", "frown"),
    "soft":      ("up", "closed", "smile"),
    "tired":     ("flat", "droop", "flat"),
    "sneer":     ("angry", "narrow", "smirk"),
    "cold":      ("flat", "narrow", "flat"),
    "amused":    ("up", "narrow", "smirk"),
    "startled":  ("up", "wide", "open"),
    "grieving":  ("inner", "closed", "frown", False, True),
    "shy":       ("inner", "side", "small", True),
    "smile":     ("up", "closed", "grin"),
    "gentle":    ("up", "closed", "smile"),
    "serious":   ("down", "narrow", "flat"),
    "mischievous": ("oneup", "narrow", "smirk"),
    "sad":       ("inner", "droop", "frown", False, True),
    "pleasant":  ("up", "open", "smile"),
    "delighted": ("up", "closed", "grin"),
    "fascinated": ("up", "wide", "open"),
    "cheerful":  ("up", "closed", "grin"),
    "worried":   ("inner", "open", "flat"),
    "excited":   ("up", "wide", "open"),
    "sly":       ("oneup", "narrow", "smirk"),
    "grinning":  ("up", "narrow", "grin"),
}

INK = "#241f33"


# ----------------------------------------------------------------------------
# Colour + silhouette helpers
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
# Colour + silhouette helpers
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
# Colour + silhouette helpers
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
# Colour + silhouette helpers
# ----------------------------------------------------------------------------

def darken(c, f=0.74):
    return (max(0, int(c[0] * f)), max(0, int(c[1] * f)), max(0, int(c[2] * f)))


def lighten(c, f=0.34):
    return (min(255, int(c[0] + (255 - c[0]) * f)),
            min(255, int(c[1] + (255 - c[1]) * f)),
            min(255, int(c[2] + (255 - c[2]) * f)))


def mixc(a, b, t):
    return (int(a[0] + (b[0] - a[0]) * t),
            int(a[1] + (b[1] - a[1]) * t),
            int(a[2] + (b[2] - a[2]) * t))


def head_pts(hw, hh, n=64):
    """Anime head silhouette: rounded dome on top, tapering to a soft chin."""
    right = []
    for i in range(n + 1):
        t = i / n
        if t < 0.50:
            w = hw * math.sqrt(max(0.0, 1.0 - ((0.50 - t) / 0.50) ** 2))
        else:
            u = (t - 0.50) / 0.50
            w = hw * (1.0 - 0.84 * u ** 1.9)
        right.append((w, hh * t))
    return right


def ink_outline(img, color="#241f33", width=2, scale=3):
    """Wrap a figure in a clean ink contour so it reads on any background."""
    a = img.getchannel("A")
    dil = a
    for _ in range(max(1, int(round(width)) * scale)):
        dil = dil.filter(ImageFilter.MaxFilter(3))
    ring = ImageChops.subtract(dil, a)
    ink = Image.new("RGBA", img.size, hx(color) + (0,))
    ink.putalpha(ring)
    return Image.alpha_composite(ink, img).convert("RGBA")


def _cosprofile(keys):
    """Smooth (cosine) interpolation through (y, half-width) keys."""
    keys = sorted(keys)

    def f(y):
        if y <= keys[0][0]:
            return keys[0][1]
        if y >= keys[-1][0]:
            return keys[-1][1]
        for i in range(len(keys) - 1):
            y0, v0 = keys[i]
            y1, v1 = keys[i + 1]
            if y0 <= y <= y1:
                t = (y - y0) / max(1e-6, (y1 - y0))
                t = (1.0 - math.cos(math.pi * t)) / 2.0
                return v0 + (v1 - v0) * t
        return keys[-1][1]

    return f


def _catmull_closed(pts, samples=8):
    """Closed Catmull-Rom spline through control points (rounds corners)."""
    n = len(pts)
    out = []
    for i in range(n):
        p0, p1, p2, p3 = pts[(i - 1) % n], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        for j in range(samples):
            t = j / samples
            t2, t3 = t * t, t * t * t
            x = 0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t +
                       (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 +
                       (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
            y = 0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t +
                       (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 +
                       (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
            out.append((x, y))
    return out


def _catmull_open(pts, samples=8):
    """Open Catmull-Rom polyline through control points (smooths a curve)."""
    if len(pts) < 3:
        return list(pts)
    P = [pts[0]] + list(pts) + [pts[-1]]
    out = []
    for i in range(len(P) - 3):
        p0, p1, p2, p3 = P[i], P[i + 1], P[i + 2], P[i + 3]
        for j in range(samples):
            t = j / samples
            t2, t3 = t * t, t * t * t
            x = 0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t +
                       (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 +
                       (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
            y = 0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t +
                       (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 +
                       (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
            out.append((x, y))
    out.append(pts[-1])
    return out


def almond(x0, y0, x1, y1, w):
    """A leaf/almond lens from (x0,y0) to (x1,y1) with bulge width w."""
    mx, my = (x0 + x1) / 2.0, (y0 + y1) / 2.0
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / L, dx / L
    return [(x0, y0), (mx + nx * w, my + ny * w), (x1, y1), (mx - nx * w, my - ny * w)]


def render_figure(tag, expr="neutral", flat=None):
    """Draw a stylized character. `flat` overrides every colour with one
    (used for dark in-scene silhouettes)."""
    spec = SPRITE_SPECS.get(tag, SPRITE_SPECS["wanderer"])
    ex = EXPR.get(expr) or EXPR["neutral"]
    b, eye, mouth = ex[:3]
    blush = len(ex) > 3 and bool(ex[3])
    tear = len(ex) > 4 and bool(ex[4])

    if flat:
        skin = hair = coat = dark = accent = trim = hx(flat)
    else:
        skin, hair = hx(spec["skin"]), hx(spec["hair"])
        coat, dark = hx(spec["coat"]), hx(spec["coat_dark"])
        accent, trim = hx(spec["accent"]), hx(spec["trim"])

    ink_c = hx(INK) if isinstance(INK, str) else INK
    coat_sh = darken(coat, 0.82)
    hair_sh = darken(hair, 0.80)
    hair_hi = lighten(hair, 0.30)
    hair2 = hair if flat else hx(spec.get("hair2", spec["hair"]))
    skin_sh = darken(skin, 0.90)
    iris_col = dark if flat else hx(spec.get("eyes", spec["accent"]))
    eye_scale = 1.0 if flat else spec.get("eye_scale", 1.0)

    FS = 3  # figure supersample (smoother edges than the global SS)
    W_, H_ = 700, 1120
    img = Image.new("RGBA", (W_ * FS, H_ * FS), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    def P(x, y):
        return (x * FS, y * FS)

    def poly(pts, fill):
        d.polygon([P(*p) for p in pts], fill=fill)

    def rpoly(pts, fill, samples=8):
        """Rounded polygon — smooths corners so shapes are never boxy."""
        d.polygon([P(*p) for p in _catmull_closed(pts, samples)], fill=fill)

    def ell(x0, y0, x1, y1, fill):
        d.ellipse([P(min(x0, x1), min(y0, y1)), P(max(x0, x1), max(y0, y1))], fill=fill)

    def line(pts, fill, w=2):
        if len(pts) >= 3:
            pts = _catmull_open(pts)
        d.line([P(*p) for p in pts], fill=fill, width=max(1, int(round(w * FS))), joint="curve")

    def soft(pts, color, alpha=150):
        nonlocal img, d
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(lay).polygon([P(*p) for p in _catmull_closed(pts, 6)], fill=tuple(color)[:3] + (alpha,))
        img = Image.alpha_composite(img, lay)
        d = ImageDraw.Draw(img)

    def soft_ell(x0, y0, x1, y1, color, alpha=140):
        nonlocal img, d
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(lay).ellipse(
            [P(min(x0, x1), min(y0, y1)), P(max(x0, x1), max(y0, y1))],
            fill=tuple(color)[:3] + (alpha,))
        img = Image.alpha_composite(img, lay)
        d = ImageDraw.Draw(img)

    def limb(x0, y0, x1, y1, w0, w1, fill):
        """Smooth tapered capsule with rounded caps."""
        dx, dy = x1 - x0, y1 - y0
        L = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / L, dx / L
        m = 14
        r, l = [], []
        for i in range(m + 1):
            t = i / m
            px, py = x0 + dx * t, y0 + dy * t
            w = w0 + (w1 - w0) * t
            r.append((px + nx * w, py + ny * w))
            l.append((px - nx * w, py - ny * w))
        poly(r + l[::-1], fill)
        ell(x1 - w1, y1 - w1, x1 + w1, y1 + w1, fill)
        ell(x0 - w0, y0 - w0, x0 + w0, y0 + w0, fill)

    def grad_poly(pts, top, bottom, alpha=95):
        nonlocal img, d
        w, h = img.size
        small = vgrad(8, h, [(0.0, tuple(top)), (1.0, tuple(bottom))])
        gi = (Image.fromarray(np.clip(small, 0, 255).astype(np.uint8), "RGB")
              .resize((w, h), Image.BILINEAR).convert("RGBA"))
        mask = Image.new("L", img.size, 0)
        ImageDraw.Draw(mask).polygon([P(*p) for p in pts], fill=alpha)
        gi.putalpha(mask)
        img = Image.alpha_composite(img, gi)
        d = ImageDraw.Draw(img)

    # ---- proportions ----
    cx = 350.0
    feet = 1080.0
    Ht = float(spec["height"])
    hr = spec.get("head_ratio", 0.165)
    head_h = Ht * hr
    head_w = head_h * 0.80
    hw = head_w / 2.0
    head_top = feet - Ht
    chin = head_top + head_h
    shoulder_y = chin + head_h * 0.13
    waist_y = shoulder_y + (feet - shoulder_y) * 0.34
    hip_y = shoulder_y + (feet - shoulder_y) * 0.50
    coat_hem = feet - (feet - hip_y) * 0.30
    shoulder_w = head_w * 2.10
    bust_w = shoulder_w * 0.90
    waist_w = shoulder_w * 0.64
    hip_w = shoulder_w * 0.84
    hem_w = shoulder_w * 1.40
    neck_w = head_w * 0.32
    leg_w = head_w * 0.32
    style = spec["hair_style"]

    # ---- ground shadow (soft) ----
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse([P(cx - hem_w * 0.72, feet - 16), P(cx + hem_w * 0.72, feet + 16)],
                               fill=(18, 14, 28, 55))
    sh = sh.filter(ImageFilter.GaussianBlur(6 * FS))
    img = Image.alpha_composite(img, sh)
    d = ImageDraw.Draw(img)

    # ---- legs ----
    for s in (-1, 1):
        xt = cx + s * head_w * 0.30
        xa = cx + s * head_w * 0.26
        limb(xt, hip_y + head_h * 0.04, xa, feet - 20, leg_w * 0.50, leg_w * 0.40, dark)
        ell(xa - leg_w * 0.60, feet - 34, xa + leg_w * 0.60, feet + 2, darken(dark, 0.72))

    # ---- body silhouette (smooth profile) ----
    bw = _cosprofile([
        (shoulder_y, shoulder_w / 2),
        (shoulder_y + (waist_y - shoulder_y) * 0.55, bust_w / 2),
        (waist_y, waist_w / 2),
        (hip_y, hip_w / 2),
        (coat_hem, hem_w / 2),
    ])
    N = 56
    ys = [shoulder_y + (coat_hem - shoulder_y) * i / N for i in range(N + 1)]
    right = [(cx + bw(y), y) for y in ys]
    hem_arc = [(cx + (hem_w / 2) * math.cos(t), coat_hem + head_h * 0.13 * math.sin(t))
               for t in [math.pi * i / 24 for i in range(25)]]
    left = [(cx - bw(y), y) for y in reversed(ys)]
    body = right + hem_arc + left
    poly(body, coat)
    for s in (-1, 1):
        ell(cx + s * shoulder_w / 2 - head_w * 0.20, shoulder_y - head_h * 0.12,
            cx + s * shoulder_w / 2 + head_w * 0.20, shoulder_y + head_h * 0.24, coat)
    if not flat:
        grad_poly(body, lighten(coat, 0.10), darken(coat, 0.86), 70)
    sh_pts = [(cx + bw(y) * 0.14, y) for y in ys] + [(cx + bw(y), y) for y in reversed(ys)]
    poly(sh_pts, coat_sh)
    # curved collar neckline
    rpoly([(cx - head_w * 0.36, shoulder_y + head_h * 0.01),
           (cx, shoulder_y + head_h * 0.42),
           (cx + head_w * 0.36, shoulder_y + head_h * 0.01)], trim)
    # curved sash / belt following the waist
    rpoly([(cx - bw(waist_y) * 1.03, waist_y - head_h * 0.11),
           (cx, waist_y - head_h * 0.13),
           (cx + bw(waist_y) * 1.03, waist_y - head_h * 0.11),
           (cx + bw(waist_y) * 1.03, waist_y + head_h * 0.09),
           (cx, waist_y + head_h * 0.11),
           (cx - bw(waist_y) * 1.03, waist_y + head_h * 0.09)], accent)
    if spec.get("leaf") and not flat:
        rpoly(almond(cx - head_w * 0.13, shoulder_y + head_h * 0.34, cx, shoulder_y + head_h * 0.18, head_w * 0.06), accent)
        rpoly(almond(cx, shoulder_y + head_h * 0.18, cx + head_w * 0.13, shoulder_y + head_h * 0.34, head_w * 0.06), accent)
        # curved hem band following the hem arc
        rpoly([(cx - hem_w * 0.50, coat_hem - head_h * 0.02),
               (cx, coat_hem + head_h * 0.06),
               (cx + hem_w * 0.50, coat_hem - head_h * 0.02),
               (cx + hem_w * 0.50, coat_hem + head_h * 0.05),
               (cx, coat_hem + head_h * 0.12),
               (cx - hem_w * 0.50, coat_hem + head_h * 0.05)], accent)

    # ---- arms + hands (rounded sleeves) ----
    for s in (-1, 1):
        sx = cx + s * shoulder_w * 0.44
        ex = cx + s * (shoulder_w * 0.50 + head_w * 0.14)
        ey = shoulder_y + (coat_hem - shoulder_y) * 0.80
        limb(sx, shoulder_y + head_h * 0.04, ex, ey, head_w * 0.17, head_w * 0.19, coat)
        if not flat:
            limb(sx + s * head_w * 0.06, shoulder_y + head_h * 0.14, ex, ey - head_h * 0.06,
                 head_w * 0.045, head_w * 0.045, coat_sh)
        hx0 = cx + s * (shoulder_w * 0.48 + head_w * 0.10)
        hy0 = ey + head_h * 0.15
        ell(hx0 - head_w * 0.10, hy0 - head_h * 0.09, hx0 + head_w * 0.10, hy0 + head_h * 0.11, skin)

    # ---- neck ----
    limb(cx, chin - head_h * 0.16, cx, shoulder_y + head_h * 0.08, neck_w * 0.55, neck_w * 0.62, skin)
    if not flat:
        soft_ell(cx - neck_w * 0.66, chin - head_h * 0.12, cx + neck_w * 0.66, chin + head_h * 0.08,
                 skin_sh, 150)

    # ---- back hair ----
    if style == "long":
        back_bot = shoulder_y + head_h * 1.15
        back_w = hw * 1.55
    elif style == "bob":
        back_bot = chin + head_h * 0.24
        back_w = hw * 1.34
    else:
        back_bot = chin + head_h * 0.08
        back_w = hw * 1.18
    bp = head_pts(back_w, back_bot - head_top + head_h * 0.28)
    back = [(cx + wx, head_top - head_h * 0.16 + wy) for wx, wy in bp]
    back += [(cx - wx, head_top - head_h * 0.16 + wy) for wx, wy in reversed(bp)]
    poly(back, hair)
    if not flat and spec.get("hair2") and back_bot > chin:
        cut = chin + head_h * 0.02
        h2 = [(cx + wx, head_top - head_h * 0.16 + wy) for wx, wy in bp
              if head_top - head_h * 0.16 + wy >= cut]
        h2 += [(cx - wx, head_top - head_h * 0.16 + wy) for wx, wy in reversed(bp)
               if head_top - head_h * 0.16 + wy >= cut]
        if len(h2) > 3:
            poly(h2, hair2)

    # ---- head ----
    hp = head_pts(hw, head_h)
    head_poly = ([(cx + wx, head_top + wy) for wx, wy in hp] +
                 [(cx - wx, head_top + wy) for wx, wy in reversed(hp)])
    poly(head_poly, skin)
    if not flat:
        soft_ell(cx - hw * 0.62, chin - head_h * 0.34, cx + hw * 0.62, chin + head_h * 0.02,
                 skin_sh, 110)

    # human ears
    if not spec.get("ears"):
        for s in (-1, 1):
            ell(cx + s * hw * 0.84, head_top + head_h * 0.44,
                cx + s * hw * 1.08, head_top + head_h * 0.64, skin)

    # ---- front hair (smooth wavy fringe) ----
    if not flat:
        ell(cx - hw * 1.12, head_top - head_h * 0.22, cx + hw * 1.12, head_top + head_h * 0.40, hair)
        n = 44
        xs = [cx + (i / n - 0.5) * head_w * 2.12 for i in range(n + 1)]
        fr = [(x, head_top - head_h * 0.06) for x in xs]
        for x in reversed(xs):
            tt = (x - cx) / (head_w * 1.06)
            yy = head_top + head_h * (0.40 + 0.09 * math.cos(tt * math.pi * 3.0) + 0.05 * tt * tt)
            fr.append((x, yy))
        poly(fr, hair)
        fsh = [(x, head_top + head_h * 0.30) for x in xs]
        for x in reversed(xs):
            tt = (x - cx) / (head_w * 1.00)
            fsh.append((x, head_top + head_h * (0.415 + 0.07 * math.cos(tt * math.pi * 3.0))))
        soft(fsh, darken(skin, 0.87), 90)
        for i in range(-2, 3):
            ox = i * hw * 0.36
            line([(cx + ox * 0.85, head_top + head_h * 0.02),
                  (cx + ox * 1.02, head_top + head_h * 0.24),
                  (cx + ox * 1.08, head_top + head_h * 0.44)], hair_sh, 2)
        if style == "spiky":
            for i in range(-2, 3):
                bx = cx + i * hw * 0.6
                rpoly([(bx - head_w * 0.11, head_top + head_h * 0.04),
                       (bx - head_w * 0.05, head_top - head_h * 0.28),
                       (bx, head_top - head_h * 0.46),
                       (bx + head_w * 0.05, head_top - head_h * 0.28),
                       (bx + head_w * 0.11, head_top + head_h * 0.04)], hair)
        sl_bot = chin + head_h * (0.55 if style == "long" else 0.06)
        for s in (-1, 1):
            limb(cx + s * hw * 0.88, head_top + head_h * 0.24, cx + s * hw * 1.16,
                 sl_bot, head_w * 0.11, head_w * 0.07, hair)
            if spec.get("hair2"):
                limb(cx + s * hw * 0.96, chin - head_h * 0.10, cx + s * hw * 1.14,
                     sl_bot, head_w * 0.09, head_w * 0.06, hair2)
        d.arc([P(cx - hw * 0.98, head_top - head_h * 0.04), P(cx + hw * 0.98, head_top + head_h * 0.40)],
              205, 335, fill=hair_hi, width=max(1, int(head_h * 0.05)))

    # ---- face ----
    eye_y = head_top + head_h * 0.60
    eye_dx = hw * 0.42
    ew = hw * 0.30 * eye_scale
    eh = head_h * 0.115 * eye_scale
    brow_y = eye_y - head_h * 0.155
    mouth_y = head_top + head_h * 0.83

    def draw_eye(ex0, s):
        if eye == "closed":
            d.arc([P(ex0 - ew, eye_y - eh * 0.6), P(ex0 + ew, eye_y + eh * 0.6)],
                  200, 340, fill=ink_c, width=int(2.0 * FS))
            return
        if eye == "droop":
            top, bot = eye_y - eh * 0.15, eye_y + eh * 1.05
        elif eye == "narrow":
            top, bot = eye_y - eh * 0.42, eye_y + eh * 0.34
        elif eye == "wide":
            top, bot = eye_y - eh * 1.18, eye_y + eh * 1.05
        else:
            top, bot = eye_y - eh * 0.86, eye_y + eh * 0.74
        ex0 = ex0 + (s * ew * 0.28 if eye == "side" else 0)
        d.ellipse([P(ex0 - ew, top), P(ex0 + ew, bot)], fill=(250, 247, 242))
        ir = min(ew * 0.92, (bot - top) * 0.60)
        icy = (top + bot) / 2
        d.ellipse([P(ex0 - ir, icy - ir * 1.06), P(ex0 + ir, icy + ir * 1.06)], fill=iris_col)
        d.ellipse([P(ex0 - ir, icy - ir * 1.06), P(ex0 + ir, icy + ir * 1.06)],
                  outline=darken(iris_col, 0.6), width=max(1, int(FS)))
        d.ellipse([P(ex0 - ir * 0.44, icy - ir * 0.48), P(ex0 + ir * 0.44, icy + ir * 0.48)],
                  fill=(18, 16, 24))
        d.ellipse([P(ex0 - ir * 0.60, icy - ir * 0.92), P(ex0 - ir * 0.02, icy - ir * 0.30)],
                  fill=(255, 255, 255))
        d.arc([P(ex0 - ew * 1.02, top - eh * 0.10), P(ex0 + ew * 1.02, top + (bot - top) * 0.9)],
              180, 360, fill=ink_c, width=int(2.1 * FS))
        d.ellipse([P(ex0 - ew, top), P(ex0 + ew, bot)], outline=ink_c, width=max(1, int(FS)))

    if spec.get("mask"):
        rpoly([(cx - hw * 0.90, head_top + head_h * 0.42),
               (cx + hw * 0.90, head_top + head_h * 0.42),
               (cx + hw * 0.80, chin - head_h * 0.02),
               (cx - hw * 0.80, chin - head_h * 0.02)], (222, 226, 232))
        for s in (-1, 1):
            ell(cx + s * eye_dx - ew * 1.05, eye_y - eh * 1.25,
                cx + s * eye_dx + ew * 1.05, eye_y + eh * 1.25, (10, 12, 16))
    else:
        for s in (-1, 1):
            draw_eye(cx + s * eye_dx, s)
        for s in (-1, 1):
            ex0 = cx + s * eye_dx
            inner = ex0 - s * ew * 1.02
            outer = ex0 + s * ew * 1.12
            midx = (inner + outer) / 2
            dy = {"flat": 0, "up": -head_h * 0.06, "down": head_h * 0.05,
                  "inner": -head_h * 0.05, "angry": head_h * 0.05}.get(b, 0)
            if b == "oneup":
                dy = -head_h * 0.085 if s > 0 else head_h * 0.02
            if b == "angry":
                line([(inner, brow_y + abs(dy)), (midx, brow_y + dy * 0.4), (outer, brow_y - dy * 0.3)], ink_c, 3)
            elif b == "inner":
                line([(inner, brow_y + abs(dy)), (midx, brow_y + dy * 0.5), (outer, brow_y - dy)], ink_c, 3)
            else:
                line([(inner, brow_y + dy), (midx, brow_y + dy - head_h * 0.014), (outer, brow_y + dy - head_h * 0.012)], ink_c, 3)
        mw = head_w * 0.20
        if mouth == "smile":
            d.arc([P(cx - mw, mouth_y - mw * 0.7), P(cx + mw, mouth_y + mw * 0.7)],
                  20, 160, fill=ink_c, width=int(2.0 * FS))
        elif mouth == "grin":
            d.chord([P(cx - mw, mouth_y - mw * 0.3), P(cx + mw, mouth_y + mw * 1.1)],
                    10, 170, fill=(158, 74, 82))
            d.arc([P(cx - mw, mouth_y - mw * 0.3), P(cx + mw, mouth_y + mw * 1.1)],
                  10, 170, fill=ink_c, width=max(1, int(FS)))
        elif mouth == "frown":
            d.arc([P(cx - mw, mouth_y + mw * 0.1), P(cx + mw, mouth_y + mw * 1.4)],
                  200, 340, fill=ink_c, width=int(2.0 * FS))
        elif mouth == "smirk":
            d.arc([P(cx - mw * 0.9, mouth_y - mw * 0.5), P(cx + mw * 1.15, mouth_y + mw * 0.9)],
                  20, 120, fill=ink_c, width=int(2.0 * FS))
        elif mouth == "open":
            ell(cx - mw * 0.48, mouth_y - mw * 0.30, cx + mw * 0.48, mouth_y + mw * 0.62, (150, 68, 78))
        elif mouth == "small":
            line([(cx - mw * 0.32, mouth_y + head_h * 0.004), (cx, mouth_y), (cx + mw * 0.32, mouth_y + head_h * 0.004)], ink_c, 3)
        else:
            line([(cx - mw * 0.46, mouth_y + head_h * 0.006), (cx, mouth_y), (cx + mw * 0.46, mouth_y + head_h * 0.006)], ink_c, 3)
        if blush:
            for s in (-1, 1):
                soft_ell(cx + s * hw * 0.62 - hw * 0.16, eye_y + head_h * 0.04,
                         cx + s * hw * 0.62 + hw * 0.16, eye_y + head_h * 0.20,
                         (226, 122, 132), 120)
        if tear:
            for s in (-1, 1):
                ex0 = cx + s * eye_dx
                ell(ex0 - head_w * 0.025, eye_y + eh * 1.15, ex0 + head_w * 0.025,
                    eye_y + eh * 2.7, (150, 200, 235))

    # ---- fabric folds (curved) ----
    if not flat:
        fold = darken(coat, 0.79)
        for s in (-1, 1):
            line([(cx + s * bw(waist_y) * 0.30, waist_y + head_h * 0.24),
                  (cx + s * bw(waist_y) * 0.42, waist_y + (coat_hem - waist_y) * 0.55),
                  (cx + s * bw(hip_y) * 0.46, coat_hem - head_h * 0.10)], fold, 2)
        line([(cx, waist_y + head_h * 0.28),
              (cx + head_h * 0.02, waist_y + (coat_hem - waist_y) * 0.5),
              (cx, coat_hem - head_h * 0.14)], fold, 2)

    # ---- animal ears (rounded) ----
    if spec.get("ears"):
        for s in (-1, 1):
            bx = cx + s * hw * 0.80
            rpoly([(bx - head_w * 0.15, head_top + head_h * 0.06),
                   (bx - head_w * 0.06, head_top - head_h * 0.24),
                   (bx + s * head_w * 0.05, head_top - head_h * 0.54),
                   (bx + head_w * 0.10, head_top - head_h * 0.20),
                   (bx + head_w * 0.15, head_top + head_h * 0.06)], hair)
            if not flat and spec["ears"] == "fox":
                rpoly([(bx - head_w * 0.08, head_top - head_h * 0.10),
                       (bx, head_top - head_h * 0.38),
                       (bx + head_w * 0.08, head_top - head_h * 0.10)], accent)

    # ---- hat ----
    if spec.get("hat") in ("kasa", "veiled"):
        hcol = dark
        ell(cx - head_w * 1.42, head_top + head_h * 0.02, cx + head_w * 1.42,
            head_top + head_h * 0.30, hcol)
        rpoly([(cx - head_w * 0.60, head_top + head_h * 0.14),
               (cx - head_w * 0.40, head_top - head_h * 0.18),
               (cx, head_top - head_h * 0.46),
               (cx + head_w * 0.40, head_top - head_h * 0.18),
               (cx + head_w * 0.60, head_top + head_h * 0.14)], hcol)
        rpoly([(cx - head_w * 0.56, head_top - head_h * 0.01),
               (cx, head_top + head_h * 0.03),
               (cx + head_w * 0.56, head_top - head_h * 0.01),
               (cx + head_w * 0.56, head_top + head_h * 0.05),
               (cx, head_top + head_h * 0.09),
               (cx - head_w * 0.56, head_top + head_h * 0.05)], accent)
        if spec["hat"] == "veiled" and not flat:
            veil = Image.new("RGBA", img.size, (0, 0, 0, 0))
            ImageDraw.Draw(veil).polygon(
                [P(*p) for p in _catmull_closed([
                    (cx - head_w * 1.42, head_top + head_h * 0.20),
                    (cx - head_w * 1.30, head_top + head_h * 0.95),
                    (cx + head_w * 1.30, head_top + head_h * 0.95),
                    (cx + head_w * 1.42, head_top + head_h * 0.20)], 6)],
                fill=(30, 20, 45, 110))
            img = Image.alpha_composite(img, veil)
            d = ImageDraw.Draw(img)

    # ---- leaf (Nahida) ----
    if spec.get("leaf"):
        rpoly(almond(cx + head_w * 0.30, head_top - head_h * 0.04, cx + head_w * 0.58, head_top - head_h * 0.30, head_w * 0.07), accent)
        rpoly(almond(cx + head_w * 0.20, head_top - head_h * 0.12, cx + head_w * 0.44, head_top - head_h * 0.42, head_w * 0.06), accent)

    if flat:
        return img

    return ink_outline(img, width=2, scale=FS)


def sprite_figure(tag, expr):
    W_s, H_s = 700, 1120
    lay = render_figure(tag, expr).resize((W_s, H_s), Image.LANCZOS)
    spec = SPRITE_SPECS.get(tag, SPRITE_SPECS["wanderer"])
    accent = hx(spec["accent"])
    aura = Image.new("RGBA", (W_s, H_s), (0, 0, 0, 0))
    ad = ImageDraw.Draw(aura)
    ad.ellipse([W_s // 2 - 190, H_s - 90, W_s // 2 + 190, H_s - 10], fill=accent + (40,))
    aura = aura.filter(ImageFilter.GaussianBlur(28))
    return Image.alpha_composite(aura, lay)


def paste_figure(arr, tag, cx_frac, base_frac, h_frac, flat=None, expr="neutral", rotate=0):
    """Paste a scaled character (dark silhouette by default) onto a plate.

    Normally `base_frac` is where the feet rest. When `rotate` is non-zero the
    figure is turned (e.g. 90 for a body lying down) and `base_frac` becomes the
    figure's centre instead."""
    fig = render_figure(tag, expr, flat=flat)
    target_h = int(H * h_frac)
    target_w = max(1, int(fig.width * target_h / fig.height))
    fig = fig.resize((target_w, target_h), Image.LANCZOS)
    if rotate:
        fig = fig.rotate(rotate, expand=True, resample=Image.BICUBIC)
        x = int(W * cx_frac - fig.width / 2)
        y = int(H * base_frac - fig.height / 2)
    else:
        x = int(W * cx_frac - target_w / 2)
        y = int(H * base_frac - target_h)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    layer.alpha_composite(fig, (max(0, x), max(0, y)))
    return composite(arr, layer)


# ----------------------------------------------------------------------------
# Backgrounds
# ----------------------------------------------------------------------------

def bg_annex(variant):
    pal = {
        "night": (["#0b0b16", "#141428", "#1b1b32"], 0.0, "rain"),
        "predawn": (["#171a2c", "#242842", "#3a3c54"], 0.12, "rain"),
        "dawn": (["#3a3550", "#6b5b6e", "#c99a7a"], 0.35, "dust"),
        "day": (["#4b4a5c", "#6a6a78", "#9a9484"], 0.55, "dust"),
        "evening": (["#2a2334", "#3a2c3a", "#5a3f44"], 0.22, "dust"),
    }[variant]
    stops, warmth, kind = pal
    arr = vgrad(W, H, [(0.0, hx(stops[0])), (0.55, hx(stops[1])), (1.0, hx(stops[2]))])
    # back wall darkening + floor
    arr = composite(arr, shape(lambda d: d.polygon(S([(0, 470), (W, 440), (W, H), (0, H)]),
                                                   fill=(10, 9, 16, 235)), (10, 9, 16), 2))
    # shelves (vertical strips) left/right
    rnd = random.Random(11)
    lay = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for side in (-1, 1):
        x0 = 0 if side < 0 else W * 0.72
        for i in range(5):
            xx = (x0 + i * 70) * SS
            d.rectangle([xx, 60 * SS, (xx + 26 * SS), 470 * SS], fill=(7, 6, 12, 200))
            for r in range(4):
                yy = (110 + r * 95) * SS
                d.rectangle([xx - 4 * SS, yy, xx + 30 * SS, yy + 8 * SS], fill=(30, 26, 40, 160))
    arr = composite(arr, down(lay))
    # windows
    for (bx, warm) in ((0.30, True), (0.62, False)):
        box = (W * bx, 90, W * bx + 200, 430)
        wcol = (120, 130, 150) if variant in ("night", "predawn") else (200, 190, 170)
        arr = composite(arr, window_layer(box, wcol + (220,)))
        arr = add_glow(arr, (box[0] + box[2] - box[0]) / 2 + box[0] - (box[2] - box[0]) / 2,
                       (box[1] + box[3]) / 2, 260, wcol, 0.28 if variant in ("night", "predawn") else 0.5)
    # one lamp
    arr = add_glow(arr, W * 0.5, H * 0.72, 320, (230, 190, 120), 0.5)
    # rain / dust
    lay = particles(new_layer(), 260 if kind == "rain" else 160, 5, kind,
                    (170, 190, 210) if kind == "rain" else (230, 220, 190), 3.5)
    arr = composite(arr, down(lay))
    return finish(arr, 0.55, 7, 0.16, seed=hseed(variant) % 97)


def bg_courtyard():
    arr = vgrad(W, H, [(0.0, hx("#6fa0b8")), (0.5, hx("#a9c4c2")), (1.0, hx("#c9c6a4"))])
    arr = add_glow(arr, W * 0.7, H * 0.22, 420, (255, 240, 200), 0.55)
    arr = composite(arr, ridge_layer(430, 60, hx("#7f9aa0"), seed=2, bl=3))
    # Akademiya dome silhouette
    lay = new_layer(); d = ImageDraw.Draw(lay)
    d.ellipse([W * 0.36 * SS, 250 * SS, W * 0.64 * SS, 470 * SS], fill=hx("#4e6a68") + (255,))
    d.polygon(S([(W * 0.44, 300), (W * 0.56, 300), (W * 0.56, 470), (W * 0.44, 470)]),
              fill=hx("#3d5452") + (255,))
    arr = composite(arr, down(lay))
    arr = composite(arr, forest_layer(500, hx("#3e5a3a"), seed=4, count=18, bl=2.5))
    # big lotus leaves foreground
    lay = new_layer(); d = ImageDraw.Draw(lay)
    for i in range(6):
        x = W * (0.08 + i * 0.17)
        yy = H * 0.95 - (i % 2) * 40
        d.ellipse([x - 120 * SS, yy - 60 * SS, x + 120 * SS, yy + 60 * SS],
                  fill=hx("#2f5a3a") + (255,))
    arr = composite(arr, bl := down(lay))
    arr = composite(arr, ridge_layer(620, 40, hx("#223f28"), seed=6, bl=3))
    return finish(arr, 0.42, 6, 0.12, seed=21)


def bg_rooftop():
    arr = vgrad(W, H, [(0.0, hx("#050a1c")), (0.55, hx("#12203c")), (1.0, hx("#3a3550"))])
    # stars + milky way
    rnd = np.random.default_rng(3)
    for ch in range(3):
        arr[:, :, ch] += 0
    arr = add_glow(arr, W * 0.4, H * 0.28, 520, (120, 140, 210), 0.28, 1.4)
    stars = new_layer(); d = ImageDraw.Draw(stars)
    for _ in range(420):
        x = random.uniform(0, W) * SS; y = random.uniform(0, H * 0.62) * SS
        s = random.uniform(0.6, 2.2) * SS
        d.ellipse([x, y, x + s, y + s], fill=(240, 240, 255, random.randint(90, 230)))
    arr = composite(arr, down(stars))
    arr = add_glow(arr, W * 0.78, H * 0.16, 90, (255, 250, 230), 0.9)
    # city below
    arr = composite(arr, skyline_layer(560, hx("#0a1226"), seed=8, max_h=200, bl=2))
    for i in range(30):
        arr = add_glow(arr, random.uniform(0, W), random.uniform(560, 620), 10,
                       (240, 190, 110), 0.8)
    # parapet
    arr = composite(arr, shape(lambda d: d.polygon(S([(0, 600), (W, 590), (W, H), (0, H)]),
                                                   fill=(16, 14, 24, 255)), (16, 14, 24), 1.5))
    return finish(arr, 0.5, 4, 0.1, seed=34)


def bg_dining():
    arr = vgrad(W, H, [(0.0, hx("#3a2f28")), (0.6, hx("#4a3628")), (1.0, hx("#2a1f18"))])
    for bx in (0.12, 0.42, 0.72):
        arr = composite(arr, window_layer((W * bx, 80, W * bx + 150, 420), (250, 220, 170, 220)))
        arr = add_glow(arr, W * bx + 75, 250, 220, (250, 220, 170), 0.4)
    # long table
    arr = composite(arr, shape(lambda d: d.polygon(S([(0, 560), (W, 530), (W, 720), (0, 720)]),
                                                   fill=(64, 40, 26, 255)), (64, 40, 26), 1))
    for i in range(7):
        x = W * (0.08 + i * 0.13)
        arr = add_glow(arr, x, 540, 26, (255, 200, 120), 1.0)
    arr = composite(arr, down(particles(new_layer(), 120, 12, "dust", (255, 230, 190), 3)))
    return finish(arr, 0.5, 6, 0.14, seed=41)


def bg_corridor(snow=False):
    arr = vgrad(W, H, [(0.0, hx("#8fa0a8")), (1.0, hx("#4a5560"))])
    arr = composite(arr, shape(lambda d: d.polygon(S([(0, 90), (W, 60), (W, 660), (0, 690)]),
                                                   fill=(60, 66, 74, 200)), (60, 66, 74), 4))
    # receding arches
    for i in range(6):
        t = i / 6
        x = lerp(120, W * 0.5, t); rw = lerp(300, 60, t); y0 = lerp(120, 300, t); y1 = lerp(640, 480, t)
        arr = composite(arr, shape(lambda d, x=x, rw=rw, y0=y0, y1=y1: d.ellipse(
            [(x - rw / 2) * SS, y0 * SS, (x + rw / 2) * SS, y1 * SS], outline=(220, 225, 230, 120)),
            (220, 225, 230), 2))
    col = (235, 240, 245) if snow else (200, 210, 220)
    lay = particles(new_layer(), 300 if not snow else 220, 15, "snow" if snow else "rain", col, 3)
    arr = composite(arr, down(lay))
    # gold ink at the edges of the world
    eg = new_layer(); d = ImageDraw.Draw(eg)
    d.rectangle([20 * SS, 20 * SS, (W - 20) * SS, (H - 20) * SS], outline=GOLD + (90,), width=4 * SS)
    arr = composite(arr, blur(down(eg), 2))
    return finish(arr, 0.5, 5, 0.16, seed=52)


def bg_pavilion():
    arr = vgrad(W, H, [(0.0, hx("#2a2440")), (0.55, hx("#4a3f5a")), (1.0, hx("#6a5a58"))])
    arr = add_glow(arr, W * 0.5, H * 0.3, 460, (200, 180, 220), 0.4)
    arr = composite(arr, ridge_layer(430, 70, hx("#2a2440"), seed=17, bl=3))
    # pavilion posts + roof
    lay = new_layer(); d = ImageDraw.Draw(lay)
    roof = [(W * 0.28, 340), (W * 0.5, 250), (W * 0.72, 340)]
    d.polygon(S(roof), fill=hx("#171320") + (255,))
    for x in (0.33, 0.45, 0.55, 0.67):
        d.rectangle(S((W * x, 340, W * x + 12, 560)), fill=hx("#171320") + (255,))
    arr = composite(arr, down(lay))
    arr = composite(arr, down(particles(new_layer(), 140, 19, "snow", (230, 225, 240), 3)))
    return finish(arr, 0.55, 6, 0.18, seed=63)


def bg_furnace(variant):
    sky = {
        "dusk": [(0.0, hx("#3a1f1a")), (0.5, hx("#8a3f22")), (1.0, hx("#d9773a"))],
        "night": [(0.0, hx("#120a0a")), (0.5, hx("#3a1612")), (1.0, hx("#6a2a14"))],
        "morning": [(0.0, hx("#5a4a44")), (0.5, hx("#b08868")), (1.0, hx("#e0b483"))],
        "warped": [(0.0, hx("#2a0a0a")), (0.5, hx("#5a1010")), (1.0, hx("#8a1c14"))],
    }[variant]
    arr = vgrad(W, H, sky)
    arr = add_glow(arr, W * 0.55, H * 0.6, 520, (255, 120, 40), 0.5)
    # furnace mass
    lay = new_layer(); d = ImageDraw.Draw(lay)
    d.polygon(S([(W * 0.34, 220), (W * 0.68, 200), (W * 0.74, 660), (W * 0.28, 660)]),
              fill=(20, 12, 10, 255))
    d.rectangle(S((W * 0.44, 300, W * 0.58, 430)), fill=(255, 150, 60, 255))
    arr = composite(arr, down(lay))
    arr = add_glow(arr, W * 0.51, 365, 300, (255, 140, 50), 0.8)
    # worker silhouettes
    arr = composite(arr, down(particles(new_layer(), 60, 23, "ash", (40, 20, 16), 5)))
    if variant == "warped":
        arr = composite(arr, ink_edge_warp())
    if variant == "night":
        for i in range(8):
            arr = add_glow(arr, W * (0.1 + i * 0.11), 500, 16, (255, 200, 110), 1.0)
    return finish(arr, 0.55, 7, 0.14, seed=hseed(variant) % 89)


def ink_edge_warp():
    lay = new_layer(); d = ImageDraw.Draw(lay)
    for _ in range(60):
        x = random.uniform(0, W); y = random.uniform(0, H)
        d.arc([x * SS - 40 * SS, y * SS - 40 * SS, x * SS + 40 * SS, y * SS + 40 * SS],
              0, 360, fill=(120, 10, 10, 60), width=2 * SS)
    return blur(down(lay), 3)


def bg_furnace_room():
    arr = vgrad(W, H, [(0.0, hx("#1a0f0c")), (1.0, hx("#2e1a12"))])
    arr = composite(arr, shape(lambda d: d.rectangle(S((W * 0.1, 200, W * 0.9, 560)),
                                                     outline=(90, 60, 40, 200)), (90, 60, 40), 5))
    arr = add_glow(arr, W * 0.5, 400, 260, (255, 150, 70), 0.4)
    # crystal + brass device
    lay = new_layer(); d = ImageDraw.Draw(lay)
    d.rectangle(S((W * 0.42, 430, W * 0.58, 520)), fill=(120, 90, 40, 255))
    d.polygon(S([(W * 0.5, 380), (W * 0.55, 430), (W * 0.45, 430)]), fill=(150, 190, 220, 255))
    arr = composite(arr, down(lay))
    arr = add_glow(arr, W * 0.5, 400, 160, (150, 190, 220), 0.8)
    return finish(arr, 0.6, 6, 0.14, seed=71)


def bg_sickward():
    arr = vgrad(W, H, [(0.0, hx("#3a3a3c")), (1.0, hx("#1a1a1c"))])
    arr = fog_band(arr, 380, 140, (120, 120, 120), 0.5)
    lay = new_layer(); d = ImageDraw.Draw(lay)
    for i in range(5):
        x = W * (0.06 + i * 0.2)
        d.rectangle(S((x, 420, x + 150, 520)), fill=(60, 60, 64, 255))
        d.rectangle(S((x, 400, x + 40, 440)), fill=(80, 80, 84, 255))
    arr = composite(arr, blur(down(lay), 1.5))
    arr = composite(arr, down(particles(new_layer(), 150, 26, "ash", (210, 210, 210), 3)))
    return finish(arr, 0.55, 7, 0.16, seed=81)


def bg_shrine():
    arr = vgrad(W, H, [(0.0, hx("#1a0f22")), (0.6, hx("#3a1f3a")), (1.0, hx("#5a2a30"))])
    arr = add_glow(arr, W * 0.5, H * 0.3, 420, (200, 120, 160), 0.3)
    # torii
    lay = new_layer(); d = ImageDraw.Draw(lay)
    d.rectangle(S((W * 0.3, 260, W * 0.34, 600)), fill=CRIMSON + (255,))
    d.rectangle(S((W * 0.66, 260, W * 0.7, 600)), fill=CRIMSON + (255,))
    d.rectangle(S((W * 0.26, 250, W * 0.74, 272)), fill=CRIMSON + (255,))
    d.rectangle(S((W * 0.28, 300, W * 0.72, 318)), fill=CRIMSON + (255,))
    arr = composite(arr, down(lay))
    # steps
    arr = composite(arr, shape(lambda d: d.polygon(S([(W * 0.2, 600), (W * 0.8, 600), (W, 720), (0, 720)]),
                                                   fill=(40, 26, 30, 255)), (40, 26, 30), 1))
    arr = composite(arr, down(particles(new_layer(), 120, 29, "dust", (240, 200, 220), 3)))
    return finish(arr, 0.58, 6, 0.15, seed=91)


def bg_lab(variant):
    arr = vgrad(W, H, [(0.0, hx("#dfe4e8")), (1.0, hx("#aab2bc"))])
    if variant == "cube":
        arr = vgrad(W, H, [(0.0, hx("#20232c")), (1.0, hx("#0c0e14"))])
    lay = new_layer(); d = ImageDraw.Draw(lay)
    for i in range(8):
        x = W * (0.05 + i * 0.12)
        col = (120, 180, 220, 180) if variant != "cube" else (60, 90, 120, 160)
        d.rectangle(S((x, 120, x + 30, 520)), fill=col)
        if variant != "cube":
            arr = add_glow(arr, x + 15, 320, 120, (150, 200, 230), 0.5)
    arr = composite(arr, down(lay))
    # glass wall seams
    for i in range(4):
        arr = composite(arr, shape(lambda d, i=i: d.rectangle(
            S((W * (0.25 + i * 0.18), 60, W * (0.25 + i * 0.18) + 3, 660)),
            fill=(255, 255, 255, 60)), (255, 255, 255), 1))
    if variant == "flicker":
        arr = composite(arr, shape(lambda d: d.rectangle(S((0, 0, W, H)), fill=(120, 120, 140, 90)),
                                   (120, 120, 140), 8))
    return finish(arr, 0.4, 5, 0.1, seed=hseed(variant) % 79)


def bg_house(variant):
    stops = {
        "snow": [(0.0, hx("#26303f")), (0.55, hx("#4a5a68")), (1.0, hx("#dfe6ea"))],
        "dark": [(0.0, hx("#151a24")), (1.0, hx("#2a3040"))],
        "dawn": [(0.0, hx("#5a5a78")), (0.55, hx("#c98f7a")), (1.0, hx("#e6c9a0"))],
    }[variant]
    arr = vgrad(W, H, stops)
    ground = hx("#eef2f4") if variant != "dark" else hx("#3a4250")
    arr = composite(arr, shape(lambda d: d.polygon(S([(0, 520), (W, 500), (W, H), (0, H)]),
                                                   fill=ground + (255,)), ground, 2))
    # house
    lit = variant == "dawn" or variant == "dark"
    lay = new_layer(); d = ImageDraw.Draw(lay)
    d.rectangle(S((W * 0.34, 380, W * 0.66, 540)), fill=(60, 44, 36, 255))
    d.polygon(S([(W * 0.30, 380), (W * 0.5, 300), (W * 0.70, 380)]), fill=(40, 28, 24, 255))
    arr = composite(arr, down(lay))
    win_col = (255, 220, 140) if lit else (30, 34, 44)
    arr = composite(arr, window_layer((W * 0.45, 420, W * 0.55, 480), win_col + (255,), bar=False))
    if lit:
        arr = add_glow(arr, W * 0.5, 450, 160, (255, 210, 130), 0.7)
    arr = composite(arr, down(particles(new_layer(), 180 if variant == "snow" else 60, 31,
                                        "snow" if variant == "snow" else "dust", (240, 244, 248), 3)))
    return finish(arr, 0.5, 6, 0.14, seed=hseed(variant) % 71)


def bg_veranda():
    arr = vgrad(W, H, [(0.0, hx("#2a3240")), (0.6, hx("#6a7480")), (1.0, hx("#c9a878"))])
    arr = composite(arr, shape(lambda d: d.polygon(S([(0, 500), (W, 480), (W, H), (0, H)]),
                                                   fill=(70, 52, 40, 255)), (70, 52, 40), 1))
    # wooden posts + railing
    lay = new_layer(); d = ImageDraw.Draw(lay)
    for x in (0.12, 0.5, 0.88):
        d.rectangle(S((W * x, 120, W * x + 16, 520)), fill=(40, 30, 24, 255))
    d.rectangle(S((0, 380, W, 396)), fill=(40, 30, 24, 220))
    arr = composite(arr, down(lay))
    arr = add_glow(arr, W * 0.7, H * 0.25, 320, (255, 210, 150), 0.4)
    return finish(arr, 0.5, 6, 0.14, seed=101)


def bg_tatami():
    arr = vgrad(W, H, [(0.0, hx("#3a3226")), (1.0, hx("#6a5a40"))])
    arr = composite(arr, shape(lambda d: d.polygon(S([(0, 460), (W, 460), (W, H), (0, H)]),
                                                   fill=(150, 130, 80, 255)), (150, 130, 80), 1))
    # paper screens
    lay = new_layer(); d = ImageDraw.Draw(lay)
    for i in range(4):
        x = W * (0.08 + i * 0.22)
        d.rectangle(S((x, 90, x + 210, 460)), outline=(60, 50, 34, 200))
        d.rectangle(S((x + 100, 90, x + 110, 460)), fill=(70, 60, 44, 255))
    arr = composite(arr, down(lay))
    arr = composite(arr, shape(lambda d: d.rectangle(S((W * 0.36, 470, W * 0.64, 560)),
                                                     fill=(90, 80, 60, 255)), (90, 80, 60), 3))
    arr = add_glow(arr, W * 0.5, 300, 300, (230, 210, 160), 0.35)
    return finish(arr, 0.52, 6, 0.16, seed=111)


def bg_green_corridor():
    arr = vgrad(W, H, [(0.0, hx("#2a4038")), (1.0, hx("#16261f"))])
    for i in range(6):
        x = W * (0.1 + i * 0.14)
        arr = composite(arr, shape(lambda d, x=x: d.rectangle(
            S((x, 100, x + 90, 560)), fill=(40, 70, 60, 160)), (40, 70, 60), 6))
    arr = add_glow(arr, W * 0.5, 200, 360, (120, 180, 140), 0.3)
    return finish(arr, 0.5, 6, 0.14, seed=121)


def bg_akademiya_dawn():
    arr = vgrad(W, H, [(0.0, hx("#c9d2c0")), (0.55, hx("#e0e4cc")), (1.0, hx("#a9c4a0"))])
    arr = add_glow(arr, W * 0.3, H * 0.2, 420, (255, 250, 220), 0.6)
    arr = composite(arr, skyline_layer(430, hx("#4e7a5a"), seed=33, max_h=240, bl=2.5))
    # scholars silhouettes
    lay = new_layer(); d = ImageDraw.Draw(lay)
    for i in range(10):
        x = random.uniform(0, W) * SS
        y = random.uniform(470, 560) * SS
        d.ellipse([x - 6 * SS, y - 40 * SS, x + 6 * SS, y - 28 * SS], fill=(30, 50, 40, 200))
        d.rectangle([x - 8 * SS, y - 28 * SS, x + 8 * SS, y], fill=(30, 50, 40, 200))
    arr = composite(arr, down(lay))
    return finish(arr, 0.36, 5, 0.12, seed=131)


def bg_cinders():
    arr = vgrad(W, H, [(0.0, hx("#6a4520")), (0.5, hx("#8a5a28")), (1.0, hx("#241a14"))])
    arr = add_glow(arr, W * 0.5, H * 0.35, 480, (255, 170, 80), 0.35)
    arr = composite(arr, ridge_layer(430, 50, hx("#3a2416"), seed=35, bl=3))
    arr = composite(arr, shape(lambda d: d.polygon(S([(0, 520), (W, 500), (W, H), (0, H)]),
                                                   fill=(24, 18, 14, 255)), (24, 18, 14), 2))
    arr = composite(arr, down(particles(new_layer(), 120, 37, "ash", (60, 40, 30), 4)))
    return finish(arr, 0.55, 7, 0.15, seed=141)


def bg_white(variant):
    arr = np.full((H, W, 3), 245.0)
    if variant == "street":
        arr = vgrad(W, H, [(0.0, hx("#dfe4ea")), (1.0, hx("#f2f0e8"))])
        arr = composite(arr, skyline_layer(500, hx("#c2c8d0"), seed=41, max_h=260, bl=6))
    elif variant == "dark":
        arr = vgrad(W, H, [(0.0, hx("#e8e4da")), (1.0, hx("#6a6258"))])
        arr = composite(arr, shape(lambda d: d.rectangle(S((0, 0, W, H)), fill=(40, 30, 24, 120)),
                                   (40, 30, 24), 40))
    elif variant == "burn":
        arr = vgrad(W, H, [(0.0, hx("#2a1a10")), (0.5, hx("#b0622a")), (1.0, hx("#e8c27a"))])
        arr = composite(arr, down(particles(new_layer(), 200, 43, "ash", (40, 24, 16), 5)))
        arr = add_glow(arr, W * 0.5, H * 0.7, 520, (255, 140, 50), 0.5)
    elif variant == "stage":
        arr = np.full((H, W, 3), 14.0)
        arr = add_glow(arr, W * 0.5, H * 0.5, 300, (240, 235, 220), 0.8)
        arr = composite(arr, shape(lambda d: d.rectangle(S((W * 0.42, H * 0.24, W * 0.58, H * 0.78)),
                                                         fill=(240, 236, 224, 255)), (240, 236, 224), 2))
    return finish(arr, 0.3 if variant == "stage" else 0.25, 4, 0.05, seed=hseed(variant) % 61)


def bg_montage():
    arr = vgrad(W, H, [(0.0, hx("#5a5a62")), (1.0, hx("#8a7a60"))])
    for i in range(3):
        x0 = W * (0.05 + i * 0.32)
        arr = composite(arr, shape(lambda d, x0=x0: d.rectangle(
            S((x0, 140, x0 + 300, 540)), outline=(240, 236, 220, 200)), (240, 236, 220), 2))
        arr = add_glow(arr, x0 + 150, 340, 180, (200, 180, 120), 0.25)
    return finish(arr, 0.5, 6, 0.16, seed=151)


# ----------------------------------------------------------------------------
# CG plates
# ----------------------------------------------------------------------------

def cg_scene(scene_fn, *args, crash=0.30):
    """A full-bleed painterly scene used as the base of a CG plate."""
    return scene_fn(*args)


def cg_frame(arr, seed=1):
    arr = vignette(arr, 0.5)
    arr = paper_finish(arr, 0.12, seed)
    arr = grain(arr, 4, seed + 1)
    arr = ink_frame(np.clip(arr, 0, 255), 24, (18, 16, 24), 130)
    return arr


def _feather(arr, cx=W * 0.5, cy=H * 0.5, scale=1.0, color=GOLD):
    lay = new_layer(); d = ImageDraw.Draw(lay)
    d.line([(cx * SS, cy * SS - 180 * scale * SS), (cx * SS, cy * SS + 180 * scale * SS)],
           fill=color + (230,), width=3 * SS)
    for i in range(-6, 7):
        t = i / 6.0
        yy = cy + t * 160 * scale
        w = (1 - abs(t)) * 70 * scale
        d.line([(cx * SS, yy * SS), ((cx + w) * SS, (yy + 26 * scale) * SS)], fill=color + (150,), width=2 * SS)
        d.line([(cx * SS, yy * SS), ((cx - w) * SS, (yy + 26 * scale) * SS)], fill=color + (150,), width=2 * SS)
    return composite(arr, blur(down(lay), 0.6))


def _hand(arr, cx=W * 0.5, cy=H * 0.5, scale=1.0, color=(20, 18, 26), alpha=210):
    lay = new_layer(); d = ImageDraw.Draw(lay)
    d.rounded_rectangle([(cx - 50 * scale) * SS, (cy - 40 * scale) * SS,
                         (cx + 60 * scale) * SS, (cy + 120 * scale) * SS],
                        radius=40 * scale * SS, fill=color + (alpha,))
    for i in range(4):
        fx = cx - 40 * scale + i * 34 * scale
        d.rounded_rectangle([fx * SS, (cy - 130 * scale) * SS,
                             (fx + 24 * scale) * SS, (cy + 10 * scale) * SS],
                            radius=12 * scale * SS, fill=color + (alpha,))
    d.rounded_rectangle([(cx - 90 * scale) * SS, (cy - 10 * scale) * SS,
                         (cx - 40 * scale) * SS, (cy + 70 * scale) * SS],
                        radius=20 * scale * SS, fill=color + (alpha,))
    return composite(arr, down(lay))


def _case(arr, cx=W * 0.5, cy=H * 0.52, scale=1.0):
    base = cg_scene(bg_annex, "evening")
    base = composite(base, shape(lambda d: d.rectangle(S((0, 0, W, H)), fill=(10, 9, 16, 120)), (10, 9, 16), 20))
    lay = new_layer(); d = ImageDraw.Draw(lay)
    bw, bh = 340 * scale, 220 * scale
    d.rectangle([(cx - bw / 2) * SS, (cy - bh / 2) * SS, (cx + bw / 2) * SS, (cy + bh / 2) * SS],
                fill=(18, 17, 22, 255))
    d.rectangle([(cx - 30) * SS, (cy - bh / 2 - 6) * SS, (cx + 30) * SS, (cy - bh / 2 + 6) * SS],
                fill=GOLD + (255,))
    base = composite(base, down(lay))
    return base


def _lens(arr, cx=W * 0.5, cy=H * 0.5, scale=1.0):
    lay = new_layer(); d = ImageDraw.Draw(lay)
    r = 120 * scale
    d.ellipse([(cx - r) * SS, (cy - r) * SS, (cx + r) * SS, (cy + r) * SS], fill=VIOLET + (230,))
    d.ellipse([(cx - r * 0.5) * SS, (cy - r * 0.5) * SS,
               (cx + r * 0.3) * SS, (cy + r * 0.3) * SS], fill=(240, 230, 255, 200))
    d.line([(cx - r * 0.7) * SS, (cy + r * 0.9) * SS, (cx + r * 0.8) * SS, (cy + r * 0.5) * SS],
           fill=(90, 60, 120, 255), width=3 * SS)
    arr = composite(arr, down(lay))
    arr = add_glow(arr, cx, cy, r * 2.2, VIOLET, 0.5)
    return arr


def cg_plate(key):
    # Base scene selection per CG
    if key == "prologue_echo":
        arr = cg_scene(bg_annex, "night")
        arr = paste_figure(arr, "echo", 0.5, 1.02, 0.95, flat=SILHOUETTE)
        arr = _hand(arr, W * 0.5, H * 0.62, 1.3, (90, 60, 120), 200)
    elif key == "prologue_tea":
        arr = cg_scene(bg_annex, "evening")
        arr = add_glow(arr, W * 0.5, H * 0.55, 260, (240, 200, 140), 0.5)
    elif key == "folio_page":
        arr = cg_scene(bg_annex, "night")
        arr = composite(arr, shape(lambda d: d.rectangle(S((W * 0.36, H * 0.3, W * 0.64, H * 0.72)),
                                                         fill=(240, 236, 224, 235)), (240, 236, 224), 2))
    elif key == "first_page_burn":
        arr = bg_white("burn")
    elif key == "nahida_between":
        arr = cg_scene(bg_dining)
        arr = paste_figure(arr, "wanderer", 0.30, 1.0, 0.86, flat=SILHOUETTE)
        arr = paste_figure(arr, "echo", 0.70, 1.0, 0.86, flat=SILHOUETTE)
        arr = paste_figure(arr, "nahida", 0.50, 1.0, 0.66, flat=SILHOUETTE)
    elif key == "wanderer_soup":
        arr = cg_scene(bg_dining)
        arr = paste_figure(arr, "wanderer", 0.62, 1.0, 0.9, flat=SILHOUETTE)
        arr = composite(arr, shape(lambda d: d.ellipse(S((W * 0.28, H * 0.55, W * 0.44, H * 0.72)),
                                                       fill=(220, 200, 160, 255)), (220, 200, 160), 3))
    elif key == "margin_door":
        arr = cg_scene(bg_corridor)
    elif key == "gold_feather":
        arr = cg_scene(bg_annex, "night")
        arr = _feather(arr)
    elif key == "sword_dance":
        arr = cg_scene(bg_furnace, "night")
        arr = paste_figure(arr, "wanderer", 0.36, 1.0, 0.88, flat=SILHOUETTE)
        arr = paste_figure(arr, "echo", 0.64, 1.0, 0.88, flat=SILHOUETTE)
    elif key == "puppet_furnace":
        arr = cg_scene(bg_furnace, "warped")
        arr = paste_figure(arr, "wanderer", 0.5, 1.0, 0.9, flat=SILHOUETTE)
        arr = add_glow(arr, W * 0.5, H * 0.55, 300, (255, 200, 120), 0.6)
    elif key == "sleeping_puppet":
        arr = cg_scene(bg_tatami)
        arr = paste_figure(arr, "wanderer", 0.5, 0.74, 0.4, flat=SILHOUETTE, rotate=90)
        arr = add_glow(arr, W * 0.5, H * 0.55, 240, (255, 210, 150), 0.35)
    elif key == "raiden_yae":
        arr = cg_scene(bg_shrine)
        arr = paste_figure(arr, "ei", 0.40, 1.0, 0.92, flat=SILHOUETTE)
        arr = paste_figure(arr, "yae", 0.62, 1.0, 0.9, flat=SILHOUETTE)
        arr = add_glow(arr, W * 0.5, H * 0.32, 320, (205, 175, 240), 0.3)
    elif key == "niwa_note":
        arr = cg_scene(bg_furnace_room)
        arr = paste_figure(arr, "wanderer", 0.42, 1.0, 0.9, flat=SILHOUETTE)
        arr = composite(arr, shape(lambda d: d.rectangle(S((W * 0.34, H * 0.34, W * 0.66, H * 0.7)),
                                                         fill=(238, 232, 214, 240)), (238, 232, 214), 2))
    elif key == "child_drawing":
        arr = cg_scene(bg_house, "dawn")
        arr = composite(arr, shape(lambda d: d.rectangle(S((W * 0.3, H * 0.26, W * 0.7, H * 0.74)),
                                                         fill=(242, 236, 220, 240)), (242, 236, 220), 3))
        arr = paste_figure(arr, "wanderer", 0.5, 0.74, 0.34, flat=SILHOUETTE)
        arr = add_glow(arr, W * 0.62, H * 0.4, 90, (230, 170, 70), 0.6)
    elif key == "hooked_pinkies":
        arr = cg_scene(bg_house, "dawn")
        arr = _hand(arr, W * 0.42, H * 0.55, 0.9, (40, 26, 20), 210)
        arr = _hand(arr, W * 0.55, H * 0.52, 0.9, (40, 26, 20), 180)
    elif key == "empty_bed":
        arr = cg_scene(bg_house, "dawn")
        arr = composite(arr, shape(lambda d: d.rectangle(S((W * 0.32, H * 0.5, W * 0.68, H * 0.78)),
                                                         fill=(200, 196, 190, 255)), (200, 196, 190), 3))
    elif key == "black_case":
        arr = _case(cg_scene(bg_annex, "evening"))
    elif key == "gnosis_violet":
        arr = cg_scene(bg_annex, "night")
        arr = _lens(arr)
    elif key == "glass_cell":
        arr = cg_scene(bg_lab, "cube")
        arr = paste_figure(arr, "wanderer", 0.5, 1.0, 0.86, flat=SILHOUETTE)
        arr = composite(arr, shape(lambda d: d.polygon(
            S([(W * 0.22, H * 0.10), (W * 0.45, H * 0.10), (W * 0.30, H * 0.98), (W * 0.22, H * 0.98)]),
            fill=(185, 215, 245, 45)), (185, 215, 245), 4))
    elif key == "two_palms":
        arr = cg_scene(bg_lab, "cube")
        arr = _hand(arr, W * 0.44, H * 0.55, 1.1, (230, 230, 240), 200)
        arr = _hand(arr, W * 0.56, H * 0.55, 1.1, VIOLET, 170)
        arr = add_glow(arr, W * 0.5, H * 0.6, 120, (150, 200, 255), 0.8)
    elif key == "doctor_lane":
        arr = cg_scene(bg_akademiya_dawn)
        for i, fx in enumerate((0.18, 0.32, 0.82)):
            arr = paste_figure(arr, "dottore", fx, 1.0, 0.6, flat=SILHOUETTE)
        arr = paste_figure(arr, "dottore", 0.5, 1.02, 0.98, flat=SILHOUETTE)
    elif key == "echo_bowed":
        arr = cg_scene(bg_annex, "evening")
        arr = paste_figure(arr, "wanderer", 0.4, 1.0, 0.9, flat=SILHOUETTE)
        arr = paste_figure(arr, "echo", 0.6, 1.0, 0.82, flat=SILHOUETTE)
    elif key == "wanderer_echo_on_page":
        arr = bg_white("plain")
        arr = paste_figure(arr, "wanderer", 0.34, 0.98, 0.72, flat=SILHOUETTE)
        arr = paste_figure(arr, "echo", 0.66, 0.98, 0.72, flat=SILHOUETTE)
    elif key == "ending_wanderer":
        arr = cg_scene(bg_annex, "day")
        arr = _hand(arr, W * 0.5, H * 0.5, 1.1, (40, 30, 60), 130)
    elif key == "ending_scaramouche":
        arr = cg_scene(bg_annex, "day")
        arr = add_glow(arr, W * 0.5, H * 0.35, 200, (255, 220, 160), 0.6)
    elif key == "ending_true":
        arr = cg_scene(bg_annex, "day")
        arr = _feather(arr, W * 0.5, H * 0.3, 0.7)
    elif key == "folio_black":
        arr = cg_scene(bg_annex, "night")
        arr = composite(arr, shape(lambda d: d.rectangle(S((W * 0.38, H * 0.28, W * 0.62, H * 0.74)),
                                                         fill=(14, 13, 18, 255)), (14, 13, 18), 3))
    elif key == "margin_door_shut":
        arr = cg_scene(bg_corridor)
    elif key == "blank_dot":
        arr = bg_white("plain")
        arr = composite(arr, shape(lambda d: d.ellipse(S((W * 0.48, H * 0.48, W * 0.52, H * 0.52)),
                                                       fill=(30, 28, 34, 255)), (30, 28, 34), 1))
    else:
        arr = cg_scene(bg_annex, "night")
    return cg_frame(arr, seed=hseed(key) % 137)


# ----------------------------------------------------------------------------
# Registry
# ----------------------------------------------------------------------------

BACKGROUNDS = {
    "annex_night": lambda: bg_annex("night"),
    "annex_predawn": lambda: bg_annex("predawn"),
    "annex_dawn": lambda: bg_annex("dawn"),
    "annex_day": lambda: bg_annex("day"),
    "annex_evening": lambda: bg_annex("evening"),
    "courtyard_day": bg_courtyard,
    "rooftop_night": bg_rooftop,
    "dining_evening": bg_dining,
    "corridor_mist": lambda: bg_corridor(False),
    "corridor_mist_snow": lambda: bg_corridor(True),
    "shakkei_pavilion": bg_pavilion,
    "cinders_path": bg_cinders,
    "mikage_furnace": lambda: bg_furnace("dusk"),
    "furnace_yard_night": lambda: bg_furnace("night"),
    "furnace_morning": lambda: bg_furnace("morning"),
    "furnace_yard_warped": lambda: bg_furnace("warped"),
    "furnace_room": bg_furnace_room,
    "sickward": bg_sickward,
    "shrine_night": bg_shrine,
    "lab_white": lambda: bg_lab("white"),
    "lab_glasscube": lambda: bg_lab("cube"),
    "lab_flicker": lambda: bg_lab("flicker"),
    "small_house": lambda: bg_house("snow"),
    "small_house_dark": lambda: bg_house("dark"),
    "house_dawn": lambda: bg_house("dawn"),
    "veranda": bg_veranda,
    "tatami_room": bg_tatami,
    "green_corridor": bg_green_corridor,
    "akademiya_dawn": bg_akademiya_dawn,
    "montage": bg_montage,
    "white_page": lambda: bg_white("plain"),
    "white_page_street": lambda: bg_white("street"),
    "white_page_dark": lambda: bg_white("dark"),
    "white_page_burn": lambda: bg_white("burn"),
    "page_black_stage": lambda: bg_white("stage"),
}

CGS = {
    "prologue_echo", "prologue_tea", "folio_page", "first_page_burn",
    "nahida_between", "wanderer_soup", "margin_door", "gold_feather",
    "sword_dance", "puppet_furnace", "sleeping_puppet", "raiden_yae",
    "niwa_note", "child_drawing", "hooked_pinkies", "empty_bed",
    "black_case", "gnosis_violet", "glass_cell", "two_palms", "doctor_lane",
    "echo_bowed", "wanderer_echo_on_page", "ending_wanderer",
    "ending_scaramouche", "ending_true", "folio_black", "margin_door_shut",
    "blank_dot",
}

SPRITES = {
    "wanderer": ["neutral", "guarded", "smug", "flustered", "hurt", "soft", "tired"],
    "echo": ["sneer", "cold", "amused", "startled", "grieving", "shy", "smile"],
    "nahida": ["gentle", "serious", "mischievous", "sad"],
    "dottore": ["pleasant", "delighted", "cold", "fascinated"],
    "tighnari": ["neutral", "sly"],
    "cyno": ["neutral", "grinning"],
    "ei": ["neutral", "sad", "serious", "soft"],
    "yae": ["neutral", "amused", "smug", "serious"],
}

## Characters whose sprites come from hand-supplied expression sheets (sliced by
## tools/import_sheets.py) rather than this generator.  gen_sprites skips them so
## it cannot overwrite the imported art.  Pass `--only <tag>` to force-regenerate.
SHEET_CHARS = {"wanderer", "echo", "nahida", "dottore", "tighnari", "cyno",
               "ei", "yae"}


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

def save(arr, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB").save(path, optimize=True)


def save_webp(arr, path, quality=87):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB").save(
        path, format="WEBP", quality=quality, method=5)


def gen_backgrounds(only):
    out = os.path.join(IMAGES, "bg")
    for key, fn in BACKGROUNDS.items():
        if only and key not in only and ("bg_" + key) not in only:
            continue
        random.seed("bg:" + key)
        arr = fn()
        save_webp(arr, os.path.join(out, key + ".webp"))
        print("bg   ", key)


def gen_cgs(only):
    out = os.path.join(IMAGES, "cg")
    for key in sorted(CGS):
        if only and key not in only and ("cg_" + key) not in only:
            continue
        random.seed("cg:" + key)
        save_webp(cg_plate(key), os.path.join(out, key + ".webp"))
        print("cg   ", key)


def gen_sprites(only):
    out = os.path.join(IMAGES, "sprites")
    for tag, exps in SPRITES.items():
        if tag in SHEET_CHARS and not (only and tag in only):
            print("spr   (skip, sheet-based)", tag)
            continue
        for exp in exps:
            if only and ("%s_%s" % (tag, exp)) not in only and tag not in only:
                continue
            random.seed("sp:%s:%s" % (tag, exp))
            img = sprite_figure(tag, exp)
            os.makedirs(out, exist_ok=True)
            img.save(os.path.join(out, "%s_%s.png" % (tag, exp)), optimize=True)
            print("spr  ", tag, exp)


def montage():
    thumbs = []
    out = os.path.join(ROOT, "tools", "out")
    os.makedirs(out, exist_ok=True)
    items = []
    for key in BACKGROUNDS:
        p = os.path.join(IMAGES, "bg", key + ".webp")
        if os.path.exists(p):
            items.append(("BG " + key, Image.open(p)))
    for key in sorted(CGS):
        p = os.path.join(IMAGES, "cg", key + ".webp")
        if os.path.exists(p):
            items.append(("CG " + key, Image.open(p)))
    cols = 5
    tw, th = 256, 144
    rows = (len(items) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw, rows * (th + 16)), (30, 30, 38))
    d = ImageDraw.Draw(sheet)
    for i, (label, im) in enumerate(items):
        im = im.convert("RGB").resize((tw, th))
        x = (i % cols) * tw
        y = (i // cols) * (th + 16)
        sheet.paste(im, (x, y))
        d.text((x + 4, y + th + 2), label[:34], fill=(230, 230, 230))
    path = os.path.join(out, "montage.png")
    sheet.save(path)
    print("montage ->", path)


def emit_rpy():
    """Write game/images.rpy listing every generated image."""
    lines = [
        "################################################################################",
        "## Twice-Told Tale - Image Definitions",
        "################################################################################",
        "##",
        "## AUTO-GENERATED by tools/make_art.py. Do not edit by hand; re-run",
        "## `python3 tools/make_art.py --rpy` after changing the art registry.",
        "##",
        "## Each image is a procedurally generated, copyright-free plate in a",
        "## consistent ink-and-paper style. Replace any file with hand-drawn art of",
        "## the same name to override it. See ASSETS.md for specifications.",
        "",
        "## ---- Backgrounds -----------------------------------------------------------",
        "",
    ]
    for key in BACKGROUNDS:
        lines.append('image bg %s = "images/bg/%s.webp"' % (key, key))
    lines += ["", "## ---- CG illustrations ------------------------------------------------------", ""]
    for key in sorted(CGS):
        lines.append('image cg %s = "images/cg/%s.webp"' % (key, key))
    lines += ["", "## ---- Character sprites -----------------------------------------------------", ""]
    for tag, exps in SPRITES.items():
        for exp in exps:
            lines.append('image %s %s = "images/sprites/%s_%s.png"' % (tag, exp, tag, exp))
    lines.append("")
    path = os.path.join(ROOT, "game", "images.rpy")
    with open(path, "w") as f:
        f.write("\n".join(lines))
    print("rpy  ->", path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", default=None)
    ap.add_argument("--montage", action="store_true")
    ap.add_argument("--bg", action="store_true")
    ap.add_argument("--cg", action="store_true")
    ap.add_argument("--sprites", action="store_true")
    ap.add_argument("--rpy", action="store_true")
    args = ap.parse_args()

    only = set(args.only) if args.only else None
    do_all = not (args.bg or args.cg or args.sprites)
    if do_all or args.bg:
        gen_backgrounds(only)
    if do_all or args.cg:
        gen_cgs(only)
    if do_all or args.sprites:
        gen_sprites(only)
    if args.rpy or do_all:
        emit_rpy()
    if args.montage:
        montage()


if __name__ == "__main__":
    main()
