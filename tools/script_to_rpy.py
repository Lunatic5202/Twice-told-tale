#!/usr/bin/env python3
"""
script_to_rpy.py — semi-automated converter for Twice-Told Tale.

Turns the extracted screenplay text (NAME: line style, with [BG]/[CG]/[MUSIC]/
[SFX] cues and "CHOICE ·" blocks) into a *draft* Ren'Py .rpy scene file.

It is deliberately semi-automated: it gets the structure right (labels, cues,
menus, branches, effects, ending routes) so a human can polish the prose. Every
guess it is unsure about is emitted as a `# TODO(parser): ...` comment rather
than silently dropped, and unmapped backgrounds/CGs/sounds fall back to generic
placeholder images so the draft still lints.

Usage:
    python3 tools/script_to_rpy.py SCRIPT.txt -o game/scenes/act2plus_draft.rpy
    python3 tools/script_to_rpy.py SCRIPT.txt -o out.rpy --from-scene 2.1
    python3 tools/script_to_rpy.py SCRIPT.txt -o out.rpy --report

Run `--report` alone to print the cue inventory without writing a script.
"""

from __future__ import annotations

import argparse
import re
import sys

# --------------------------------------------------------------------------
# Speaker tags -> Ren'Py character variables
# --------------------------------------------------------------------------

SPEAKERS = {
    "NARRATION": "n",
    "MC": "mc",
    "SCARAMOUCHE": "echo",
    "WANDERER": "wanderer",
    "NAHIDA": "nahida",
    "DOTTORE": "dottore",
    "PAIMON": "paimon",
    "MARGIN NOTE": "margin",
    "NEW LINE": "newline_char",
    "NOTE": "note",
    "TIGHNARI": "tighnari",
    "CYNO": "cyno",
    "YAE MIKO": "miko",
    "EI": "ei",
    "ESCHER": "escher",
    "THE PUPPET": "puppet",
    "PUPPET": "puppet",
    "THE BOY": "boy",
    "BOY": "boy",
    "NIWA": "niwa",
    "KATSURAGI": "katsuragi",
    "WORKER": "worker",
    "WORKER 2": "worker2",
    "STUDENT": "student",
}

# Labels already hand-written in the vertical slice; excluded by default.
EXCLUDE_LABELS = {
    "prologue_0_1",
    "prologue_0_2",
    "act1_1_1",
    "act1_1_2",
    "act1_1_3",
    "act1_1_4",
    "act1_1_5",
    "act1_1_6",
    "act1_1_7",
    "act1_montage",
}

ENDING_LABELS = {
    "A": "ending_wanderer",
    "B": "ending_scaramouche",
    "C": "ending_true",
    "F": "ending_gnosis_box",
    "G": "ending_burned_pages",
    "H": "ending_blank_page",
}

BAD_ENDING_LABELS = {
    "1": "ending_archivist",
    "2": "ending_burn_it_down",
    "3": "ending_quiet_page",
}

ROUTE_LABELS = {
    "THE WANDERER ENDING": "ending_wanderer",
    "THE SCARAMOUCHE ENDING": "ending_scaramouche",
    "THE TRUE ENDING": "ending_true",
    "THE GNOSIS BOX": "ending_gnosis_box",
    "BURNED PAGES": "ending_burned_pages",
    "BLANK PAGE": "ending_blank_page",
    "THE ARCHIVIST": "ending_archivist",
    "BURN IT DOWN": "ending_burn_it_down",
    "NEUTRAL ENDING": "ending_neutral",
}

# --------------------------------------------------------------------------
# Cue -> asset key heuristic maps
# --------------------------------------------------------------------------

MUSIC_RE = re.compile(r"[\u201c\"]([^\u201d\"]+)[\u201d\"]")

BG_KEYWORDS = [
    ("courtyard", "courtyard_day"),
    ("rooftop", "rooftop_night"),
    ("roof", "rooftop_night"),
    ("refectory", "dining_evening"),
    ("dining", "dining_evening"),
    ("archive annex", "annex"),
    ("annex", "annex"),
    ("archive", "annex"),
]

CG_KEYWORDS = [
    ("steps out of the ink", "prologue_echo"),
    ("reached out his hand", "folio_page"),
    ("first page burns", "first_page_burn"),
    ("teacher quieting", "nahida_between"),
    ("between the two of them", "nahida_between"),
    ("at the soup", "wanderer_soup"),
    ("door in the margin", "margin_door"),
    ("gold feather", "gold_feather"),
    ("niwa", "niwa_note"),
    ("fingers hooked", "hooked_pinkies"),
    ("empty bed", "empty_bed"),
    ("black case", "black_case"),
    ("glass cell", "glass_cell"),
    ("same pane", "two_palms"),
    ("end of the lane", "doctor_lane"),
    ("cheek", "ending_wanderer"),
    ("very young", "ending_scaramouche"),
    ("window light", "ending_true"),
    ("gnosis", "gnosis_violet"),
    ("burnt halves", "margin_door_shut"),
    ("feather on the stone", "blank_dot"),
]

SFX_KEYWORDS = [
    ("bell", "sfx_bell"),
    ("chime", "sfx_chime"),
    ("glass", "sfx_glass"),
    ("page", "sfx_page"),
    ("pen", "sfx_pen"),
    ("nib", "sfx_pen"),
]

TIME_WORDS = [
    ("before dawn", "annex_predawn"),
    ("predawn", "annex_predawn"),
    ("midnight", "annex_night"),
    ("night", "annex_night"),
    ("dawn", "annex_dawn"),
    ("morning", "annex_day"),
    ("noon", "annex_day"),
    ("day", "annex_day"),
    ("afternoon", "annex_day"),
    ("evening", "annex_evening"),
]


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = text.replace("\u2019", "_").replace("'", "_")
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")


def esc(text: str) -> str:
    """Escape a line for a double-quoted Ren'Py string."""
    text = text.replace("\\", "\\\\")
    text = text.replace('"', '\\"')
    text = text.replace("[", "[[").replace("{", "{{")
    text = text.replace("%", "%%")
    return text


# --------------------------------------------------------------------------
# Line / unit tokenizer
# --------------------------------------------------------------------------

PAGE_ARTIFACT = re.compile(r"^\s*(Page \d+ of \d+|Twice-Told Tale:.*)\s*$")
SCENE_RE = re.compile(r"^\s*(?:DAY\s+(\d+)\s*\u00b7\s*)?SCENE\s+([0-9]+\.[0-9]+)\s*\u00b7\s*(.+?)\s*$")
MONTAGE_RE = re.compile(r"^\s*DAY\s+(\d+)\s*\u00b7\s*MONTAGE\s*\u00b7\s*(.+?)\s*$")
ENDING_RE = re.compile(r"^\s*ENDING\s+([A-H])\s*\u00b7\s*(.+?)\s*$")
BAD_ENDING_RE = re.compile(r"^\s*BAD ENDING\s+(\d+)\s*\u00b7\s*(.+?)\s*$")
NEUTRAL_RE = re.compile(r"^\s*NEUTRAL ENDING\s*\u00b7\s*(.+?)\s*$")
EPILOGUE_RE = re.compile(r"^\s*EPILOGUE\s*\u00b7\s*(.+?)\s*$")
SHARED_RE = re.compile(r"^\s*SHARED BEAT\s*\u00b7\s*(.+?)\s*$")
CHOICE_RE = re.compile(r"^\s*CHOICE\s*\u00b7\s*(.*)$")
OPTION_RE = re.compile(r"^\s*([A-H])\.\s*(.*)$")
BRANCH_RE = re.compile(r"^\s*If\s+([A-H])\s*:\s*(.*)$")
CUES = ("BG", "CG", "MUSIC", "SFX")
SPEAKER_RE = re.compile(r"^\s*([A-Z][A-Z0-9 .'\u2019]+?):\s*(.*)$")


def is_header(line: str):
    for label, rx in (
        ("scene", SCENE_RE),
        ("montage", MONTAGE_RE),
        ("ending", ENDING_RE),
        ("bad_ending", BAD_ENDING_RE),
        ("neutral", NEUTRAL_RE),
        ("epilogue", EPILOGUE_RE),
        ("shared", SHARED_RE),
    ):
        m = rx.match(line)
        if m:
            return label, m
    return None, None


def starts_unit(line: str) -> bool:
    if is_header(line)[0]:
        return True
    if line.lstrip().startswith("["):
        return True
    if CHOICE_RE.match(line):
        return True
    if OPTION_RE.match(line):
        return True
    if BRANCH_RE.match(line):
        return True
    if line.lstrip().startswith("THE LAST CHOICE"):
        return True
    m = SPEAKER_RE.match(line)
    if m and m.group(1).strip().upper() in SPEAKERS:
        return True
    return False


def tokenize(text: str):
    """Return a list of units: (header_kind_or_None, [lines])."""
    units = []
    current = None
    for raw in text.splitlines():
        if PAGE_ARTIFACT.match(raw):
            continue
        if not raw.strip():
            if current:
                units.append(current)
                current = None
            continue
        if current is None:
            current = (is_header(raw)[0], [raw])
        elif starts_unit(raw):
            units.append(current)
            current = (is_header(raw)[0], [raw])
        else:
            current[1].append(raw)
    if current:
        units.append(current)
    return units


# --------------------------------------------------------------------------
# Asset resolution
# --------------------------------------------------------------------------

def bg_image(cue_text: str, scene_location: str = "") -> str:
    low = (cue_text + " " + scene_location).lower()
    for kw, img in BG_KEYWORDS:
        if kw in low:
            if img == "annex":
                for tw, name in TIME_WORDS:
                    if tw in low:
                        return name
                return "annex_day"
            return img
    return "todo"


def cg_image(cue_text: str) -> str:
    low = cue_text.lower()
    for kw, img in CG_KEYWORDS:
        if kw in low:
            return img
    return "todo"


def sfx_key(cue_text: str):
    low = cue_text.lower()
    for kw, name in SFX_KEYWORDS:
        if kw in low:
            return name
    return None


def music_key(cue_text: str):
    m = MUSIC_RE.search(cue_text)
    if m:
        return slugify(m.group(1))
    return None


def auto_key(text: str, prefix: str) -> str:
    """Deterministic placeholder image attribute for an unmapped cue."""
    words = re.findall(r"[A-Za-z0-9]+", text.lower())[:5]
    key = prefix + "_" + "_".join(words)
    return key[:48].strip("_")


def _color_for(seed: str) -> str:
    """Stable muted color so each distinct auto placeholder looks different."""
    h = 0
    for ch in seed:
        h = (h * 131 + ord(ch)) & 0xFFFFFF
    r = 0x30 + (h & 0x5F)
    g = 0x30 + ((h >> 8) & 0x5F)
    b = 0x30 + ((h >> 16) & 0x5F)
    return "#%02x%02x%02x" % (r, g, b)


def _short(desc: str, limit: int = 70) -> str:
    desc = re.sub(r"\s+", " ", desc).strip()
    if len(desc) > limit:
        desc = desc[: limit - 1].rstrip() + "\u2026"
    return desc


# --------------------------------------------------------------------------
# Effect / condition parsing
# --------------------------------------------------------------------------

STAT_TOKENS = {"W": "w", "B": "b", "M": "m", "PEN": "pen"}


def parse_effects(effect_text: str):
    """Return (stat_bumps, flag_sets, availability_python_or_None)."""
    bumps = []
    flags = []
    avail = None

    # "Available if ..." -> python condition
    am = re.search(r"Available if\s+(.+?)(?:\.|Route:|$)", effect_text, re.I)
    if am:
        cond = am.group(1).strip()
        avail = to_python_cond(cond)

    # Stat deltas like "M \u22121", "W +1", "PEN +1", "B +1"
    for m in re.finditer(r"\b(W|B|M|PEN)\s*([\u2212+\-])\s*(\d+)", effect_text):
        token, sign, num = m.group(1), m.group(2), int(m.group(3))
        amount = num if sign == "+" else -num
        bumps.append((STAT_TOKENS[token], amount))

    # "sets FIXER", "Sets PROMISE_BROKEN."
    for m in re.finditer(r"[Ss]ets\s+([A-Z_]+)", effect_text):
        flags.append(m.group(1).lower())

    return bumps, flags, avail


def to_python_cond(cond: str) -> str:
    c = cond
    c = c.replace("\u2265", ">=").replace("\u2264", "<=")
    c = re.sub(r"\bis set\b", "", c, flags=re.I)
    for token, var in STAT_TOKENS.items():
        c = re.sub(r"\b%s\b" % token, var, c)
    c = re.sub(r"\b(PROMISE_MADE|PROMISE_BROKEN|FIXER|BOX)\b",
               lambda m: m.group(1).lower(), c)
    c = re.sub(r"\s*,\s*and\s+", " and ", c)
    c = re.sub(r"\s*,\s*", " and ", c)
    c = re.sub(r"\band\s+and\b", "and", c)
    c = re.sub(r"\s+", " ", c).strip()
    return c


# --------------------------------------------------------------------------
# Renderer
# --------------------------------------------------------------------------

class Renderer:
    def __init__(self, report: bool, scene_transition=None):
        self.out = []
        self.report = report
        self.scene_transition = scene_transition
        self.menu_counter = 0
        self.unmapped_bg = set()
        self.unmapped_cg = set()
        self.unmapped_sfx = set()
        self.unmapped_music = set()
        self.warnings = []
        self.auto_images = {}  # (tag, attr) -> descriptive label

    def emit(self, indent, text=""):
        self.out.append(("    " * indent + text) if text else "")

    def warn(self, msg):
        self.warnings.append(msg)

    # -- cues --------------------------------------------------------------
    def cue(self, kind, text, scene_location="", indent=1):
        text = text.strip()
        if kind == "BG":
            img = bg_image(text, scene_location)
            if img == "todo":
                self.unmapped_bg.add(text)
                img = auto_key(text, "x_bg")
                self.auto_images[("bg", img)] = text
            self.emit(indent, "scene bg %s  # TODO(parser): %s" % (img, self._comment(text)))
            if self.scene_transition:
                self.emit(indent, "with %s" % self.scene_transition)
        elif kind == "CG":
            img = cg_image(text)
            if img == "todo":
                self.unmapped_cg.add(text)
                img = auto_key(text, "x_cg")
                self.auto_images[("cg", img)] = text
            self.emit(indent, "scene cg %s  # TODO(parser): %s" % (img, self._comment(text)))
            if self.scene_transition:
                self.emit(indent, "with %s" % self.scene_transition)
        elif kind == "MUSIC":
            music = music_key(text)
            if music:
                self.emit(indent, "play music audio.%s fadein 2.0  # %s" % (music, self._comment(text)))
            else:
                self.unmapped_music.add(text)
                self.emit(indent, "# TODO(parser music): %s" % self._comment(text))
        elif kind == "SFX":
            key = sfx_key(text)
            if key:
                self.emit(indent, "play sound audio.%s  # %s" % (key, self._comment(text)))
            else:
                self.unmapped_sfx.add(text)
                self.emit(indent, "# TODO(parser sfx): %s" % self._comment(text))

    @staticmethod
    def _comment(text):
        text = re.sub(r"\s+", " ", text)
        return text[:160]

    # -- dialogue ----------------------------------------------------------
    def dialogue(self, speaker, line, indent=1):
        tag = SPEAKERS[speaker]
        self.emit(indent, '%s "%s"' % (tag, esc(re.sub(r"\s+", " ", line).strip())))

    def narration(self, line, indent=1):
        self.emit(indent, 'n "%s"' % esc(re.sub(r"\s+", " ", line).strip()))

    def comment(self, text, indent=1):
        for part in re.sub(r"\s+", " ", text).split("\n"):
            self.emit(indent, "# " + part)

    def finish_label(self, label):
        """Endings and the shared beat must not fall through into one another."""
        if label and label.startswith("ending_"):
            self.emit(1, "")
            self.emit(1, "return")


# --------------------------------------------------------------------------
# Driver
# --------------------------------------------------------------------------

def render(text: str, exclude, report=False, scene_transition=None):
    # Trim front matter: start at "Prologue: Marginalia".
    idx = text.find("Prologue: Marginalia")
    if idx != -1:
        text = text[idx:]
    # Trim the production appendix that follows the script proper.
    for stopper in ("\n  Production Notes", "\n  Production notes"):
        cut = text.find(stopper)
        if cut != -1:
            text = text[:cut]
            break
    units = tokenize(text)
    r = Renderer(report, scene_transition)

    current_label = None
    scene_location = ""
    pending_menu = None  # dict with options, prompt

    def close_menu():
        nonlocal pending_menu
        pending_menu = None

    def flush():
        pass

    i = 0
    while i < len(units):
        kind, lines = units[i]
        raw = "\n".join(lines)
        joined = re.sub(r"\s+", " ", raw).strip()

        # ---- headers / labels ----
        if kind:
            r.finish_label(current_label)
            _, m = is_header(lines[0])
            if kind == "scene":
                day = m.group(1)
                number = m.group(2)
                desc = re.sub(r"\s+", " ", m.group(3))
                major, minor = number.split(".")
                label = ("prologue_0_%s" % minor) if major == "0" else "act%s_%s_%s" % (major, major, minor)
                scene_location = desc
                pages = re.search(r"\((\d+)\s+pages? left\)", desc)
                title = re.sub(r"\s*\(\d+\s+pages? left\)", "", desc)
                if label in exclude:
                    current_label = None
                else:
                    current_label = label
                    r.emit(0, "")
                    r.emit(0, "label %s:" % label)
                    daypart = "DAY %s \u00b7 " % day if day else ""
                    r.emit(1, "# %sSCENE %s \u00b7 %s" % (daypart, number, title))
                    if pages:
                        r.emit(1, "$ set_page(%s%s)" % (pages.group(1),
                               (", %s" % day) if day else ""))
                    r.emit(1, '$ show_title("%sSCENE %s\\n%s")' % (daypart, number, title))
            elif kind == "montage":
                day = m.group(1)
                title = re.sub(r"\s+", " ", m.group(2))
                label = "act1_montage" if not current_label else "montage_%s" % slugify(title)
                if label in exclude:
                    current_label = None
                else:
                    current_label = label
                    r.emit(0, "")
                    r.emit(0, "label %s:" % label)
                    r.emit(1, "# DAY %s \u00b7 MONTAGE \u00b7 %s" % (day, title))
                    r.emit(1, '$ show_title("DAY %s \\u00b7 MONTAGE\\n%s")' % (day, title))
            elif kind == "ending":
                label = ENDING_LABELS.get(m.group(1), "ending_%s" % m.group(1).lower())
                current_label = label
                r.emit(0, "")
                r.emit(0, "label %s:" % label)
                r.emit(1, "# ENDING %s \u00b7 %s" % (m.group(1), re.sub(r"\s+", " ", m.group(2))))
            elif kind == "bad_ending":
                label = BAD_ENDING_LABELS.get(m.group(1), "ending_bad_%s" % m.group(1))
                current_label = label
                r.emit(0, "")
                r.emit(0, "label %s:" % label)
                r.emit(1, "# BAD ENDING %s \u00b7 %s" % (m.group(1), re.sub(r"\s+", " ", m.group(2))))
            elif kind == "neutral":
                current_label = "ending_neutral"
                r.emit(0, "")
                r.emit(0, "label ending_neutral:")
                r.emit(1, "# NEUTRAL ENDING \u00b7 %s" % re.sub(r"\s+", " ", m.group(1)))
            elif kind == "epilogue":
                current_label = "ending_epilogue"
                r.emit(0, "")
                r.emit(0, "label ending_epilogue:")
                r.emit(1, "# EPILOGUE \u00b7 %s" % re.sub(r"\s+", " ", m.group(1)))
            elif kind == "shared":
                current_label = "ending_shared_beat"
                r.emit(0, "")
                r.emit(0, "label ending_shared_beat:")
                r.emit(1, "# SHARED BEAT \u00b7 %s" % re.sub(r"\s+", " ", m.group(1)))
            i += 1
            continue

        if current_label is None:
            i += 1
            continue

        # ---- cues ----
        if joined.startswith("["):
            inner = joined.strip("[]")
            cm = re.match(r"^(%s):\s*(.*)$" % "|".join(CUES), inner)
            if cm:
                r.cue(cm.group(1), cm.group(2), scene_location)
            else:
                r.comment(inner)
            i += 1
            continue

        # ---- choice header ----
        cm = CHOICE_RE.match(lines[0])
        if cm:
            prompt = re.sub(r"\s+", " ", cm.group(1)).strip()
            r.menu_counter += 1
            opts = []
            j = i + 1
            while j < len(units):
                om = OPTION_RE.match(units[j][1][0])
                if not om:
                    break
                opt_text = re.sub(r"\s+", " ", "\n".join(units[j][1])).strip()
                opts.append((om.group(1), opt_text))
                j += 1
            prompt_clean = re.sub(r"\s*\([^)]*\)\s*", " ", prompt).strip()
            r.emit(1, "")
            r.emit(1, "# CHOICE: %s" % r._comment(prompt))
            had_route, sel = _emit_menu(r, opts)
            # branches follow?
            k = j
            branches = {}
            order = []
            while k < len(units):
                bk, blines = units[k]
                if bk:  # next header ends the branch region
                    break
                bm = BRANCH_RE.match(blines[0])
                if bm:
                    letter = bm.group(1)
                    if letter not in branches:
                        branches[letter] = []
                        order.append(letter)
                    if bm.group(2).strip():
                        branches[letter].append(("dialogue_raw", bm.group(2).strip()))
                    k += 1
                    continue
                if branches:
                    # body content of the most recent branch
                    branches[order[-1]].append((bk, "\n".join(blines)))
                    k += 1
                    continue
                break
            # emit branches
            first = True
            for letter in order:
                kw = "if" if first else "elif"
                r.emit(1, "%s %s == %r:" % (kw, sel, letter))
                body = branches[letter]
                mark = len(r.out)
                for bkind, blines in body:
                    _render_element(r, bkind, blines, scene_location)
                if not any(l.strip() and not l.lstrip().startswith("#")
                           for l in r.out[mark:]):
                    r.emit(2, "pass")
                first = False
            i = k
            continue

        # ---- standalone option run (e.g. Scene 4.4's THE LAST CHOICE) ----
        if OPTION_RE.match(lines[0]):
            opts = []
            j = i
            while j < len(units):
                m2 = OPTION_RE.match(units[j][1][0])
                if not m2:
                    break
                opts.append((m2.group(1),
                             re.sub(r"\s+", " ", "\n".join(units[j][1])).strip()))
                j += 1
            r.menu_counter += 1
            r.emit(1, "")
            had_route, sel = _emit_menu(r, opts)
            # 4.4 has no "If X:" branches; any following prose stays as-is.
            i = j
            continue

        # ---- branch marker outside a menu (fallback) ----
        bm = BRANCH_RE.match(lines[0])
        if bm:
            r.emit(1, "# TODO(parser): stray branch 'If %s'" % bm.group(1))
            if bm.group(2).strip():
                r.emit(1, 'n "%s"' % esc(bm.group(2).strip()))
            i += 1
            continue

        # ---- dialogue ----
        sm = SPEAKER_RE.match(lines[0])
        if sm and sm.group(1).strip().upper() in SPEAKERS:
            speaker = sm.group(1).strip().upper()
            r.dialogue(speaker, joined[len(sm.group(1)) + 1:])
            i += 1
            continue

        # ---- free text ----
        if re.match(r"MC \(name entry\)", joined, re.I):
            r.emit(1, "")
            r.emit(1, "python:")
            r.emit(2, '_entered = renpy.input("{i}What is your name?{/i}",')
            r.emit(3, 'default="", length=24, exclude="{}[]").strip()')
            r.emit(2, "if _entered:")
            r.emit(3, "mc_name = _entered")
        elif joined.upper().startswith("THE LAST CHOICE"):
            r.comment(joined)
        elif re.match(r"^(ACT\s+\d+|SHARED BEAT|The Endings|Requires:|Route:)", joined):
            r.comment(joined)
        else:
            r.narration(joined)
        i += 1

    r.finish_label(current_label)
    return r


def _emit_menu(r, opts):
    """Emit a Ren'Py `menu:` for (letter, opt_text) pairs.

    Returns (had_route, sel) where sel is the per-menu branch selector variable.
    """
    r.emit(1, "menu:")
    sel = "_sel_%d" % r.menu_counter
    had_route = False
    for letter, opt_text in opts:
        letter2, body = OPTION_RE.match(opt_text).groups()
        body = re.sub(r"\s+", " ", body).strip()
        display = re.sub(r"\s*\([^)]*\)\s*$", "", body)
        display = re.sub(r"\s*Available if.*$", "", display, flags=re.I)
        display = re.sub(r"\s*Route:.*$", "", display, flags=re.I).strip()
        route_m = re.search(r"Route:\s*([^.\n]+)", body, re.I)
        bumps, flags, avail = parse_effects(body)
        r.emit(2, '"%s"%s:' % (esc(display), (" if (%s)" % avail) if avail else ""))
        stmts = 0
        r.emit(3, '$ %s = "%s"' % (sel, letter2))
        stmts += 1
        for stat, amount in bumps:
            r.emit(3, "$ bump(%r, %d)" % (stat, amount))
            stmts += 1
        for flag in flags:
            r.emit(3, "$ %s = True" % flag)
            stmts += 1
        if route_m:
            had_route = True
            route = route_m.group(1).strip().upper()
            target = None
            for key, lab in ROUTE_LABELS.items():
                if key in route:
                    target = lab
                    break
            if target:
                r.emit(3, "jump %s" % target)
                stmts += 1
            else:
                r.emit(3, "# TODO(parser): route %r" % route)
        if stmts == 0:
            r.emit(3, "pass")
    r.emit(1, "")
    if had_route:
        r.emit(1, "# every option routes explicitly; nothing falls through")
    return had_route, sel


def _render_element(r, kind, lines, scene_location, indent=2):
    raw = lines if isinstance(lines, str) else "\n".join(lines)
    joined = re.sub(r"\s+", " ", raw).strip()
    if joined.startswith("["):
        inner = joined.strip("[]")
        cm = re.match(r"^(%s):\s*(.*)$" % "|".join(CUES), inner)
        if cm:
            r.cue(cm.group(1), cm.group(2), scene_location, indent=indent)
        else:
            r.comment(inner, indent=indent)
        return
    sm = SPEAKER_RE.match(joined)
    if sm and sm.group(1).strip().upper() in SPEAKERS:
        r.dialogue(sm.group(1).strip().upper(), joined[len(sm.group(1)) + 1:], indent=indent)
        return
    r.narration(joined, indent=indent)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("script", help="extracted script text")
    ap.add_argument("-o", "--output", help="output .rpy path")
    ap.add_argument("--from-scene", help="only emit scenes at/after this scene number (e.g. 2.1)")
    ap.add_argument("--no-exclude", action="store_true",
                    help="do not exclude already-written slice labels")
    ap.add_argument("--report", action="store_true", help="print cue inventory")
    ap.add_argument("--scene-transition", default=None,
                    help="emit `with <name>` after each scene change (e.g. ink_dissolve)")
    args = ap.parse_args()

    text = open(args.script, encoding="utf-8").read()
    exclude = set() if args.no_exclude else EXCLUDE_LABELS

    # --from-scene: exclude every label that sorts before it.
    if args.from_scene:
        cut = tuple(int(x) for x in args.from_scene.split("."))
        for lab in list(EXCLUDE_LABELS):
            m = re.match(r"act(\d+)_(\d+)_(\d+)", lab)
            if m:
                if (int(m.group(2)), int(m.group(3))) < cut:
                    exclude.add(lab)

    r = render(text, exclude, report=args.report,
               scene_transition=args.scene_transition)

    if args.report:
        print("== Unmapped BG ==")
        for s in sorted(r.unmapped_bg):
            print("  -", s)
        print("== Unmapped CG ==")
        for s in sorted(r.unmapped_cg):
            print("  -", s)
        print("== Unmapped MUSIC ==")
        for s in sorted(r.unmapped_music):
            print("  -", s)
        print("== Unmapped SFX ==")
        for s in sorted(r.unmapped_sfx):
            print("  -", s)
        if not args.output:
            return

    if args.output:
        header = (
            "################################################################################\n"
            "## Twice-Told Tale - DRAFT (auto-generated by tools/script_to_rpy.py)\n"
            "##\n"
            "## This file is a machine-assisted first pass. Polish the prose, resolve\n"
            "## every `# TODO(parser):` marker, and fold the result into the hand-edited\n"
            "## act files. Do not treat it as final copy.\n"
            "################################################################################\n"
        )
        lines = [header]
        if r.auto_images:
            lines.append("init 10 python:\n")
            for (tag, attr), desc in sorted(r.auto_images.items()):
                c = _color_for(attr)
                if tag == "bg":
                    lines.append("    renpy.image((%r, %r), bg_placeholder(%r, %r))\n"
                                 % (tag, attr, _short(desc), c))
                else:
                    lines.append("    renpy.image((%r, %r), cg_placeholder(%r))\n"
                                 % (tag, attr, _short(desc)))
            lines.append("\n")
        lines.append("\n".join(r.out))
        lines.append("\n")
        with open(args.output, "w", encoding="utf-8") as f:
            f.write("".join(lines))
        sys.stderr.write("wrote %s (%d lines, %d auto images)\n"
                         % (args.output, len(r.out), len(r.auto_images)))


if __name__ == "__main__":
    main()
