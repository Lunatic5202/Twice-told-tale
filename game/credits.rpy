################################################################################
## Twice-Told Tale - Credits
################################################################################
##
## The credits roll. Two entry points share one body:
##
##   * `credits`     - the menu version, reachable from the main menu,
##   * `credits_roll` - the in-game version, played at the end of every ending.
##
## It scrolls on its own and can be dismissed with a click, Escape, or the
## Return button.

## The roll. The credits body is ~2000px tall, so the travel is sized to
## carry the last line all the way to the bottom of the frame instead of
## clipping it off-screen.
transform credit_roll(dur=55.0):
    ypos 1.0
    linear dur ypos -1.85


## The credits themselves. Shared by both screens so the two can never
## disagree about who made what.
screen credits_body():

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

    text "Author":
        xalign 0.5
        size 26
        color "#7a7280"
    text "Lunatic":
        xalign 0.5
        size 34
        color "#e6dfd0"

    text "Story & Script":
        xalign 0.5
        size 26
        color "#7a7280"
    text "Lunatic":
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

    text "Genshin Impact and its characters are © HoYoverse / miHoYo.\nA non-commercial fan work. Not affiliated with HoYoverse.":
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


screen credits():

    tag menu
    modal True

    add Solid("#08080f")

    vbox at credit_roll(55.0):
        xalign 0.5
        spacing 30
        xmaximum 900

        use credits_body()

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


## The in-game roll, played at the end of every ending.
screen credits_roll():

    modal True

    ## The page counter belongs to the story, not the credits.
    on "show" action Hide("page_counter")

    ## A veil rather than a wall, so the ending plate still breathes behind
    ## the roll.
    add Solid("#08080fe6")

    vbox at credit_roll(70.0):
        xalign 0.5
        spacing 30
        xmaximum 900

        use credits_body()

    key "dismiss" action Return()
    key "game_menu" action Return()

    button:
        background None
        xfill True
        yfill True
        action Return()

    textbutton _("Return"):
        xalign 0.985
        yalign 0.96
        action Return()
