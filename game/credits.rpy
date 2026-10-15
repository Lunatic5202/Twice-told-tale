################################################################################
## Twice-Told Tale - Credits
################################################################################
##
## The credits roll, shown from the main menu. It scrolls on its own and can be
## dismissed with a click, Escape, or the Return button.

transform credit_roll(dur=55.0):
    ypos 1.0
    linear dur ypos -1.0


screen credits():

    tag menu
    modal True

    add Solid("#08080f")

    vbox at credit_roll(55.0):
        xalign 0.5
        spacing 30
        xmaximum 900

        null height 60
        text "TWICE-TOLD TALE":
            xalign 0.5
            size 64
            color gui.accent_color
            font gui.interface_text_font
        text "a 30-day otome visual novel":
            xalign 0.5
            size 30
            color "#9a9284"

        null height 40

        text "Story & Script":
            xalign 0.5
            size 26
            color "#7a7280"
        text "the author":
            xalign 0.5
            size 34
            color "#e6dfd0"

        text "Produced for a single reader":
            xalign 0.5
            size 26
            color "#7a7280"
        text "Lunatic":
            xalign 0.5
            size 34
            color "#e6dfd0"

        null height 30

        text "Illustration":
            xalign 0.5
            size 26
            color "#7a7280"
        text "procedural ink-and-paper plates (tools/make_art.py)":
            xalign 0.5
            size 30
            color "#e6dfd0"

        text "Music & Sound":
            xalign 0.5
            size 26
            color "#7a7280"
        text "CC0 tracks by OpenGameArt.org contributors":
            xalign 0.5
            size 30
            color "#e6dfd0"
        text "(per-track credits in game/audio/CREDITS.md)":
            xalign 0.5
            size 24
            color "#9a9284"

        text "Type":
            xalign 0.5
            size 26
            color "#7a7280"
        text "Cinzel Decorative by Natanael Gama (OFL-1.1)":
            xalign 0.5
            size 30
            color "#e6dfd0"
        text "Crimson Text by Sebastian Kosch (OFL-1.1)":
            xalign 0.5
            size 30
            color "#e6dfd0"
        text "Hassengard by Geminorum (freeware, non-commercial)":
            xalign 0.5
            size 30
            color "#e6dfd0"

        text "Built with":
            xalign 0.5
            size 26
            color "#7a7280"
        text "Ren'Py (renpy.org)":
            xalign 0.5
            size 30
            color "#e6dfd0"

        null height 40

        text "A non-commercial fan work. Not affiliated with HoYoverse.\nGenshin Impact and its characters belong to their respective owners.":
            xalign 0.5
            text_align 0.5
            size 26
            color "#8a8290"

        null height 30
        text "Thanks for playing.":
            xalign 0.5
            size 40
            color gui.accent_color
        null height 120

    key "dismiss" action Return()
    key "game_menu" action Return()

    button:
        background None
        xfill True
        yfill True
        action Return()

    textbutton _("Return"):
        xalign 0.985
        yalign 0.02
        action Return()
