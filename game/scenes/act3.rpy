################################################################################
## Twice-Told Tale - Act 3: The Second Box  (scenes 3.1-3.7)
################################################################################
label act3_3_1:
    # DAY 22 · SCENE 3.1 · Sumeru City, the Akademiya Steps · Morning
    scene bg akademiya_dawn
    with act_wipe
    $ set_page(8, 22)
    $ show_act("III", "The Second Box")
    $ show_title("DAY 22 · SCENE 3.1\nSumeru City, the Akademiya Steps · Morning")
    play music audio.clean_instruments fadein 2.0  # “Clean Instruments”: sterile piano, a metronome underneath.
    # The Wanderer is walking half a step ahead of you. The Echo is a shade at your shoulder, visible only as a tint in the air where he stands.
    wanderer "Stay between us. Don’t speak to anyone in a white coat."
    echo "(dry) He means him. He knows no one else here would dare."
    mc "Is Dottore really in the city?"
    wanderer "Nahida says he’s registered under a false name at the Hall of Science. Which is the same as shouting it from the rooftops."
    echo "He wants to be found. He doesn’t do anything he doesn’t want observed."
    # A courier in a gray coat crosses the plaza and presses a small flat case into your hands before you can step away. He is gone into the crowd by the time you look up.
    scene cg black_case
    with scene_fade
    wanderer "Don’t."
    echo "(softly) Open it."

    # CHOICE: A black case and two opposite instructions.
    menu:
        "Open it in the open, together.":
            $ _sel_8 = "A"
            $ bump('w', 1)
            $ bump('b', 1)
        "Hand it to the Wanderer.":
            $ _sel_8 = "B"
            $ bump('w', 1)
        "Open it alone, behind the pillar, quickly.":
            $ _sel_8 = "C"
            $ bump('m', 1)

    if _sel_8 == 'A':
        # You hold it between the three of you. The brass clicks.
        pass
    elif _sel_8 == 'B':
        wanderer "(taking it, surprised) ...Thank you. [[He opens it with two fingers, as one handles something dead.]"
    elif _sel_8 == 'C':
        # Behind the pillar the latch pops easily. You’re alone with it for four seconds. It is
        # Inside the case, on black velvet, lies a glass lens the size of a coin. It is cold, and in the middle of it hangs a tiny captive electric glow.
        play sound audio.sfx_chime
        echo "(very quietly) That’s mine."
        wanderer "That’s ours."
        echo "(a sound that is almost a laugh) Don’t. Don’t make it ours now."
        scene cg gnosis_violet
        with scene_fade
        # A note lies folded beneath it.
        note "Archivist. You stole my half-written book and left me the ledger. Come to the Hall of Science tonight. Come alone, or the Gnosis stays in my drawer. I only want to talk. —D."

label act3_3_2:
    # SCENE 3.2 · The Annex · Afternoon
    $ show_title("SCENE 3.2\nThe Annex · Afternoon")
    scene bg annex_day
    with scene_fade
    tighnari "It’s a trap. The cleanest, most transparent trap in Sumeru. Do not go."
    cyno "If you do go, I stand outside the door. That’s not a request."
    nahida "The Gnosis is the bait, but it is not what he wants. He wants what the Folio has become."
    mc "What has it become?"
    nahida "A door. The first book that holds two selves of one soul without breaking either. He wants to open it, and see how it was made."
    wanderer "And then?"
    nahida "And then he’ll make a thousand of them."
    # A beat. Nobody speaks.
    echo "(coldly) He’ll make them out of people like Niwa."
    echo "I want to go."
    wanderer "No."
    echo "I’m not asking you."
    mc "(to both) Neither of you decides alone. That’s the rule."

    # CHOICE: Who goes to the Hall of Science?
    menu:
        "Go yourself, with Cyno at the door.":
            $ _sel_9 = "A"
            $ bump('m', 1)
            $ bump('w', 1)
        "Go with the Wanderer, openly.":
            $ _sel_9 = "B"
            $ bump('w', 2)
        "Go with the Echo, openly.":
            $ _sel_9 = "C"
            $ bump('b', 2)
        "Go alone, without telling anyone.":
            $ _sel_9 = "D"
            $ bump('pen', 1)

    # Whichever you choose, the Doctor has already planned for it. That is the point of him.

label act3_3_3:
    # DAY 24 · SCENE 3.3 · The Hall of Science · Night
    $ set_page(7, 24)
    $ show_title("DAY 24 · SCENE 3.3\nThe Hall of Science · Night")
    scene bg lab_white
    with scene_fade
    play music audio.the_doctor_s_hour fadein 2.0  # “The Doctor’s Hour”: a clean harpsichord line, played perfectly and with no warmth.
    dottore "(without turning) You came. Delightful. I had a wager with myself that you wouldn’t."
    dottore "(turning) The Folio-mender. And the Wanderer, of course. And... ah. There. There. Look at that shimmer behind your shoulder."
    echo "(from the air, tight) Don’t look at me."
    dottore "I’m not. I’m observing the empty space where you are. Entirely different."
    # He smiles. The smile goes nowhere near his eyes.
    dottore "Let’s not waste each other’s evening. I have a Gnosis, which you want. You have a book, which I want. I propose the oldest trade in the world."
    wanderer "No."
    dottore "I haven’t said the terms."
    wanderer "They’ll be monstrous."
    dottore "They’ll be generous, which is worse."
    # He takes a slim vial from his pocket and sets it on the glass table. It glows a pale gold.
    dottore "You two are a mistake. A beautiful one, perhaps, but a mistake. Two halves of one mind, both desperately overcrowding one little body. I can fix that."
    dottore "One draught. The Echo is returned to the Wanderer, whole, sealed, quiet. No more arguing at dinner. No more tinting the air. No more ink."
    dottore "The Wanderer gets his Gnosis back. And the book gets to be mine."
    # Silence. The harpsichord ticks on.
    wanderer "(very low) ...He means to erase him."
    dottore "I mean to reintegrate him. The word matters."
    echo "It means the same thing. The word is just a nicer coat."
    # The Echo’s voice has gone thin. The Wanderer’s hand has tightened on his own sleeve.
    # They both look at you.

    # CHOICE: The Doctor’s deal.
    menu:
        "“No.” Push the vial back across the glass.":
            $ _sel_10 = "A"
            $ bump('w', 1)
            $ bump('b', 1)
            $ bump('m', 1)
        "“What happens to the book?” Stall and listen.":
            $ _sel_10 = "B"
            $ bump('m', 1)
        "“Let them decide. Out loud.”":
            $ _sel_10 = "C"
            $ bump('w', 1)
            $ bump('b', 1)
        "Take the vial. Pocket it quietly.":
            $ _sel_10 = "D"
            $ bump('pen', 2)

    if _sel_10 == 'A':
        dottore "(delighted) Oh, I knew you’d say that. Pity. I’d already printed the second page of the proposal."
    elif _sel_10 == 'B':
        dottore "The book belongs to a library, naturally. My library."
        mc "(inwardly) That isn’t an answer. That’s a menu."
    elif _sel_10 == 'C':
        wanderer "I don’t want to be whole if the price is him."
        echo "(a long beat) ...And I’d like to keep my seat at the table. Small as it is."
    elif _sel_10 == 'D':
        # The vial is warm against your palm. The Doctor’s smile deepens by one precise
        dottore "(softly) Good. Hold it. Hold it and think."

label act3_3_4:
    # SCENE 3.4 · The Locked Room
    $ show_title("SCENE 3.4\nThe Locked Room")
    play sound audio.sfx_glass  # Glass, rotating. A hiss. A door sealing.
    scene bg lab_glasscube
    with scene_fade
    dottore "(over a speaker, cheerful) I did say I only wanted to talk. I never promised you’d leave while we did."
    scene cg glass_cell
    with scene_fade
    wanderer "(muffled) Let her out!"
    dottore "The Folio, please. The remaining pages are the only thing I need. Slide it through the slot. After that, the Gnosis and the draught are yours."
    echo "(barely audible, behind the glass) Don’t. Please don’t. He’ll tear the last three pages out and burn the rest."
    echo "I know what he does. I was there when he did it to me."
    # The glass cube’s walls begin to hum.
    play music audio.clean_instruments fadein 2.0  # “Clean Instruments” returns, but warped. A string tears slowly across it.

    # CHOICE: The hostage choice.
    menu:
        "Hold the Folio and refuse.":
            $ _sel_11 = "A"
            $ bump('w', 1)
            $ bump('b', 1)
            $ bump('m', 1)
        "Tear out one blank page and slide that through.":
            $ _sel_11 = "B"
            $ bump('m', 2)
        "Write a single word in the margin, quickly, in the hum.":
            $ _sel_11 = "C"
            $ bump('m', 1)
        "Slide the Folio through the slot.":
            $ _sel_11 = "D"
            $ bump('pen', 2)

    if _sel_11 == 'A':
        dottore "Then we wait. I’m very good at waiting. It is, I believe, the one trait the two of us share."
    elif _sel_11 == 'B':
        # Dottore examines the page against the light for four full seconds.
        dottore "(with something like admiration) ...Clever. Not enough. But clever."
    elif _sel_11 == 'C':
        # You write: open. The word flares. Hairline cracks run across the glass cell, hard to see,
        pass
    elif _sel_11 == 'D':
        # The Folio slides through the slot like a letter dropped in a mailbox. It makes no sound
        pass

label act3_3_5:
    # SCENE 3.5 · The Echo Breaks the Glass
    $ show_title("SCENE 3.5\nThe Echo Breaks the Glass")
    scene bg lab_flicker
    with scene_fade
    echo "I can’t do this alone. I haven’t the strength."
    wanderer "(through the glass) Then use mine."
    echo "You’ve never offered before."
    wanderer "I’ve never needed to."
    scene cg two_palms
    with scene_fade
    play sound audio.sfx_glass  # Glass shattering. A thunderclap, not from the sky. A roar of violet light, followed by silence.
    # The glass cube falls in a cascade of bright dust.
    # And in the dust, for the first time, the two of them are standing side by side in the same room: the Wanderer’s body, and the Echo, visible and solid, to every eye in the laboratory. It lasts four seconds. It looks like both of them are about to fall over.
    dottore "(delighted, whispering) Oh. You can do that. You can do that."
    dottore "Thank you. Truly. That’s the data I needed."
    # He steps back through a door that wasn’t there a moment ago. It closes. A lock turns.
    cyno "(kicking at the door, snarling) He’s gone."
    tighnari "He had it planned. The whole thing was a test of whether they could do it."
    # On the floor, in the glittering dust, lies a small velvet case. It is open. The Gnosis is gone.
    # Beside it lie a torn corner of the Folio and a single line of the Doctor’s handwriting.
    note "Day 30. The old dawn. I’ll collect the rest then. —D."

label act3_3_6:
    # DAY 25 · SCENE 3.6 · The Annex · Dawn
    $ set_page(6, 25)
    $ show_title("DAY 25 · SCENE 3.6\nThe Annex · Dawn")
    scene bg annex_dawn
    with scene_fade
    play music audio.what_we_can_t_take_back fadein 2.0  # “What We Can’t Take Back”: a single low cello.
    # The Echo is solid, and cannot stop looking at his own hands.
    echo "He used us. We did exactly what he wanted."
    wanderer "We also saved her."
    echo "Both can be true."
    # The Wanderer lowers himself to the floor and leans his back against the table. The Echo does the same, a foot away.
    # For a long moment neither speaks.
    wanderer "You held my hand."
    echo "(sharp) Our hands were on the same wall."
    wanderer "You held my hand."
    echo "...Yes."
    # He pulls his knees up. He looks younger than he ever has.
    echo "I’m so tired of hating you. It takes more than I have."
    wanderer "I’m so tired of being afraid of you."
    # The two of them laugh, once, at the same time, and neither of them knows what to do about it.

    # CHOICE: The quiet after.
    menu:
        "Sit down between them. Say nothing.":
            $ _sel_12 = "A"
            $ bump('w', 1)
            $ bump('b', 1)
        "Make tea. Three cups.":
            $ _sel_12 = "B"
            $ bump('m', 1)
        "Ask the Wanderer what he’s most afraid the Echo will say on Day 30.":
            $ _sel_12 = "C"
            $ bump('w', 2)
        "Ask the Echo what he’s most afraid the Wanderer will say on Day 30.":
            $ _sel_12 = "D"
            $ bump('b', 2)

    if _sel_12 == 'C':
        wanderer "That I was right to throw him away."
        wanderer "And that I’d do it again. (quietly) I wouldn’t. But I’m afraid he’ll think I would."
    elif _sel_12 == 'D':
        echo "That he’ll say “I’m sorry.”"
        echo "(brittle) I don’t know what to do with sorry. I’ve never been given one."

label act3_3_7:
    # DAY 27 · SCENE 3.7 · The Rooftop of the Annex · Evening
    $ set_page(4, 27)
    $ show_title("DAY 27 · SCENE 3.7\nThe Rooftop of the Annex · Evening")
    scene bg rooftop_night
    with scene_fade
    play music audio.three_pages fadein 2.0  # “Three Pages”: piano, spare, patient.
    # The Folio has three pages left that aren’t torn or inked, and the Doctor’s torn corner is stitched onto the margin with a thread of his own cold handwriting. The thread is shaped like a clean signature.
    # Nahida appears at the stair door, very small against the dark.
    nahida "Whatever you write on the last page, you’ll be writing it for all of us."
    nahida "There is a hole in the pages where the Doctor tore. You can fill it, or leave it. If you fill it, you’ll be choosing something. The Folio has never been asked to choose before."
    mc "What would I be choosing?"
    nahida "Who gets to hold the pen."
    # She looks at the sky.
    nahida "One of them, or neither, or both. I won’t tell you which is right. I’m the God of Wisdom; I know that’s a lie that people mostly want to be told."
    # She smiles, small and tired, and goes back down.
    n "SCORE CHECK (hidden): If PEN ≥ 3, the Folio begins to glow on its own, and the Echo knows it. Proceed to Act 4 · Bad Route Warning (the book starts burning from the margins; the ink answers to the Doctor’s pen, not yours). Otherwise, proceed to Act 4 · Day 28."
    # END OF ACT 3
    n "Act 4: The Fourth Page Two confessions and one dawn. The Rule of Three says a thing changes on the fourth."

    jump act4_4_1

