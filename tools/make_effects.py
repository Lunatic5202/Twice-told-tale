#!/usr/bin/env python3
################################################################################
## Twice-Told Tale - Effect Asset Generator
################################################################################
##
## Generates the small support textures used by the animation/transition layer:
##
##   game/gui/mask/wipe_lr.png       linear wipe mask (left -> right)
##   game/gui/mask/wipe_tb.png       linear wipe mask (top -> bottom)
##   game/gui/mask/wipe_diag.png     linear wipe mask (diagonal)
##   game/gui/mask/wipe_radial.png   radial wipe mask (centre -> edge)
##   game/gui/overlay/mote.png       soft glowing dust mote
##   game/gui/overlay/fiber.png      short drifting fibre / ash streak
##
## Everything is deterministic and copyright-free. Re-run after editing:
##
##     python3 tools/make_effects.py
##
## The wipe masks are consumed by the ImageDissolve transitions in
## game/animations.rpy; the motes by the ambience overlay in the same file.

import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
GUI = os.path.join(ROOT, "game", "gui")
MASK = os.path.join(GUI, "mask")
OVERLAY = os.path.join(GUI, "overlay")

W, H = 1280, 720


def save_l(arr, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    Image.fromarray(arr.astype("uint8"), mode="L").save(path, optimize=True)
    print("wrote", os.path.relpath(path, ROOT))


def save_rgba(im, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im.save(path, optimize=True)
    print("wrote", os.path.relpath(path, ROOT))


def linear_lr():
    g = np.linspace(0, 255, W, dtype=np.float64)
    return np.tile(g, (H, 1))


def linear_tb():
    g = np.linspace(0, 255, H, dtype=np.float64)
    return np.tile(g[:, None], (1, W))


def linear_diag():
    yy, xx = np.mgrid[0:H, 0:W]
    t = (xx / W + yy / H) / 2.0
    return t * 255.0


def radial():
    yy, xx = np.mgrid[0:H, 0:W]
    cx, cy = W / 2.0, H / 2.0
    # Normalise so the corners sit at 0 and the centre at 255.
    d = np.sqrt(((xx - cx) / cx) ** 2 + ((yy - cy) / cy) ** 2) / np.sqrt(2.0)
    v = np.clip(1.0 - d, 0.0, 1.0)
    return (v ** 0.85) * 255.0


def make_mote(size=64, warm=(255, 246, 226)):
    """A soft round glow with a bright core."""
    yy, xx = np.mgrid[0:size, 0:size]
    c = (size - 1) / 2.0
    d = np.sqrt((xx - c) ** 2 + (yy - c) ** 2) / c
    core = np.clip(1.0 - d, 0.0, 1.0) ** 2.4
    halo = np.clip(1.0 - d * 0.7, 0.0, 1.0) ** 1.6 * 0.45
    a = np.clip(core + halo, 0.0, 1.0)
    rgba = np.zeros((size, size, 4), dtype=np.float64)
    rgba[..., 0] = warm[0]
    rgba[..., 1] = warm[1]
    rgba[..., 2] = warm[2]
    rgba[..., 3] = a * 255.0
    return Image.fromarray(rgba.astype("uint8"), mode="RGBA")


def make_fiber(w=56, h=10, warm=(240, 230, 210)):
    """A short soft streak, like a drifting fibre or fleck of ash."""
    ss = 4
    yy, xx = np.mgrid[0:h * ss, 0:w * ss]
    cx, cy = (w * ss) / 2.0, (h * ss) / 2.0
    dx = (xx - cx) / cx
    dy = (yy - cy) / cy
    body = np.clip(1.0 - np.sqrt(dx ** 2 * 0.15 + dy ** 2 * 3.2), 0.0, 1.0)
    a = np.clip(body, 0.0, 1.0) ** 1.5
    rgba = np.zeros((h * ss, w * ss, 4), dtype=np.float64)
    rgba[..., 0] = warm[0]
    rgba[..., 1] = warm[1]
    rgba[..., 2] = warm[2]
    rgba[..., 3] = a * 255.0
    im = Image.fromarray(rgba.astype("uint8"), mode="RGBA").resize((w, h), Image.LANCZOS)
    return im.filter(ImageFilter.GaussianBlur(0.4))


def main():
    save_l(linear_lr(), os.path.join(MASK, "wipe_lr.png"))
    save_l(linear_tb(), os.path.join(MASK, "wipe_tb.png"))
    save_l(linear_diag(), os.path.join(MASK, "wipe_diag.png"))
    save_l(radial(), os.path.join(MASK, "wipe_radial.png"))

    save_rgba(make_mote(), os.path.join(OVERLAY, "mote.png"))
    save_rgba(make_fiber(), os.path.join(OVERLAY, "fiber.png"))


if __name__ == "__main__":
    main()
