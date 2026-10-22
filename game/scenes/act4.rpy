################################################################################
## Twice-Told Tale - Act 4: The Doctor's Hour  (scenes 4.1-4.4)
################################################################################
label act4_4_1:
    # DAY 28 · SCENE 4.1 · The Archive Annex · Evening
    scene bg annex_evening
    with act_wipe
    $ set_page(3, 28)
    $ show_act("IV", "The Doctor's Hour")
    $ show_title("DAY 28 · SCENE 4.1\nThe Archive Annex · Evening")
    play music audio.what_i_never_said fadein 2.0  # “What I Never Said”: solo piano, slow, one hand.
    n "If PEN ≥ 3 (Bad Route Warning): [[The margins of the Folio smolder, a thin orange line eating inward. The ink obeys a clean, cold hand that isn’t yours. The Wanderer sees it before you do.]"
    wanderer "(low) Quill, the page is burning."
    wanderer "Whatever you’ve done... stop. [[Reduce all remaining pages by 1. The Doctor’s pen is writing the book now. Proceed to the Day 28 scene as normal, but every choice that adds W or B adds 1 less.]"
    wanderer "I owe you an account."
    wanderer "The Echo has waited five centuries for it. I’m not sure he’ll want to hear it from me. But he has to hear it from someone."
    # The air beside him thickens into the Echo. He sits on the arm of the sofa, arms folded, listening with the full attention of someone pretending he isn’t.
    wanderer "When I was cut loose, when I was made to go, I thought: good. I thought: let him be the one who suffers, the one who stays with the Shogun’s silence. I’ll walk away with the part of me that still has a chance."
    wanderer "And I called it surviving."
    wanderer "I spent five hundred years in a body that remembered nothing, wearing a name that belonged to nobody, and I was relieved. I was relieved that there was no one left to ask me what I had abandoned."
    echo "(small) I asked. Every night."
    wanderer "I know. I could hear you. I’d turn up the wind until I couldn’t."
    # A very long silence.
    wanderer "I’m sorry. It isn’t enough. It was never going to be enough. But it’s true, and I’m not going to hide behind a smaller word."
    echo "(rough) Say it again."
    wanderer "I’m sorry."
    echo "Again."
    wanderer "I’m sorry. I’m sorry I left you in there."
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
        echo "(thick) ...You’ve already made it. You’re a menace. [[He takes a cup.]"
    elif _sel_13 == 'C':
        echo "(without looking up) Not now. [[A beat.] ...Stay, though."
    elif _sel_13 == 'D':
        wanderer "(a shuddering breath) Thank you. I thought I’d have to do this alone."

label act4_4_2:
    # DAY 29 · SCENE 4.2 · The Roof of the Archive · Night
    $ set_page(2, 29)
    $ show_title("DAY 29 · SCENE 4.2\nThe Roof of the Archive · Night")
    scene bg rooftop_night
    with scene_fade
    play music audio.the_last_evening fadein 2.0  # “The Last Evening”: the lullaby from Act 2, now in a major key. It is almost unbearable.
    echo "My turn."
    echo "I have a lie to unravel, and I want you to be the one who hears it. Not him. You."
    mc "I’ll hear it."
    echo "The history books say a madman with a bladesmith’s grudge broke the sword schools of Inazuma. A nameless smith, nursing his dead father’s hate."
    echo "It’s in a letter now. Kaedehara Yoshinori’s. The record changes, and the world tells itself the tale it prefers."
    echo "It’s wrong."
    # He turns his head. In the starlight, the violet of his eyes is almost the color of the ink.
    echo "It was me. I broke the Futsu. I scattered the Hyakume. I tore down the Senju. I did it for a Shogun who had thrown me away and a God who would never say my name."
    echo "I was good at it. That’s the part I can’t stop hearing."
    echo "And now the book says it was someone else, and everyone is relieved, and no one has to know."
    echo "I can’t tell if I’m angry that the lie exists, or grateful."

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
            $ bump('b', 1)
            $ bump('pen', 1)
        "“I don’t care what the book says. I know who you are now.”":
            $ _sel_14 = "D"
            $ bump('b', 2)

    if _sel_14 == 'A':
        echo "(a short, harsh laugh) You would say that."
        echo "(quieter) ...Stand beside me, then. We’ll see how long you last."
    elif _sel_14 == 'B':
        echo "Both. (he repeats it like a foreign word) Both. That is... a very small and very large thing to ask."
    elif _sel_14 == 'C':
        echo "(narrow) Don’t excuse me. I’d rather be hated truthfully. [[The temperature drops a degree.]"
    elif _sel_14 == 'D':
        # He says nothing for a long, long time. Then, abruptly:
        echo "Idiot. [[It is the gentlest thing he has ever called you.]"
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
    dottore "Good morning. You kept your promise. How quaint."
    dottore "I’ll make this brief. The Folio, the last page, and the Echo’s seal. In return, the Wanderer lives. The Echo is... filed."
    wanderer "(stepping forward) Try it."
    echo "(stepping forward at the same time) Try it."
    # They look at each other. A flicker of something almost comic crosses both their faces. Then it’s gone.
    # The air splits. Green light rolls across the street. The Folio flares in your arms, and the three white pages turn themselves, one by one.
    play sound audio.sfx_page  # Pages, turning. A choir, far off.
    with quake
    nahida "(arriving at the end of the lane, small and very serious) The Doctor has forced the final page open. The book will be written now whether we choose or not."
    nahida "Who writes it is up to you."
    # The pen appears in your hand. It was never a pen. It is the quill you mended page eleven with.

label act4_4_4:
    # SCENE 4.4 · The Last Page · The Choice
    $ show_title("SCENE 4.4\nThe Last Page · The Choice")
    scene bg white_page_street
    with scene_fade
    play music audio.the_old_dawn fadein 2.0
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

    # Every option routes explicitly; the page-decision choice uses the automatic gate order.
    play sound audio.sfx_bell  # A distant bell. The first light, spilling.
    # END OF ACT 4
    # The Endings Every main ending (Wanderer, Scaramouche, True, and Neutral) shares the same first beat: the Doctor’s defeat. What differs is what is left standing afterward. The Gnosis Box, Burned Pages, Blank Page, and the two bad endings have their own scenes.

