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
define quick_fade = Fade(0.18, 0.0, 0.22, color="#0a0a14")
define white_fade = Fade(0.5, 0.12, 0.5, color="#f4ecd8")
define ink_dissolve = ImageDissolve("gui/mask/ink_dissolve.png", 0.9, ramplen=8)
define page_wipe = ImageDissolve("gui/mask/ink_dissolve.png", 0.7, reverse=True, ramplen=8)
define soft_wipe = Pixellate(0.4, 12)

## Weighted scene and act changes. Every scene change in the script uses
## `scene_fade`, so giving it texture here changes the whole game at once: the
## old plate bleeds into the next one through the ink mask instead of a flat
## dissolve. `scene_ink` is the slower variant for reflective beats.
##
## Act boundaries are deliberately heavier: they dip to ink and stay there for a
## beat while the act card lands, so a chapter break actually reads as a turn of
## the page. `act_wipe` opens and closes each act card.
define scene_fade = ImageDissolve("gui/mask/ink_dissolve.png", 0.5, ramplen=10)
define scene_ink = ImageDissolve("gui/mask/ink_dissolve.png", 0.75, ramplen=12)
define act_wipe = Fade(0.55, 0.18, 0.65, color="#0a0a14")

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
## Splash screen
## ----------------------------------------------------------------------------

## "Made by Lunatic" fades in, holds, then fades out.
style splash_byline_text is gui_text:
    font gui.display_font
    size gui.scale(46)
    color "#ece5d3"
    outlines [(3, "#0a0a14cc", 0, 0)]

transform splash_byline:
    xalign 0.5
    yalign 0.5
    alpha 0.0
    linear 0.7 alpha 1.0
    pause 1.1
    linear 0.7 alpha 0.0


## The title is type, not a bitmap, so it stays sharp and can be glitched. The
## reveal is a brief chromatic split: the cream logotype never moves - only two
## coloured ghosts flicker around it - so it reads as a digital glitch rather
## than a shake.
transform title_settle:
    subpixel True
    alpha 0.0
    linear 0.04 alpha 1.0
    pause 0.04
    alpha 0.2
    pause 0.03
    alpha 1.0
    pause 0.05
    alpha 0.4
    pause 0.03
    alpha 1.0
    pause 100.0

transform title_ghost(dx, dy=0):
    subpixel True
    alpha 0.25
    xoffset dx
    yoffset dy
    linear 0.04 alpha 0.9
    pause 0.03
    xoffset dx * 1.6
    alpha 0.45
    pause 0.03
    xoffset dx * 0.4
    alpha 0.9
    pause 0.04
    xoffset dx * 1.2
    alpha 0.35
    pause 0.03
    xoffset -dx * 0.5
    alpha 0.7
    pause 0.03
    linear 0.08 alpha 0.0
    xoffset 0
    pause 100.0

## A calm fade for the Reduce Motion preference.
transform title_soft:
    subpixel True
    alpha 0.0
    linear 0.6 alpha 1.0
    pause 100.0

screen splash_title():
    zorder 10

    fixed:
        xfill True
        yfill True

        if persistent.reduce_motion:
            text "Twice-Told Tale" style "splash_logo_text" xalign 0.5 yalign 0.5 at title_soft
        else:
            text "Twice-Told Tale" style "splash_logo_text" color "#ff2f5e" outlines [] xalign 0.5 yalign 0.5 at title_ghost(-7, -2)
            text "Twice-Told Tale" style "splash_logo_text" color "#2fe0ff" outlines [] xalign 0.5 yalign 0.5 at title_ghost(7, 2)
            text "Twice-Told Tale" style "splash_logo_text" xalign 0.5 yalign 0.5 at title_settle


label splashscreen:
    scene black
    with None

    ## The theme starts here so the game is never silent, and continues into the
    ## main menu and the prologue.
    play music audio.marginalia fadein 2.0

    ## Act one: the byline fades in and out.
    show expression Text("Made by Lunatic", style="splash_byline_text") as byline at splash_byline
    with None
    $ renpy.pause(2.6, hard=False)
    hide byline
    with Dissolve(0.3)

    ## Act two: the title glitches into place.
    show screen splash_title
    with None
    $ renpy.pause(2.4, hard=False)

    scene black
    hide screen splash_title
    with ink_dissolve

    return
