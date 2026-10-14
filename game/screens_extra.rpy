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
    alpha 0.0
    yoffset -14
    linear 0.22 alpha 1.0 yoffset 0
    pause 1.7
    linear 0.38 alpha 0.0 yoffset -14

screen stat_toast(text="", color="#ffffff"):
    zorder 200

    if text:
        frame:
            at stat_toast_move
            xalign 0.5
            yalign 0.06
            padding (30, 14)
            background Solid("#0b0b12dd")
            text text:
                color color
                size 27
                xalign 0.5
                yalign 0.5

        timer 2.4 action Hide("stat_toast")


## ----------------------------------------------------------------------------
## Scene title banner
## ----------------------------------------------------------------------------
## A centred title card shown for a beat at the top of each scene. Driven by
## the show_title() helper in logic.rpy.

transform scene_title_anim:
    alpha 0.0
    linear 0.5 alpha 1.0
    pause 0.6
    linear 0.5 alpha 0.0

screen scene_title(text=""):
    zorder 90

    frame:
        background None
        xalign 0.5
        yalign 0.5
        at scene_title_anim
        text text:
            xalign 0.5
            yalign 0.5
            textalign 0.5
            color "#ffffff"
            size 46
            outlines [(3, "#000000cc", 0, 0)]


## ----------------------------------------------------------------------------
## Page counter
## ----------------------------------------------------------------------------
## "Thirty days, thirty pages." A small diegetic counter in the corner.

screen page_counter():
    zorder 10

    if pages_left is not None:
        frame:
            background Solid("#0b0b1266")
            xalign 0.99
            yalign 0.015
            padding (16, 8)
            text "[pages_left] PAGES LEFT":
                size 20
                color "#d8d0c0"
