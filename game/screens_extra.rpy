################################################################################
## Twice-Told Tale - Extra Screens
################################################################################
##
## HUD and feedback screens that sit on top of the normal Ren'Py interface:
## the stat-change toast, the scene title banner, and the diegetic page
## counter.

## ----------------------------------------------------------------------------
## Sprite slots
## ----------------------------------------------------------------------------
## Five standing positions, left to right, so busy scenes (two leads plus
## visitors) can stage cleanly.

transform at_far_left:
    xalign 0.02
    yalign 1.0

transform at_left:
    xalign 0.22
    yalign 1.0

transform at_center:
    xalign 0.5
    yalign 1.0

transform at_right:
    xalign 0.78
    yalign 1.0

transform at_far_right:
    xalign 0.98
    yalign 1.0


## ----------------------------------------------------------------------------
## Stat-change toast
## ----------------------------------------------------------------------------
## Shown briefly whenever a choice changes a bond or the Editor's Pen. The
## availability of ending gates stays hidden; only the change the player just
## caused is surfaced.

transform stat_toast_move:
    subpixel True
    alpha 0.0
    yoffset -22
    xoffset 18
    parallel:
        linear 0.22 alpha 1.0
    parallel:
        easeout 0.30 yoffset 0 xoffset 0
    pause 1.7
    parallel:
        linear 0.38 alpha 0.0
    parallel:
        easein 0.38 yoffset -18

screen stat_toast(text="", color="#ffffff"):
    zorder 200

    if text:
        frame:
            at stat_toast_move
            xalign 0.5
            yalign 0.06
            padding (0, 0)
            background Solid("#0b0b12dd")

            hbox:
                spacing 0

                ## A colour-coded spine hints at which stat moved.
                add Solid(color, xysize=(6, 42))

                text text:
                    color color
                    size 27
                    yalign 0.5
                    xoffset 18
                    yoffset -1

                null width 18

        timer 2.4 action Hide("stat_toast")


## ----------------------------------------------------------------------------
## Scene title banner
## ----------------------------------------------------------------------------
## A centred title card shown for a beat at the top of each scene. Driven by
## the show_title() helper in logic.rpy.

transform scene_title_anim:
    subpixel True
    alpha 0.0
    zoom 1.06
    parallel:
        linear 0.45 alpha 1.0
    parallel:
        easeout 0.60 zoom 1.0
    pause 1.0
    linear 0.55 alpha 0.0

transform scene_title_rule:
    subpixel True
    xzoom 0.001
    pause 0.25
    easeout 0.55 xzoom 1.0
    pause 0.7
    linear 0.5 alpha 0.0

screen scene_title(text=""):
    zorder 90

    frame:
        background None
        xalign 0.5
        yalign 0.5
        at scene_title_anim

        vbox:
            xalign 0.5
            yalign 0.5
            spacing 16

            text text:
                xalign 0.5
                textalign 0.5
                font gui.title_font
                color "#ffffff"
                size 46
                outlines [(3, "#000000cc", 0, 0)]

            add Solid("#d6b25e", xysize=(280, 2)) at scene_title_rule:
                xalign 0.5


## ----------------------------------------------------------------------------
## Page counter
## ----------------------------------------------------------------------------
## "Thirty days, thirty pages." A small diegetic counter in the corner.

transform page_counter_breathe:
    subpixel True
    alpha 0.86
    block:
        easein 2.4 alpha 1.0
        easeout 2.4 alpha 0.86
        repeat

screen page_counter():
    zorder 10

    if pages_left is not None:
        frame:
            at page_counter_breathe
            background Solid("#0b0b1266")
            xalign 0.99
            yalign 0.015
            padding (16, 8)
            text "[pages_left] PAGES LEFT":
                size 20
                color "#d8d0c0"


## ----------------------------------------------------------------------------
## Auto-forward indicator
## ----------------------------------------------------------------------------
## A small badge that pulses while auto-forward mode is on, so the player always
## knows why the story is advancing on its own.

transform mode_badge_pulse:
    subpixel True
    alpha 0.72
    block:
        easein 1.0 alpha 1.0
        easeout 1.0 alpha 0.72
        repeat

screen auto_indicator():
    zorder 96

    if preferences.afm_enable and not config.skipping:
        frame:
            at mode_badge_pulse
            style "mode_indicator_frame"
            ypos gui.scale(52)

            hbox:
                spacing gui.scale(6)

                text _("Auto") style "mode_indicator_text"
                text "▸" style "skip_triangle"


init python:
    config.overlay_screens.append("auto_indicator")
