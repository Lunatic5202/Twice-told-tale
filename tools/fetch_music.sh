#!/usr/bin/env bash
# Download CC0 music from OpenGameArt and normalize to .ogg cue files.
# Every source is CC0 (public domain). See game/audio/CREDITS.md.
set -u
cd "$(dirname "$0")/.."
MUS=game/audio/music
TMP="$(mktemp -d)"
mkdir -p "$MUS"

fetch() { # url out
  if [ -s "$2" ]; then echo "skip $2"; return; fi
  curl -sL --max-time 90 "$1" -o "$TMP/raw"
  ffmpeg -nostdin -loglevel error -y -i "$TMP/raw" -c:a libvorbis -q:a 4 "$2" \
    && echo "ok   $(basename "$2")" || echo "FAIL $1"
}

# --- source tracks ---------------------------------------------------------
B="https://opengameart.org/sites/default/files"
fetch "$B/ambientmain_0.ogg"                            "$TMP/src_tragic.ogg"
fetch "$B/Snowfall%20%28Looped%20ver.%29_0.ogg"         "$TMP/src_snow.ogg"
fetch "$B/ObservingTheStar.ogg"                         "$TMP/src_space.ogg"
fetch "$B/forest.ogg"                                   "$TMP/src_forest.ogg"
fetch "$B/cave%20themeb4.ogg"                           "$TMP/src_cave.ogg"
fetch "$B/TownTheme.mp3"                                "$TMP/src_town.ogg"
fetch "$B/the_field_of_dreams.mp3"                      "$TMP/src_field.ogg"
fetch "$B/8bit%20Bossa.mp3"                             "$TMP/src_bossa.ogg"
fetch "$B/enchanted%20tiki%2086_0.mp3"                  "$TMP/src_tiki.ogg"
fetch "$B/song18_0.mp3"                                 "$TMP/src_crystal.ogg"
fetch "$B/Next%20to%20You.mp3"                          "$TMP/src_next.ogg"
fetch "$B/Dark_Rainy_Night%28ambience%29.ogg"           "$TMP/src_rain.ogg"
fetch "$B/at%20the%20end%20of%20hope.mp3"               "$TMP/src_hope.ogg"
fetch "$B/FantasyMp3.mp3"                               "$TMP/src_fantasy.ogg"
fetch "$B/i_want_to_go_home.mp3"                        "$TMP/src_home.ogg"
fetch "$B/humanthemepreview.mp3"                        "$TMP/src_human.ogg"
fetch "$B/bleeding_out2_1.ogg"                          "$TMP/src_bleeding.ogg"
fetch "$B/preview_13.mp3"                               "$TMP/src_endscene.ogg"
fetch "$B/Lament_for_a_Warriors_Soul_0.mp3"             "$TMP/src_lament.ogg"
fetch "$B/Eye%20of%20the%20Storm.mp3"                   "$TMP/src_storm.ogg"
fetch "$B/Contemplation.mp3"                            "$TMP/src_contemp.ogg"
fetch "$B/untitled.mp3"                                 "$TMP/src_piano.ogg"
fetch "$B/013_Another_August.mp3"                       "$TMP/src_august.ogg"
fetch "$B/JRPG%20Piano.mp3"                             "$TMP/src_jrpg.ogg"
fetch "$B/musicbox1_spooky_waltz.ogg"                   "$TMP/src_musicbox.ogg"
fetch "$B/Lullaby.mp3"                                  "$TMP/src_lullaby.ogg"
fetch "$B/goodbye_lullaby.mp3"                          "$TMP/src_goodbye.ogg"
fetch "$B/ASimpleTrifle.ogg"                            "$TMP/src_trifle.ogg"
fetch "$B/moonlit_lullaby_for_the_lost.ogg"             "$TMP/src_moonlit.ogg"
fetch "$B/dungeon002.ogg"                               "$TMP/src_dungeon.ogg"
fetch "$B/Factory_0.ogg"                                "$TMP/src_factory.ogg"
fetch "$B/GalacticTemple.ogg"                           "$TMP/src_temple.ogg"
fetch "$B/creepyloop-v2.ogg"                            "$TMP/src_creepy.ogg"
fetch "$B/darktheme_0.mp3"                              "$TMP/src_dark0.ogg"
fetch "$B/theme.ogg"                                    "$TMP/src_dark.ogg"
fetch "$B/path_walk_remake-mp3.mp3"                     "$TMP/src_pens.ogg"
fetch "$B/awesomeness.wav"                              "$TMP/src_menu.ogg"
fetch "$B/b423b42.wav"                                  "$TMP/src_load.ogg"

# --- cue mapping: cue=source -------------------------------------------------
copy() { [ -s "$TMP/src_$2.ogg" ] && cp "$TMP/src_$2.ogg" "$MUS/$1.ogg" && echo "cue  $1 <- $2"; }

copy marginalia                    musicbox
copy marginalia_dawn               moonlit
copy double_trouble                bossa
copy hat_guy                       town
copy hat_guy_reprise               field
copy the_table                     piano
copy warm_table                    august
copy warm_table_reprise            august
copy the_boy                       lullaby
copy a_smaller_promise             goodbye
copy clean_instruments             trifle
copy reprise_clean_instruments     contemp
copy the_doctor_s_hour             dark0
copy the_old_dawn                  fantasy
copy what_i_never_said             piano
copy the_thing_unsaid              bleeding
copy six_days                      pens
copy three_pages                   jrpg
copy the_last_evening             endscene
copy what_we_can_t_take_back       home
copy a_name_is_a_small_thing       trifle
copy what_he_built_from_nothing    human
copy the_margin_door               temple
copy page_walk                     crystal
copy escher                        dark
copy mechanical_ears               dungeon
copy quiet                         snow
copy rumors                        creepy
copy slumber                       lullaby
copy smoke                         lament
copy sword_dance                   tiki
copy tatarasuna                    factory
copy three_hundred_and_eleven      musicbox
copy what_he_can_t_read            jrpg
copy what_he_kept                  home
copy what_i_remember               dark0
copy what_was_written              piano
copy which_of_us                   contemp

rm -rf "$TMP"
echo "done"
