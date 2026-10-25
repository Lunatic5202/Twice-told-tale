################################################################################
## Twice-Told Tale - Prologue: Marginalia
################################################################################

label prologue_0_1:

    scene bg annex_night with scene_fade
    $ show_title("PROLOGUE \u00b7 MARGINALIA\n\nSCENE 0.1 \u00b7 The Archive Annex \u00b7 Midnight")

    ## The title theme is already playing from the menu; only start it if the
    ## music channel is silent (e.g. the player muted and restored, or loaded in).
    if not renpy.music.get_playing("music"):
        play music audio.marginalia fadein 2.0

    n "The senior archivists have a name for the book in the locked cabinet: Folio Zero. They also have a rule about it. Don’t open it. Don’t move it. If it starts humming, fetch someone senior." 
n "It has been humming for three months. The senior archivists are all very busy."

    n "You were the only apprentice still in the building."

    mc "Folio Zero. \u201cFairy tale, encrypted. Subject: one wanderer.\u201d Page eleven. The sentence just stops."

    # [CG: Close on the page. The line reads "...and he reached out his hand,
    #  and the whole tree held its breath, and" and then a torn edge.]
    scene cg folio_page with iris_open

    mc "A sentence shouldn\u2019t end like that. Nobody should."

    # [The Pen lies beside the Folio. Gold nib, worn grip. Every apprentice is
    #  issued one.]
    scene bg annex_night with soft_dissolve

    n "The rule is written above the workbench in letters large enough to read from the door: MEND WHAT IS TORN. DO NOT ALTER THE TEXT. The Pen in your hand was issued with the rule. Nobody explained what happens if you break it."

    mc "One word. It needs an ending."

    # [SFX: Nib on paper. One word, written in her own hand: "stayed."]
    play sound audio.sfx_pen

    # [The ink does not dry. It rises.]

    # [MUSIC: The ticking stops. A single low string.]

    with quake
    n "The lamp flares and the shelves shiver. The first thing to climb out of the page is a hat brim, wide and conical, rising like a sunrise."

    # [CG: A figure steps out of the ink. A red and purple jacket, a veil
    #  printed with a single character, a mask on the hat. His eyes are shut.
    #  They open.]
    scene cg prologue_echo with soft_dissolve
    show echo sneer at at_center with soft_dissolve

    echo "...Hm."

    echo "The Gnosis is gone." 
echo "This floor is wrong." 
echo "And you—" 
echo "You look like you’re about to faint. Don’t. I have questions, and I’m not carrying you to the infirmary."

    mc "You\u2014you came out of the book."

    echo "I came out of a book, apparently. Don’t look so pleased with yourself, scribbler."

    # [He turns a full circle. His hand goes to his chest, to the gold feather
    #  there, and stays.]

    echo "Sumeru. The scholars\u2019 coop. Her little garden of books. Is this her trap? It is a poor one."

    mc "It\u2019s the Akademiya archive. There\u2019s no trap. There\u2019s a typo. I mean, there was a typo."

    echo "A typo."

    echo "I was dragged out of the dark by a typo."

    # [He laughs. It is the laugh of someone who has run out of other options.]

    echo "Fine. What do I call you?" 
mc "I—" 
echo "You have a name. Start there."

    # MC (name entry): the player types a name here. The Echo ignores it for
    # the rest of the prologue.
    python:
        _entered = renpy.input("{i}What is your name?{/i}", default="", length=24, exclude="{}[]").strip()
        if _entered:
            mc_name = _entered
    echo "Quill, then." 
mc "That’s not my—" 
echo "I didn’t ask what your mother called you. It’s what I’m calling you until this gets less ridiculous."

    # [He strides toward the archive door. At the threshold he stops as if he
    #  has walked into glass.]

    # [SFX: A soft chime. The ink around the doorframe flickers gold.]
    play sound audio.sfx_chime
    with shake

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

    scene bg annex_predawn with scene_fade
    $ show_title("SCENE 0.2 \u00b7 The Archive Annex \u00b7 Before Dawn")

    play music audio.marginalia_dawn fadein 2.0
    show echo cold at at_left with soft_dissolve

    echo "You didn’t fetch anyone."

    mc "I got as far as the stairs."

    echo "And then you came back." 
mc "I heard you trying the door." 
echo "That isn’t an answer." 
mc "It’s the one I have."

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
    scene cg first_page_burn with soft_dissolve
    $ set_page(29)

    echo "Something is counting."

    mc "Something is. I think it just started."

    # [The door at the far end of the archive opens. Someone stands in it,
    #  holding a cup of tea, mid-sip. He is wearing a hat.]
    scene bg annex_predawn with soft_dissolve
    show echo cold at at_left with soft_dissolve

    # [MUSIC: Cut. A single note held.]
    stop music fadeout 0.5
    show wanderer neutral at at_right with soft_dissolve

    # [CG: The Wanderer in the doorway, cup halfway to his mouth.]
    show cg prologue_tea with soft_dissolve
    pause
    hide cg with soft_dissolve

    wanderer "..."

    # [The cup stops halfway to his mouth.]

    # [END OF PROLOGUE]

    jump act1_1_1
