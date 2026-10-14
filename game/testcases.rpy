################################################################################
## Twice-Told Tale - Automated smoke test
################################################################################
##
## Run with:  renpy.sh . test smoke
##
## Walks the vertical slice (Prologue + Act 1): starts a new game, enters a
## name, and takes every Act 1 choice, confirming the flow reaches the end of
## the slice without a runtime error.

testcase smoke:
    $ _test.transition_timeout = 0.05
    $ _test.timeout = 20.0

    click "Start"
    pause 0.4

    advance until screen "input"
    type "Mira\n"
    pause 0.4

    advance until screen "choice"
    click "fix this"

    advance until screen "choice"
    click "Cousin"

    advance until screen "choice"
    click "sugar"

    advance until screen "choice"
    click "Can I try"

    advance until screen "choice"
    click "not ready"

    advance until screen "choice"
    click "both real"

    advance until screen "choice"
    click "Together"

    pause 0.6
    exit


################################################################################
## Draft (Act 2+) smoke test
################################################################################
##
## Run with:  renpy.sh . test draft
##
## Confirms the auto-generated Act 2+ draft parses and runs: opens a draft
## scene, then exercises Scene 4.4's last-choice menu (only the always-available
## "hand the pen to the Doctor" option is visible at default stats) and routes
## into an ending.

testcase draft:
    $ _test.transition_timeout = 0.05
    $ _test.timeout = 20.0

    run Jump("act2_2_1")
    advance
    advance
    advance
    advance

    run Jump("act4_4_4")
    advance until screen "choice"
    click "Hand the pen to the Doctor"
    pause 0.5
    exit


################################################################################
## Collection menus smoke test
################################################################################
##
## Run with:  renpy.sh . test galleries
##
## Opens each collection screen from the main menu and returns, confirming the
## Pages/Gallery/Music room screens render without a runtime error.

testcase galleries:
    $ _test.transition_timeout = 0.05
    $ _test.timeout = 20.0

    click "Pages Collected"
    pause 0.4
    click "Return"
    pause 0.2

    click "Gallery"
    pause 0.4
    click "Return"
    pause 0.2

    click "Music Room"
    pause 0.4
    click "Return"
    pause 0.2

    exit


################################################################################
## Collection progress test
################################################################################
##
## Run with:  renpy.sh . test progress
##
## Clears the persistent collection, plays the vertical slice, then asserts that
## CGs and music were auto-recorded by the interaction callback.

init python:

    def _reset_progress():
        persistent.cgs_seen = set()
        persistent.music_seen = set()
        persistent.endings_seen = set()

    def _assert_progress():
        assert len(persistent.cgs_seen) >= 1, "no CGs unlocked: %r" % (persistent.cgs_seen,)
        assert len(persistent.music_seen) >= 1, "no music unlocked: %r" % (persistent.music_seen,)

testcase progress:
    $ _test.transition_timeout = 0.05
    $ _test.timeout = 20.0

    run Function(_reset_progress)

    click "Start"
    pause 0.4

    advance until screen "input"
    type "Mira\n"
    pause 0.4

    advance until screen "choice"
    click "fix this"
    advance until screen "choice"
    click "Cousin"
    advance until screen "choice"
    click "sugar"
    advance until screen "choice"
    click "Can I try"
    advance until screen "choice"
    click "not ready"
    advance until screen "choice"
    click "both real"
    advance until screen "choice"
    click "Together"

    pause 0.5
    run Function(_assert_progress)
    exit
