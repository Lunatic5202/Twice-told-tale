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

################################################################################
## Full-route and ending coverage
################################################################################
##
## Run with:  renpy.sh . test route      (plays Act 2 through the last choice)
##             renpy.sh . test gnosis_route (opens the case alone and takes its ending)
##            renpy.sh . test endings    (jumps through every ending label)
##            renpy.sh . test gates      (unit-checks the ending gate functions)

init python:

    def _assert_ending_seen(eid):
        assert eid in persistent.endings_seen, "ending %r not recorded: %r" % (eid, persistent.endings_seen)

    def _assert_shown(name):
        assert renpy.get_screen(name) is not None, "screen %r is not showing" % name

    def _set_stats(w_, b_, m_, pen_, promise_):
        store.w = w_
        store.b = b_
        store.m = m_
        store.pen = pen_
        store.promise_made = promise_

    def _assert_gate(expected):
        gt, gw, gs = gate_true(), gate_wanderer(), gate_scaramouche()
        if expected == "none":
            assert not (gt or gw or gs), "expected no gate, got %r" % ((gt, gw, gs),)
        elif expected == "true":
            assert gt, "expected true gate"
        elif expected == "wanderer":
            assert gw and not gt, "expected wanderer gate, got %r" % ((gt, gw, gs),)
        elif expected == "scaramouche":
            assert gs and not gt, "expected scaramouche gate, got %r" % ((gt, gw, gs),)
        else:
            raise Exception("bad expectation: %r" % (expected,))

    def _assert_ending_target(expected):
        actual = ending_destination()
        assert actual == expected, "expected %r, got %r" % (expected, actual)

    def _assert_special_gates(expected):
        actual = (
            gate_gnosis_box(),
            gate_burned_pages(),
            gate_blank_page(),
            gate_burn_it_down(),
            gate_quiet_page(),
        )
        assert actual == expected, "expected special gates %r, got %r" % (expected, actual)

    def _set_story_flags(promise, opened_alone):
        store.promise_made = promise
        store.box = opened_alone

    def _assert_story_flags(promise, opened_alone):
        assert store.promise_made is promise, "promise_made was %r" % store.promise_made
        assert store.box is opened_alone, "box was %r" % store.box

testcase route:
    $ _test.transition_timeout = 0.02
    $ _test.timeout = 45.0

    run Function(_reset_progress)
    run Function(_set_story_flags, False, False)
    run Jump("act2_2_1")

    advance until screen "choice"
    click expression '“It looks like love. A clumsy one.”'
    advance until screen "choice"
    click expression 'Sit down beside him and say nothing.'
    advance until screen "choice"
    click expression '“You can dance with the memory. Nobody’s watching.”'
    advance until screen "choice"
    click expression 'Catch his wrist with both hands. No Pen.'
    advance until screen "choice"
    click expression '“We can wait. A page can wait.”'
    advance until screen "choice"
    click expression 'Stay beside him. Say nothing at all.'
    advance until screen "choice"
    click expression 'Say it plainly, nothing else.'
    run Function(_assert_story_flags, True, False)
    advance until screen "choice"
    click expression 'Open it in the open, together.'
    run Function(_assert_story_flags, True, False)
    advance until screen "choice"
    click expression 'Go yourself, with Cyno at the door.'
    advance until screen "choice"
    click expression '“No.” Push the vial back across the glass.'
    advance until screen "choice"
    click expression 'Hold the Folio and refuse.'
    advance until screen "choice"
    click expression 'Sit down between them. Say nothing.'
    advance until screen "choice"
    click expression 'Stay still. Let them have it.'
    advance until screen "choice"
    click expression '“Don’t hide behind it. Own what you did, and I’ll stand beside you while you do.”'
    advance until screen "choice"
    click "Hand the pen to the Doctor"
    pause 0.4
    run Function(_assert_ending_seen, "archivist")
    exit


testcase endings:
    $ _test.transition_timeout = 0.02
    $ _test.timeout = 60.0

    run Jump("ending_wanderer")
    advance
    run Function(_assert_ending_seen, "wanderer")
    run Jump("ending_scaramouche")
    advance
    run Function(_assert_ending_seen, "scaramouche")
    run Jump("ending_true")
    advance
    run Function(_assert_ending_seen, "true")
    run Jump("ending_gnosis_box")
    advance
    run Function(_assert_ending_seen, "gnosis_box")
    run Jump("ending_burned_pages")
    advance
    run Function(_assert_ending_seen, "burned_pages")
    run Jump("ending_blank_page")
    advance
    run Function(_assert_ending_seen, "blank_page")
    run Jump("ending_neutral")
    advance
    run Function(_assert_ending_seen, "neutral")
    run Jump("ending_archivist")
    advance
    run Function(_assert_ending_seen, "archivist")
    run Jump("ending_burn_it_down")
    advance
    run Function(_assert_ending_seen, "burn_it_down")
    $ promise_made = True
    $ promise_broken = True
    run Jump("ending_quiet_page")
    advance
    run Function(_assert_ending_seen, "quiet_page")
    exit


testcase gnosis_route:
    $ _test.transition_timeout = 0.02
    $ _test.timeout = 40.0

    run Function(_set_story_flags, False, False)
    run Jump("act3_3_1")
    advance until screen "choice"
    click expression "Open it alone, behind the pillar, quickly."
    run Function(_assert_story_flags, False, True)
    advance until screen "choice"
    click expression "Go yourself, with Cyno at the door."
    advance until screen "choice"
    click expression '“No.” Push the vial back across the glass.'
    advance until screen "choice"
    click expression "Hold the Folio and refuse."
    advance until screen "choice"
    click expression "Sit down between them. Say nothing."
    advance until screen "choice"
    click expression "Stay still. Let them have it."
    advance until screen "choice"
    click expression '“Don’t hide behind it. Own what you did, and I’ll stand beside you while you do.”'
    advance until screen "choice"
    click expression '“Look into the case.”'
    pause 0.4
    run Function(_assert_ending_seen, "gnosis_box")
    exit


testcase ending_menu_routes:
    # Exercise the actual final menu conditions and jumps, not just ending labels.
    $ _test.transition_timeout = 0.02
    $ _test.timeout = 120.0

    run Function(_set_stats, 5, 0, 0, 0, False)
    $ store.box = False
    $ store.promise_broken = False
    run Jump("act4_4_4")
    advance until screen "choice"
    click expression '“Let him walk on.” Write the Wanderer’s name on the last line.'
    advance
    run Function(_assert_ending_seen, "wanderer")

    run Function(_set_stats, 0, 5, 0, 0, False)
    $ store.box = False
    $ store.promise_broken = False
    run Jump("act4_4_4")
    advance until screen "choice"
    click expression '“Let him write himself.” Write the Echo’s name on the last line.'
    advance
    run Function(_assert_ending_seen, "scaramouche")

    run Function(_set_stats, 4, 4, 7, 1, True)
    $ store.box = False
    $ store.promise_broken = False
    run Jump("act4_4_4")
    advance until screen "choice"
    click expression 'Put the pen down and write nothing. “The book is theirs. Both of theirs.”'
    advance
    run Function(_assert_ending_seen, "true")

    run Function(_set_stats, 0, 0, 0, 0, False)
    $ store.box = False
    $ store.promise_broken = False
    run Jump("act4_4_4")
    advance until screen "choice"
    click expression 'Let the page decide. Follow the ending you have earned.'
    advance
    run Function(_assert_ending_seen, "neutral")

    run Function(_set_stats, 0, 0, 0, 0, False)
    $ store.box = False
    $ store.promise_broken = False
    run Jump("act4_4_4")
    advance until screen "choice"
    click expression 'Hand the pen to the Doctor. Always available.'
    advance
    run Function(_assert_ending_seen, "archivist")

    run Function(_set_stats, 0, 0, 0, 2, False)
    $ store.box = False
    $ store.promise_broken = False
    run Jump("act4_4_4")
    advance until screen "choice"
    click expression 'Tear the Folio in half.'
    advance
    run Function(_assert_ending_seen, "burn_it_down")

    run Function(_set_stats, 0, 0, 0, 0, False)
    $ store.box = True
    $ store.promise_broken = False
    run Jump("act4_4_4")
    advance until screen "choice"
    click expression '“Look into the case.”'
    advance
    run Function(_assert_ending_seen, "gnosis_box")

    run Function(_set_stats, 0, 0, 0, 3, True)
    $ store.box = False
    $ store.promise_broken = False
    run Jump("act4_4_4")
    advance until screen "choice"
    click expression '“Follow the burning margin.”'
    advance
    run Function(_assert_ending_seen, "burned_pages")

    run Function(_set_stats, 0, 0, 0, 3, False)
    $ store.box = False
    $ store.promise_broken = False
    run Jump("act4_4_4")
    advance until screen "choice"
    click expression '“Leave the page blank.”'
    advance
    run Function(_assert_ending_seen, "blank_page")

    run Function(_set_stats, 0, 0, 0, 2, True)
    $ store.box = False
    $ store.promise_broken = False
    run Jump("act4_4_4")
    advance until screen "choice"
    click expression 'Leave before the last page is written.'
    advance
    run Function(_assert_ending_seen, "quiet_page")
    exit


testcase gates:
    $ _test.timeout = 20.0
    run Function(_set_stats, 0, 0, 0, 0, False)
    run Function(_assert_gate, "none")
    run Function(_assert_ending_target, "ending_neutral")
    run Function(_set_stats, 6, 1, 0, 0, False)
    run Function(_assert_gate, "wanderer")
    run Function(_assert_ending_target, "ending_wanderer")
    run Function(_set_stats, 1, 6, 0, 0, False)
    run Function(_assert_gate, "scaramouche")
    run Function(_assert_ending_target, "ending_scaramouche")
    run Function(_set_stats, 4, 4, 7, 1, True)
    run Function(_assert_gate, "true")
    run Function(_assert_ending_target, "ending_true")
    run Function(_set_stats, 9, 8, 9, 1, True)
    run Function(_assert_ending_target, "ending_true")
    run Function(_set_stats, 9, 9, 9, 2, True)
    run Function(_assert_ending_target, "ending_neutral")
    run Function(_set_stats, 4, 4, 6, 1, True)
    run Function(_assert_ending_target, "ending_neutral")
    run Function(_set_stats, 4, 4, 7, 1, False)
    run Function(_assert_ending_target, "ending_neutral")
    run Function(_set_stats, 4, 4, 6, 0, True)
    run Function(_assert_gate, "none")
    # Tied high bond scores must not unlock either individual ending.
    run Function(_set_stats, 5, 5, 6, 0, False)
    run Function(_assert_gate, "none")
    run Function(_assert_ending_target, "ending_neutral")
    # True ending takes priority when tied bond scores both meet its thresholds.
    run Function(_set_stats, 5, 5, 7, 1, True)
    run Function(_assert_gate, "true")
    run Function(_assert_ending_target, "ending_true")

    # Special-ending boundaries: case flag, Pen thresholds, and promise state.
    $ store.box = False
    run Function(_set_stats, 0, 0, 0, 0, False)
    run Function(_assert_special_gates, (False, False, False, False, False))
    $ store.box = True
    run Function(_assert_special_gates, (True, False, False, False, False))
    $ store.box = False
    run Function(_set_stats, 0, 0, 0, 2, False)
    run Function(_assert_special_gates, (False, False, False, True, False))
    run Function(_set_stats, 0, 0, 0, 3, False)
    run Function(_assert_special_gates, (False, False, True, True, False))
    run Function(_set_stats, 0, 0, 0, 3, True)
    run Function(_assert_special_gates, (False, True, True, True, False))
    run Function(_set_stats, 0, 0, 0, 2, True)
    run Function(_assert_special_gates, (False, False, False, True, True))
    exit



################################################################################
## Collection screens
################################################################################
##
## Run with:  renpy.sh . test catalogues
##
## Opens each collection screen from the main menu and confirms it appears.

testcase catalogues:
    $ _test.transition_timeout = 0.05
    $ _test.timeout = 15.0

    click "Pages Collected"
    run Function(_assert_shown, "endings_gallery")
    run Return()

    click "Gallery"
    run Function(_assert_shown, "cg_gallery")
    run Return()

    click "Music Room"
    run Function(_assert_shown, "music_room")
    run Return()

    click "Credits"
    run Function(_assert_shown, "credits")
    run Return()

    exit
