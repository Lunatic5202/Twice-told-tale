################################################################################
## Twice-Told Tale - Act 2: The Warm Table  (scenes 2.1-2.17)
################################################################################
label act2_2_1:
    # DAY 9 · SCENE 2.1 · The Margin Door
    scene bg corridor_mist
    with act_wipe
    $ set_page(21, 9)
    $ show_act("II", "The Warm Table")
    $ show_title("DAY 9 · SCENE 2.1\nThe Margin Door")
    play music audio.page_walk fadein 2.0  # “Page-Walk”: a harp, glass chimes, very far away.
    nahida "(voice only, from the other side) You can see, but not touch. Nothing you do will change what happened. But what you feel leaves a mark on the page."
    nahida "When the ink cracks, someone has been hurt. Be careful what you stand in."
    # Ahead, a wooden veranda emerges from the mist. A hidden mansion, half swallowed by moss and ferns. A single lantern burns inside.
    scene bg shakkei_pavilion
    with slide_left
    echo "I know this place."
    mc "You do?"
    echo "I know the ceiling. I counted the cracks in it. There are three hundred and eleven."
    # The Wanderer stops at the last step of the veranda. He does not cross the threshold. His hand rests on the doorframe, white-knuckled.
    wanderer "I’ll wait here."
    echo "Of course you will."
    # He walks in. MC follows.

label act2_2_2:
    # SCENE 2.2 · The Sleeping Room
    $ show_title("SCENE 2.2\nThe Sleeping Room")
    scene bg tatami_room
    with slide_left
    scene cg sleeping_puppet
    with iris_open
    play music audio.slumber fadein 2.0  # “Slumber”: solo shamisen, then silence.
    echo "(very quiet) Hm. They made me smaller than I remember."
    # Footsteps. The screens slide open. Two women enter. One in purple and silver, her expression a grief held very still. The other in white and red, ears forward, a small curve to her mouth.
    scene cg raiden_yae
    with scene_fade
    pause
    miko "Here it is. The prototype."
    scene bg tatami_room
    with soft_dissolve
    show ei sad at at_left
    show yae amused at at_right
    with soft_dissolve
    ei "He is weeping."
    miko "Puppets don’t weep."
    ei "This one does. In his sleep."
    miko "Then it’s a flaw. A flaw is retired. I said so at the start. You won’t like it, but the cleanest thing is to return the wood to the tree."
    # Ei kneels. Her hand hovers over the puppet’s face and does not touch it.
    ei "He is too gentle to hold a Gnosis. I can see that."
    show ei serious at at_left
    ei "But I will not end him."
    miko "Then what?"
    ei "Free him."
    miko "(a careful pause) Free him. In a pavilion no one visits."
    ei "I will seal his power so it cannot harm him. He may wake when he wishes, and live as he likes."
    miko "And if he never wakes?"
    show ei soft at at_left
    ei "(a long breath) Then he will have rest."
    # She takes a small gold feather from her sleeve and presses it into the sleeper’s hand. His fingers curl around it without waking.
    ei "So that he may know whose he was, if he ever needs to."
    show yae smug at at_right
    miko "Or so that he knows who left him."
    ei "...Yes. That, too."
    hide ei
    hide yae
    with soft_dissolve
    play sound audio.sfx_page
    # The ink on the floor splits: a hairline crack running toward the Echo’s feet.
    echo "Pity."
    echo "She stood over me and decided I was too soft, and she called it kindness."
    echo "Pity is the cruelest knife a god owns. It leaves no wound anyone can point to."

    # CHOICE: The crack is spreading. He is looking at you.
    menu:
        "“It looks like love. A clumsy one.”":
            $ _sel_1 = "A"
            $ bump('m', 1)
        "“It looks like she didn’t know how to hold you.”":
            $ _sel_1 = "B"
            $ bump('b', 1)
        "“What do you think it was?”":
            $ _sel_1 = "C"
            $ bump('m', 1)
            $ bump('b', 1)

    if _sel_1 == 'A':
        echo "(sharply) Clumsy. A clumsy love left me in a closet."
        mc "(softly) I know. I said clumsy. I didn’t say good."
    elif _sel_1 == 'B':
        echo "(a short breath, almost a laugh) Hold. Yes. She never learned how."
    elif _sel_1 == 'C':
        echo "(a silence that goes on too long) ...I think it was both. I think that is what I cannot forgive."

label act2_2_3:
    # DAY 10 · SCENE 2.3 · The Threshold
    $ set_page(20, 10)
    $ show_title("DAY 10 · SCENE 2.3\nThe Threshold")
    scene bg veranda
    with scene_fade
    play music audio.what_he_kept fadein 2.0  # “What He Kept”: low strings.
    wanderer "You didn’t need to see that."
    mc "Neither did you."
    wanderer "I’ve seen it before. Once. In a capsule behind a door Nahida kept. I made myself watch."
    wanderer "I thought for a very long time she had thrown me away. And then I saw her hand hover, and not touch."
    wanderer "It doesn’t fix anything. It just means it was never simple."
    # He finally steps inside, one pace, and then stops.
    wanderer "That’s all I can manage today. Tell him that."

label act2_2_4:
    # DAY 11 · SCENE 2.4 · The Archive Annex · Night
    $ set_page(19, 11)
    $ show_title("DAY 11 · SCENE 2.4\nThe Archive Annex · Night")
    scene bg annex_night
    with scene_fade
    play music audio.three_hundred_and_eleven fadein 2.0  # “Three Hundred and Eleven”: a music box, played badly on purpose.
    echo "I woke up."
    echo "Nobody did it for me. I woke up by myself, in the dark, and there was no one. So I counted the ceiling. I counted it again. Three hundred and eleven."
    echo "I don’t need you to say anything."

    # CHOICE: You are sitting nearby. He has not looked at you.
    menu:
        "Sit down beside him and say nothing.":
            $ _sel_2 = "A"
            $ bump('m', 1)
        "Pour him a cup of tea, no sugar.":
            $ _sel_2 = "B"
            $ bump('w', 1)
        "“You woke up on your own. That counts.”":
            $ _sel_2 = "C"
            $ bump('b', 1)

    if _sel_2 == 'A':
        echo "Don’t pity me."
        mc "I don’t. I’m sitting."
    elif _sel_2 == 'B':
        echo "(takes it) Bitter."
        mc "I thought you might want it honest tonight."
    elif _sel_2 == 'C':
        echo "(a very small laugh) It counts. It does. I’d like it to count more."

    # END OF PAGE-WALK ONE

    # A quiet return to the present before the next memory.
    scene bg annex_night
    with scene_fade
    $ show_title("INTERLUDE · What the Memory Leaves Behind")
    play music audio.the_table fadein 1.5

    n "When the page releases you, the room seems too ordinary to be trusted. A lamp. A table. Rain tapping the high windows. The Echo has both hands around his cup, though the tea has gone cold."

    mc "You remembered the ceiling before you remembered anything else."
    echo "It was there. It didn't ask questions."
    wanderer "I could have come back."
    echo "You could have done a great many things."
    wanderer "I know."
    echo "Stop saying that as if knowing is the same as having carried it."

    n "The Wanderer looks toward the window. He does not leave. It is not an apology, but it is the first time he stays in a room after being told exactly how he failed."

    menu:
        "Ask what the memory got wrong.":
            $ bump("m", 1)
            mc "A memory can be true and still leave things out. What did it leave out?"
            echo "The part where I waited for footsteps. Every night, I thought I heard them."
            wanderer "I did come back once."
            echo "..."
            wanderer "I stood outside the door. I heard you counting. I thought if I opened it, I'd have to become someone who knew what to say."
            echo "So you left."
            wanderer "Yes."
            n "The confession does not repair anything. It gives the hurt an actual shape."
        "Ask the Wanderer to stay until the tea is cold.":
            $ bump("w", 1)
            mc "No more explanations tonight. Stay until the tea is cold."
            wanderer "It already is."
            echo "Then you have a head start."
            n "The Wanderer sits. The Echo does not thank him. He does, however, stop watching the door."
        "Ask the Echo whether he wants the next memory now.":
            $ bump("b", 1)
            mc "We can stop before the next door."
            echo "I know."
            mc "That wasn't an answer."
            echo "No. I want to see it. I just don't want him to call my wanting it permission to leave me alone in it."
            wanderer "I won't."
            echo "You don't get to promise that on my behalf."
            wanderer "Then I promise I'll ask."

    n "The Folio lies open between you. Its next page smells faintly of iron and salt. Nobody reaches for it until the rain changes direction."

    n "Act 2, Page-Walk Two: Tatarasuna — betrayal, and the people who tried to make a home anyway."
    $ set_page(18, 12)
    n "DAY 12 · INTERLUDE · The Akademiya Corridor (18 pages left)"
    scene bg green_corridor
    with slide_left
    play music audio.rumors fadein 2.0  # “Rumors”: a clarinet, thin and wary.
    # Two students whisper at a window.
    student "...a Fatui doctor. Asking about old Irminsul records. Nobody’s seen his face."
    # The Wanderer, walking a few steps ahead, goes completely still. His cup does not spill. He puts it down very, very carefully on the windowsill.
    wanderer "(to no one) Of course he is."

label act2_2_5:
    # DAY 13 · SCENE 2.5 · The Margin Door, Second Page
    $ set_page(17, 13)
    $ show_title("DAY 13 · SCENE 2.5\nThe Margin Door, Second Page")
    scene bg cinders_path
    with door_blinds
    play music audio.tatarasuna fadein 2.0  # “Tatarasuna”: low taiko pulse, a hammer keeping time.
    nahida "(voice only) This is the second room."
    # The Wanderer, behind them, takes one step across the doorway. Then a second. Then stops.
    wanderer "I’ll go as far as I can."
    echo "(without turning) That’s one more than last time."
    scene bg mikage_furnace
    with scene_fade

label act2_2_6:
    # SCENE 2.6 · The Forge
    $ show_title("SCENE 2.6\nThe Forge")
    # A man with a tied-back topknot and a worn yoriki’s coat leads a barefoot puppet into the yard. A red feather is stitched into his collar.
    katsuragi "Found him wandering by the shore. No name, no people. Poor thing doesn’t even know where he’s from."
    # He is lying. He leans in and speaks under his breath.
    katsuragi "(low) Keep that gold feather out of sight. Don’t tell anyone where you really came from. Understand?"
    # The puppet nods. He does not understand. He holds the feather close to his chest.
    # [CG: The gold feather turning in the Echo's fingers.]
    show cg gold_feather with soft_dissolve
    pause
    hide cg with soft_dissolve

    worker "A wandering eccentric, is he? A kabukimono."
    worker2 "Look at the hat. Look at the feet."
    # A broad-shouldered smith with a scarred forearm shoves a hammer into the puppet’s hands.
    niwa "Hold it like a bird, kid. Not too tight, not too loose. Birds don’t like being strangled."
    echo "(watching, very quiet) Niwa."
    mc "You knew him."
    echo "He was the loudest man in the yard. He was never quiet. He taught me how to hold a hammer. He yelled at me when I held it wrong. He yelled when I held it right, because he was proud of me."
    play sound audio.sfx_hammer
    with shake

label act2_2_7:
    # SCENE 2.7 · The Night of the Blade
    $ show_title("SCENE 2.7\nThe Night of the Blade")
    scene bg furnace_yard_night
    with scene_fade
    play music audio.sword_dance fadein 2.0  # “Sword Dance”: shamisen and drum, joyous and a little reckless.
    scene cg sword_dance
    with scene_fade
    niwa "(shouting over the music) Kabukimono! Show them how a wanderer dances!"
    # Beside MC, the Echo’s foot is tapping the beat. He has not noticed.

    # CHOICE: His foot is keeping time.
    menu:
        "“You can dance with the memory. Nobody’s watching.”":
            $ _sel_3 = "A"
            $ bump('b', 1)
        "“You look happy in there.”":
            $ _sel_3 = "B"
            $ bump('m', 1)
        "Say nothing. Tap your own foot along with his.":
            $ _sel_3 = "C"
            $ bump('w', 1)

    if _sel_3 == 'A':
        echo "(stops, then, deliberately, starts again) I was bad at it. He told me I was good."
        mc "Both of those can be true."
    elif _sel_3 == 'B':
        echo "I was. (He laughs, then doesn’t.) That’s the problem with it."
    elif _sel_3 == 'C':
        # He notices. He looks at her foot. He looks away. His own does not stop.
        pass

label act2_2_8:
    # SCENE 2.8 · A Visitor with a Kind Face
    $ show_title("SCENE 2.8\nA Visitor with a Kind Face")
    scene bg furnace_morning
    with scene_fade
    play music audio.escher fadein 2.0  # “Escher”: a clean, polite piano motif with something wrong underneath.
    escher "A little crystal marrow in the charge. You’ll find the steel runs hotter, cleaner, faster. Think how many more blades you could make."
    niwa "(arms crossed) It’s a lot of promises for one lump of rock."
    escher "Skepticism is healthy. Try it first. I’ll stay as long as you like."
    # The Wanderer, two paces inside the door, goes gray.
    wanderer "That’s him."
    echo "Who?"
    wanderer "Look at his hands. Watch how he takes notes."
    # Escher smiles at a worker. The smile is the exact shape of a man examining a specimen.
    play sound audio.sfx_roar
    with jolt

label act2_2_9:
    # DAY 14 · SCENE 2.9 · The Plague of Tatarasuna
    $ set_page(16, 14)
    $ show_title("DAY 14 · SCENE 2.9\nThe Plague of Tatarasuna")
    scene bg sickward
    with scene_fade
    play music audio.smoke fadein 2.0  # “Smoke”: a single bowed string, distorted.
    n "The crystal marrow is the remains of a serpent. It was never going to burn clean."
    # The puppet runs along the cots, bare feet gone black with soot. He is carrying a bundle of wet cloth.
    echo "I went to the shrine. They told me to."
    scene bg shrine_night
    with scene_fade
    show yae neutral at at_center
    with soft_dissolve
    miko "The Shogun is not receiving anyone. She has sealed herself away."
    puppet "(very small) They are dying. Please."
    miko "(a long pause) I’ll send help. Immediately."
    puppet "You are lying."
    show yae smug at at_center
    miko "I never lie about help. I only lie about how long it takes."
    hide yae
    with soft_dissolve
    # The Echo, watching, makes a tiny sound that is nearly a laugh.
    echo "She said “immediately.” I believed her for one whole night."

label act2_2_10:
    # SCENE 2.10 · The Page as He Remembers It
    $ show_title("SCENE 2.10\nThe Page as He Remembers It")
    scene bg furnace_yard_warped
    with soft_wipe
    play music audio.what_i_remember fadein 2.0  # “What I Remember”: the Escher motif, played slowly and wrongly.
    escher "(smooth, sad) I’m very sorry. Niwa has fled. He took his family in the night and left you all to this."
    # A wooden box is pressed into the puppet’s hands.
    escher "The furnace needs purging. Take this to the heart of it. You’re the only one who can survive it."
    scene cg puppet_furnace
    with iris_open
    play sound audio.sfx_roar
    with quake
    # He comes out. He is alive. The box is open. Inside lies a small, withered, human heart.
    escher "(softly) From a man Niwa killed. For you. He knew what you wanted."
    # The puppet drops the box. He throws the heart as far as he can. Then he runs.
    echo "(flat) That’s the second one. That is what Niwa did to me."
    echo "I have thought about it for five hundred years. He left. He left me a heart in a box and he left."

label act2_2_11:
    # SCENE 2.11 · The Truth Page
    $ show_title("SCENE 2.11\nThe Truth Page")
    # The red fades. The ink on the page turns white, then silver. The warping stops. Everything is suddenly, painfully clear.
    play music audio.what_was_written fadein 2.0  # “What Was Written”: solo cello, bare.
    scene bg furnace_room
    with scene_fade
    niwa "(to himself) If I go into the heart of it, I can hold it steady. Long enough. Just long enough."
    # He sets his hand against the device. A second shadow falls across the floor. Escher, in the doorway, glasses catching the light.
    escher "That is a very generous plan, Niwa. Unfortunately I need your heart more than your courage."
    # The light goes out of the room. The camera pulls back before anything is shown.
    play sound audio.sfx_roar
    with quake
    # Later. Niwa’s workbench, the hammer still on it. A scrap of paper under the hammer.
    scene cg niwa_note
    with iris_open
    echo "..."
    # He doesn’t move. He doesn’t speak. The ink at his feet begins to crack.
    echo "He did not leave."
    echo "He did not leave."
    echo "I spent five centuries hating a man who was going to give his life and I... I hated him. I hated his family. I broke his bloodline’s school with my own hands."
    # He turns on the Folio. His hand shoots toward the open page, not to touch it. To tear it out.
    echo "Take it back. Strike it. Strike the whole name. If it’s me, if it’s all me, then take me out of it—"
    # The ink around him splits with a sound like a bell cracking.

    # CHOICE: He is reaching for the page. Move.
    menu:
        "Catch his wrist with both hands. No Pen.":
            $ _sel_4 = "A"
            $ bump('m', 1)
            $ bump('b', 1)
        "Use the Pen to hold the page still.":
            $ _sel_4 = "B"
            $ bump('pen', 1)
            $ bump('m', -1)
        "Step back and let the Wanderer speak.":
            $ _sel_4 = "C"
            $ bump('w', 1)
            $ bump('m', 1)

    if _sel_4 == 'A':
        echo "(shaking) Let go."
        mc "No."
        echo "Quill—"
        mc "I said no."
    elif _sel_4 == 'B':
        # The page locks. The Echo freezes with his hand a finger-width from it. A page in the
        echo "(slowly) You held me still."
        echo "You held me still."
    elif _sel_4 == 'C':
        # She steps back. The Wanderer crosses the threshold completely, for the first time,
        # In all three cases, the Wanderer arrives in the next beat.
        wanderer "I did that."
        wanderer "I reached for the page and I tore myself out of it. I thought I’d fix it. The world just wrote itself again, the same, without me. Every person I’d hurt was still hurt. Niwa was still dead."
        wanderer "The only thing that changed was that I had to come back and live with it. Alone. With no one who knew my name."
        echo "(hoarse) Then what was any of it for?"
        wanderer "I don’t know. I’m still looking for that. But I can tell you the answer isn’t going away."
        # The Echo’s knees go. The Wanderer goes down with him, one hand still around his arm. The ink beneath them steadies.
        play music audio.warm_table fadein 3.0

label act2_2_12:
    # DAY 17 · SCENE 2.12 · The Archive Annex · Dawn
    $ set_page(13, 17)
    $ show_title("DAY 17 · SCENE 2.12\nThe Archive Annex · Dawn")
    scene bg annex_dawn
    with scene_fade
    play music audio.quiet fadein 2.0  # “Quiet”: almost silence, a faint wind.
    echo "There’s a third door."
    wanderer "There is."
    echo "I don’t want to open it."
    wanderer "I know."

    # CHOICE: He has asked a question without asking it.
    menu:
        "“We can wait. A page can wait.”":
            $ _sel_5 = "A"
            $ bump('w', 1)
        "“We go together. Same day. All three of us.”":
            $ _sel_5 = "B"
            $ bump('m', 1)
        "“Your decision. We’ll follow.”":
            $ _sel_5 = "C"
            $ bump('b', 1)

    if _sel_5 == 'A':
        echo "One day. Only one."
        wanderer "Fine."
    elif _sel_5 == 'B':
        echo "(a long exhale) Together. Fine. Together."
    elif _sel_5 == 'C':
        echo "(startled) ...You’d follow me."
        mc "Into a furnace, apparently."
        # END OF PAGE-WALK TWO
        n "Act 2, Page-Walk Three: The Boy and the Promise Betrayal by mortality. All three walk in together."

label act2_2_13:
    # DAY 18 · SCENE 2.13 · The Margin Door, Third Page
    $ set_page(12, 18)
    $ show_title("DAY 18 · SCENE 2.13\nThe Margin Door, Third Page")
    scene bg corridor_mist_snow
    with door_blinds
    play music audio.the_boy fadein 2.0  # “The Boy”: a lullaby on a thin flute, almost too slow to follow.
    nahida "(voice only) The third room is the smallest. I’m sorry for that."
    # This time the Wanderer does not stop at the door. He walks through and falls into step beside the Echo, not touching him, close enough to.
    echo "(without looking) You’re not hovering."
    wanderer "I’m walking."
    echo "Same thing, in your case."
    wanderer "...Perhaps."

label act2_2_14:
    # SCENE 2.14 · A House at the Edge of Tatarasuna
    $ show_title("SCENE 2.14\nA House at the Edge of Tatarasuna")
    scene bg small_house
    with scene_fade
    # A boy of about eight sits propped against pillows, wrapped in a blanket twice his size. A barefoot puppet is trying, and failing, to cook rice.
    boy "You’re doing it wrong again."
    puppet "I am following the instructions."
    boy "The instructions say water, Kabu. Not more water."
    puppet "I thought it would help."
    # The boy laughs, and the laugh turns into a cough. The puppet is at his side before it ends.
    echo "(from the doorway, almost inaudibly) He called me Kabu."
    mc "Because of Kabukimono?"
    echo "Because he couldn’t say it. He was five when his parents died of the sickness. Three years later he still hadn’t learned to finish the word."
    echo "I never corrected him."
    # Inside, the boy has stopped coughing. He pulls a crumpled paper from under his pillow and holds it up.
    boy "I drew it. For when the sickness is gone."
    scene cg child_drawing
    with iris_open
    boy "You’ll live there. With me. As family."
    puppet "I’m a puppet."
    boy "I know."
    puppet "I don’t know how to be a... brother."
    boy "You’re doing it right now, Kabu."
    # He holds out a small hand, little finger crooked.
    boy "Promise. We’ll live together. Always."
    # The puppet stares at the finger. After a long moment, he hooks his own around it.
    scene cg hooked_pinkies
    with scene_fade
    puppet "...Promise."

label act2_2_15:
    # SCENE 2.15 · The Long Winter
    $ show_title("SCENE 2.15\nThe Long Winter")
    scene bg montage
    with scene_fade
    play music audio.six_days fadein 2.0  # “Six Days”: the lullaby, now with a heartbeat under it, getting faster.
    echo "I ran for six days. I found every herb the village had a name for."
    echo "I came back on the sixth night."
    scene bg small_house_dark
    with scene_fade
    # The puppet stands in the doorway, holding the satchel. He doesn’t come in.
    scene cg empty_bed
    with scene_fade
    # The ink around the puppet cracks. Then the ink around the Echo cracks. They are the same crack.
    echo "He promised."
    echo "He was eight. He wasn’t allowed to promise a thing like that. No one is. No one should be allowed to promise a thing like that to someone who won’t die."
    echo "There was nobody to hate. I looked. I looked everywhere."

    # CHOICE: The crack is under all three of you.
    menu:
        "Stay beside him. Say nothing at all.":
            $ _sel_6 = "A"
            $ bump('m', 1)
        "“Neither of you broke it.”":
            $ _sel_6 = "B"
            $ bump('b', 1)
        "“What was he like?”":
            $ _sel_6 = "C"
            $ bump('w', 1)

    if _sel_6 == 'A':
        # You stay. The crack stops at your feet. It does not close, but it stops.
        pass
    elif _sel_6 == 'B':
        echo "Say that again."
        mc "Neither of you broke it."
        echo "(rough) It feels as though I did."
    elif _sel_6 == 'C':
        echo "(a shaky breath) Loud. He was very loud. Like Niwa. He said I held my tea like a funeral."
        wanderer "(softly) You still do."

label act2_2_16:
    # SCENE 2.16 · The Promise
    $ show_title("SCENE 2.16\nThe Promise")
    scene bg house_dawn
    with scene_fade
    play music audio.a_smaller_promise fadein 2.0  # “A Smaller Promise”: solo flute, one clear line.
    echo "Promises are what people say to feel better about leaving."
    echo "Every one I’ve heard has been a lie, or a mistake, or a funeral."
    mc "Then I’ll make a smaller one."
    echo "Quill."
    mc "Not forever. Not “always.” Not something a person can’t keep."
    mc "On the last page, whatever’s happening, wherever I am, I’ll be at the archive door."
    echo "(a bitter little breath) That’s the cheapest oath I’ve ever heard."
    mc "It’s the one I can keep."
    echo "Everyone says that."
    mc "Then watch."

    # CHOICE: The Promise. All options set PROMISE_MADE (the promise has been made;
    menu:
        "Say it plainly, nothing else.":
            $ _sel_7 = "A"
            $ bump('m', 1)
        "Hold out your little finger.":
            $ _sel_7 = "B"
            $ bump('b', 1)
        "“Both of us.” Look at the Wanderer.":
            $ _sel_7 = "C"
            $ bump('w', 1)

    $ promise_made = True

    if _sel_7 == 'A':
        echo "(a pause) ...Plain. Fine. Plain I can believe."
    elif _sel_7 == 'B':
        # He looks at the finger the way one looks at a snake, or a gift. He doesn’t take it. He
        echo "That’s a child’s thing."
        mc "It’s still a promise."
    elif _sel_7 == 'C':
        wanderer "(after a beat) I was going to be there anyway."
        wanderer "...Both of us. Fine."
        play sound audio.sfx_page

label act2_2_17:
    # DAY 21 · SCENE 2.17 · The Archive Annex · Night
    $ set_page(9, 21)
    $ show_title("DAY 21 · SCENE 2.17\nThe Archive Annex · Night")
    scene bg annex_night
    with scene_fade
    play music audio.warm_table fadein 2.0  # “Warm Table”: the cello from the dining scene, brighter now.
    # The Echo takes the cup. No sugar. He drinks it all the way down.
    wanderer "You didn’t spit it out."
    echo "I’m not going to dignify that."
    wanderer "You drank all of it."
    echo "It’s... acceptable."
    # The Wanderer almost smiles. He catches himself. He doesn’t catch himself soon enough.
    # The Folio lies on the table between the cups. MC turns it to the contents page. Three headings in clear ink: The Pavilion. Tatarasuna. The Boy.
    # And below them, a fourth line. The ink is pale, almost invisible. There is no title. Just a page number: 30.
    nahida "(from the doorway, unannounced as ever) Three doors. The Rule of Three says a thing changes on the fourth."
    nahida "I’m afraid that one is not mine to write."
    # She looks at MC.
    nahida "And the Doctor is in Sumeru City. He asked for the archive by name."
    stop music fadeout 1.0
    # END OF ACT 2
    n "Act 3: The Second Box The Doctor wants the Folio. Everyone has a price, and he knows yours."

    jump act3_3_1

