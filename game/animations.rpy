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


## ----------------------------------------------------------------------------
## Slow camera moves
## ----------------------------------------------------------------------------
## These are attached to whole image tags (see the registration at the bottom of
## this file) so every background drifts and every CG pushes in on its own.

## Motion amounts. These are store variables (not constants) so the "Reduce
## Motion" preference can flatten them at runtime; see _apply_motion() below.
define KEN_ZOOM = 1.06
define KEN_ZOOM2 = 1.13
define KEN_OX = 20
define KEN_OY = 12
define CG_ZOOM = 1.06
define BREATHE_ZOOM = 0.009
define BREATHE_LIFT = 3
define TITLE_ZOOM = 1.06
define TITLE_ZOOM2 = 1.13
define TITLE_OX = 16

## A gentle endless pan-and-breathe for backgrounds. The base zoom keeps the
## slightly-larger-than-screen plate covering the frame at all times.
transform ken_burns:
    subpixel True
    zoom KEN_ZOOM
    xalign 0.5
    yalign 0.5
    parallel:
        block:
            easein 24.0 zoom KEN_ZOOM2
            easeout 24.0 zoom KEN_ZOOM
            repeat
    parallel:
        block:
            easein 32.0 xoffset KEN_OX yoffset -KEN_OY
            easeout 32.0 xoffset -KEN_OX yoffset KEN_OY
            repeat

## CGs hold, then push in slowly and settle back, like a held breath.
transform cg_push:
    subpixel True
    zoom 1.0
    xalign 0.5
    yalign 0.5
    block:
        easein 7.0 zoom CG_ZOOM
        pause 3.5
        easeout 7.0 zoom 1.0
        pause 2.5
        repeat


## ----------------------------------------------------------------------------
## Ambient dust
## ----------------------------------------------------------------------------
## Faint motes and fibres that drift slowly upward through the frame, tying the
## otherwise-still backgrounds to the atmosphere overlay.

image mote = "gui/overlay/mote.png"
image fiber = "gui/overlay/fiber.png"

transform mote_drift(xp, ystart, dur, delay, z, drift):
    subpixel True
    xpos xp
    ypos ystart
    zoom z
    alpha 0.0
    pause delay
    block:
        ypos ystart
        xoffset 0
        alpha 0.0
        parallel:
            linear 1.4 alpha 0.5
            pause (dur - 2.8)
            linear 1.4 alpha 0.0
        parallel:
            linear dur ypos -0.14 xoffset drift
        repeat

init python:
    import random as _pyrandom

    _mrng = _pyrandom.Random(20261015)
    AMBIENT_MOTES = []
    for _i in range(18):
        AMBIENT_MOTES.append((
            _mrng.uniform(0.02, 0.98),          # x position
            _mrng.uniform(1.05, 1.35),          # start y (just under the frame)
            _mrng.uniform(11.0, 19.0),          # drift duration
            _mrng.uniform(0.0, 13.0),           # start delay
            _mrng.uniform(0.12, 0.42),          # zoom
            _mrng.uniform(-54.0, 54.0),         # horizontal drift
            _mrng.choice(["mote", "fiber"]),    # sprite
        ))

screen ambience():
    ## Below the dialogue/choice UI (which sits at the default zorder) but above
    ## the scene itself, so the dust drifts in front of the art, not the text.
    zorder -1

    if not main_menu and not renpy.get_screen("game_menu") and not persistent.reduce_motion:
        for _xp, _ys, _dur, _delay, _z, _drift, _img in AMBIENT_MOTES:
            add _img at mote_drift(_xp, _ys, _dur, _delay, _z, _drift)


## ----------------------------------------------------------------------------
## Reduce Motion
## ----------------------------------------------------------------------------
## An accessibility preference that flattens the camera moves, sprite breathing,
## title drift, and ambient dust for players who are sensitive to motion. It is
## exposed as a checkbox in Preferences. The one-shot UI slides (notify, quick
## menu) are brief enough to leave alone.

default persistent.reduce_motion = False

init python:
    _MOTION_FULL = dict(
        KEN_ZOOM=1.06, KEN_ZOOM2=1.13, KEN_OX=20, KEN_OY=12, CG_ZOOM=1.06,
        BREATHE_ZOOM=0.009, BREATHE_LIFT=3,
        TITLE_ZOOM=1.06, TITLE_ZOOM2=1.13, TITLE_OX=16,
    )
    _MOTION_NONE = dict(
        KEN_ZOOM=1.0, KEN_ZOOM2=1.0, KEN_OX=0, KEN_OY=0, CG_ZOOM=1.0,
        BREATHE_ZOOM=0.0, BREATHE_LIFT=0,
        TITLE_ZOOM=1.06, TITLE_ZOOM2=1.06, TITLE_OX=0,
    )

    def _apply_motion(interactive=False):
        rm = bool(getattr(persistent, "reduce_motion", False))

        for _k, _v in (_MOTION_NONE if rm else _MOTION_FULL).items():
            setattr(store, _k, _v)

        if rm:
            config.tag_transform.pop("bg", None)
            config.tag_transform.pop("cg", None)
            if "ambience" in config.overlay_screens:
                config.overlay_screens.remove("ambience")
            if interactive:
                renpy.hide_screen("ambience")
        else:
            config.tag_transform["bg"] = ken_burns
            config.tag_transform["cg"] = cg_push
            if "ambience" not in config.overlay_screens:
                config.overlay_screens.append("ambience")

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
