################################################################################
## Twice-Told Tale - Prologue: Marginalia
################################################################################

label prologue_0_1:

    scene bg annex_night with fade
    $ show_title("PROLOGUE \u00b7 MARGINALIA\n\nSCENE 0.1 \u00b7 The Archive Annex \u00b7 Midnight")

    play music audio.marginalia fadein 2.0

    n "Everyone in the archive knows about the Folio. Nobody has read it. It sits in a cabinet that hums, and for three months it has waited for someone with steady hands and no sense of self-preservation."

    n "That is you."

    mc "Folio Zero. \u201cFairy tale, encrypted. Subject: one wanderer.\u201d Page eleven. The sentence just stops."

    # [CG: Close on the page. The line reads "...and he reached out his hand,
    #  and the whole tree held its breath, and" and then a torn edge.]
    scene cg folio_page with dissolve

    mc "A sentence shouldn\u2019t end like that. Nobody should."

    # [The Pen lies beside the Folio. Gold nib, worn grip. Every apprentice is
    #  issued one.]
    scene bg annex_night with dissolve

    n "Rule one of the archive: mend what is torn, and never change what is written. The Pen can do both. Only one of them is allowed."

    mc "Just the last word. Just so it can breathe."

    # [SFX: Nib on paper. One word, written in her own hand: "stayed."]
    play sound audio.sfx_pen

    # [The ink does not dry. It rises.]

    # [MUSIC: The ticking stops. A single low string.]

    n "The lamp flares and the shelves shiver. The first thing to climb out of the page is a hat brim, wide and conical, rising like a sunrise."

    # [CG: A figure steps out of the ink. A red and purple jacket, a veil
    #  printed with a single character, a mask on the hat. His eyes are shut.
    #  They open.]
    scene cg prologue_echo with dissolve
    show echo sneer at center with dissolve

    echo "...Hm."

    echo "The Gnosis is gone. The floor is not a floor I recognize. And you are holding a feather pen like a woman about to be hanged for it."

    mc "You\u2014you came out of the book."

    echo "I came out of something. Be precise, scribbler, it is the only thing your kind is good for."

    # [He turns a full circle. His hand goes to his chest, to the gold feather
    #  there, and stays.]

    echo "Sumeru. The scholars\u2019 coop. Her little garden of books. Is this her trap? It is a poor one."

    mc "It\u2019s the Akademiya archive. There\u2019s no trap. There\u2019s a typo. I mean, there was a typo."

    echo "A typo."

    echo "I was dragged out of the dark by a typo."

    # [He laughs. It is the laugh of someone who has run out of other options.]

    echo "Fine. What do I call the hand that did this? You have a name."

    # MC (name entry): the player types a name here. The Echo ignores it for
    # the rest of the prologue.
    python:
        _entered = renpy.input("{i}What is your name?{/i}", default="", length=24, exclude="{}[]").strip()
        if _entered:
            mc_name = _entered
    echo "Quill. You will be Quill. Names are cheap. I have had four."

    # [He strides toward the archive door. At the threshold he stops as if he
    #  has walked into glass.]

    # [SFX: A soft chime. The ink around the doorframe flickers gold.]
    play sound audio.sfx_chime

    echo "...No."

    echo "What have you done to me?"

    mc "I don\u2019t know! I didn\u2019t know it could do anything!"

    # [She lifts the Folio. He takes one step toward her. The threshold lets
    #  him cross. He steps back. It stops him.]

    n "He stays within forty paces of the book. Wherever it goes, he goes."

    echo "A leash."

    echo "I am leashed to a library book."

    jump prologue_0_2


label prologue_0_2:

    scene bg annex_predawn with fade
    $ show_title("SCENE 0.2 \u00b7 The Archive Annex \u00b7 Before Dawn")

    play music audio.marginalia_dawn fadein 2.0
    show echo cold at left with dissolve

    echo "You did not run for help."

    mc "I thought about it."

    echo "You thought about it, and then you sat down and read the book. Tell me why."

    mc "Because the page I mended says what happens next. And I wanted to know if you\u2019d like it."

    echo "And?"

    # [She turns the Folio toward the light. A new line has appeared at the
    #  bottom of page eleven, in a hand she does not know.]

    mc "\u201cThirty pages. One name will remain.\u201d"

    # [SFX: Distant bell. The first light touches the window. The top corner of
    #  page one begins to curl, and a fine line of ash drifts up from it.]
    play sound audio.sfx_bell

    # [CG: The first page burns. A small ring of ash, a counter on the cover
    #  turning from 30 to 29.]
    scene cg first_page_burn with dissolve
    $ set_page(29)

    echo "Something is counting."

    mc "Something is. I think it just started."

    # [The door at the far end of the archive opens. Someone stands in it,
    #  holding a cup of tea, mid-sip. He is wearing a hat.]
    scene bg annex_predawn with dissolve
    show echo cold at left with dissolve

    # [MUSIC: Cut. A single note held.]
    stop music fadeout 0.5
    show wanderer neutral at right with dissolve

    wanderer "..."

    # [The cup stops halfway to his mouth.]

    # [END OF PROLOGUE]

    jump act1_1_1
