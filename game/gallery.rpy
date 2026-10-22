################################################################################
## Twice-Told Tale - Collection
################################################################################
##
## Progress that outlives a single save: the endings you've reached ("Pages
## Collected"), the illustrations you've seen (Gallery), and the score you've
## heard (Music Room). Unlocks are stored in `persistent`, so they survive new
## games, and are recorded automatically as you play.

## ---- Persistence -----------------------------------------------------------

default persistent.endings_seen = set()
default persistent.cgs_seen = set()
default persistent.music_seen = set()


init python:

    def unlock_cg(name):
        if name in CG_BY_NAME and name not in persistent.cgs_seen:
            persistent.cgs_seen.add(name)
            renpy.save_persistent()

    def unlock_music(cue):
        if cue in MUSIC_NAMES and cue not in persistent.music_seen:
            persistent.music_seen.add(cue)
            renpy.save_persistent()

    def record_ending(eid):
        if eid not in persistent.endings_seen:
            persistent.endings_seen.add(eid)
            renpy.save_persistent()

    def _pretty_cue(cue):
        """Turn a cue id into a display title, e.g. the_doctor_s_hour."""
        t = cue.replace("_s_", "_'s_").replace("_t_", "_'t_")
        words = [w if w.startswith("'") else (w[:1].upper() + w[1:]) for w in t.split("_")]
        return " ".join(words)

    def _track_discoveries():
        """Runs at the start of every interaction; records CGs on screen and
        the music currently playing."""
        try:
            for attr in renpy.get_attributes("cg", "master", ()):
                if attr in CG_BY_NAME:
                    unlock_cg(attr)
            cur = renpy.music.get_playing("music")
            if cur:
                base = cur.replace("\\", "/").rsplit("/", 1)[-1].rsplit(".", 1)[0]
                if base in MUSIC_NAMES:
                    unlock_music(base)
        except Exception:
            pass

    config.start_interact_callbacks.append(_track_discoveries)


## ---- Catalogues ------------------------------------------------------------

init python:

    ENDINGS = [
        dict(id="wanderer", code="A", title="Her Name", tone="Warm",
             cg="ending_wanderer",
             line="You wrote the Wanderer's name, and the ink held."),
        dict(id="scaramouche", code="B", title="The Lamp-Keeper", tone="Bittersweet",
             cg="ending_scaramouche",
             line="You wrote the Echo's true name, and gave the hat away."),
        dict(id="true", code="C", title="The Passenger", tone="Golden",
             cg="ending_true",
             line="You set the pen down and let them write it together."),
        dict(id="gnosis_box", code="F", title="The Gnosis Box", tone="Horror",
             cg="gnosis_violet",
             line="You wanted to know what was inside."),
        dict(id="burned_pages", code="G", title="Burned Pages", tone="Tragedy",
             cg="first_page_burn",
             line="You reached for the door and left them to finish the page."),
        dict(id="blank_page", code="H", title="Blank Page", tone="Existential",
             cg="blank_dot",
             line="Nothing was written. The page remains."),
        dict(id="neutral", code="N", title="Margins", tone="Open",
             cg="folio_page",
             line="The Echo finished it, in his own hand."),
        dict(id="archivist", code="1", title="The Archivist's Fee", tone="Cold",
             cg="folio_black",
             line="The Doctor kept a very small fee: one page."),
        dict(id="burn_it_down", code="2", title="Burn It Down", tone="Violent",
             cg="margin_door_shut",
             line="You pulled the Folio apart. The paper screamed."),
        dict(id="quiet_page", code="3", title="The Quiet Page", tone="Still",
             cg="empty_bed",
             line="The Echo waited at the door. You were not there."),
    ]

    CGS = [
        dict(name="prologue_echo", title="The Echo"),
        dict(name="prologue_tea", title="The Tea"),
        dict(name="folio_page", title="The Folio Page"),
        dict(name="first_page_burn", title="The First Page Burns"),
        dict(name="nahida_between", title="Nahida Between Them"),
        dict(name="wanderer_soup", title="Wanderer's Soup"),
        dict(name="margin_door", title="The Margin Door"),
        dict(name="gold_feather", title="The Gold Feather"),
        dict(name="sword_dance", title="The Sword Dance"),
        dict(name="puppet_furnace", title="The Puppet in the Furnace"),
        dict(name="sleeping_puppet", title="The Sleeping Puppet"),
        dict(name="raiden_yae", title="Raiden & Yae"),
        dict(name="niwa_note", title="Niwa's Note"),
        dict(name="child_drawing", title="The Child's Drawing"),
        dict(name="hooked_pinkies", title="Hooked Pinkies"),
        dict(name="empty_bed", title="The Empty Bed"),
        dict(name="black_case", title="The Black Case"),
        dict(name="gnosis_violet", title="The Gnosis, Violet"),
        dict(name="glass_cell", title="The Glass Cell"),
        dict(name="two_palms", title="Two Palms"),
        dict(name="doctor_lane", title="The Doctor's Lane"),
        dict(name="echo_bowed", title="The Bow"),
        dict(name="wanderer_echo_on_page", title="Wanderer & Echo, on the Page"),
        dict(name="ending_wanderer", title="Ending · Her Name"),
        dict(name="ending_scaramouche", title="Ending · The Lamp-Keeper"),
        dict(name="ending_true", title="Ending · The Passenger"),
        dict(name="folio_black", title="The Folio Goes Black"),
        dict(name="margin_door_shut", title="The Margin Door, Shut"),
        dict(name="blank_dot", title="The Blank Dot"),
    ]

    CG_BY_NAME = set(c["name"] for c in CGS)
    for _c in CGS:
        _c["path"] = "images/cg/%s.png" % _c["name"]

    _MUSIC_ORDER = [
        "marginalia", "marginalia_dawn", "double_trouble", "hat_guy",
        "hat_guy_reprise", "warm_table", "warm_table_reprise", "the_boy",
        "a_smaller_promise", "clean_instruments", "reprise_clean_instruments",
        "the_doctor_s_hour", "the_old_dawn", "what_i_never_said",
        "the_thing_unsaid", "six_days", "three_pages", "the_last_evening",
        "what_we_can_t_take_back", "a_name_is_a_small_thing",
        "what_he_built_from_nothing", "the_margin_door", "page_walk", "escher",
        "mechanical_ears", "quiet", "rumors", "slumber", "smoke", "sword_dance",
        "tatarasuna", "the_table", "three_hundred_and_eleven",
        "what_he_can_t_read", "what_he_kept", "what_i_remember",
        "what_was_written", "which_of_us",
    ]

    MUSIC = [dict(cue=c, title=_pretty_cue(c),
                  path="audio/music/%s.ogg" % c) for c in _MUSIC_ORDER]
    MUSIC_NAMES = set(_MUSIC_ORDER)


init python:

    def ending_info(eid):
        """The ENDINGS row for an ending id, or a blank stand-in."""
        for e in ENDINGS:
            if e["id"] == eid:
                return e
        return dict(id=eid, code="", title="", tone="", cg=None, line="")

    def endings_found():
        return sum(1 for e in ENDINGS if e["id"] in persistent.endings_seen)

    def cgs_found():
        return sum(1 for c in CGS if c["name"] in persistent.cgs_seen)

    def music_found():
        return sum(1 for m in MUSIC if m["cue"] in persistent.music_seen)


################################################################################
## Screens
################################################################################

## Pages Collected #############################################################

screen endings_gallery():

    tag menu

    use game_menu(_("Pages Collected"), scroll="viewport"):

        style_prefix "collection"

        vbox:
            spacing 18

            text "The Folio keeps every ending you reach. [endings_found()] of [len(ENDINGS)] pages collected."

            for e in ENDINGS:

                $ _seen = e["id"] in persistent.endings_seen

                frame:
                    background Solid("#12121add")
                    padding (22, 16)
                    xfill True

                    hbox:
                        spacing 22

                        ## The page's marginal index.
                        text e["code"]:
                            size 40
                            color (gui.accent_color if _seen else "#3a3a44")
                            min_width 46

                        vbox:
                            spacing 4
                            if _seen:
                                text "%s  ·  %s" % (e["title"], e["tone"]):
                                    color "#e6dfd0"
                                    size 32
                                text e["line"]:
                                    color "#a49b8b"
                                    size 24
                            else:
                                text "· · ·  not yet written":
                                    color "#5a5560"
                                    size 30


## Gallery (CGs) ###############################################################

screen cg_gallery():

    tag menu

    use game_menu(_("Gallery"), scroll="viewport"):

        style_prefix "collection"

        vbox:
            spacing 16

            text "Illustrations you've seen. [cgs_found()] of [len(CGS)] collected."

            for row in range(0, len(CGS), 3):

                hbox:
                    spacing 16

                    for c in CGS[row:row + 3]:

                        $ _seen = c["name"] in persistent.cgs_seen

                        button:
                            xysize (282, 178)
                            background Solid("#12121add")
                            padding (0, 0)
                            action (Show("cg_viewer", name=c["name"]) if _seen else NullAction())

                            if _seen:
                                add c["path"]:
                                    xysize (282, 158)
                                    align (0.5, 0.0)
                                text c["title"]:
                                    size 17
                                    color "#cfc7b8"
                                    align (0.5, 1.0)
                            else:
                                text "?":
                                    size 60
                                    color "#33333e"
                                    align (0.5, 0.5)


screen cg_viewer(name=None):

    modal True
    zorder 150

    add "images/cg/%s.png" % name

    key "dismiss" action Hide("cg_viewer")
    key "game_menu" action Hide("cg_viewer")

    button:
        background None
        xfill True
        yfill True
        action Hide("cg_viewer")

    text "click anywhere to close":
        xalign 0.5
        yalign 0.985
        size 18
        color "#ffffff88"


## Music Room ##################################################################

screen music_room():

    tag menu

    use game_menu(_("Music Room"), scroll="viewport"):

        style_prefix "collection"

        vbox:
            spacing 10

            text "The score, as you unlock it. [music_found()] of [len(MUSIC)] tracks."

            textbutton _("Stop the music"):
                action Stop("music")

            null height 6

            for m in MUSIC:

                $ _seen = m["cue"] in persistent.music_seen

                if _seen:
                    textbutton m["title"] action Play("music", m["path"])
                else:
                    text "· · ·  %s" % m["title"]:
                        color "#3a3a44"


style collection_text is gui_text
style collection_button is gui_button
style collection_button_text is gui_button_text

style collection_text:
    color "#cfc7b8"
    size 26

style collection_button_text:
    color "#cfc7b8"
    hover_color gui.accent_color
    size 30
