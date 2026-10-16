################################################################################
## Twice-Told Tale - Characters
################################################################################
##
## Speaking cast, plus the narrator, the player-named heroine, and the two
## special dialogue tags used by the ending scenes.

## The heroine. Her name is entered by the player during the prologue.
## Dialogue tags in the script are "MC".
define mc = Character("[mc_name]", color="#e58aa8", who_outlines=[(1, "#00000080")])

## The Wanderer. Dry, clipped, sarcastic.
define wanderer = Character("Wanderer", color="#6fd3c7", who_outlines=[(1, "#00000080")])

## Scaramouche / The Echo. Theatrical, silky, venomous.
## Dialogue tag in the script is SCARAMOUCHE.
define echo = Character("Scaramouche", color="#b06bd6", who_outlines=[(1, "#00000080")])

## Nahida. Gentle, exact, sly.
define nahida = Character("Nahida", color="#8fd35a", who_outlines=[(1, "#00000080")])

## Dottore. Courteous, clinical, curious.
define dottore = Character("Dottore", color="#7fb0d9", who_outlines=[(1, "#00000080")])

## Prose narration. No name box.
define n = Character(None, what_prefix="", what_suffix="")

## A margin note written in the Folio.
define margin = Character("Margin Note", color="#c9a0e0", what_italic=True,
                          who_outlines=[(1, "#00000080")])

## A line that appears in the Folio that is not in any known hand.
define newline_char = Character("New Line", color="#bdbdbd", what_italic=True,
                                who_outlines=[(1, "#00000080")])

## A note left for MC (the Doctor's notes).
define note = Character("Note", color="#bdbdbd", what_italic=True,
                        who_outlines=[(1, "#00000080")])


## ---- Supporting cast (Act 2 onward; defined now so later scenes resolve) ---

define tighnari = Character("Tighnari", color="#a8c860", who_outlines=[(1, "#00000080")])
define cyno = Character("Cyno", color="#c0a060", who_outlines=[(1, "#00000080")])
define miko = Character("Yae Miko", color="#e08fb0", who_outlines=[(1, "#00000080")])
define ei = Character("Ei", color="#9a7fd0", who_outlines=[(1, "#00000080")])

## The past self, before Irminsul: the operative "Escher" is the Doctor in
## disguise, and the puppet/boy are the Wanderer's earlier forms.
define escher = Character("Escher", color="#7fb0d9", who_outlines=[(1, "#00000080")])
define puppet = Character("The Puppet", color="#b06bd6", what_italic=True,
                          who_outlines=[(1, "#00000080")])
define boy = Character("The Boy", color="#c9a0e0", who_outlines=[(1, "#00000080")])
define niwa = Character("Niwa", color="#c0a878", who_outlines=[(1, "#00000080")])
define katsuragi = Character("Katsuragi", color="#a0a0c0", who_outlines=[(1, "#00000080")])
define worker = Character("Worker", color="#9a9a9a", who_outlines=[(1, "#00000080")])
define worker2 = Character("Worker 2", color="#9a9a9a", who_outlines=[(1, "#00000080")])
define student = Character("Student", color="#9a9a9a", who_outlines=[(1, "#00000080")])

## Ending cards (a full-screen title + body, styled large and centred).
define end_card = Character(None, what_style="end_card_text")

style end_card_text is say_dialogue:
    size 40
    xalign 0.5
    textalign 0.5
