################################################################################
## Twice-Told Tale - Endings  (gated, plus the shared beat)
################################################################################
label ending_shared_beat:
    # SHARED BEAT · The Doctor Loses
    scene bg white_page_street
    with scene_fade
    show dottore cold at at_center
    with soft_dissolve
    play music audio.reprise_clean_instruments fadein 2.0  # “Reprise: Clean Instruments”: the sterile piano, cracking.
    dottore "(for the first time, not smiling) That isn’t possible. The seal was mine."
    nahida "(quietly) You wrote a book without the one thing a book needs, Doctor. A reader."
    # The Wanderer and Echo press their palms to the open page. The Folio answers with their joined mark; Dottore's ink peels away from the margin.
    scene cg two_palms
    with ink_dissolve
    pause
    play sound audio.sfx_page
    scene bg white_page_street
    with page_wipe
    show dottore cold at at_center
    with soft_dissolve
    dottore "The seal is coming apart."
    nahida "It was never yours to keep."
    dottore "(softly) Fascinating."
    # His false door folds shut. The gray masks scatter into the morning, leaving the street and the Folio in the characters' hands.

    return

label ending_wanderer:
    $ record_ending("wanderer")
    call ending_shared_beat from _call_ending_shared_beat
    # ENDING A · THE WANDERER ENDING · “Her Name”
    scene bg annex_day
    with scene_fade
    play music audio.a_name_is_a_small_thing fadein 2.0  # “A Name Is a Small Thing”: warm woodwinds, a light step.
    # You write the Wanderer’s name on the last line, in full. The ink holds.
    # The air goes quiet. Beside the Wanderer, the shimmer of the Echo thins to a breath, then to a light, then to a mark on the page, and the Echo steps back, not erased but settled. He smiles. It isn’t unkind.
    echo "(gently) Go on. He’s the one who gets to walk out the door. I’ll keep the book."
    wanderer "(quickly) I don’t want you in a book. I want you with me."
    echo "I’ll be there. I’m in the sleeve of your coat. In the way you hold your tea. In the thing you think at three in the morning that you won’t say out loud."
    echo "That’s more of a home than I ever had."
    scene cg ending_wanderer
    with scene_fade
    # Weeks later, the Wanderer sits alone at the annex table. He has made two cups of tea. He drinks one. He leaves the other, steaming, on the other side.
    wanderer "(to the empty chair) ...It’s not sugary."
    # The cup is empty when he looks back. Neither of them is surprised.
    # He puts on his hat. He steps into the sunlight. Behind him, the Folio closes of its own accord, and the cover reads:
    n "A Tale Told Once, and Well."
    # END · Wanderer Ending · Warm

    # The closing ritual: the name of the ending fades up, then the
    # ending plate, then the credits.
    call ending_title_card("wanderer") from _call_ending_title_card
    scene cg ending_wanderer with Dissolve(2.2)
    pause 4.5
    call ending_epilogue() from _call_ending_epilogue

    return

label ending_scaramouche:
    $ record_ending("scaramouche")
    call ending_shared_beat from _call_ending_shared_beat_1
    # ENDING B · THE SCARAMOUCHE ENDING · “The Lamp-Keeper”
    scene bg annex_day
    with scene_fade
    play music audio.what_he_built_from_nothing fadein 2.0  # “What He Built From Nothing”: a solo cello, gradually joined by a guitar.
    # You write the Echo’s name. His real one. The one he gave you in the dark, in the first week, and told you to forget.
    # The Wanderer’s shoulders drop. For a heartbeat he looks frightened, as someone does before a door they chose to walk through. Then he exhales.
    wanderer "(smiling, small) You were always the louder one."
    echo "(startled) I was?"
    wanderer "I just let you carry the volume. I’m tired. I’d like to rest. It’s... all right to rest, now."
    scene cg ending_scaramouche
    with scene_fade
    # The Wanderer passes the hat to him. It is the only goodbye he knows how to give.
    echo "(thickly) I won’t wear this."
    wanderer "You will. You’ll hate how it fits."
    play sound audio.sfx_door
    # Time passes. The Echo, now whole, keeps the archive. He lights the lamps. He labels the shelves in an angry, beautiful hand. He is not kind to scholars. He is very kind to the ones who forget their umbrellas.
    # On the first day of each month, the Folio opens on the table, and a new line appears in the margin, in a hand like his own, but softer.
    margin "Tea’s getting cold. Come to bed."
    # He smiles at it, as if he’d written it himself. Maybe he did.
    # END · Scaramouche Ending · Bittersweet

    # The closing ritual: the name of the ending fades up, then the
    # ending plate, then the credits.
    call ending_title_card("scaramouche") from _call_ending_title_card_1
    scene cg ending_scaramouche with Dissolve(2.2)
    pause 4.5
    call ending_epilogue() from _call_ending_epilogue_1

    return

label ending_true:
    $ record_ending("true")
    call ending_shared_beat from _call_ending_shared_beat_2
    # ENDING C · THE TRUE ENDING · “The Passenger”
    scene bg white_page
    with scene_fade
    play music audio.the_last_evening fadein 3.0
    # You set the pen down on the page.
    mc "I’m not going to write it."
    mc "It isn’t mine. It was never mine. I’m the one who mended the spine, that’s all. The story’s theirs."
    nahida "(very quietly) You understand what that means? If you leave the last page empty, the two of them will have to write it between themselves."
    mc "Yes."
    wanderer "(startled) She means... us?"
    echo "(grimly) She means we’re going to have to talk."
    wanderer "We’ve been talking for thirty days."
    echo "We’ve been shouting for thirty days. That’s a different thing."
    # A pause. Then both of them, at the same time, begin to laugh, helplessly, the way two people do at the end of a very long funeral.
    scene cg wanderer_echo_on_page
    with scene_fade
    # They pick it up together. Two hands on one pen. They write.
    play sound audio.sfx_pen  # A pen, scratching. Slow. Sure.
    wanderer "(reading, aloud) There was once a boy who was split in two."
    echo "(reading) And for five hundred years, neither half could forgive the other."
    wanderer "And then, one rainy week, a stranger mended a book."
    echo "And in the ink, they found they were the same."
    # The page fills itself. The words rise from white into gold. When it is done, the Folio snaps shut with a sound like a door closing in a house that is, at last, warm.
    scene bg annex_day
    with scene_fade
    play music audio.warm_table_reprise fadein 2.0  # “Warm Table (Reprise)”: the cello from the dining scene, now with the full ensemble.
    # The Wanderer and the Echo sit on either side of you. They have, somehow, begun to share the body: the Echo steps out for an hour each evening, for tea, and steps back in for the night. The arrangement is not elegant. It is theirs.
    echo "You made a promise. You said you’d be at the door when the last page burned."
    mc "And I was."
    echo "(looking down at his cup) ...You were."
    echo "I’m going to say something and I’m going to say it exactly once. If you tell anyone I said it, I’ll deny it in front of the Seven."
    wanderer "(lazily) He’s blushing."
    echo "I’m not."
    # He puts down his cup. He doesn’t look at you. His voice is very small and very clear.
    echo "Thank you for mending me."
    scene cg ending_true
    with scene_fade
    # A last line of text fades in across the picture.
    n "The story is never finished. It is only handed on."
    # END · True Ending · Golden

    # The closing ritual: the name of the ending fades up, then the
    # ending plate, then the credits.
    call ending_title_card("true") from _call_ending_title_card_2
    scene cg ending_true with Dissolve(2.2)
    pause 4.5
    call ending_epilogue() from _call_ending_epilogue_2

    return

label ending_gnosis_box:
    $ record_ending("gnosis_box")
    # ENDING F · THE GNOSIS BOX
    # Gate: BOX = TRUE. Tone: psychological horror; no new explanation of the Gnosis is asserted.
    scene bg annex_dawn
    with scene_fade
    play music audio.the_thing_unsaid fadein 2.0  # “The Thing Unsaid”: one low note with a faint, irregular overtone.
    wanderer "You’ve been looking at it for ten minutes."
    mc "I’m trying to remember what I saw."
    echo "You opened it alone. That was the point, wasn’t it? No witness. No one to tell you what it meant."
    mc "I saw the Gnosis. I think. The light was there, and then it was behind my eyes. I can’t tell which happened first."
    wanderer "Did it show you something?"
    mc "I don’t know. Every time I try to describe it, I remember a different room."
    # The Wanderer reaches for the case. The Echo catches his wrist. For once, neither makes a joke.
    echo "Don’t."
    wanderer "I wasn’t going to open it."
    echo "You were going to see whether you could. That’s how it starts."
    mc "What starts?"
    echo "The part where you convince yourself that knowing a thing and surviving it are the same achievement."
    # A thin violet line appears between the lid and the case. It does not brighten. It does not fade.
    wanderer "We could take it to Nahida."
    mc "And tell her what?"
    wanderer "The truth."
    mc "Which version?"
    # Silence. The case gives a small, dry click from the inside. Nobody touches it.
    echo "Put it away, Quill. Not because it’s harmless. Because you don’t know what question you asked it."
    # You close the cabinet around the case. The violet line remains visible through the keyhole.
    n "END CARD: THE GNOSIS BOX"
    n "END CARD: You wanted to know what was inside. You never asked what opening it would make of you."
    # END · The Gnosis Box

    # The closing ritual: the name of the ending fades up, then the
    # ending plate, then the credits.
    call ending_title_card("gnosis_box") from _call_ending_title_card_3
    scene cg gnosis_violet with Dissolve(2.2)
    pause 4.5
    call ending_credits() from _call_ending_credits

    return

label ending_burned_pages:
    $ record_ending("burned_pages")
    # ENDING G · BURNED PAGES
    # Gate: PROMISE_MADE = TRUE and PEN ≥ 3. Entering this ending marks the promise broken.
    scene bg white_page
    with scene_fade
    play music audio.a_smaller_promise fadein 2.0  # “A Smaller Promise”: the flute line returns, interrupted by the sound of paper catching fire.
    # You turn toward the Margin Door. It is the way out. The way back to the archive. The way you promised you would come.
    wanderer "Quill? What are you doing?"
    mc "I can still get us out. If I reach the door, I can fix this."
    echo "You can’t fix every ending by getting there first."
    mc "I promised you."
    echo "You promised you’d be at the door. You are. Look at it. You’re standing in front of it and still looking for somewhere else to run."
    # The Margin Door opens. Beyond it is the Archive Annex, warm lamplight and the familiar low table. The distance is only a few steps.
    wanderer "Then come back. We’ll do it together."
    # The Pen grows hot in your hand. A burning line travels from the nib across the page, toward the two figures. The door is open. The choice is not whether you can reach it. It is whether you will leave them to finish the page without you.
    mc "I’m sorry."
    # You step through the Margin Door. It shuts like a book. On the other side, the room is empty. The tea is cold. The Folio is open to a page with no words on it.
    # CUT TO: The archive door at dawn. The Wanderer and the Echo stand where you left them. The last page burns between them, but neither lets go.
    wanderer "She promised."
    echo "I know."
    wanderer "You waited for her."
    echo "I know."
    # The Echo looks toward the empty street. His expression is not anger. It is worse: recognition.
    echo "I believed her."
    # The page folds inward. The two names remain legible for one last second, side by side. Then the ink goes gray.
    # Later, MC reaches for the Pen to rewrite the page. The nib will not touch the paper. The Wanderer, appearing in the doorway, gently closes the Folio.
    wanderer "Don’t. You don’t get to make it hurt less by pretending it didn’t happen."
    # He leaves the book with you. No one writes on the page again.
    n "END CARD: BURNED PAGES"
    n "END CARD: Some promises are broken by the people who make them. Others are broken by the moment we choose to leave. The page is gone. The promise is not."
    # END · Burned Pages

    # The closing ritual: the name of the ending fades up, then the
    # ending plate, then the credits.
    call ending_title_card("burned_pages") from _call_ending_title_card_4
    scene cg first_page_burn with Dissolve(2.2)
    pause 4.5
    call ending_credits() from _call_ending_credits_1

    return

label ending_blank_page:
    $ record_ending("blank_page")
    # ENDING H · BLANK PAGE
    # Gate: PEN ≥ 3. Tone: existential horror; the ending refuses to confirm death, erasure, or salvation.
    scene bg white_page
    with scene_fade
    show dottore cold at at_center
    with soft_dissolve
    stop music fadeout 2.0
    dottore "How interesting. You have learned to fear the Pen. Tell me, Archivist: if the corrector is wrong, who corrects the corrector?"
    # You look down. The nib is black. Your fingers are clean.
    wanderer "Don’t answer him."
    echo "For once, I agree. He asks questions as if the answer belongs to him."
    dottore "And does it belong to you?"
    # The two figures stand on either side of you. Their outlines tremble, not like ink running, but like a drawing waiting for its artist to decide whether it should remain.
    mc "I wanted to help."
    wanderer "I know."
    mc "I thought if I found the right words—"
    wanderer "Wanting to help isn’t the same as knowing what someone needs."
    # The Echo looks at the last line. There is room for his name. Room for the Wanderer’s. Room for both. The page waits, patient and terrible.
    echo "I won’t ask you to save me by deciding what I’m allowed to become."
    mc "Then what do you want me to write?"
    echo "If you write my name, let it be because I gave it to you. Not because you’re afraid of what happens if you don’t."
    wanderer "And if you write nothing, don’t call it mercy on our behalf. Let it be your choice—and let us be more than the thing you leave blank."
    # The Pen lowers. Its tip hovers above the paper. A drop of ink gathers, perfectly round.
    # It falls. For a moment, the dot is the only mark in the world.
    # The dot vanishes. Nothing is written.
    # The page remains. The figures are not visible; the page may simply be too white to show them. There is no sound of a door closing. There is no sound of a book closing.
    n "END CARD: BLANK PAGE"
    n "END CARD: The story does not tell you what happened. For once, it does not pretend that silence is an answer."
    # END · Blank Page
    n "Neutral and Bad Endings, and the Epilogue"

    # The closing ritual: the name of the ending fades up, then the
    # ending plate, then the credits.
    call ending_title_card("blank_page") from _call_ending_title_card_5
    scene cg blank_dot with Dissolve(2.2)
    pause 4.5
    call ending_credits() from _call_ending_credits_2

    return

label ending_neutral:
    $ record_ending("neutral")
    call ending_shared_beat from _call_ending_shared_beat_3
    # NEUTRAL ENDING · “Margins”
    scene bg white_page_street
    with scene_fade
    play music audio.the_boy fadein 2.0
    # The Echo steps forward and takes the pen from your hand, gently. It’s the first time he has ever touched something of yours without being asked.
    echo "You weren’t ready. That isn’t a failing. Most people never are."
    echo "I’ll finish it. Badly, probably. But in my own hand."
    play sound audio.sfx_pen
    echo "There was once a boy who couldn’t decide whether he wanted to be remembered."
    wanderer "That’s a terrible beginning."
    echo "It’s an honest one. You can improve it tomorrow."
    # Weeks later, their arguments still fill the annex. This time, neither mistakes an argument for a goodbye.
    scene bg annex_day
    with scene_fade
    play music audio.warm_table fadein 2.0
    wanderer "Tea?"
    echo "You know I don’t like it sweet."
    wanderer "I know. I asked anyway."
    echo "...Then leave the cup there. I’ll decide when I’m ready."
    n "They do not forgive each other today. They do not leave, either. The page stays open."
    # END · Neutral Ending · Open

    # The closing ritual: the name of the ending fades up, then the
    # ending plate, then the credits.
    call ending_title_card("neutral") from _call_ending_title_card_6
    scene cg folio_page with Dissolve(2.2)
    pause 4.5
    call ending_epilogue() from _call_ending_epilogue_3

    return

label ending_archivist:
    $ record_ending("archivist")
    # BAD ENDING 1 · “The Archivist’s Fee”
    scene bg white_page_dark
    with scene_fade
    show dottore pleasant at at_center
    with soft_dissolve
    play music audio.clean_instruments fadein 2.0  # “Clean Instruments”: the metronome, relentless.
    # The Doctor takes the pen without a word. He doesn’t gloat. That is the worst thing about it.
    dottore "Thank you. I’ll be fair. A very small fee. One page."
    # He writes. The Echo’s name goes first, then the Wanderer’s. Then, last, yours.
    wanderer "(a whisper, as the ink crawls) Quill... what did you do?"
    echo "(almost kind) You’re not stupid. You were frightened. That’s different."
    scene cg folio_black
    with scene_fade
    # The street is empty. The lamp outside the archive is out.
    # END · Bad Ending 1 · The Archivist’s Fee

    # The closing ritual: the name of the ending fades up, then the
    # ending plate, then the credits.
    call ending_title_card("archivist") from _call_ending_title_card_7
    scene cg folio_black with Dissolve(2.2)
    pause 4.5
    call ending_credits() from _call_ending_credits_3

    return

label ending_burn_it_down:
    $ record_ending("burn_it_down")
    # BAD ENDING 2 · “Burn It Down”
    scene bg white_page_burn
    with scene_fade
    play music audio.tatarasuna fadein 1.0
    with quake
    # You pull the Folio apart. The paper screams.
    wanderer "(from inside the fire) What have you done?"
    echo "(laughing, high and cracked) You broke it. You broke the only place we were both real."
    # The Echo steps back into the flame. The Wanderer reaches for him. The page between their hands goes gray, and then goes out.
    scene cg margin_door_shut
    with scene_fade
    # END · Bad Ending 2 · Burn It Down

    # The closing ritual: the name of the ending fades up, then the
    # ending plate, then the credits.
    call ending_title_card("burn_it_down") from _call_ending_title_card_8
    scene cg margin_door_shut with Dissolve(2.2)
    pause 4.5
    call ending_credits() from _call_ending_credits_4

    return

label ending_quiet_page:
    $ record_ending("quiet_page")
    # BAD ENDING 3 · “The Quiet Page”
    scene bg annex_dawn
    with scene_fade
    play music audio.a_smaller_promise fadein 4.0
    if promise_broken:
        mc "I said I’d be here. I’m sorry."
        echo "You came to the door. You still chose to leave."
    else:
        mc "I don’t know what to write."
        echo "Then don’t write. Just stay with us."
    # The Echo waits at the door. The street fills with light. You are not there.
    # The Wanderer is the one who finally comes to find you, hat in his hand and eyes red.
    wanderer "He said you’d come. He kept saying it. Right up to the end."
    wanderer "He wasn’t angry. That’s what I can’t forgive."
    scene cg blank_dot
    with scene_fade
    # END · Bad Ending 3 · The Quiet Page

    # The closing ritual: the name of the ending fades up, then the
    # ending plate, then the credits.
    call ending_title_card("quiet_page") from _call_ending_title_card_9
    scene cg empty_bed with Dissolve(2.2)
    pause 4.5
    call ending_credits() from _call_ending_credits_5

    return

label ending_epilogue:
    # EPILOGUE · “The Back of the Book”
    scene bg page_black_stage
    with scene_fade
    play music audio.marginalia fadein 3.0
    # The Folio, open on a shelf in a library you’ve never seen. A hand, which might be anyone’s, turns the page. There is one more line below the last one, in a hand that isn’t the Wanderer’s or the Echo’s or yours.
    newline_char "And if you find this book, mend it gently. It’s been through a lot."
    # The hand closes the cover. The title fades in:
    n "TWICE-TOLD TALE"
    # CREDITS ROLL.
    call ending_credits() from _call_ending_credits_6

    return
