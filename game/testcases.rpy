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
