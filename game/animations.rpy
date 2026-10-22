################################################################################
## Twice-Told Tale - Animation & Transition Layer
################################################################################
##
## A single home for the "feel" of the game: extra transitions built from the
## generated wipe masks, the slow camera moves applied automatically to every
## background and CG, and the drifting dust that keeps the frame alive.
##
## Nothing here is required for the story to run; remove the file and the game
## falls back to the stock dissolves defined in gui_effects.rpy.

init offset = -1


## ----------------------------------------------------------------------------
## Transitions
## ----------------------------------------------------------------------------
## Textured, ink-flavoured transitions. `ImageDissolve` reveals the new scene
## through a mask, so the wipes below read as ink bleeding through paper rather
## than a plain fade.

define ink_wipe = ImageDissolve("gui/mask/ink_dissolve.png", 1.1, ramplen=16)
define paper_dissolve = ImageDissolve("gui/mask/ink_dissolve.png", 0.85, ramplen=4)
define soft_dissolve = ImageDissolve("gui/mask/ink_dissolve.png", 0.45, ramplen=2)

define lr_wipe = ImageDissolve("gui/mask/wipe_lr.png", 0.7, ramplen=8)
define rl_wipe = ImageDissolve("gui/mask/wipe_lr.png", 0.7, ramplen=8, reverse=True)
define tb_wipe = ImageDissolve("gui/mask/wipe_tb.png", 0.7, ramplen=8)
define bt_wipe = ImageDissolve("gui/mask/wipe_tb.png", 0.7, ramplen=8, reverse=True)
define diag_wipe = ImageDissolve("gui/mask/wipe_diag.png", 0.8, ramplen=8)

## A circular reveal out of, and into, the dark.
define circle_open = ImageDissolve("gui/mask/wipe_radial.png", 0.9, ramplen=8)
define circle_close = ImageDissolve("gui/mask/wipe_radial.png", 0.9, ramplen=8, reverse=True)

define ash_fade = Fade(0.45, 0.1, 0.6, color="#0a0a14")
define bloom_dissolve = Dissolve(0.7)

## Plain cross-fades at three weights: a quick expression swap, the house
## default, and a long reflective one.  The stock `dissolve`/`fade` remain
## available too; these just name the weights the script actually uses.
define quick_dissolve = Dissolve(0.25)
define slow_dissolve = Dissolve(0.9)
define deep_fade = Fade(0.6, 0.25, 0.7, color="#0a0a14")

## Reveals.  `blinds` lifts a scene in venetian slats, `squares_wipe`
## assembles it from a checkerboard - both read as a page being drawn rather
## than dipped.  `iris_open`/`iris_shut` open and close a circular lens for
## moments that narrow to a single detail.
define door_blinds = ImageDissolve(Tile("blindstile.png"), 0.9, 8)
define squares_wipe = ImageDissolve(Tile("squarestile.png"), 0.9, 256)
define iris_open = CropMove(0.7, "irisin")
define iris_shut = CropMove(0.7, "irisout")

## Lateral moves.  Used where the story travels - a corridor, a page turned
## sideways - so the new plate pushes the old one off in the direction of travel.
define slide_left = PushMove(0.6, "pushleft")
define slide_right = PushMove(0.6, "pushright")

## Camera punches.  These shake every layer at once, so a blow or a crash
## reads as the camera taking the hit, not just the sprite.  `hpunch`/`vpunch`
## are Ren'Py's own quarter-second shakes; `shake`/`quake`/`jolt` are longer,
## stronger variants for impacts that should rattle the whole frame.
define shake = Move((0, 7), (0, -7), 0.05, bounce=True, repeat=True, delay=0.30)
define quake = Move((0, 16), (0, -16), 0.05, bounce=True, repeat=True, delay=0.55)
define jolt = Move((-22, 0), (22, 0), 0.05, bounce=True, repeat=True, delay=0.42)


## ----------------------------------------------------------------------------
## Slow camera moves
## ----------------------------------------------------------------------------
## These are attached to whole image tags (see the registration at the bottom of
## this file) so every background drifts and every CG pushes in on its own.

## Motion amounts. These are store variables (not constants) so the "Reduce
## Motion" preference can flatten them at runtime; see _apply_motion() below.
##
## The zooms sit a little above 1.0 on purpose: the camera drifts a few pixels
## sideways, and the extra margin keeps the frame edge covered while it moves.
define KEN_ZOOM = 1.03
define KEN_ZOOM2 = 1.05
define KEN_OX = 8
define KEN_OY = 6
define CG_ZOOM = 1.0
define CG_ZOOM2 = 1.03
define BREATHE_ZOOM = 0.009
define BREATHE_LIFT = 3
define TITLE_ZOOM = 1.02
define TITLE_ZOOM2 = 1.03
define TITLE_OX = 8

## Character sprites are drawn on a 700x1120 canvas - taller than the 720px
## screen - so they must be scaled down to stand fully on the bottom edge.
## This is a fit constant, not a motion amount, so Reduce Motion leaves it alone.
define SPRITE_ZOOM = 0.63

init python:

    ## A plate always fills the frame.
    ##
    ## The picture is fitted inside the frame; behind it sits a heavily blurred
    ## copy of the same picture, blown up to cover. A plate that is not 16:9
    ## therefore shows blurred margins instead of bare black, and a plate that
    ## *is* 16:9 is unchanged - the copy is hidden completely behind it.
    def _plate(img):
        w = 48
        h = max(2, int(round(w * renpy.config.screen_height / float(renpy.config.screen_width))))

        tiny = renpy.display.transform.Transform(img, xysize=(w, h))
        blur = renpy.display.transform.Transform(
            tiny,
            zoom=renpy.config.screen_width / float(w),
            xalign=0.5,
            yalign=0.5,
        )
        front = renpy.display.transform.Transform(
            img,
            xalign=0.5,
            yalign=0.5,
            fit="contain",
        )

        box = renpy.display.layout.MultiBox(layout="fixed")
        box.add(blur)
        box.add(front)
        return box

transform bg_fit:
    subpixel True
    xalign 0.5
    yalign 0.5

transform cg_fit:
    subpixel True
    xalign 0.5
    yalign 0.5

## A gentle endless pan-and-breathe for backgrounds.
transform ken_burns:
    subpixel True
    xalign 0.5
    yalign 0.5
    zoom KEN_ZOOM
    parallel:
        block:
            easein 24.0 xoffset KEN_OX yoffset -KEN_OY
            easeout 24.0 xoffset -KEN_OX yoffset KEN_OY
            repeat

## CGs hold, then push in slowly and settle back.
transform cg_push:
    subpixel True
    xalign 0.5
    yalign 0.5
    zoom CG_ZOOM
    block:
        easein 20.0 zoom CG_ZOOM2
        easeout 20.0 zoom CG_ZOOM
        repeat


## ----------------------------------------------------------------------------
## Reduce Motion
## ----------------------------------------------------------------------------
## An accessibility preference that flattens the camera moves, sprite breathing,
## and title drift for players who are sensitive to motion. It is
## exposed as a checkbox in Preferences. The one-shot UI slides (notify, quick
## menu) are brief enough to leave alone.

default persistent.reduce_motion = False

init python:
    _MOTION_FULL = dict(
        KEN_ZOOM=1.03, KEN_ZOOM2=1.05, KEN_OX=8, KEN_OY=6,
        CG_ZOOM=1.0, CG_ZOOM2=1.03,
        BREATHE_ZOOM=0.009, BREATHE_LIFT=3,
        TITLE_ZOOM=1.02, TITLE_ZOOM2=1.03, TITLE_OX=8,
    )
    _MOTION_NONE = dict(
        KEN_ZOOM=1.0, KEN_ZOOM2=1.0, KEN_OX=0, KEN_OY=0,
        CG_ZOOM=1.0, CG_ZOOM2=1.0,
        BREATHE_ZOOM=0.0, BREATHE_LIFT=0,
        TITLE_ZOOM=1.0, TITLE_ZOOM2=1.0, TITLE_OX=0,
    )

    def _apply_motion(interactive=False):
        rm = bool(getattr(persistent, "reduce_motion", False))

        for _k, _v in (_MOTION_NONE if rm else _MOTION_FULL).items():
            setattr(store, _k, _v)

        if rm:
            config.tag_transform["bg"] = [_plate, bg_fit]
            config.tag_transform["cg"] = [_plate, cg_fit]
        else:
            config.tag_transform["bg"] = [_plate, ken_burns]
            config.tag_transform["cg"] = [_plate, cg_push]

    def set_reduce_motion(flag):
        persistent.reduce_motion = bool(flag)
        _apply_motion(interactive=True)
        renpy.restart_interaction()

    class ToggleReduceMotion(Action):
        def __call__(self):
            set_reduce_motion(not getattr(persistent, "reduce_motion", False))

        def get_selected(self):
            return bool(getattr(persistent, "reduce_motion", False))


init 10 python:
    _apply_motion()
