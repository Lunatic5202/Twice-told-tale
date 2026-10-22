#!/usr/bin/env bash
# Download CC0 sound effects (OpenGameArt) into game/audio/sfx.
# All sources are CC0. See game/audio/CREDITS.md.
set -euo pipefail
cd "$(dirname "$0")/.."
SFX=game/audio/sfx
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$SFX"
B="https://opengameart.org/sites/default/files"

# Packs (extract individual .ogg from each).
curl -fsSL --max-time 120 "$B/100-CC0-SFX_0.zip"          -o "$TMP/pack.zip"
curl -fsSL --max-time 120 "$B/book_flips_-_starninjas.zip" -o "$TMP/book.zip"
unzip -qo "$TMP/pack.zip" -d "$TMP/pack"
unzip -qo "$TMP/book.zip" -d "$TMP/book"

cp "$TMP/pack/bell_01.ogg"      "$SFX/sfx_bell.ogg"
cp "$TMP/pack/gong_01.ogg"      "$SFX/sfx_chime.ogg"
cp "$TMP/pack/glass_04.ogg"     "$SFX/sfx_glass.ogg"
cp "$TMP/book/book_flip.5.ogg"  "$SFX/sfx_page.ogg"
cp "$TMP/pack/paper_01.ogg"     "$SFX/sfx_pen.ogg"
cp "$TMP/pack/door_close_01.ogg" "$SFX/sfx_door.ogg"
cp "$TMP/pack/metal_04.ogg"     "$SFX/sfx_hammer.ogg"
cp "$TMP/pack/weird_04.ogg"     "$SFX/sfx_roar.ogg"
cp "$TMP/pack/pot_01.ogg"       "$SFX/sfx_kettle.ogg"
cp "$TMP/pack/slam_02.ogg"      "$SFX/sfx_slam.ogg"

fetch_convert() { # url out
  curl -fsSL --max-time 90 "$1" -o "$TMP/raw"
  ffmpeg -nostdin -loglevel error -y -i "$TMP/raw" -c:a libvorbis -q:a 4 "$2"
  test -s "$2"
  echo "ok   $(basename "$2")"
}
fetch_convert "$B/amb_rain_loop_1.ogg" "$SFX/sfx_rain.ogg"
fetch_convert "$B/rain-thunder.ogg"    "$SFX/sfx_thunder.ogg"
fetch_convert "$B/fire-1.ogg"          "$SFX/sfx_fire.ogg"
fetch_convert "$B/01-footstep.ogg"     "$SFX/sfx_footsteps.ogg"

ls -la "$SFX"
