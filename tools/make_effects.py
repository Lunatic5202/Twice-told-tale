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
##
## Everything is deterministic and copyright-free. Re-run after editing:
##
##     python3 tools/make_effects.py
##
## The wipe masks are consumed by the ImageDissolve transitions in
## game/animations.rpy.

import os

import numpy as np
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
GUI = os.path.join(ROOT, "game", "gui")
MASK = os.path.join(GUI, "mask")

W, H = 1280, 720


def save_l(arr, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    Image.fromarray(arr.astype("uint8"), mode="L").save(path, optimize=True)
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


def main():
    save_l(linear_lr(), os.path.join(MASK, "wipe_lr.png"))
    save_l(linear_tb(), os.path.join(MASK, "wipe_tb.png"))
    save_l(linear_diag(), os.path.join(MASK, "wipe_diag.png"))
    save_l(radial(), os.path.join(MASK, "wipe_radial.png"))


if __name__ == "__main__":
    main()
