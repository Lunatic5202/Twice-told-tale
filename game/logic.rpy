################################################################################
## Twice-Told Tale - Logic
################################################################################
##
## Stat helpers, ending gates, the ending router, and small presentation
## helpers used throughout the scenes.

init python:

    def toast_stat(text, color="#ffffff"):
        """Show a stat cue, queueing it if another cue is still on screen."""
        if renpy.get_screen("stat_toast"):
            store.stat_toast_queue.append((text, color))
        else:
            renpy.show_screen("stat_toast", text=text, color=color)
            renpy.restart_interaction()

    def advance_stat_toast():
        """Advance to the next queued cue instead of dropping a simultaneous change."""
        if store.stat_toast_queue:
            text, color = store.stat_toast_queue.pop(0)
            renpy.show_screen("stat_toast", text=text, color=color)
            renpy.restart_interaction()
        else:
            renpy.hide_screen("stat_toast")
            renpy.restart_interaction()

    def bump(stat, amount=1):
        """
        Change a bond or the Editor's Pen count and surface a brief, diegetic cue.

        Mend stays hidden: its feedback suggests the state of the Folio without
        exposing the meter or its numerical value.
        """
        if stat == "w":
            store.w += amount
            if amount > 0:
                toast_stat("The Wanderer is willing to hear you out.", "#6fd3c7")
            elif amount < 0:
                toast_stat("The Wanderer draws back.", "#6fd3c7")
        elif stat == "b":
            store.b += amount
            if amount > 0:
                toast_stat("The Echo lets you closer.", "#b06bd6")
            elif amount < 0:
                toast_stat("The Echo shuts you out.", "#b06bd6")
        elif stat == "m":
            store.m += amount
            if amount > 0:
                toast_stat("The page settles beneath your hand.", "#8f8f9f")
            elif amount < 0:
                toast_stat("A seam in the page comes loose.", "#8f8f9f")
        elif stat == "pen":
            store.pen += amount
            toast_stat("The page keeps the mark.", "#e0c060")
        else:
            raise Exception("Unknown stat: %r" % (stat,))

    CG_ACHIEVEMENTS = {
        "folio_page": ("The First Page", "A blank folio waits for a story to take shape.", "✧"),
        "prologue_echo": ("A Voice in the Margin", "Something in the page has begun to answer.", "❧"),
        "first_page_burn": ("What the Fire Kept", "Some stories begin with what survives the flame.", "✦"),
        "prologue_tea": ("Tea for Two", "For a moment, the silence has company.", "❖"),
        "nahida_between": ("A Gentle Interruption", "A small kindness makes room for a different answer.", "✿"),
        "wanderer_soup": ("A Bowl Left Warm", "Care can arrive without asking to be named.", "❖"),
        "margin_door": ("The Door in the Margin", "There is a way forward, if you choose to look.", "✧"),
        "sleeping_puppet": ("While the World Sleeps", "Even a puppet can look painfully young at rest.", "❧"),
        "raiden_yae": ("Those Who Watch Over", "Two old powers pause beside a fragile dream.", "✦"),
        "gold_feather": ("A Feather Held Close", "A small keepsake turns between careful fingers.", "✧"),
        "sword_dance": ("Steel in Step", "For one bright instant, the blades move as one.", "✦"),
        "puppet_furnace": ("Into the Heart of the Furnace", "A choice is made beneath the furnace light.", "✦"),
        "niwa_note": ("A Promise in Ink", "A familiar hand leaves words meant to be believed.", "❧"),
        "child_drawing": ("A House by the Sea", "A child's drawing holds more than its simple lines.", "✿"),
        "hooked_pinkies": ("A Little Finger Promise", "Two little fingers make a promise without words.", "❖"),
        "empty_bed": ("The Shape of Someone Missing", "A place is kept for the one who is gone.", "❧"),
        "black_case": ("For the Archivist", "A brass hasp guards whatever waits inside.", "✧"),
        "gnosis_violet": ("The Violet Answer", "Power glimmers where certainty begins to fracture.", "✦"),
        "glass_cell": ("Behind the Glass", "Close enough to see. Not close enough to reach.", "❖"),
        "two_palms": ("Two Open Hands", "What is offered, and what is accepted, are not always the same.", "✧"),
        "echo_bowed": ("The Echo Bows", "Even an echo can choose what it carries forward.", "❧"),
        "doctor_lane": ("A Convenient Offer", "The gentlest voice can still ask for too much.", "✦"),
        "ending_wanderer": ("A Name Chosen Freely", "The road ahead belongs to the one who walks it.", "❖"),
        "ending_scaramouche": ("No Longer an Echo", "A self can begin where an old name ends.", "✦"),
        "wanderer_echo_on_page": ("A Story, Rewritten", "The page holds two versions—and room for another.", "❧"),
        "ending_true": ("The Page We Keep", "Not every wound needs to become the ending.", "✧"),
        "blank_dot": ("A Blank That Remains", "Not every answer arrives as words.", "○"),
        "folio_black": ("The Folio Falls Silent", "Even a closed book leaves something behind.", "❧"),
        "margin_door_shut": ("A Door Left Closed", "Some choices are made by turning away.", "✧"),
    }

    def show_cg_achievement(cg_key):
        """Show a named achievement only when its CG is explicitly reached."""
        achievement = CG_ACHIEVEMENTS.get(cg_key)
        if not achievement:
            return
        title, description, emblem = achievement
        item = (title, description, emblem)
        if renpy.get_screen("achievement_unlocked_notify"):
            store.cg_achievement_queue.append(item)
        else:
            renpy.show_screen(
                "achievement_unlocked_notify",
                title=title, description=description, emblem=emblem
            )
            renpy.restart_interaction()

    def advance_cg_achievement():
        """Show queued CG achievements in order; never overlap banners."""
        if store.cg_achievement_queue:
            title, description, emblem = store.cg_achievement_queue.pop(0)
            renpy.show_screen(
                "achievement_unlocked_notify",
                title=title, description=description, emblem=emblem
            )
            renpy.restart_interaction()
        else:
            renpy.hide_screen("achievement_unlocked_notify")
            renpy.restart_interaction()

    def set_page(pages, day=None):
        """Update the diegetic page counter without triggering unrelated banners."""
        store.pages_left = pages
        if day is not None:
            store.current_day = day

    def show_title(text, delay=2.0):
        """Show a centred scene-title card and wait for it to fade. The wait is
        skippable (a click dismisses it early)."""
        renpy.show_screen("scene_title", text=text)
        renpy.pause(delay, hard=False)
        renpy.hide_screen("scene_title")

    def show_act(roman, title, kicker="ACT", delay=2.4):
        """Show the ceremonial act-boundary card (screens_extra.rpy) and wait
        for it to clear. Skippable, like show_title()."""
        renpy.show_screen("act_title", roman=roman, title=title, kicker=kicker)
        renpy.pause(delay, hard=False)
        renpy.hide_screen("act_title")

    ## ---- Ending gates ------------------------------------------------------
    ## Canonical order, from the script's tuning notes.

    def gate_true():
        return m >= 7 and w >= 4 and b >= 4 and pen <= 1 and promise_made

    def gate_wanderer():
        return w >= 5 and w > b

    def gate_scaramouche():
        return b >= 5 and b > w

    ## Special endings use the same named gates in the last-page menu and tests.
    def gate_gnosis_box():
        return box

    def gate_burned_pages():
        return promise_made and pen >= 3

    def gate_blank_page():
        return pen >= 3

    def gate_burn_it_down():
        return pen >= 2

    def gate_quiet_page():
        return promise_made and pen < 3

    def ending_destination():
        """Return the automatic ending selected by the canonical gate order."""
        if gate_true():
            return "ending_true"
        elif gate_wanderer():
            return "ending_wanderer"
        elif gate_scaramouche():
            return "ending_scaramouche"
        return "ending_neutral"


## ----------------------------------------------------------------------------
## Ending router
## ----------------------------------------------------------------------------
## Reached when the player makes no explicit ending choice at Scene 4.4.
## Explicit choices are evaluated in the Scene 4.4 menu itself; this router
## implements the canonical fallback order: True, then the eligible bond
## ending, then Neutral.

label ending_router:
    jump expression ending_destination()
