################################################################################
## Twice-Told Tale - Logic
################################################################################
##
## Stat helpers, ending gates, the ending router, and small presentation
## helpers used throughout the scenes.

init python:

    def _signed(n):
        """Format a stat delta as +N / -N using a typographic minus."""
        if n >= 0:
            return "+%d" % n
        else:
            return "\u2212%d" % (-n)

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
                toast_stat("The Wanderer trusts you a little more.", "#6fd3c7")
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
            toast_stat("The Editor's Pen leaves a mark.", "#e0c060")
        else:
            raise Exception("Unknown stat: %r" % (stat,))

    def set_page(pages, day=None):
        """Update the diegetic page counter at the top of a Day."""
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
