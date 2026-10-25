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

    def set_page(pages, day=None):
        """Update the diegetic page counter and announce each newly preserved page."""
        previous_pages = store.pages_left
        store.pages_left = pages
        if day is not None:
            store.current_day = day

        # A decrease means the story has preserved the next page. Keep this
        # separate from Ren'Py's generic notify screen (saves/screenshots).
        if pages is not None and previous_pages is not None and pages < previous_pages:
            if day is None:
                message = "The first page has been preserved in the Folio."
            else:
                message = "Day %s — another piece of the story is preserved." % day

            if renpy.get_screen("page_recorded_notify"):
                store.page_recorded_queue.append(message)
            else:
                renpy.show_screen("page_recorded_notify", message=message)
                renpy.restart_interaction()

    def advance_page_recorded():
        """Display queued page-recorded notices one at a time."""
        if store.page_recorded_queue:
            message = store.page_recorded_queue.pop(0)
            renpy.show_screen("page_recorded_notify", message=message)
            renpy.restart_interaction()
        else:
            renpy.hide_screen("page_recorded_notify")
            renpy.restart_interaction()

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
