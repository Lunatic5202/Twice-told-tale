################################################################################
## Twice-Told Tale - Act 1: Two at the Same Table
################################################################################

label act1_1_1:

    scene bg annex_day with act_wipe
    $ set_page(29, 1)
    $ show_act("I", "Two at the Same Table")
    $ show_title("DAY 1 \u00b7 SCENE 1.1\nThe Archive Annex \u00b7 Morning")

    play music audio.double_trouble fadein 2.0
    show echo sneer at at_left with soft_dissolve
    show wanderer neutral at at_right with soft_dissolve

    wanderer "...No. No. I haven\u2019t had enough tea for this."

    echo "Quill. Who is the child in my hat?"

    wanderer "It is not your hat."

    echo "It is plainly based on my hat. And the colors are an insult. Teal. Did you lose a bet?"

    wanderer "Hmph. I\u2019m leaving."

    # [He turns on his heel. The air in the doorway ripples green. Something
    #  small steps through it, as if the door had been waiting for her.]

    nahida "Please don\u2019t. I\u2019ve only just gone to the trouble of arriving."

    # [CG: Nahida between the two of them, a hand raised like a teacher
    #  quieting a classroom.]
    scene cg nahida_between with soft_dissolve
    scene bg annex_day with soft_dissolve
    show echo sneer at at_left
    show wanderer neutral at at_right
    show nahida gentle at at_center with soft_dissolve

    nahida "Good morning, both of you. Please don\u2019t kill each other before I\u2019ve finished explaining. It\u2019s rude to the carpets."

    nahida "Wanderer, that Folio holds the story of what I kept of you. Not the memories themselves, but the tale of them, written in a form nobody else could read. It was never meant to hold two."

    wanderer "Two."

    nahida "A tale can be told twice. Someone has told it twice."

    # [She looks at MC. Both men look at MC.]

    mc "I wrote one word."

    nahida "Which one?"

    mc "\u201cStayed.\u201d"

    nahida "Well. That explains the draft."

    echo "Spare me the metaphors, little god. What am I?"

    nahida "You are him, in the instant before he put his hand into Irminsul. Everything he knew then, you know. Everything he learned afterward, you do not."

    echo "Then I am the original. He is the revision."

    wanderer "You\u2019re the draft."

    echo "Drafts are where the truth is."

    # [A beat. They stare at each other the way two people stare into a mirror
    #  that talks back.]

    nahida "The Folio has thirty pages. One burns each dawn. When the last one goes, the record keeps one name. I have looked, and it cannot keep both."

    wanderer "Then burn it now."

    nahida "I considered it. If I burn the book, he burns with it."

    # [The Wanderer's jaw tightens. He says nothing.]

    nahida "One more thing. The Pen can rewrite what the book says. Every line it changes takes the next page with it. Use it sparingly. Or not at all."

    nahida "And no one outside this room learns that there are two. Not yet. The Doctor reads Irminsul the way you read menus."

    # [The Wanderer's hat tilts. Only slightly.]

    menu choice_1_1:
        "What do you say?"

        "\u201cI\u2019ll fix this. I can rewrite the page.\u201d":
            $ bump("m", -1)
            $ fixer = True
            nahida "(very gently) That is exactly what I was afraid you\u2019d say."
            echo "She wants to edit me. How flattering."

        "\u201cI\u2019ll stay with him until we work it out.\u201d":
            $ bump("b", 1)
            echo "Stay with me. As if I were a stray."
            wanderer "...You\u2019d be good at it, actually."

        "\u201cNeither of you is a mistake.\u201d":
            $ bump("m", 1)
            nahida "Hm. That is a very good first sentence. (To the two of them) Try to live up to it."

    jump act1_1_2


label act1_1_2:

    $ set_page(28, 2)
    scene bg courtyard_day with scene_fade
    $ show_title("DAY 2 \u00b7 SCENE 1.2\nAkademiya Courtyard \u00b7 Noon")

    play music audio.hat_guy fadein 2.0
    show echo amused at at_left with soft_dissolve
    show wanderer guarded at at_far_right with soft_dissolve

    n "The Echo cannot go more than forty paces from the Folio. The Wanderer will not let the Echo out of his sight. So the Folio goes to lunch, and everyone goes with it."

    echo "I have walked into a hundred courts. This is the first one with a duck in it."

    wanderer "The duck is a student."

    # [Two familiar silhouettes cross the courtyard. Tighnari first, ears up.
    #  Cyno behind him with a card deck.]
    show tighnari neutral at at_center with soft_dissolve
    show cyno neutral at at_right with soft_dissolve

    tighnari "Hat Guy. Why are there two of you?"

    wanderer "There aren\u2019t."

    echo "There are, rather plainly."

    cyno "Oh, I see. A double act. I\u2019d say that\u2019s a hat trick."

    tighnari "Cyno."

    cyno "I was building to it."

    # [Tighnari's eyes pass over the Echo. Nothing. No flicker. He does not
    #  know him at all.]
    # [The Echo's smile slips for half a second.]

    echo "The ranger. You look well."

    tighnari "Have we met?"

    echo "...No."

    # [SFX: A faint chime, like a page turning.]
    play sound audio.sfx_page

    tighnari "And who is this?"

    wanderer "A cousin. Don\u2019t ask."

    menu choice_1_2:
        "You are the one holding the book."

        "\u201cCousin. Visiting from Inazuma.\u201d":
            $ bump("w", 1)
            wanderer "(quietly) Good."
            echo "She lies like she\u2019s reading it off a card."

        "\u201cA visiting scholar. Very distinguished.\u201d":
            $ bump("b", 1)
            echo "(delighted) Distinguished. I\u2019m keeping that."
            wanderer "Don\u2019t encourage him."

        "\u201cHe\u2019s... complicated.\u201d":
            $ bump("m", 1)
            cyno "Complicated is a good start. We\u2019ll keep an eye on him."
            tighnari "Both eyes."

    jump act1_1_3


label act1_1_3:

    $ set_page(27, 3)
    scene bg dining_evening with scene_fade
    $ show_title("DAY 3 \u00b7 SCENE 1.3\nThe Dining Hall \u00b7 Evening")

    play music audio.the_table fadein 2.0

    # [CG: The Wanderer, standing at the end of the table, looking at the soup.
    #  Not at the people. At the soup.]
    scene cg wanderer_soup with soft_dissolve
    scene bg dining_evening with soft_dissolve
    show wanderer tired at at_right with soft_dissolve
    show echo amused at at_left with soft_dissolve

    echo "You are staring at that bowl as though it owes you money."

    wanderer "...It\u2019s a very interesting bowl."

    echo "You do not even eat."

    wanderer "I don\u2019t need to eat. That\u2019s different."

    n "He has watched dinner tables for as long as he has had eyes. People lean toward each other across them. They pass the salt without asking."

    # [MC sets two places. Then, after a moment, a third.]

    mc "Sit."

    wanderer "I just told you\u2014"

    mc "I know. Sit anyway."

    # [He sits. The Echo, after a long, theatrical sigh, sits across from him.]

    # [SFX: A teapot, a poured cup. Steam.]

    wanderer "Try the tea."

    echo "It\u2019s bitter."

    wanderer "That\u2019s the point."

    echo "It tastes like swallowing something."

    wanderer "It\u2019s the true flavor of life. It takes a while."

    echo "Spoken like someone who has made peace with swallowing things."

    # [Silence. The Wanderer looks into his cup.]

    menu choice_1_3:
        "The tea is going cold between them."

        "Add sugar to the Echo\u2019s cup without a word.":
            $ bump("b", 1)
            echo "(sips) ...Hm. That\u2019s less offensive."
            wanderer "It\u2019s not tea anymore."
            echo "It\u2019s better."

        "\u201cWhat would you like it to taste like?\u201d":
            $ bump("m", 1)
            echo "(startled) No one has ever asked me that."
            echo "...Warm. Something warm."
            wanderer "That\u2019s called tea. (He refills it.)"

        "\u201cDrink it bitter. He did.\u201d":
            $ bump("w", 1)
            echo "(sips, grimaces, sips again) I hate it. I\u2019ll finish it."
            wanderer "(almost a smile) That\u2019s how it starts."

    jump act1_1_4


label act1_1_4:

    $ set_page(26, 4)
    scene bg annex_night with scene_fade
    $ show_title("DAY 4 \u00b7 SCENE 1.4\nThe Archive Annex \u00b7 Night")

    play music audio.mechanical_ears fadein 2.0

    # [BG: Low lamp. The Echo sits against a bookcase, one hand pressed over
    #  his ear. The Wanderer stands over him with a small velvet roll of
    #  tools.]
    show echo cold at at_left with soft_dissolve
    show wanderer neutral at at_right with soft_dissolve

    echo "There\u2019s a sound. Like a sheet of tin in the wind. I can hear the lamp thinking."

    wanderer "Your ears need maintenance. Mine did, a few weeks ago. You\u2019re a draft. Nobody ever serviced you."

    echo "I do not need a seamstress."

    wanderer "You need a very small screwdriver and someone patient. I\u2019m neither. So."

    # [He looks at MC. She is already holding the Pen.]

    menu choice_1_4:
        "The ringing is making him wince."

        "\u201cCan I try something? You can say no.\u201d":
            $ bump("m", 1)
            $ bump("b", 1)
            echo "(a long pause) ...You asked."
            echo "Do it."

        "Use the Pen to smooth the sound away.":
            $ bump("pen", 1)
            $ fixer = True
            $ bump("m", -1)
            # [The ringing stops at once. A page in the Folio curls up and
            #  burns, a day early.]
            echo "(lowering his hand) That was fast."
            echo "You did not ask."
            wanderer "(flatly) That\u2019s the Pen for you."

        "\u201cTeach me how. I\u2019ll do it carefully.\u201d":
            $ bump("w", 1)
            $ bump("m", 1)
            wanderer "(handing over a tiny screwdriver, without comment) Left. Slowly."
            echo "(through his teeth) Don\u2019t breathe on me."

    jump act1_1_5


label act1_1_5:

    $ set_page(25, 5)
    scene bg annex_night with scene_fade
    $ show_title("DAY 5 \u00b7 SCENE 1.5\nThe Archive Annex \u00b7 Night")

    play music audio.what_he_can_t_read fadein 2.0
    show echo cold at at_left with soft_dissolve
    show wanderer guarded at at_right with soft_dissolve

    echo "\u201cThe Pavilion.\u201d \u201cTatarasuna.\u201d \u201cThe Boy.\u201d I can read the doors. I can\u2019t read the rooms."

    echo "You can."

    # [The Wanderer shuts the Folio with a flat hand.]

    wanderer "Not yet."

    echo "You have the keys and you hide the doors."

    wanderer "I hide them because I know what\u2019s behind them."

    echo "Coward."

    wanderer "(sharp, not loud) You have no idea what that word costs."

    menu choice_1_5:
        "They are both looking at you."

        "\u201cHe\u2019s right. You\u2019re not ready.\u201d":
            $ bump("w", 1)
            echo "Ah. So you\u2019re his."
            wanderer "(not meeting her eyes) ...That isn\u2019t what she said."

        "\u201cHe\u2019s right. It\u2019s his story. He should read it.\u201d":
            $ bump("b", 1)
            wanderer "(low) You don\u2019t know what you\u2019re asking."
            echo "(to MC, with a wicked little smile) I\u2019m beginning to like her."

        "\u201cBoth of you. Nobody leaves till you say one honest thing each.\u201d":
            $ bump("m", 1)
            echo "One honest thing. (Pause) I don\u2019t know who I am if I\u2019m not angry."
            wanderer "(after a long time) I don\u2019t know who I am if I\u2019m not tired."

    jump act1_montage


label act1_montage:

    $ set_page(24, 6)
    scene bg annex_day with scene_fade
    $ show_title("DAY 6 \u00b7 MONTAGE\n\u201cThree Small Disasters\u201d")

    play music audio.hat_guy_reprise fadein 2.0
    show echo amused at at_left with soft_dissolve
    show wanderer flustered at at_right with soft_dissolve

    n "The Echo and the Wanderer fight over the window seat. The Echo wins by sitting on the Wanderer\u2019s hat."

    n "The Echo \u201creviews\u201d the Akademiya\u2019s architecture aloud to a lecture hall. A professor takes notes."

    n "The Wanderer teaches MC to brew tea at the correct temperature. The Echo steals the first cup."

    jump act1_1_6


label act1_1_6:

    $ set_page(23, 7)
    scene bg rooftop_night with scene_fade
    $ show_title("DAY 7 \u00b7 SCENE 1.6\nThe Akademiya Rooftop \u00b7 Night")

    play music audio.which_of_us fadein 2.0
    show wanderer soft at at_center with soft_dissolve

    wanderer "I tried to erase myself, once. From Irminsul. From history. To undo what had happened."

    wanderer "It didn\u2019t work. The history rewrote itself the same way without me. Everyone I\u2019d hurt was still hurt. Everyone who died was still dead. Only I disappeared. And then I came back."

    # [He turns his cup in his hands.]

    wanderer "So now there\u2019s him. The one who still thinks that\u2019s a plan. And I keep asking myself which of us is the real one."

    menu choice_1_6:
        "He is not looking at you."

        "\u201cYou\u2019re both real.\u201d":
            $ bump("m", 1)
            wanderer "...That\u2019s a very archivist thing to say."
            wanderer "Thank you."

        "\u201cYou\u2019re the one who chose.\u201d":
            $ bump("w", 1)
            wanderer "(a pause) Chose. Yes. I suppose I did."

        "\u201cI don\u2019t know. What do you think?\u201d":
            $ bump("m", 1)
            $ bump("w", 1)
            wanderer "(long silence) I think I\u2019d like not to have to answer that tonight."

    # [SFX: A foot on the roof stairs below. A pause. Then the stairs again,
    #  quickly.]
    play sound audio.sfx_chime

    # [He leans over the stairwell. The Echo's hat is just visible,
    #  disappearing down the dark.]

    wanderer "...Forty paces."

    mc "He heard all of it."

    wanderer "Of course he did."

    jump act1_1_7


label act1_1_7:

    $ set_page(22, 8)
    scene bg annex_dawn with scene_fade
    $ show_title("DAY 8 \u00b7 SCENE 1.7\nThe Archive Annex \u00b7 Dawn")

    play music audio.the_margin_door fadein 2.0
    show nahida serious at at_center with soft_dissolve
    show wanderer guarded at at_right with soft_dissolve
    show echo cold at at_left with soft_dissolve

    nahida "The Doctor has been asking after a \u201clightning-boned prototype.\u201d He doesn\u2019t know who. He is near enough to guess."

    wanderer "Then we run out of time faster than a page a day."

    nahida "The Folio can show what he doesn\u2019t remember. The pages between the doors. You can walk them."

    nahida "Three doors, three rooms. Three betrayals. You\u2019ve been carrying them for a long time. I\u2019d rather you didn\u2019t carry them alone anymore."

    # [At the back of the annex, the shelves shift. A small door opens in the
    #  margin of the world.]

    # [CG: A door in the margin, edged in gold ink. Beyond it, mist and the
    #  smell of wet stone.]
    scene cg margin_door with door_blinds
    scene bg annex_dawn with soft_dissolve
    show nahida serious at at_center
    show wanderer guarded at at_right
    show echo cold at at_left

    echo "Show me."

    wanderer "(very quietly) You\u2019ll regret it."

    echo "Then I will regret it with my eyes open."

    menu choice_1_7:
        "End of Act 1. The door is open."

        "\u201cTogether. All three of us.\u201d":
            $ bump("m", 1)

        "\u201cWait one more night.\u201d":
            $ bump("w", 1)
            # [a page burns anyway]
            $ set_page(21, 8)

        "Step through first.":
            $ bump("b", 1)

    # [END OF ACT 1]

    jump act2_2_1
