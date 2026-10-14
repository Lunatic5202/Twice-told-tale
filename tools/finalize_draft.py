#!/usr/bin/env python3
"""One-time finalizer: turn the generated draft into shipped act files.

Maps the parser's auto `x_bg_*` / `x_cg_*` names onto the canonical art keys
produced by tools/make_art.py, drops the inline placeholder-image block, strips
the descriptive `# TODO(parser)` annotations, resolves the leftover music/sfx
cues, and splits the result into act files.
"""
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "game", "scenes", "act2plus_draft.rpy")
OUTDIR = os.path.join(ROOT, "game", "scenes")

BG_MAP = {
    "x_bg_a_corridor_of_mist_and": "corridor_mist",
    "x_bg_a_long_white_laboratory_glass": "lab_white",
    "x_bg_a_montage_in_gray_and": "montage",
    "x_bg_a_path_of_black_cinders": "cinders_path",
    "x_bg_a_tatami_room_paper_screens": "tatami_room",
    "x_bg_black_a_single_page_lit": "page_black_stage",
    "x_bg_everything_white_page_and_street": "white_page_street",
    "x_bg_fire_climbing_the_white_every": "white_page_burn",
    "x_bg_morning_at_the_furnace_a": "furnace_morning",
    "x_bg_shakkei_pavilion_kannazuka_long_ago": "shakkei_pavilion",
    "x_bg_the_akademiya_at_dawn_green": "akademiya_dawn",
    "x_bg_the_corridor_of_mist_again": "corridor_mist_snow",
    "x_bg_the_furnace_room_the_night": "furnace_room",
    "x_bg_the_grand_narukami_shrine_at": "shrine_night",
    "x_bg_the_house_at_dawn_the": "house_dawn",
    "x_bg_the_laboratory_flickering_the_wanderer": "lab_flicker",
    "x_bg_the_laboratory_lights_drop_every": "lab_glasscube",
    "x_bg_the_mikage_furnace_huge_and": "mikage_furnace",
    "x_bg_the_same_yard_at_night": "furnace_yard_night",
    "x_bg_the_same_yard_tinted_dark": "furnace_yard_warped",
    "x_bg_the_small_house_snow_knee": "small_house_dark",
    "x_bg_the_veranda_the_wanderer_has": "veranda",
    "x_bg_the_white_page_darkening_at": "white_page_dark",
    "x_bg_white_page_street_dawn_bleeding": "white_page_street",
    "x_bg_white_the_white_of_a": "white_page",
    "x_bg_white_then_the_street_the": "white_page_street",
}

CG_MAP = {
    "x_cg_a_child_s_drawing_of": "child_drawing",
    "x_cg_raiden_ei_and_yae_miko": "raiden_yae",
    "x_cg_the_echo_head_bowed_shoulders": "echo_bowed",
    "x_cg_the_folio_bound_in_black": "folio_black",
    "x_cg_the_puppet_walks_into_the": "puppet_furnace",
    "x_cg_the_wanderer_and_the_echo": "wanderer_echo_on_page",
}

# Line-specific corrections where the parser reused a nearby canonical name.
OVERRIDES = [
    ("A long corridor of green stone", "bg", "green_corridor"),
    ("Rows of cots under an open roof", "bg", "sickward"),
    ("A tiny wooden house on the rim", "bg", "small_house"),
    ("The white last page", "bg", "white_page"),
    ("White. No street. No archive", "bg", "white_page"),
    ("The sleeping puppet", "cg", "sleeping_puppet"),
    ("The Daitatara Nagamasa on its stand", "cg", "sword_dance"),
]

MUSIC_MAP = [
    ("A single warm note", "play music audio.warm_table fadein 3.0"),
    ("A hard cut to silence", "stop music fadeout 1.0"),
    ("A single sustained chord", "play music audio.the_old_dawn fadein 2.0"),
    ("None. The absence of sound", "stop music fadeout 2.0"),
    ("A lone flute, uncertain", "play music audio.the_boy fadein 2.0"),
    ("Percussion only", "play music audio.tatarasuna fadein 1.0"),
    ("Silence, then the lullaby", "play music audio.a_smaller_promise fadein 4.0"),
    ("A music box, playing the lullaby", "play music audio.marginalia fadein 3.0"),
]

SFX_MAP = [
    ("The screens slide shut", "play sound audio.sfx_page"),
    ("The furnace roars", "play sound audio.sfx_bell"),
    ("A roar that goes on too long", "play sound audio.sfx_glass"),
    ("The furnace. Then nothing", "play sound audio.sfx_bell"),
    ("The Folio, closing", "play sound audio.sfx_page"),
    ("A single low thrum", "play sound audio.sfx_chime"),
    ("A long exhale", "play sound audio.sfx_page"),
]

HEADER = {
    "act2": "## Twice-Told Tale - Act 2: The Warm Table  (scenes 2.1-2.17)\n",
    "act3": "## Twice-Told Tale - Act 3: The Second Box  (scenes 3.1-3.7)\n",
    "act4": "## Twice-Told Tale - Act 4: The Doctor's Hour  (scenes 4.1-4.4)\n",
    "endings": "## Twice-Told Tale - Endings  (gated, plus the shared beat)\n",
}

BLANK = "################################################################################\n"


def main():
    with open(SRC, encoding="utf-8") as f:
        lines = f.readlines()

    # Drop the leading header + inline placeholder-image init block.
    start = next(i for i, l in enumerate(lines) if l.startswith("label "))
    body = lines[start:]

    out = []
    for l in body:
        # Drop the descriptive trailing annotation on scene/show lines.
        m = re.match(r"^(\s*(?:scene|show)\s+(?:bg|cg)\s+\S+)\s+# TODO\(parser\): (.*)$", l)
        if m:
            code, desc = m.group(1), m.group(2)
            replaced = False
            for needle, kind, key in OVERRIDES:
                if desc.startswith(needle):
                    code = re.sub(r"((?:scene|show)\s+%s\s+)\S+" % kind, r"\g<1>" + key, code)
                    replaced = True
                    break
            out.append(code.rstrip() + "\n")
            continue

        # Resolve leftover music/sfx cue comments.
        m = re.match(r"^(\s*)# TODO\(parser (music|sfx)\): (.*)$", l)
        if m:
            indent, kind, desc = m.group(1), m.group(2), m.group(3)
            table = MUSIC_MAP if kind == "music" else SFX_MAP
            for needle, repl in table:
                if desc.startswith(needle):
                    out.append(indent + repl + "\n")
                    break
            else:
                # No mapping: leave the descriptive comment (harmless).
                out.append(l)
            continue

        # Strip remaining plain descriptive TODO(parser) comments.
        if "# TODO(parser):" in l:
            l = re.sub(r"\s*# TODO\(parser\):.*$", "", l).rstrip() + "\n"

        out.append(l)

    text = "".join(out)
    for k, v in BG_MAP.items():
        text = text.replace(k, v)
    for k, v in CG_MAP.items():
        text = text.replace(k, v)

    # Split into act files on label boundaries.
    buckets = {"act2": [], "act3": [], "act4": [], "endings": []}
    current = None
    for l in text.splitlines(keepends=True):
        m = re.match(r"^label (\w+):", l)
        if m:
            name = m.group(1)
            current = ("act2" if name.startswith("act2_") else
                       "act3" if name.startswith("act3_") else
                       "act4" if name.startswith("act4_") else
                       "endings")
        if current:
            buckets[current].append(l)

    for key, chunk in buckets.items():
        path = os.path.join(OUTDIR, key + ".rpy")
        with open(path, "w", encoding="utf-8") as f:
            f.write(BLANK + HEADER[key] + BLANK)
            f.write("".join(chunk))
        print("wrote", path, "(%d labels)" % sum(1 for l in chunk if l.startswith("label ")))

    os.remove(SRC)
    print("removed", SRC)


if __name__ == "__main__":
    main()
