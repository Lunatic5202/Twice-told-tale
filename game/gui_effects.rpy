################################################################################
## Twice-Told Tale - Interface Effects
################################################################################
##
## The atmospheric layer over the stock Ren'Py interface:
##
##   * a small library of custom transitions (ink dissolves, fades, wipes)
##   * an animated ink-nib mouse cursor
##   * a blinking ink-drop "click to continue" marker
##   * a splash / loading screen shown before the main menu
##   * a drifting vignette + grain overlay used in-game
##   * motion transforms reused by the choice menu and main menu
##
## Nothing here is required for the story to run; it can all be removed and the
## game will still be playable with the stock look.

init offset = -1


## ----------------------------------------------------------------------------
## Transitions
## ----------------------------------------------------------------------------
## A handful of named transitions. `ink_dissolve`/`page_wipe` use the generated
## noise mask so scenes bleed into one another like ink through paper.

define ink_fade = Fade(0.45, 0.15, 0.55, color="#0a0a14")
define scene_fade = Fade(0.35, 0.05, 0.40, color="#0a0a14")
define quick_fade = Fade(0.18, 0.0, 0.22, color="#0a0a14")
define white_fade = Fade(0.5, 0.12, 0.5, color="#f4ecd8")
define ink_dissolve = ImageDissolve("gui/mask/ink_dissolve.png", 0.9, ramplen=8)
define page_wipe = ImageDissolve("gui/mask/ink_dissolve.png", 0.7, reverse=True, ramplen=8)
define soft_wipe = Pixellate(0.4, 12)

## A default used after every scene/sprite change in the script (set on the
## Character objects so expression changes cross-fade instead of snapping).
define config.say_attribute_transition = Dissolve(0.2)
define config.say_attribute_transition_layer = "master"


## ----------------------------------------------------------------------------
## Animated ink-nib cursor
## ----------------------------------------------------------------------------
## Replaces the OS pointer with an animated fountain-pen nib. Re-run
## tools/make_gui_assets.py to regenerate the frames.

init python:
    ## config.mouse cycles one cursor per frame, so frames are repeated to
    ## slow the flicker of the nib's glint down to something calm.
    _CURSOR_FRAMES = 4
    _CURSOR_HOLD = 7

    def _cursor_list(prefix):
        return [("gui/cursor/%s_%d.png" % (prefix, i // _CURSOR_HOLD), 1, 1)
                for i in range(_CURSOR_FRAMES * _CURSOR_HOLD)]

    config.mouse = {
        "default": _cursor_list("pen"),
        "hover": _cursor_list("pen_hover"),
    }


## ----------------------------------------------------------------------------
## Click-to-continue marker
## ----------------------------------------------------------------------------
## Ren'Py uses a screen named "ctc" automatically, so defining one here gives
## every speaking character the same animated ink-drop prompt.

image ctc_ink:
    "gui/overlay/ctc_drop.png"
    subpixel True
    zoom 0.9
    alpha 0.0
    block:
        linear 0.45 alpha 0.85 yoffset -4
        linear 0.45 alpha 0.25 yoffset 0
        repeat

screen ctc(ctc=None):
    zorder 100
    add "ctc_ink":
        xalign 0.985
        yalign 0.985


## ----------------------------------------------------------------------------
## In-game atmosphere overlay
## ----------------------------------------------------------------------------
## A soft vignette, a very slow ink bloom, and drifting film grain. Registered
## as an overlay screen so it sits above the scene but below the dialogue HUD.

image film_grain = Tile("gui/overlay/grain.png")

transform grain_drift:
    subpixel True
    xoffset 0
    yoffset 0
    linear 1.3 xoffset 14 yoffset 9
    linear 1.3 xoffset -9 yoffset -11
    linear 1.3 xoffset 7 yoffset 5
    linear 1.3 xoffset 0 yoffset 0
    repeat

transform ink_bloom:
    subpixel True
    xalign 0.5
    yalign 0.5
    zoom 1.25
    rotate 0
    alpha 0.0
    parallel:
        linear 1.4 alpha 0.10
        block:
            linear 9.0 alpha 0.16
            linear 9.0 alpha 0.10
            repeat
    parallel:
        linear 46.0 rotate 10
        linear 46.0 rotate -10
        repeat
    parallel:
        linear 34.0 zoom 1.34
        linear 34.0 zoom 1.25
        repeat

screen atmosphere():
    zorder 5
    if not main_menu:
        add "gui/overlay/vignette.png"
        add "gui/overlay/ink_blot.png" at ink_bloom
        add "film_grain" at grain_drift

init python:
    if "atmosphere" not in config.overlay_screens:
        config.overlay_screens.append("atmosphere")


## ----------------------------------------------------------------------------
## Reusable motion transforms
## ----------------------------------------------------------------------------

## Staggered entrance for menu choices, then a hover lift. Use as:
##     at choice_in(i * 0.06), focus_lift
transform choice_in(delay=0.0):
    subpixel True
    alpha 0.0
    yoffset 26
    pause delay
    parallel:
        linear 0.24 alpha 1.0
    parallel:
        easeout 0.30 yoffset 0

## Hover lift shared by choice buttons and menu navigation.
transform focus_lift:
    subpixel True
    on idle:
        easein 0.15 xoffset 0 zoom 1.0
    on hover:
        easeout 0.15 xoffset 16 zoom 1.02

## A gentler lift for the large vertical navigation stack.
transform nav_lift:
    subpixel True
    on idle:
        easein 0.15 xoffset 0
    on hover:
        easeout 0.15 xoffset 22

## Fade-and-rise used for titles and cards.
transform rise_in(delay=0.0, dist=18, dur=0.5):
    subpixel True
    alpha 0.0
    yoffset dist
    pause delay
    parallel:
        linear dur alpha 1.0
    parallel:
        easeout dur yoffset 0

## Slow breathing scale for title flourishes.
transform breathe(min_z=1.0, max_z=0.985, period=2.6):
    subpixel True
    zoom min_z
    block:
        easein_quad period zoom max_z
        easeout_quad period zoom min_z
        repeat


## ----------------------------------------------------------------------------
## Splash / loading screen
## ----------------------------------------------------------------------------

image splash_quill:
    "gui/cursor/pen_hover_0.png"
    subpixel True
    zoom 2.2
    rotate 0
    block:
        easein 0.9 rotate -7
        easeout 0.9 rotate 7
        repeat

transform splash_blot:
    subpixel True
    xalign 0.5
    yalign 0.5
    zoom 1.35
    rotate 0
    alpha 0.0
    parallel:
        linear 1.2 alpha 0.55
    parallel:
        linear 3.2 zoom 1.0 rotate 5

transform splash_progress:
    xanchor 0.0
    xzoom 0.001
    pause 0.4
    easeout 2.1 xzoom 1.0

screen splash_loading():
    zorder 200

    add Solid("#07070e")

    add "gui/overlay/ink_blot.png" at splash_blot

    vbox:
        xalign 0.5
        yalign 0.42
        spacing 10

        text "Twice-Told Tale":
            at rise_in(0.15, 22, 0.9)
            xalign 0.5
            size 66
            color "#ece5d3"
            outlines [(3, "#0a0a14dd", 0, 0)]

        text "a tale told twice":
            at rise_in(0.65, 12, 0.8)
            xalign 0.5
            italic True
            size 22
            color "#8fa8b0"

    add "splash_quill" at rise_in(0.5, 0, 0.6):
        xalign 0.5
        yalign 0.63

    fixed:
        xalign 0.5
        yalign 0.74
        xysize (380, 3)
        add Solid("#26263a")
        add Solid("#d6b25e", xysize=(380, 3)) at splash_progress

    text "turning the page…":
        at rise_in(1.1, 8, 0.7)
        xalign 0.5
        yalign 0.80
        size 18
        color "#6f8a90"

label splashscreen:
    scene black
    with None
    show screen splash_loading
    $ renpy.pause(2.8, hard=False)
    hide screen splash_loading
    with ink_dissolve
    return
