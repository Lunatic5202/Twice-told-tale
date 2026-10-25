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
## visitors) can stage cleanly. Each slot carries a subtle idle "breath" - a
## gentle scale around the character's feet plus a slow lift - so that standing
## sprites never sit perfectly still. The periods are deliberately mismatched so
## two characters on screen never fall into step.

transform at_far_left:
    xpos 0.02
    xanchor 0.5
    yalign 1.0
    subpixel True
    transform_anchor True
    zoom SPRITE_ZOOM
    on show:
        xoffset -360
        alpha 0.0
        parallel:
            easeout 0.5 xoffset 0
        parallel:
            linear 0.35 alpha 1.0
    on hide:
        easein 0.4 xoffset -360 alpha 0.0
    block:
        easein 3.6 zoom (SPRITE_ZOOM * (1.0 + BREATHE_ZOOM)) yoffset -BREATHE_LIFT
        easeout 3.6 zoom SPRITE_ZOOM yoffset 0
        repeat

transform at_left:
    xpos 0.22
    xanchor 0.5
    yalign 1.0
    subpixel True
    transform_anchor True
    zoom SPRITE_ZOOM
    on show:
        xoffset -360
        alpha 0.0
        parallel:
            easeout 0.5 xoffset 0
        parallel:
            linear 0.35 alpha 1.0
    on hide:
        easein 0.4 xoffset -360 alpha 0.0
    block:
        easein 3.0 zoom (SPRITE_ZOOM * (1.0 + BREATHE_ZOOM)) yoffset -(BREATHE_LIFT - 1)
        easeout 3.0 zoom SPRITE_ZOOM yoffset 0
        repeat

transform at_center:
    xpos 0.5
    xanchor 0.5
    yalign 1.0
    subpixel True
    transform_anchor True
    zoom SPRITE_ZOOM
    on show:
        yoffset 44
        alpha 0.0
        parallel:
            easeout 0.5 yoffset 0
        parallel:
            linear 0.35 alpha 1.0
    on hide:
        easein 0.35 yoffset 44 alpha 0.0
    block:
        easein 3.4 zoom (SPRITE_ZOOM * (1.0 + BREATHE_ZOOM)) yoffset -BREATHE_LIFT
        easeout 3.4 zoom SPRITE_ZOOM yoffset 0
        repeat

## Right-side characters are mirrored (negative xzoom) so they face left,
## toward the centre of the frame.
transform at_right:
    xpos 0.78
    xanchor 0.5
    yalign 1.0
    subpixel True
    transform_anchor True
    xzoom -SPRITE_ZOOM
    yzoom SPRITE_ZOOM
    on show:
        xoffset 360
        alpha 0.0
        parallel:
            easeout 0.5 xoffset 0
        parallel:
            linear 0.35 alpha 1.0
    on hide:
        easein 0.4 xoffset 360 alpha 0.0
    block:
        easein 3.2 xzoom -(SPRITE_ZOOM * (1.0 + BREATHE_ZOOM)) yzoom (SPRITE_ZOOM * (1.0 + BREATHE_ZOOM)) yoffset -(BREATHE_LIFT - 1)
        easeout 3.2 xzoom -SPRITE_ZOOM yzoom SPRITE_ZOOM yoffset 0
        repeat

transform at_far_right:
    xpos 0.98
    xanchor 0.5
    yalign 1.0
    subpixel True
    transform_anchor True
    xzoom -SPRITE_ZOOM
    yzoom SPRITE_ZOOM
    on show:
        xoffset 360
        alpha 0.0
        parallel:
            easeout 0.5 xoffset 0
        parallel:
            linear 0.35 alpha 1.0
    on hide:
        easein 0.4 xoffset 360 alpha 0.0
    block:
        easein 2.8 xzoom -(SPRITE_ZOOM * (1.0 + BREATHE_ZOOM)) yzoom (SPRITE_ZOOM * (1.0 + BREATHE_ZOOM)) yoffset -BREATHE_LIFT
        easeout 2.8 xzoom -SPRITE_ZOOM yzoom SPRITE_ZOOM yoffset 0
        repeat

# Dedicated marks for crowded 4-figure line-up (echo/tighnari/cyno/wanderer)
transform at_far_left_crowd:
    xpos 0.143
    xanchor 0.5
    yalign 1.0
    subpixel True
    transform_anchor True
    zoom SPRITE_ZOOM
    on show:
        xoffset -360
        alpha 0.0
        parallel:
            easeout 0.5 xoffset 0
        parallel:
            linear 0.35 alpha 1.0
    on hide:
        easein 0.4 xoffset -360 alpha 0.0
    block:
        easein 3.0 zoom (SPRITE_ZOOM * (1.0 + BREATHE_ZOOM)) yoffset -(BREATHE_LIFT - 1)
        easeout 3.0 zoom SPRITE_ZOOM yoffset 0
        repeat

transform at_left_crowd:
    xpos 0.400
    xanchor 0.5
    yalign 1.0
    subpixel True
    transform_anchor True
    zoom SPRITE_ZOOM
    on show:
        xoffset -360
        alpha 0.0
        parallel:
            easeout 0.5 xoffset 0
        parallel:
            linear 0.35 alpha 1.0
    on hide:
        easein 0.4 xoffset -360 alpha 0.0
    block:
        easein 3.2 zoom (SPRITE_ZOOM * (1.0 + BREATHE_ZOOM)) yoffset -(BREATHE_LIFT - 1)
        easeout 3.2 zoom SPRITE_ZOOM yoffset 0
        repeat

transform at_right_crowd:
    xpos 0.623
    xanchor 0.5
    yalign 1.0
    subpixel True
    transform_anchor True
    xzoom -SPRITE_ZOOM
    yzoom SPRITE_ZOOM
    on show:
        xoffset 360
        alpha 0.0
        parallel:
            easeout 0.5 xoffset 0
        parallel:
            linear 0.35 alpha 1.0
    on hide:
        easein 0.4 xoffset 360 alpha 0.0
    block:
        easein 3.4 xzoom -(SPRITE_ZOOM * (1.0 + BREATHE_ZOOM)) yzoom (SPRITE_ZOOM * (1.0 + BREATHE_ZOOM)) yoffset -(BREATHE_LIFT - 1)
        easeout 3.4 xzoom -SPRITE_ZOOM yzoom SPRITE_ZOOM yoffset 0
        repeat

transform at_far_right_crowd:
    xpos 0.865
    xanchor 0.5
    yalign 1.0
    subpixel True
    transform_anchor True
    xzoom -SPRITE_ZOOM
    yzoom SPRITE_ZOOM
    on show:
        xoffset 360
        alpha 0.0
        parallel:
            easeout 0.5 xoffset 0
        parallel:
            linear 0.35 alpha 1.0
    on hide:
        easein 0.4 xoffset 360 alpha 0.0
    block:
        easein 3.6 xzoom -(SPRITE_ZOOM * (1.0 + BREATHE_ZOOM)) yzoom (SPRITE_ZOOM * (1.0 + BREATHE_ZOOM)) yoffset -BREATHE_LIFT
        easeout 3.6 xzoom -SPRITE_ZOOM yzoom SPRITE_ZOOM yoffset 0
        repeat


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

        timer 2.4 action Function(advance_stat_toast)


## ----------------------------------------------------------------------------
## Scene title banner
## ----------------------------------------------------------------------------
## A centred title card shown for a beat at the top of each scene. Driven by
## the show_title() helper in logic.rpy. It rises out of the dissolve, draws a
## fine gold rule beneath, and holds just long enough to read.

transform scene_title_anim:
    subpixel True
    alpha 0.0
    zoom 1.04
    yoffset 12
    parallel:
        linear 0.45 alpha 1.0
    parallel:
        easeout 0.6 zoom 1.0 yoffset 0
    pause 0.95
    linear 0.45 alpha 0.0

transform scene_title_rule:
    subpixel True
    xalign 0.5
    xzoom 0.02
    alpha 0.0
    pause 0.25
    alpha 1.0
    easeout 0.55 xzoom 1.0
    pause 0.55
    linear 0.45 alpha 0.0

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
            spacing 18

            text text:
                xalign 0.5
                textalign 0.5
                font gui.title_font
                color "#ffffff"
                size 46
                outlines [(3, "#000000cc", 0, 0)]

            add "gui/overlay/rule_gold.png":
                xysize (300, 2)
                xalign 0.5
                at scene_title_rule


## ----------------------------------------------------------------------------
## Act title card
## ----------------------------------------------------------------------------
## The heavier card shown at each act boundary. A dark veil closes over the
## frame, cinematic bars slide in, and the act number is set in the logo face -
## then it all lifts to reveal the act's first scene. Driven by show_act() in
## logic.rpy.

transform act_veil:
    subpixel True
    alpha 0.0
    linear 0.4 alpha 1.0
    pause 1.5
    linear 0.5 alpha 0.0

transform card_bar_top:
    subpixel True
    xalign 0.5
    yalign 0.0
    yoffset -140
    easeout 0.45 yoffset 0
    pause 1.2
    easein 0.4 yoffset -140

transform card_bar_bottom:
    subpixel True
    xalign 0.5
    yalign 1.0
    yoffset 140
    easeout 0.45 yoffset 0
    pause 1.2
    easein 0.4 yoffset 140

transform act_kicker_in:
    subpixel True
    alpha 0.0
    linear 0.45 alpha 1.0
    pause 1.1
    linear 0.45 alpha 0.0

transform act_num_in:
    subpixel True
    alpha 0.0
    zoom 1.12
    parallel:
        linear 0.4 alpha 1.0
    parallel:
        easeout 0.7 zoom 1.0
    pause 0.9
    linear 0.45 alpha 0.0

screen act_title(roman="I", title="", kicker="ACT"):
    zorder 92

    ## Dark veil so the act break reads as its own moment.
    add Solid("#0a0a14") at act_veil

    ## Cinematic bars.
    add "gui/overlay/bar_top.png" at card_bar_top
    add "gui/overlay/bar_bottom.png" at card_bar_bottom

    frame:
        background None
        xalign 0.5
        yalign 0.5

        vbox:
            xalign 0.5
            yalign 0.5
            spacing 12

            text kicker:
                xalign 0.5
                font gui.display_font
                size 22
                color "#c9b789"
                kerning 8
                at act_kicker_in

            text roman:
                xalign 0.5
                font gui.logo_font
                size 118
                color "#ece5d3"
                outlines [(5, "#0a0a14cc", 0, 0)]
                at act_num_in

            add "gui/overlay/rule_gold.png":
                xysize (520, 2)
                xalign 0.5
                at scene_title_rule

            text title:
                xalign 0.5
                textalign 0.5
                font gui.title_font
                size 42
                color "#ffffff"
                outlines [(3, "#000000cc", 0, 0)]
                at act_kicker_in


## ----------------------------------------------------------------------------
## Page-recorded banner
## ----------------------------------------------------------------------------
## A compact, Inazuma-inspired Folio notice. This is intentionally separate
## from Ren'Py's generic notify screen so quicksaves and screenshots keep their
## familiar feedback. Notices are queued by logic.rpy and shown one at a time.

transform page_recorded_appear:
    subpixel True
    on show:
        xoffset 420
        alpha 0.0
        parallel:
            easeout 0.38 xoffset 0
        parallel:
            easeout 0.30 alpha 1.0
    on hide:
        parallel:
            easein 0.28 xoffset 280
        parallel:
            easein 0.28 alpha 0.0

screen page_recorded_notify(message="A page has been preserved in the Folio."):
    zorder 180

    if preferences.transitions:
        frame:
            at page_recorded_appear
            xalign 0.985
            yalign 0.105
            xmaximum 560
            background Solid("#101018e8")
            padding (18, 12)

            hbox:
                spacing 14

                text "❧":
                    font gui.display_font
                    size 38
                    color "#d9bd7b"
                    yalign 0.5

                vbox:
                    spacing 3

                    text "PAGE RECORDED":
                        font gui.title_font
                        size 20
                        color "#e4ca8b"

                    text "[message]":
                        font gui.interface_text_font
                        size 16
                        color "#eee8da"
                        xmaximum 465
    else:
        frame:
            xalign 0.985
            yalign 0.105
            xmaximum 560
            background Solid("#101018e8")
            padding (18, 12)

            hbox:
                spacing 14

                text "❧":
                    font gui.display_font
                    size 38
                    color "#d9bd7b"
                    yalign 0.5

                vbox:
                    spacing 3

                    text "PAGE RECORDED":
                        font gui.title_font
                        size 20
                        color "#e4ca8b"

                    text "[message]":
                        font gui.interface_text_font
                        size 16
                        color "#eee8da"
                        xmaximum 465

    timer 3.4 action Function(advance_page_recorded)


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
            ypos 52

            hbox:
                spacing 6

                text _("Auto") style "mode_indicator_text"
                text "▸" style "skip_triangle"


init python:
    config.overlay_screens.append("auto_indicator")
