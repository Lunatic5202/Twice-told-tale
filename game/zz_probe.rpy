init python:

    import hashlib

    def _trace(msg):
        with open("/tmp/opencode/probe_trace.txt", "a") as f:
            f.write(str(msg) + "\n")

    def _hash_surf(surf):
        try:
            w, h = surf.get_size()
            acc = []
            for i in range(16):
                for j in range(9):
                    acc.append(tuple(surf.get_at((w * i // 15, h * j // 8))))
            return hashlib.md5(repr(acc).encode("utf-8")).hexdigest()
        except Exception:
            return "nohash"

    _last_hash = [""]

    def _shot(name, tries=12):
        import os
        d = "/tmp/opencode/shots"
        if not os.path.isdir(d):
            os.makedirs(d)
        for i in range(tries):
            try:
                surf = renpy.display.draw.screenshot(renpy.game.interface.surftree)
            except Exception:
                import traceback
                _trace("SHOT-ERR\n" + traceback.format_exc())
                return False
            h = _hash_surf(surf)
            if h != _last_hash[0]:
                _last_hash[0] = h
                renpy.display.scale.image_save_unscaled(surf, os.path.join(d, name + ".png"))
                _trace("saved %s (fresh, try %d)" % (name, i))
                return True
            _pause_safe(0.25)
        _trace("STALE %s - frame never changed" % name)
        return False

    def _pause_safe(d):
        try:
            renpy.pause(d)
        except Exception:
            import traceback
            _trace("PAUSE-ERR\n" + traceback.format_exc())

    def _preload(paths):
        try:
            for p in paths:
                renpy.loadable(p)
            _trace("preloaded %d" % len(paths))
        except Exception:
            import traceback
            _trace("PRELOAD-ERR\n" + traceback.format_exc())

    def _geom(layer, tag):
        """Return (x0, x1, y0, y1) of the drawn content for a shown image."""
        from renpy.game import context
        try:
            entries = context().scene_lists.layers.get(layer, [])
            for e in entries:
                if e.tag == tag:
                    d = e.displayable
                    r = d.render(1280, 720, 0.0, 0.0)
                    return "%s render %sx%s" % (repr(d)[:60], r.width, r.height)
            return "tag %s not found in %s" % (tag, layer)
        except Exception:
            import traceback
            return "ERR " + traceback.format_exc()

image probe_black = Solid("#ff00ff")

label probe_all:
    $ _preload(["images/bg/courtyard_day.png", "images/bg/annex_dawn.png",
    "images/cg/nahida_between.png", "images/cg/ending_true.png",
    "images/sprites/echo_amused.png", "images/sprites/wanderer_guarded.png",
    "images/sprites/tighnari_neutral.png", "images/sprites/cyno_neutral.png"])
    scene probe_black with None
    $ _pause_safe(0.5)
    $ _shot("empty")

    show echo amused at at_left
    $ _pause_safe(0.9)
    $ _shot("echo")
    $ _trace("echo: " + _geom("master", "echo"))

    hide echo
    show wanderer guarded at at_far_right
    $ _pause_safe(0.9)
    $ _shot("wanderer")
    $ _trace("wanderer far_right: " + _geom("master", "wanderer"))

    hide wanderer
    show wanderer guarded at at_center
    $ _pause_safe(0.9)
    $ _shot("wanderer_center")
    $ _trace("wanderer center: " + _geom("master", "wanderer"))

    hide wanderer
    show tighnari neutral at at_center
    $ _pause_safe(0.9)
    $ _shot("tighnari")

    hide tighnari
    show cyno neutral at at_right
    $ _pause_safe(0.9)
    $ _shot("cyno")

    hide cyno
    show echo amused at at_left
    show wanderer guarded at at_far_right
    show tighnari neutral at at_center
    show cyno neutral at at_right
    $ _pause_safe(0.9)
    $ _shot("four")

    scene cg nahida_between with None
    $ _pause_safe(1.2)
    $ _shot("cg_nahida")

    scene bg courtyard_day with None
    $ _pause_safe(1.2)
    $ _shot("bg_courtyard")

    scene bg annex_dawn with None
    $ _pause_safe(1.2)
    $ _shot("bg_annex")

    $ renpy.quit()

testcase probe:
    $ _test.transition_timeout = 0.05
    $ _test.timeout = 120.0
    run Jump("probe_all")
    pause 30
    exit
