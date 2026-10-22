################################################################################
## Twice-Told Tale - Variables
################################################################################
##
## All persistent story state lives here. These are `default` variables, so
## they are reset at the start of a new game and carried by saves.

## The player-named heroine. The Echo calls her "Quill" regardless.
default mc_name = "Quill"

## Bonds. W and B are visible to the player; M is hidden ("Mend").
default w = 0                # Wanderer Bond
default b = 0                # Balladeer (Scaramouche / the Echo) Bond
default m = 0                # Mend (hidden)

## The Editor's Pen. Each use of the Pen to rewrite the page increments this.
default pen = 0

## Story flags.
default fixer = False        # Set when the player uses the Pen to "fix" a hurt.
default box = False          # Set only when MC opens the black case alone (3.1).
default promise_made = False # Set by every option in Scene 2.16.
default promise_broken = False  # Set by the high-Pen and Quiet Page choices at 4.4.

## Diegetic page counter. Thirty days, thirty pages.
default pages_left = 30
default current_day = 0
