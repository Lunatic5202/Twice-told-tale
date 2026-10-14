################################################################################
## Twice-Told Tale - Placeholder Art
################################################################################
##
## Until real art is delivered, every background, CG, and sprite expression is
## rendered as a labelled placeholder so the whole script is playable and
## lint-clean. To swap in real art, replace the *definition* below with a file
## path (or delete the block and drop a file named to match), e.g.:
##
##     image bg annex_night = "images/bg/annex_night.png"
##
## The asset requirements for real art are collected in ASSETS.md at the
## project root.

init python:

    def bg_placeholder(label, color):
        return Fixed(
            Solid(color),
            Text(
                label,
                color="#ffffffdd",
                size=46,
                textalign=0.5,
                xalign=0.5,
                yalign=0.42,
            ),
            Text(
                "(background placeholder)",
                color="#ffffff55",
                size=22,
                textalign=0.5,
                xalign=0.5,
                yalign=0.52,
            ),
            alt="",
        )

    def cg_placeholder(label, color="#0d0d16"):
        return Fixed(
            Solid(color),
            Text(
                "CG  \u00b7  " + label,
                color="#ffffffdd",
                size=40,
                textalign=0.5,
                xalign=0.5,
                yalign=0.46,
            ),
            Text(
                "(event illustration placeholder)",
                color="#ffffff55",
                size=22,
                textalign=0.5,
                xalign=0.5,
                yalign=0.54,
            ),
            alt="",
        )

    def sprite_placeholder(fill, label, w=380, h=760):
        return Fixed(
            Solid(fill, xsize=w, ysize=h),
            Text(
                label,
                color="#ffffffcc",
                size=30,
                textalign=0.5,
                xalign=0.5,
                yalign=0.5,
            ),
            xysize=(w, h),
        )


## ---- Backgrounds -----------------------------------------------------------

image bg annex_night = bg_placeholder("The Archive Annex \u2014 Midnight", "#14142a")
image bg annex_predawn = bg_placeholder("The Archive Annex \u2014 Before Dawn", "#1d2038")
image bg annex_dawn = bg_placeholder("The Archive Annex \u2014 Dawn", "#3a3550")
image bg annex_day = bg_placeholder("The Archive Annex \u2014 Daylight", "#46465c")
image bg annex_evening = bg_placeholder("The Archive Annex \u2014 Evening", "#2c2636")
image bg courtyard_day = bg_placeholder("Akademiya Courtyard \u2014 Noon", "#41503c")
image bg rooftop_night = bg_placeholder("The Akademiya Rooftop \u2014 Night", "#101826")
image bg dining_evening = bg_placeholder("The Dining Hall \u2014 Evening", "#3a2f28")


## ---- CGs (17 total; only the ones used by the slice are wired so far) ------

init python:
    _cg_defs = [
        ("cg prologue_echo", "Prologue \u2014 The Echo steps out of the ink"),
        ("cg prologue_tea", "Prologue \u2014 The Wanderer in the doorway, holding tea"),
        ("cg folio_page", "Prologue \u2014 Close on the torn page"),
        ("cg first_page_burn", "Prologue \u2014 The first page burns"),
        ("cg nahida_between", "1.1 \u2014 Nahida between the two of them"),
        ("cg wanderer_soup", "1.3 \u2014 The Wanderer and the soup"),
        ("cg margin_door", "1.7 \u2014 The Margin Door"),
        ("cg gold_feather", "Page-Walk One \u2014 The gold feather"),
        ("cg niwa_note", "Page-Walk Two \u2014 Niwa's note"),
        ("cg hooked_pinkies", "2.14 \u2014 Two little fingers hooked"),
        ("cg empty_bed", "2.15 \u2014 The empty bed and the drawing"),
        ("cg black_case", "3.1 \u2014 The black case and the Gnosis"),
        ("cg glass_cell", "3.4 \u2014 Glass cell, three silhouettes"),
        ("cg two_palms", "3.5 \u2014 Two palms on one pane"),
        ("cg doctor_lane", "4.3 \u2014 The Doctor at the end of the lane"),
        ("cg ending_wanderer", "Ending A \u2014 The fading hand"),
        ("cg ending_scaramouche", "Ending B \u2014 The hat passed over"),
        ("cg ending_true", "Ending C \u2014 Three cups in the window"),
        ("cg gnosis_violet", "Gnosis Box \u2014 The violet line"),
        ("cg margin_door_shut", "Burned Pages \u2014 The Margin Door shuts"),
        ("cg blank_dot", "Blank Page \u2014 The blank dot"),
    ]

    for _name, _label in _cg_defs:
        renpy.image(_name, cg_placeholder(_label))


## ---- Sprite expressions ----------------------------------------------------

init python:
    _sprite_fill = {
        "wanderer": "#2f6d68",
        "echo": "#5a3170",
        "nahida": "#3f6b2a",
        "dottore": "#3a5570",
        "paimon": "#7a6420",
        "tighnari": "#4a5e2e",
        "cyno": "#5e4a24",
    }

    _sprite_defs = {
        "wanderer": ["neutral", "guarded", "smug", "flustered", "hurt", "soft", "tired"],
        "echo": ["sneer", "cold", "amused", "startled", "grieving", "shy", "smile"],
        "nahida": ["gentle", "serious", "mischievous", "sad"],
        "dottore": ["pleasant", "delighted", "cold", "fascinated"],
        "paimon": ["cheerful", "worried", "excited"],
        "tighnari": ["neutral", "sly"],
        "cyno": ["neutral", "grinning"],
    }

    for _tag, _exps in _sprite_defs.items():
        for _exp in _exps:
            renpy.image(
                (_tag, _exp),
                sprite_placeholder(
                    _sprite_fill[_tag],
                    "%s\n%s" % (_tag.capitalize(), _exp),
                ),
            )
