################################################################################
## Twice-Told Tale - Act 4: The Doctor's Hour  (scenes 4.1-4.4)
################################################################################
label act4_4_1:
    # DAY 28 · SCENE 4.1 · The Archive Annex · Evening
    scene bg annex_evening
    with act_wipe
    $ set_page(2, 28)
    $ show_act("IV", "The Doctor's Hour")
    $ show_title("DAY 28 · SCENE 4.1\nThe Archive Annex · Evening")
    play music audio.what_i_never_said fadein 2.0  # “What I Never Said”: solo piano, slow, one hand.
    if pen >= 3:
        # The Folio's warning is part of the story; no unimplemented stat penalty is implied.
        n "The margins of the Folio smolder, a thin orange line eating inward. The ink moves in a clean, cold hand that isn’t yours."
        wanderer "(low) Quill, the page is burning."
        wanderer "Whatever you’ve done... he’s writing through it now."
    wanderer "I owe you an explanation."
    echo "You owe me more than that."
    wanderer "I know."
    echo "Don’t start."
    n "The Wanderer looks down at his hands. He rubs a thumb over the old callus at the base of his finger, then seems to realize he is doing it."
    wanderer "When I left the Shogun’s palace, I told myself I was the one who’d been wronged. That if I walked away, I could keep the part of me that hadn’t been ruined yet."
    echo "And what about me?"
    wanderer "I didn’t think about you."
    echo "You must have."
    wanderer "I did. That’s why I kept moving."
    n "The Echo’s arms loosen. He looks furious about it."
    wanderer "For five hundred years, I was relieved nobody could ask me why I’d left you. I told myself I’d survived. I didn’t ask what survival had cost you."
    echo "(quietly) I asked you. Every night."
    wanderer "I heard you."
    echo "..." 
    wanderer "I turned up the wind until I couldn’t hear you anymore."
    n "The room goes quiet. The kettle ticks as it cools."
    wanderer "I’m sorry."
    echo "That’s it?"
    wanderer "That’s what I have. I’m not going to dress it up."
    echo "Say it again."
    wanderer "I’m sorry I left you there."
    scene cg echo_bowed
    with iris_open

    # CHOICE: The silence that follows.
    menu:
        "Stay still. Let them have it.":
            $ _sel_13 = "A"
            $ bump('m', 1)
        "Quietly slide the teapot across, an offering.":
            $ _sel_13 = "B"
            $ bump('w', 1)
            $ bump('b', 1)
        "Look at the Echo. Wait to see if he wants you.":
            $ _sel_13 = "C"
            $ bump('b', 2)
        "Put a hand on the Wanderer’s sleeve.":
            $ _sel_13 = "D"
            $ bump('w', 2)

    if _sel_13 == 'A':
        # The room holds its breath. Nobody speaks. It’s the kindest thing you could have
        pass
    elif _sel_13 == 'B':
        echo "(thick) ...You already made tea. You’re a menace."
        n "He takes the cup with both hands. He waits for the Wanderer to look at him before he drinks."
    elif _sel_13 == 'C':
        echo "(without looking up) Not now."
        n "You start to draw your hand back. The Echo catches your sleeve with two fingers."
        echo "Stay, though."
    elif _sel_13 == 'D':
        wanderer "(a shaky breath) Thanks."
        n "He looks embarrassed by the word, as if it has come out in the wrong voice."

label act4_4_2:
    # DAY 29 · SCENE 4.2 · The Roof of the Archive · Night
    $ set_page(1, 29)
    $ show_title("DAY 29 · SCENE 4.2\nThe Roof of the Archive · Night")
    scene bg rooftop_night
    with scene_fade
    play music audio.the_last_evening fadein 2.0  # “The Last Evening”: the lullaby from Act 2, now in a major key. It is almost unbearable.
    echo "My turn."
    echo "I have a lie to unravel, and I want you to be the one who hears it. Not him. You."
    mc "I’ll hear it."
    echo "There’s something I haven’t told you."
    mc "Is it about the schools?"
    echo "You know about the schools?"
    mc "I know the records. I didn’t know what was true."
    echo "Well. The records got that part wrong."
    n "He picks at a loose thread on his sleeve. It comes free. He winds it around one finger."
    echo "I broke the Futsu. I helped scatter the Hyakume. I was there when the Senju fell. I did it because I wanted them to hurt the way I’d been hurt."
    mc "Do you regret it?"
    echo "Of course I regret it. I also remember how it felt to win."
    n "He looks up, daring you to flinch."
    echo "The book says someone else did it. Part of me is glad. Part of me hates that I’m glad."
    echo "I don’t know what to do with that."

    # CHOICE: The lie that lets him off.
    menu:
        "“Don’t hide behind it. Own what you did, and I’ll stand beside you while you do.”":
            $ _sel_14 = "A"
            $ bump('b', 2)
            $ bump('m', 1)
        "“The record can be wrong and you can still be sorry. Both are true.”":
            $ _sel_14 = "B"
            $ bump('m', 2)
        "“Leave the record. You don’t owe the dead your suffering.”":
            $ _sel_14 = "C"
            $ bump('b', -1)
            $ bump('pen', 1)
        "“I don’t care what the book says. I know who you are now.”":
            $ _sel_14 = "D"
            $ bump('b', 2)

    if _sel_14 == 'A':
        echo "(a short, harsh laugh) You make it sound easy."
        echo "(quieter) ...Stay, then. Don’t promise you’ll like me."
    elif _sel_14 == 'B':
        echo "Both."
        n "He says it again under his breath, as if checking whether the word changes the facts."
        echo "I don’t know if I can believe that yet."
    elif _sel_14 == 'C':
        echo "(sharp) Don’t excuse me. I did it. I don’t want a kinder version of the story."
        echo "I just don’t know if the true version is the whole of me."
    elif _sel_14 == 'D':
        # He says nothing for a long, long time. Then, abruptly:
        echo "Idiot."
        n "He says it without looking at you. For once, he doesn’t take it back."
        play sound audio.sfx_bell  # A distant bell. Midnight.
        echo "Tomorrow the Doctor comes. Tomorrow the book ends. Tomorrow I find out whether any of this was real."
        echo "I’m... asking you not to leave before then."
        mc "I promised."
        echo "(turning away) I’m aware. I’m saying it anyway."

label act4_4_3:
    # DAY 30 · SCENE 4.3 · The Archive Door · Dawn
    $ set_page(1, 30)
    $ show_title("DAY 30 · SCENE 4.3\nThe Archive Door · Dawn")
    scene bg annex_dawn
    with scene_fade
    play music audio.the_old_dawn fadein 2.0  # “The Old Dawn”: strings rising from nothing, a drumbeat, soft, in the distance.
    # You stand at the door. The Folio is under your arm. Behind you, the Wanderer and the Echo stand shoulder to shoulder, in the same weak light.
    # The street is empty. Then it isn’t.
    scene cg doctor_lane
    with door_blinds
    dottore "Good morning. You came after all."
    mc "You said you’d meet us here."
    dottore "I said I would be here. I made no promises about the terms."
    dottore "The Folio. The last page. The Echo’s seal. Give me those, and the Wanderer walks away. The Echo will be returned to the record."
    echo "You mean erased."
    dottore "I mean I won’t have to keep explaining the difference."
    wanderer "(stepping forward) Don’t come any closer."
    echo "(at the same time) For once, I agree with him."
    # They look at each other. A flicker of something almost comic crosses both their faces. Then it’s gone.
    # The air splits. Green light rolls across the street. The Folio flares in your arms, and the three white pages turn themselves, one by one.
    play sound audio.sfx_page  # Pages, turning. A choir, far off.
    with quake
    nahida "(arriving at the end of the lane, breathless) He’s forced the last page open."
    mc "Can we close it?"
    nahida "Not now. The story is moving on its own."
    nahida "But you can still choose what you write into it."
    # The pen appears in your hand. It was never a pen. It is the quill you mended page eleven with.

label act4_4_4:
    # SCENE 4.4 · The Last Page · The Choice
    $ show_title("SCENE 4.4\nThe Last Page · The Choice")
    scene bg white_page_street
    with scene_fade
    play music audio.the_old_dawn fadein 2.0
    play sound audio.sfx_bell  # A distant bell. The first light, spilling.
    # Several lines wait on the page, unsigned. They are the ways the tale can end.
    # THE LAST CHOICE. Gate checks are hidden and applied automatically, unless noted.

    menu:
        "“Let him walk on.” Write the Wanderer’s name on the last line." if (w >= 5 and w > b):
            $ _sel_15 = "A"
            jump ending_wanderer
        "“Let him write himself.” Write the Echo’s name on the last line." if (b >= 5 and b > w):
            $ _sel_15 = "B"
            jump ending_scaramouche
        "Put the pen down and write nothing. “The book is theirs. Both of theirs.”" if (m >= 7 and w >= 4 and b >= 4 and pen <= 1 and promise_made):
            $ _sel_15 = "C"
            jump ending_true
        "Let the page decide. Follow the ending you have earned.":
            jump ending_router
        "Hand the pen to the Doctor. Always available.":
            $ _sel_15 = "D"
            jump ending_archivist
        "Tear the Folio in half." if (pen >= 2):
            $ _sel_15 = "E"
            jump ending_burn_it_down
        "“Look into the case.”" if (box):
            $ _sel_15 = "F"
            jump ending_gnosis_box
        "“Follow the burning margin.”" if (promise_made and pen >= 3):
            $ _sel_15 = "G"
            $ promise_broken = True
            jump ending_burned_pages
        "“Leave the page blank.”" if (pen >= 3):
            $ _sel_15 = "H"
            jump ending_blank_page
        "Leave before the last page is written." if (promise_made and pen < 3):
            $ _sel_15 = "I"
            $ promise_broken = True
            jump ending_quiet_page

    # Every option routes explicitly; the page-decision choice uses the automatic gate order.
    # END OF ACT 4
    # The Endings Every main ending (Wanderer, Scaramouche, True, and Neutral) shares the same first beat: the Doctor’s defeat. What differs is what is left standing afterward. The Gnosis Box, Burned Pages, Blank Page, and the two bad endings have their own scenes.

