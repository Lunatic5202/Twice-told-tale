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
    wanderer "Stay between us. And don’t talk to anyone in a white coat."
    mc "That narrows it down in the Akademiya."
    echo "He means the Doctor. Try to keep up."
    wanderer "Nahida says he’s registered under a false name at the Hall of Science."
    mc "So he wants us to find him."
    echo "Or he wants us to think we found him. Either way, don’t walk in first."
    # A courier in a gray coat crosses the plaza and presses a small flat case into your hands before you can step away. He is gone into the crowd by the time you look up.
    scene cg black_case
    with iris_open
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
        scene cg gnosis_violet
        with iris_open
        play sound audio.sfx_chime
        echo "That’s mine."
        wanderer "Then we don’t leave it in his hands."
        note "Archivist. You stole my half-written book and left me the ledger. Come to the Hall of Science tonight. Come alone, or the Gnosis stays in my drawer. I only want to talk. —D."
    elif _sel_8 == 'B':
        wanderer "(taking it, surprised) ...Thank you."
        # He opens it with two fingers, as one handles something dead.
        scene cg gnosis_violet
        with iris_open
        play sound audio.sfx_chime
        echo "That’s mine."
        wanderer "I know. I’m not taking it from you."
        note "Archivist. You stole my half-written book and left me the ledger. Come to the Hall of Science tonight. Come alone, or the Gnosis stays in my drawer. I only want to talk. —D."
    elif _sel_8 == 'C':
        $ box = True
        # Behind the pillar the latch pops easily. You’re alone with it for four seconds. It is
        # Inside the case, on black velvet, lies a glass lens the size of a coin. It is cold, and in the middle of it hangs a tiny captive electric glow.
        play sound audio.sfx_chime
        echo "(very quietly) That’s mine."
        wanderer "That’s ours."
        echo "(a sound that is almost a laugh) Don’t. Don’t make it ours now."
        scene cg gnosis_violet
        with iris_open
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
            $ bump('m', -1)

    if _sel_9 == 'A':
        cyno "I’ll be outside the door. If anything changes, say my name."
        mc "You’ll hear it."
    elif _sel_9 == 'B':
        wanderer "I’ll stand beside you. No speaking for you, unless you ask."
        mc "That’s all I need."
    elif _sel_9 == 'C':
        echo "You chose me. Don’t make me regret trusting that."
        mc "I won’t ask you to be anyone else."
    elif _sel_9 == 'D':
        wanderer "You came without telling us. I can see that."
        echo "And you still brought the book. That’s enough for him."

    # Whichever approach you choose, the Doctor has already planned for it.


label act3_3_2b:
    # DAY 23 · SCENE 3.2B · The Annex · Late Afternoon
    $ set_page(7, 23)
    $ show_title("DAY 23 · SCENE 3.2B\nThe Archive Annex · Late Afternoon")
    scene bg annex_day
    with soft_dissolve
    stop music fadeout 1.0
    play music audio.the_table fadein 2.0

    n "The case sits in the middle of the table. Nobody has touched it since the courier left. The room has arranged itself around it: three cups, three chairs, and one thing none of them will name."

    wanderer "We should give it to Nahida."
    echo "And tell her what? That the Doctor mailed me a piece of myself like a party invitation?"
    wanderer "I was going to say we should tell her the truth."
    echo "You always say that as though truth were one object. Something you can put on a table and point at."
    mc "Then tell me what part you think is missing."

    n "The Echo looks at the Folio, not at you. His outline is clearer than it was yesterday. The light catches the seam of his sleeve; for one impossible second, it looks like cloth instead of a memory of cloth."

    echo "When he changed his name, the world changed around him. People forgot. Records rearranged themselves. But I was left with the before. I remember every version he tried to bury."
    wanderer "I didn't bury you because I thought you were a lie."
    echo "No. You buried me because I was true."
    wanderer "..."
    echo "That is worse, isn't it?"

    menu:
        "Ask the Wanderer what he remembers choosing.":
            $ bump('w', 1)
            wanderer "I remember wanting the pain to stop. I told myself that if I could stop remembering, I could stop being the person who caused it."
            wanderer "I never asked who would be left holding the memories."
            echo "You can start by not looking away when I speak."
        "Ask the Echo what he wants besides an apology.":
            $ bump('b', 1)
            echo "A day that belongs to me. A choice that isn't made for me. A name I can keep without it being a weapon."
            mc "Those sound like things we can begin with."
            echo "Begin. Such a hopeful word for a room full of unfinished things."
        "Move the case away from the Folio.":
            $ bump('m', 1)
            n "You slide the case to the far end of the table. It is a small movement. Both of them watch your hand as if you have moved a mountain."
            mc "We don't have to let him set the terms of every conversation."
            wanderer "No. We don't."
            echo "Keep saying that until we believe it."

    play sound audio.sfx_page
    n "A line appears in the Folio's margin, written in a narrow hand neither of them recognizes: 'A door is not a home.'"
    mc "Did either of you write that?"
    wanderer "No."
    echo "And yet it sounds like something I would have said."
    n "Outside, the Akademiya bells mark the hour. The case remains closed. For the first time since it arrived, nobody is waiting for it to open."


label act3_3_3:
    # DAY 24 · SCENE 3.3 · The Hall of Science · Night
    $ set_page(6, 24)
    $ show_title("DAY 24 · SCENE 3.3\nThe Hall of Science · Night")
    scene bg lab_white
    with squares_wipe
    show dottore pleasant at at_center
    with soft_dissolve
    play music audio.the_doctor_s_hour fadein 2.0  # “The Doctor’s Hour”: a clean harpsichord line, played perfectly and with no warmth.
    dottore "(without turning) You came. I wasn’t sure you would."
    dottore "(turning) The Folio-mender. The Wanderer. And the rather interesting gap beside you."
    echo "(from the air) Stop staring at it."
    dottore "I’m looking at the room. You happen to be the most interesting thing missing from it."
    # He smiles. The smile goes nowhere near his eyes.
    if _sel_9 == "D":
        n "You came alone. The corridor behind you is empty. Somewhere beyond the wall, a second lock turns."
        n "The Doctor notices you listening and says nothing."
    dottore "I have the Gnosis you came for. You have the book I want. We could save ourselves a great deal of time."
    wanderer "No."
    dottore "You haven’t heard the offer."
    wanderer "I’ve met you."
    dottore "That does tend to shorten negotiations."
    # He takes a slim vial from his pocket and sets it on the glass table. It glows a pale gold.
    dottore "The Echo is unstable. You know that. He’s becoming visible, then solid, then neither. How long do you think he can keep doing that?"
    echo "Long enough to tell you to go to hell."
    dottore "Charming. I can stop the instability. One draught, and you’re back where you belong."
    wanderer "Inside me."
    dottore "Integrated. Quiet. No more pain for either of you."
    echo "You mean I stop being a person."
    dottore "I mean the problem stops being a problem."
    # Silence. The harpsichord ticks on.
    wanderer "(very low) He means to erase you."
    dottore "I mean to restore the original configuration."
    echo "I heard you the first time."
    dottore "Then you understand the offer."
    echo "I understand you want me to stop answering back."
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
            $ bump('m', -1)

    if _sel_10 == 'A':
        show dottore delighted at at_center
        with soft_dissolve
        dottore "(delighted) Oh, I knew you’d say that. Pity. I’d already printed the second page of the proposal."
    elif _sel_10 == 'B':
        dottore "The book belongs in a collection. Mine."
        mc "(inwardly) He says that like the book has already been packed."
    elif _sel_10 == 'C':
        wanderer "I don’t want to be whole if the price is him."
        echo "(a long beat) ...And I’d like to keep my seat at the table. Small as it is."
    elif _sel_10 == 'D':
        # The vial is warm against your palm. The Doctor’s smile deepens by one precise
        show dottore cold at at_center
        with soft_dissolve
        dottore "(softly) Good. Hold it. Hold it and think."

    if fixer:
        echo "You’ve tried to smooth a hurt away before. Did it become less real?"
        mc "No. I remember that now."

label act3_3_4:
    # SCENE 3.4 · The Locked Room
    $ show_title("SCENE 3.4\nThe Locked Room")
    play sound audio.sfx_glass  # Glass, rotating. A hiss. A door sealing.
    scene bg lab_glasscube
    with scene_fade
    with shake
    dottore "(over a speaker, cheerful) I said I wanted to talk. I never said you could leave whenever you liked."
    scene cg glass_cell
    with iris_open
    if _sel_9 == "A":
        cyno "(from the corridor, muffled) Quill! Answer me!"
        mc "I'm here!"
        cyno "Stay away from the slot. I'm looking for the release."
    elif _sel_9 == "B":
        wanderer "(muffled, close to the glass) I told you to stay behind me."
        mc "You said you wouldn't speak for me unless I asked."
        wanderer "I know. I'm asking you to stay back."
    elif _sel_9 == "C":
        echo "(from the other side of the glass, voice thin) You chose me. Don't make me regret trusting that."
        mc "I don't."
    else:
        n "Footsteps stop beyond the glass. The Wanderer and Echo must have followed after all; neither looks pleased to have been right about the trap."
        wanderer "(muffled) You came alone. You still brought the book."
        echo "And you thought we wouldn't notice you were gone?"
        mc "I didn't want you dragged into this."
        wanderer "Too late."
    dottore "The Folio, please. The remaining pages are the only thing I need. Slide it through the slot. After that, the Gnosis and the draught are yours."
    echo "(barely audible, behind the glass) Don’t give him the book."
    mc "He’ll hurt you if I don’t."
    echo "He’ll hurt all of us if you do."
    echo "I know what he does. I remember the part he leaves out when he tells the story."
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
            $ bump('m', -2)

    if _sel_11 == 'A':
        dottore "Then we wait. I’m very good at waiting. It is, I believe, the one trait the two of us share."
    elif _sel_11 == 'B':
        # Dottore examines the page against the light for four full seconds.
        dottore "(with something like admiration) ...Clever. Not enough. But clever."
    elif _sel_11 == 'C':
        # The word flares; hairline cracks race across the glass, then stop at the frame.
        play sound audio.sfx_glass
        scene bg lab_flicker
        with quake
        dottore "A lovely attempt. The glass is still stronger than one word. For now."
    elif _sel_11 == 'D':
        # The Folio slides through the slot. The Doctor takes it, but keeps it within sight.
        play sound audio.sfx_page
        dottore "Thank you. I’ll keep it safe until we’re finished."
        echo "He has the book. Don’t let him keep it."

label act3_3_5:
    # SCENE 3.5 · The Echo Breaks the Glass
    $ show_title("SCENE 3.5\nThe Echo Breaks the Glass")
    scene bg lab_flicker
    with scene_fade
    echo "I can’t do this alone."
    wanderer "(through the glass) I know."
    echo "Don’t just say it."
    wanderer "Take my hand. Or don’t. I’m not going to make you."
    n "The Echo stares at him through the glass. Then he puts his palm against it, fingers spread. The Wanderer matches him from the other side."
    scene cg two_palms
    with iris_open
    play sound audio.sfx_glass  # Glass shattering. A thunderclap, not from the sky. A roar of violet light, followed by silence.
    with quake
    # The glass cube falls in a cascade of bright dust.
    # And in the dust, for the first time, the two of them are standing side by side in the same room: the Wanderer’s body, and the Echo, visible and solid, to every eye in the laboratory. It lasts four seconds. It looks like both of them are about to fall over.
    dottore "(delighted, whispering) Oh. You can do that. You can do that."
    dottore "Thank you. Truly. That’s the data I needed."
    # He steps back through a door that wasn’t there a moment ago. It closes. A lock turns.
    cyno "(kicking at the door, snarling) He’s gone."
    tighnari "He had it planned. The whole thing was a test of whether they could do it."
    # The Echo pulls the Folio back through the broken slot before Dottore escapes.
    if _sel_11 == 'D':
        echo "The book!"
        # The Wanderer catches it as it skids across the floor.
        wanderer "Got it."
    # On the floor, in the glittering dust, lies a small velvet case. It is open. The Gnosis is gone.
    # Beside it lie a torn corner of the Folio and a single line of the Doctor’s handwriting.
    # The Wanderer picks up the empty case and carries it back to the annex.
    wanderer "He left us the case."
    echo "No. He left us the question."
    note "Day 30. The old dawn. I’ll collect the rest then. —D."

label act3_3_6:
    # DAY 25 · SCENE 3.6 · The Annex · Dawn
    $ set_page(5, 25)
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
    echo "We were trying to break the same wall."
    wanderer "I know."
    echo "You keep saying that."
    wanderer "Because I don’t know what else to say."
    echo "Then don’t say anything."
    # He pulls his knees up. He looks younger than he ever has.
    echo "I’m tired."
    wanderer "I know."
    echo "I said don’t."
    wanderer "Sorry."
    n "The Wanderer looks as surprised by the word as the Echo does. Neither of them knows what to do with it, so the Echo leans his head back against the table and closes his eyes."
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


label act3_3_6b:
    # DAY 26 · SCENE 3.6B · The Akademiya Rooftop · Dusk
    $ set_page(4, 26)
    $ show_title("DAY 26 · SCENE 3.6B\nThe Akademiya Rooftop · Dusk")
    scene bg rooftop_night
    with scene_fade
    play music audio.three_pages fadein 2.0

    n "By dusk, the broken glass has become a report, the report has become a rumor, and the rumor has become three different stories. In one, the Doctor was attacked. In another, the lab was empty. In the third, there was never a second figure in the room at all."

    tighnari "The official report says the containment field failed because of a power fluctuation."
    cyno "That is technically true."
    tighnari "It is also a lie."
    cyno "Those are not mutually exclusive."

    mc "Can you prove what happened?"
    tighnari "I can prove the glass was broken from the inside. I can prove the Doctor removed the case before the guards arrived. I cannot prove what the witnesses saw when the two of them stood together."
    cyno "I can prove that several witnesses have suddenly remembered appointments elsewhere."
    wanderer "He'll make sure no one can testify."
    echo "No. He'll make sure they can testify to anything except what happened."

    n "The Echo stands at the parapet, solid enough to cast a shadow. He keeps his hands tucked into his sleeves, as though he is afraid the evening might take them back."

    mc "Are you frightened of disappearing?"
    echo "I'm frightened I’ll disappear and you’ll tell yourself it was for the best."
    wanderer "I wouldn’t."
    echo "You don’t know that. You thought it before."
    wanderer "..." 
    echo "I don’t need a promise. I need you to tell me when you start thinking I’d be easier to live without."
    wanderer "I can do that."
    echo "Then do it before I have to ask."

    menu:
        "Ask them to make a rule for the last four days.":
            $ bump('m', 1)
            mc "No decisions about the other one without asking first. Not even decisions meant to help."
            wanderer "Agreed."
            echo "I reserve the right to complain about the wording."
            mc "Granted."
        "Tell the Echo he doesn't have to prove he is real.":
            $ bump('b', 1)
            mc "You don't have to become visible to deserve a place here."
            echo "I know that."
            n "He says it too quickly. After a moment, he looks down at his hands."
            echo "...I am trying to know it."
        "Tell the Wanderer that guilt cannot be his only way forward.":
            $ bump('w', 1)
            mc "You can take responsibility without making yourself a punishment."
            wanderer "I don't know how to do that yet."
            mc "Then learn before dawn."
            wanderer "Bossy."
            mc "You noticed."
            n "His smile is brief, but it arrives without being dragged out of him."

    n "Below, the city lights come on one by one. The Folio opens in the wind, but no page turns. Its remaining paper holds still, as if listening."
    echo "Four days."
    wanderer "Four days."
    mc "We don't have to know the ending tonight."
    echo "No. But we do have to be here when it comes."


label act3_3_7:
    # DAY 27 · SCENE 3.7 · The Rooftop of the Annex · Evening
    $ set_page(3, 27)
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
    if pen >= 3:
        n "As Nahida disappears down the stair, a thin orange line wakes along the Folio’s margin. The Echo sees it. His expression closes."
        echo "He’s already writing."
    # END OF ACT 3
    n "Act 4: The Fourth Page Two confessions and one dawn. The Rule of Three says a thing changes on the fourth."

    jump act4_4_1

