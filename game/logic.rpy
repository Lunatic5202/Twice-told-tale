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
        """Show the stat-change toast (screens_extra.rpy)."""
        renpy.show_screen("stat_toast", text=text, color=color)
        renpy.restart_interaction()

    def bump(stat, amount=1):
        """
        Change a bond or the Editor's Pen count and surface the change.

        stat is one of "w", "b", "m", "pen". M is the hidden Mend stat; its
        toast is deliberately muted so the player notices that *something*
        shifted without naming the hidden meter as a game mechanic.
        """
        if stat == "w":
            store.w += amount
            toast_stat("Wanderer Bond %s" % _signed(amount), "#6fd3c7")
        elif stat == "b":
            store.b += amount
            toast_stat("Scaramouche Bond %s" % _signed(amount), "#b06bd6")
        elif stat == "m":
            store.m += amount
            toast_stat("Mend %s" % _signed(amount), "#8f8f9f")
        elif stat == "pen":
            store.pen += amount
            toast_stat("Editor's Pen used", "#e0c060")
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


## ----------------------------------------------------------------------------
## Ending router
## ----------------------------------------------------------------------------
## Reached when the player makes no explicit ending choice at Scene 4.4.
## Explicit choices are evaluated in the Scene 4.4 menu itself; this router
## implements the canonical fallback order: True, then the eligible bond
## ending, then Neutral.

label ending_router:
    if gate_true():
        jump ending_true
    elif gate_wanderer():
        jump ending_wanderer
    elif gate_scaramouche():
        jump ending_scaramouche
    else:
        jump ending_neutral
