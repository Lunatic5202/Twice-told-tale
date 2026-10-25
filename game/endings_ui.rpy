################################################################################
## Twice-Told Tale - Ending Presentation
################################################################################
##
## The closing ritual every ending shares:
##
##   1. the frame fades down to ink,
##   2. the name of the ending fades up, slowly, and holds,
##   3. the ending plate comes back up under it,
##   4. the credits roll.
##
## The data (code, title, tone, one-line summary) comes from the ENDINGS
## table in gallery.rpy, so the collection screen and the ending card can
## never drift apart.

init offset = -1


## A flat ink-black plate used to carry the ending card.
image ending_black = Solid("#08080f")


## The card's entrance: a slow fade, a slight rise, and the faintest push in.
transform ending_card_in:
    subpixel True
    alpha 0.0
    yoffset 26
    zoom 0.985
    ease 3.4 alpha 1.0 yoffset 0 zoom 1.0


screen ending_card(code="", title="", tone="", line=""):
    zorder 150

    vbox:
        at ending_card_in
        xalign 0.5
        yalign 0.5
        xmaximum 920
        spacing 6

        if code:
            text "ENDING " + code:
                xalign 0.5
                size 24
                color "#8a8290"
                kerning 8

        text title:
            xalign 0.5
            size 62
            color gui.accent_color
            font gui.title_font
            outlines [(3, "#000000cc", 0, 0)]

        null height 14

        add "gui/overlay/rule_gold.png":
            xysize (380, 2)
            xalign 0.5

        null height 14

        text line:
            xalign 0.5
            text_align 0.5
            size 27
            color "#bdb4a4"
            italic True

        null height 6

        text tone:
            xalign 0.5
            size 22
            color "#7a7280"
            kerning 5


## ----------------------------------------------------------------------------
## Labels
## ----------------------------------------------------------------------------

## Fade down to ink, then fade the name of the ending up and hold it.
label ending_title_card(eid):
    $ _e = ending_info(eid)

    scene ending_black with Dissolve(1.6)

    show screen ending_card(_e["code"], _e["title"], _e["tone"], _e["line"]) with None
    pause 5.5
    hide screen ending_card with Dissolve(1.4)

    return


## The credits roll, played over the ending plate.
label ending_credits():
    play music audio.marginalia fadein 3.0
    call screen credits_roll
    stop music fadeout 2.0
    return
