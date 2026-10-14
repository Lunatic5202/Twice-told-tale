# ASSETS.md — Twice-Told Tale

Asset manifest for artists and audio. The game currently ships with **labelled
placeholders** (see `game/images_placeholders.rpy` and the silent `.ogg` files in
`game/audio/`), so everything is playable and lint-clean before real art lands.

## Conventions

| Item | Spec |
|------|------|
| Base resolution | **1280 × 720** (16:9), virtual; art drawn at 2× for crispness |
| Backgrounds | **1920 × 1080** PNG or WebP, full-bleed (no letterboxing) |
| CGs | **1920 × 1080** PNG or WebP, full-bleed |
| Sprites | **~760 px tall** at 720p (≈1600–1900 px tall at 2×), transparent PNG |
| Sprite anchor | feet at the bottom edge; drawn to sit on the say-box line |
| Sprites | facing slightly toward centre; consistent light direction |
| Audio (music) | `.ogg` Vorbis, loopable, −16 LUFS integrated |
| Audio (SFX) | `.ogg` Vorbis, normalized to ~−6 dBFS peak |
| Fonts | see `game/gui/` (Ren'Py default DejaVu/OpenSans set) |

Replacing a placeholder: drop the matching file in place, then in
`game/images_placeholders.rpy` change the definition to a file path, e.g.

```renpy
image bg annex_night = "images/bg/annex_night.png"
image wanderer neutral = "images/sprites/wanderer_neutral.png"
image cg folio_page = "images/cg/folio_page.png"
```

Recommended folders: `game/images/bg/`, `game/images/sprites/`, `game/images/cg/`.

---

## Character sprites

Seven characters need sprite sets. Each expression is a separate transparent
image named `<tag>_<expression>.png`. Neutral/blank base pose first.

| Character | Tag | Expressions needed | Notes |
|-----------|-----|--------------------|-------|
| The Wanderer | `wanderer` | `neutral`, `guarded`, `smug`, `flustered`, `hurt`, `soft`, `tired` | Hat included except `soft` (hat off) |
| Scaramouche / The Echo | `echo` | `sneer`, `cold`, `amused`, `startled`, `grieving`, `shy`, `smile` | Red/purple jacket, veiled hat, mask on brim; `smile` = the rare real one |
| Nahida | `nahida` | `gentle`, `serious`, `mischievous`, `sad` | |
| Dottore | `dottore` | `pleasant`, `delighted`, `cold`, `fascinated` | White coat, blue-grey palette |
| Paimon | `paimon` | `cheerful`, `worried`, `excited` | |
| Tighnari | `tighnari` | `neutral`, `sly` | |
| Cyno | `cyno` | `neutral`, `grinning` | |

Placeholder image keys currently registered: `image (<tag>, "<expression>")`.

**Special cases**
- The Puppet and The Boy (Wanderer's past forms) have no sprite yet — either a
  dedicated sprite or handled entirely in CG. See Page-Walk acts.
- Escher (Dottore in disguise) can reuse the `dottore` sprite with a costume
  variant.

---

## Backgrounds

Canonical location plates, then per-scene lighting/staging variants. Source
script tags these `[BG: …]`. Reusable plates are the priority.

### Core plates (highest priority)

| Image key | Location | Description |
|-----------|----------|-------------|
| `bg annex_night` | Archive Annex | Long reading room, shelves like cliffs, one lamp, monsoon rain on high windows |
| `bg annex_predawn` | Archive Annex | Same room, grey light at the windows, predawn |
| `bg annex_dawn` | Archive Annex | Dawn, warm grey |
| `bg annex_day` | Archive Annex | Daylight, dust in shafts of light |
| `bg annex_evening` | Archive Annex | Evening, low lamp |
| `bg courtyard_day` | Akademiya Courtyard | Sunlit, students on benches, fountain, huge lotus leaves |
| `bg dining_evening` | Refectory / Dining Hall | Long table, candles, steam, evening through tall windows |
| `bg rooftop_night` | Akademiya Rooftop | Flat roof, huge Sumeru sky, warm wind, lanterns far below |

### Story locations (Act 2+)

| Location | Description |
|----------|-------------|
| The corridor of mist | Wet stone, gold ink glowing at the edges of the world, soundless rain; a quieter, snow-drifting variant |
| Shakkei Pavilion | Kannazuka, long ago |
| Tatarasuna / Mikage Furnace | Huge and red against dusk; workers with hammers; night variant hung with lanterns; morning variant |
| The tatami room | Paper screens, single futon, a sleeping puppet |
| The sick-ward | Rows of cots, grey-faced workers, wet cloths, fog of ash |
| Grand Narukami Shrine | Night; fox-eared woman on the steps |
| The tiny wooden house | Rim of a village, one lit window, snow on the roof |
| The Doctor's laboratory | Long white lab, humming glass tubes; darkened "glass cube" variant |
| The ruined/warped yard | Tinted dark red, edges warped like old glass |
| The white page | Pure white "page" space used across endings; variants for darkening edges, burning, black stage with one lit page |

> Full per-scene `[BG:]` descriptions (54 cues) are in the source script; use
> them for staging and character blocking within these plates.

---

## CG illustrations

Source script tags these `[CG: …]`. 27 cues; group by act. Suggested file name
in parentheses (matching placeholder keys where already wired).

### Prologue — Marginalia
- (cg folio_page) Close on the torn page: `"...and he reached out his hand, and
  the whole tree held its breath, and"` then a torn edge.
- (cg prologue_echo) A figure steps out of the ink: red/purple jacket, veiled
  hat, mask on the brim; eyes shut, then open.
- (cg first_page_burn) The first page burns; a ring of ash; cover counter turns
  30 → 29.
- (cg prologue_tea) The Wanderer in the doorway, cup halfway to his mouth.

### Act 1 — The Two of Them
- (cg nahida_between) Nahida between the two of them, hand raised like a teacher
  quieting a room.
- (cg wanderer_soup) The Wanderer at the end of the table, looking only at the
  soup.
- (cg margin_door) A door in the margin, edged in gold ink; mist and wet stone
  beyond.

### Page-Walk One — Tatarasuna
- (cg gold_feather) The gold feather turning in the Echo's fingers.
- The Daitatara Nagamasa on its stand; a young puppet and Katsuragi mid-dance,
  swords flashing; Niwa clapping; Nozomu sketching.
- The puppet walks into the furnace carrying the box, light pouring around him.
- The sleeping puppet, a tear on his cheek.
- Raiden Ei and Yae Miko standing over the sleeper.

### Page-Walk Two — The Boy
- (cg niwa_note) Niwa's note: `"Kid—if you're reading this, I didn't go. Hold the
  hammer like a bird. I'll be right back."`
- A child's drawing: house by the sea, two figures, a hat, a teapot, a large sun.
- The house at dawn; three of them in the snow.

### Act 2 — The Warm Table
- (cg hooked_pinkies) Two little fingers hooked; warm window light behind.
- (cg empty_bed) The empty bed; the drawing laid on the pillow; blanket folded.

### Act 3 — Clean Instruments / The Case
- (cg black_case) A plain black case, brass hasp, lid reads `"For the Archivist.
  Do open it."`
- (cg gnosis_violet) The Gnosis: pale violet lens, lit from within, velvet bed,
  hairline crack along the lower edge.
- (cg glass_cell) You in a glass cell, Folio under one arm; the Wanderer palms
  the wall; Cyno strains at a door; the Echo a violet bruise against the glass.
- (cg two_palms) Two hands — one real, one shadow — flat on the same pane; a
  bright electric seam between them.

### Act 4 — The Doctor's Hour
- (cg doctor_lane) The Doctor in his white coat at the end of the lane, a line of
  grey-masked figures behind, the cracked Gnosis in hand.
- The Echo's hand to the Wanderer's cheek, fading as it does; the Wanderer's hand
  closing over it.

### Endings
- (cg ending_wanderer) **Ending A:** the fading hand.
- (cg ending_scaramouche) **Ending B:** the hat passed over.
- (cg ending_true) **Ending C:** the three of them in the window light, cups in
  hand; gold title card `"The Passenger."`

### Motifs / cases (reused across endings)
- (cg margin_door_shut) Burnt halves of a book in rain; one sodden page reading
  `"stayed."`
- (cg blank_dot) An empty door; a hat on a step; a single pale violet feather.
- The Folio bound in black: three names inside, cover reads `"Case 0031: The
  Archivist."`

---

## Music

38 cues. Placeholder silent files live in `game/audio/music/`; replace in place
keeping the filename. Source script names each cue.

`a_name_is_a_small_thing`, `a_smaller_promise`, `clean_instruments`,
`double_trouble`, `escher`, `hat_guy`, `hat_guy_reprise`, `marginalia`,
`marginalia_dawn`, `mechanical_ears`, `page_walk`, `quiet`,
`reprise_clean_instruments`, `rumors`, `six_days`, `slumber`, `smoke`,
`sword_dance`, `tatarasuna`, `the_boy`, `the_doctor_s_hour`, `the_last_evening`,
`the_margin_door`, `the_old_dawn`, `the_table`, `the_thing_unsaid`,
`three_hundred_and_eleven`, `three_pages`, `warm_table`, `warm_table_reprise`,
`what_he_built_from_nothing`, `what_he_can_t_read`, `what_he_kept`,
`what_i_never_said`, `what_i_remember`, `what_was_written`,
`what_we_can_t_take_back`, `which_of_us`

**Motif notes**
- `marginalia` / `marginalia_dawn`: music box + ticking clock; dawn variant
  slower. Main theme.
- `hat_guy` / `hat_guy_reprise`: flute + stumbling drum. The Wanderer.
- `double_trouble`: pizzicato, a little too cheerful.
- `the_table` / `warm_table` (+ reprise): solo cello, warm and slow. Domesticity.
- `escher`, `mechanical_ears`, `the_doctor_s_hour`: the Doctor / trauma theme.
- `three_hundred_and_eleven`, `three_pages`, `six_days`: the countdown (pages/days).

---

## Sound effects

20 source cues; 5 placeholder files exist. Add new files as named keys in
`game/audio.rpy`.

Placeholders: `sfx_bell`, `sfx_chime`, `sfx_glass`, `sfx_page`, `sfx_pen`.

Additional cues needing sound: nib/pen scratching (slow, sure); teapot & poured
cup; footsteps on roof stairs; sliding screens + rain on roof + guttering
lantern; hammers, laughter, bellows; furnace roar; coughing; long roar into
silence; Folio closing; low thrum; glass rotating / hiss / door sealing; glass
shattering + thunderclap + violet-light roar; distant bells (midnight / first
light); choir; long exhale + a door closing far off.

---

## UI / other

- **Title screen art** — `game/gui/main_menu.png`, `game/gui/game_menu.png`
  (currently generated placeholders; replace with thematic versions).
- **Window title / logo** — "Twice-Told Tale".
- **Stat-toast icons** — optional small icons for the Wanderer / Echo / Mend
  meters (`game/screens_extra.rpy`, screen `stat_toast`).
- **Page counter** — the 30→1 ash counter motif; optional custom frame.

### Generated effect art (`tools/make_gui_assets.py`)

Purely decorative assets that make the interface feel intentional. All are
procedurally generated and safe to replace with hand-drawn versions; re-running
`python3 tools/make_gui_assets.py` regenerates them.

| File | Size | Used by |
| --- | --- | --- |
| `game/gui/cursor/pen_{0-3}.png`, `pen_hover_{0-3}.png` | 32×32 | animated nib mouse cursor (`gui_effects.rpy`) |
| `game/gui/overlay/ctc_drop.png` | 40×40 | blinking click-to-continue marker (screen `ctc`) |
| `game/gui/mask/ink_dissolve.png` | 512×512 | `ink_dissolve` / `page_wipe` transitions |
| `game/gui/overlay/vignette.png` | 1280×720 | in-game atmosphere overlay |
| `game/gui/overlay/grain.png` | 256×256 (tiled) | drifting film grain |
| `game/gui/overlay/ink_blot.png` | 1024×1024 | main-menu / splash ink bloom |

Behaviour for all of the above lives in `game/gui_effects.rpy` (transitions,
cursor, CTC, splash/loading screen, atmosphere overlay, menu-motion transforms).

