#!/usr/bin/env python3
"""Generate the placeholder GUI artwork used by the interface polish layer.

Run from the project root:

    python3 tools/make_gui_assets.py

This writes (all paths relative to game/gui/):

    cursor/pen_N.png          animated ink-nib pointer (N = 0..3)
    cursor/pen_hover_N.png    glowing variant for hover states
    mask/ink_dissolve.png     256-grey mask (1280x720) for the ink-dissolve transition
    overlay/vignette.png      soft dark vignette, 1280x720
    overlay/grain.png         tileable film grain, 256x256
    overlay/ink_blot.png      soft ink splotches for menu decoration
    overlay/bar_top.png       cinematic letterbox bar, 1280x130 (bar_bottom mirrors it)
    overlay/rule_gold.png     gold flourish rule that fades out at both ends
    overlay/page_border.png   thin gold double-rule border for a resizable Frame
    particle/rain.png         falling-rain streak sprite
    particle/snow.png         soft snowflake sprite
    particle/ember.png        glowing ember sprite
    particle/leaf.png         drifting leaf sprite

Everything here is meant to be replaced by a real artist. The generator keeps
the game looking intentional until then, and re-running it is harmless.
"""

import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
GUI = os.path.normpath(os.path.join(HERE, "..", "game", "gui"))

RES = (1280, 720)
CURSOR_SIZE = 32
CURSOR_FRAMES = 4


def ensure(*parts):
    path = os.path.join(GUI, *parts)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path


def draw_pen(glow=False, frame=0):
    """An upright fountain-pen nib, ~90px tall on a square canvas."""
    s = 96
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx = s // 2

    body = (26, 26, 40, 255)
    body_edge = (8, 8, 18, 255)
    gold = (214, 178, 94, 255)
    nib = (255, 248, 214, 255) if glow else (230, 218, 194, 255)
    nib_edge = (52, 42, 26, 255)

    if glow:
        halo = Image.new("RGBA", (s, s), (0, 0, 0, 0))
        hd = ImageDraw.Draw(halo)
        hd.polygon([(cx, 4), (cx - 15, 54), (cx + 15, 54)], fill=(120, 220, 220, 200))
        hd.rectangle([cx - 15, 54, cx + 15, s - 2], fill=(120, 220, 220, 160))
        halo = halo.filter(ImageFilter.GaussianBlur(5))
        img = Image.alpha_composite(halo, img)
        d = ImageDraw.Draw(img)

    d.polygon([(cx, 6), (cx - 11, 52), (cx + 11, 52)], fill=nib, outline=nib_edge)
    d.line([(cx, 10), (cx, 46)], fill=(70, 58, 38, 255), width=2)
    d.ellipse([cx - 3, 36, cx + 3, 42], fill=(70, 58, 38, 255))
    d.rectangle([cx - 11, 52, cx + 11, 58], fill=gold)
    d.rectangle([cx - 11, 58, cx + 11, s - 4], fill=body, outline=body_edge)

    gx = cx - 7 + frame * 4
    d.ellipse([gx - 2, 18, gx + 2, 22], fill=(255, 255, 245, 230))

    return img


def finalize_cursor(img, size=CURSOR_SIZE, tip_at=(1, 1)):
    """Rotate the nib to point up-left, trim it, and pin the tip to `tip_at`."""
    rot = img.rotate(45, resample=Image.BICUBIC, expand=True)
    bbox = rot.getbbox()
    cropped = rot.crop(bbox)

    scale = (size - 3) / max(cropped.size)
    new_size = (max(1, round(cropped.width * scale)), max(1, round(cropped.height * scale)))
    cropped = cropped.resize(new_size, Image.LANCZOS)

    # The tip is the topmost opaque pixel after the rotation.
    alpha = np.array(cropped.getchannel("A"))
    ys, xs = np.nonzero(alpha)
    tip = (xs[ys.argmin()], ys.min())

    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    canvas.alpha_composite(cropped, (tip_at[0] - tip[0], tip_at[1] - tip[1]))
    return canvas


def make_cursors():
    for frame in range(CURSOR_FRAMES):
        for glow, suffix in ((False, ""), (True, "_hover")):
            pen = draw_pen(glow=glow, frame=frame)
            cur = finalize_cursor(pen)
            cur.save(ensure("cursor", "pen%s_%d.png" % (suffix, frame)))
    print("cursors: %d frames x2 states" % CURSOR_FRAMES)


def make_vignette():
    w, h = RES
    yy, xx = np.mgrid[0:h, 0:w]
    nx = (xx - w / 2) / (w / 2)
    ny = (yy - h / 2) / (h / 2)
    dist = np.sqrt(nx * nx + ny * ny)
    alpha = np.clip((dist - 0.55) / 0.85, 0, 1) ** 1.6
    alpha = (alpha * 205).astype(np.uint8)

    out = np.zeros((h, w, 4), dtype=np.uint8)
    out[..., 3] = alpha
    Image.fromarray(out, "RGBA").save(ensure("overlay", "vignette.png"))
    print("vignette: %dx%d" % RES)


def make_grain():
    rng = np.random.default_rng(7)
    n = 256
    gray = rng.integers(0, 256, (n, n), dtype=np.uint8)
    out = np.zeros((n, n, 4), dtype=np.uint8)
    out[..., 0] = gray
    out[..., 1] = gray
    out[..., 2] = gray
    out[..., 3] = 18
    Image.fromarray(out, "RGBA").save(ensure("overlay", "grain.png"))
    print("grain: %dx%d" % (n, n))


def make_ink_mask():
    rng = np.random.default_rng(3)
    # An ImageDissolve mask must match the scene size, or the dissolve only
    # advances across the top-left corner of the frame. Keep the noise source
    # at the same 16:9 aspect so the grain does not stretch.
    small = rng.random((36, 64))
    im = Image.fromarray((small * 255).astype(np.uint8), "L")
    im = im.resize(RES, Image.BICUBIC).filter(ImageFilter.GaussianBlur(2.5))
    im.save(ensure("mask", "ink_dissolve.png"))
    print("ink mask: %dx%d" % RES)


def make_ctc_drop():
    """A small ink droplet used as the click-to-continue marker."""
    s = 40
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([11, 16, 29, 34], fill=(240, 234, 220, 255))
    d.polygon([(20, 5), (11, 20), (29, 20)], fill=(240, 234, 220, 255))
    d.ellipse([17, 21, 23, 27], fill=(150, 190, 195, 255))
    img.save(ensure("overlay", "ctc_drop.png"))
    print("ctc drop: %dx%d" % (s, s))


def make_ink_blot():
    rng = np.random.default_rng(11)
    s = 1024
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for _ in range(14):
        cx, cy = rng.integers(60, s - 60, 2)
        r = int(rng.integers(40, 150))
        col = tuple(int(v) for v in rng.integers(20, 55, 3)) + (int(rng.integers(40, 110)),)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    img = img.filter(ImageFilter.GaussianBlur(24))
    # Fade the blot out toward the edges so it tiles into the frame cleanly.
    arr = np.array(img, dtype=np.float32)
    yy, xx = np.mgrid[0:s, 0:s]
    edge = np.minimum.reduce([xx, yy, s - 1 - xx, s - 1 - yy]) / (s * 0.18)
    fade = np.clip(edge, 0, 1)
    arr[..., 3] *= fade
    Image.fromarray(arr.astype(np.uint8), "RGBA").save(ensure("overlay", "ink_blot.png"))
    print("ink blot: %dx%d" % (s, s))


def make_letterbox():
    """Soft cinematic letterbox bars: solid at the frame edge, fading out
    inward. bar_top.png and bar_bottom.png are the same bar mirrored."""
    w, _ = RES
    h = 130
    yy = np.arange(h)[:, None].astype(np.float32) / (h - 1)
    alpha = np.clip(1.0 - yy * 1.35, 0, 1) ** 1.5
    alpha = (alpha * 240).astype(np.uint8)

    out = np.zeros((h, w, 4), dtype=np.uint8)
    out[..., 3] = np.broadcast_to(alpha, (h, w)).copy()

    Image.fromarray(out, "RGBA").save(ensure("overlay", "bar_top.png"))
    Image.fromarray(out[::-1], "RGBA").save(ensure("overlay", "bar_bottom.png"))
    print("letterbox bars: %dx%d" % (w, h))


def make_gold_rule():
    """A thin gold rule that fades out at both ends - used as a flourish under
    titles and scene cards."""
    w = 720
    h = 3
    xx = np.arange(w)[None, :].astype(np.float32) / (w - 1)
    alpha = np.clip(np.sin(xx * math.pi), 0.0, 1.0) ** 0.85

    out = np.zeros((h, w, 4), dtype=np.uint8)
    out[..., 0] = 214
    out[..., 1] = 178
    out[..., 2] = 94
    out[..., 3] = (alpha * 235).astype(np.uint8)

    Image.fromarray(out, "RGBA").save(ensure("overlay", "rule_gold.png"))
    print("gold rule: %dx%d" % (w, h))


def make_page_border():
    """A thin gold double-rule border with corner ticks, built to be used as a
    Ren'Py Frame: the corners are preserved and the straight edges stretch to
    fit any panel size (see weather.rpy / screens.rpy). The centre is fully
    transparent so the border can frame whatever is behind it."""
    unit = 48          # distance preserved at each corner
    size = unit * 3
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    gold = (214, 178, 94, 190)
    faint = (214, 178, 94, 90)
    inset = 6
    far = size - 1 - inset

    # Outer rule.
    d.rectangle([inset, inset, far, far], outline=gold, width=1)
    # Inner rule, a few pixels in.
    d.rectangle([inset + 5, inset + 5, far - 5, far - 5], outline=faint, width=1)

    # Corner ticks that overlap both rules.
    tick = 12
    for cx, cy, sx, sy in ((inset, inset, 1, 1),
                           (far, inset, -1, 1),
                           (inset, far, 1, -1),
                           (far, far, -1, -1)):
        d.line([(cx, cy), (cx + sx * tick, cy)], fill=gold, width=1)
        d.line([(cx, cy), (cx, cy + sy * tick)], fill=gold, width=1)

    img.save(ensure("overlay", "page_border.png"))
    print("page border: %dx%d (Frame %d)" % (size, size, unit))


def _radial(size, cut=1.0, power=1.0):
    """A soft radial falloff: 1.0 at the centre, fading to 0 at `cut` of the
    way to the corner."""
    c = (size - 1) / 2.0
    yy, xx = np.mgrid[0:size, 0:size]
    dist = np.sqrt((xx - c) ** 2 + (yy - c) ** 2) / c
    return np.clip((cut - dist) / cut, 0, 1) ** power


def make_rain():
    """A short vertical streak, bright at the middle and tapered at the tips."""
    w, h = 5, 56
    along = np.clip(np.sin(np.linspace(0, 1, h)[:, None] * math.pi), 0, 1) ** 0.6
    across = np.exp(-(np.linspace(-1, 1, w)[None, :] ** 2) * 6.0)
    alpha = along * across

    out = np.zeros((h, w, 4), dtype=np.uint8)
    out[..., 0] = 200
    out[..., 1] = 218
    out[..., 2] = 228
    out[..., 3] = (alpha * 165).astype(np.uint8)

    im = Image.fromarray(out, "RGBA").filter(ImageFilter.GaussianBlur(0.7))
    im.save(ensure("particle", "rain.png"))
    print("rain sprite: %dx%d" % (w, h))


def make_snow():
    s = 14
    out = np.zeros((s, s, 4), dtype=np.uint8)
    out[..., 0] = 245
    out[..., 1] = 246
    out[..., 2] = 250
    out[..., 3] = (_radial(s, 0.92, 1.3) * 235).astype(np.uint8)

    im = Image.fromarray(out, "RGBA").filter(ImageFilter.GaussianBlur(1.0))
    im.save(ensure("particle", "snow.png"))
    print("snow sprite: %dx%d" % (s, s))


def make_ember():
    """A warm dot: a bright core inside a soft halo."""
    s = 11
    core = _radial(s, 0.55, 0.6)
    halo = _radial(s, 1.0, 1.1)
    alpha = np.clip(core + halo * 0.55, 0, 1)

    out = np.zeros((s, s, 4), dtype=np.uint8)
    out[..., 0] = 255
    out[..., 1] = 152
    out[..., 2] = 64
    out[..., 3] = (alpha * 240).astype(np.uint8)

    im = Image.fromarray(out, "RGBA").filter(ImageFilter.GaussianBlur(0.7))
    im.save(ensure("particle", "ember.png"))
    print("ember sprite: %dx%d" % (s, s))


def make_leaf():
    """A small, slightly irregular leaf with a darker midrib."""
    s = 20
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.polygon([(10, 2), (14, 7), (15, 13), (10, 18), (5, 13), (6, 7)],
              fill=(150, 168, 96, 225))
    d.line([(10, 4), (10, 16)], fill=(92, 106, 56, 220), width=1)
    img = img.rotate(24, resample=Image.BICUBIC, expand=False)
    img.save(ensure("particle", "leaf.png"))
    print("leaf sprite: %dx%d" % (s, s))


def make_particles():
    make_rain()
    make_snow()
    make_ember()
    make_leaf()


def main():
    make_cursors()
    make_vignette()
    make_grain()
    make_ink_mask()
    make_ctc_drop()
    make_ink_blot()
    make_letterbox()
    make_gold_rule()
    make_page_border()
    make_particles()


if __name__ == "__main__":
    main()
