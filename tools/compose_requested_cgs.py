#!/usr/bin/env python3
"""Compose the eight ending CG plates from bundled artwork and sprites."""
import os

from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import numpy as np


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CG_DIR = os.path.join(ROOT, "game", "images", "cg")
BG_DIR = os.path.join(ROOT, "game", "images", "bg")
SPRITE_DIR = os.path.join(ROOT, "game", "images", "sprites")
SIZE = (1920, 1080)


def image(path):
    return Image.open(path).convert("RGBA")


def fit(path):
    return image(path).resize(SIZE, Image.Resampling.LANCZOS)


def bg(name):
    return fit(os.path.join(BG_DIR, name + ".png"))


def cg(name):
    return fit(os.path.join(CG_DIR, name + ".png"))


def sprite(name):
    return image(os.path.join(SPRITE_DIR, name + ".png"))


def vignette(img, strength=105):
    yy, xx = np.mgrid[0:SIZE[1], 0:SIZE[0]]
    cx, cy = SIZE[0] / 2, SIZE[1] / 2
    max_d = (cx * cx + cy * cy) ** 0.5
    distance = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / max_d
    alpha = np.clip((distance - 0.48) / 0.42, 0.0, 1.0) ** 1.7 * strength
    mask = Image.fromarray(alpha.astype(np.uint8), mode="L")
    overlay = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    overlay.putalpha(mask.filter(ImageFilter.GaussianBlur(45)))
    return Image.alpha_composite(img.convert("RGBA"), overlay)


def tint(img, color, opacity):
    layer = Image.new("RGBA", SIZE, color + (opacity,))
    return Image.alpha_composite(img.convert("RGBA"), layer)


def glow(img, xy, radius, color, opacity):
    layer = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    x, y = xy
    draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=color + (opacity,))
    layer = layer.filter(ImageFilter.GaussianBlur(radius * 0.65))
    return Image.alpha_composite(img.convert("RGBA"), layer)


def place_sprite(canvas, tag, expression, box, opacity=255):
    character = sprite("%s_%s" % (tag, expression))
    character.thumbnail(box, Image.Resampling.LANCZOS)
    if opacity != 255:
        alpha = character.getchannel("A").point(lambda value: value * opacity // 255)
        character.putalpha(alpha)
    x = (SIZE[0] - character.width) // 2
    y = SIZE[1] - character.height
    canvas.alpha_composite(character, (x, y))
    return canvas


def place_sprite_at(canvas, tag, expression, center_x, bottom_y, box, opacity=255):
    character = sprite("%s_%s" % (tag, expression))
    character.thumbnail(box, Image.Resampling.LANCZOS)
    if opacity != 255:
        alpha = character.getchannel("A").point(lambda value: value * opacity // 255)
        character.putalpha(alpha)
    x = int(center_x - character.width / 2)
    y = int(bottom_y - character.height)
    canvas.alpha_composite(character, (x, y))
    return canvas


def save(name, plate):
    path = os.path.join(CG_DIR, name + ".png")
    plate.convert("RGB").save(path, optimize=True)
    print("saved", path)


def create_blank_dot():
    plate = bg("white_page")
    plate = ImageEnhance.Contrast(plate).enhance(0.82)
    plate = glow(plate, (960, 540), 90, (120, 116, 136), 100)
    ink = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(ink)
    draw.ellipse((952, 532, 968, 548), fill=(28, 25, 33, 255))
    plate = Image.alpha_composite(plate, ink.filter(ImageFilter.GaussianBlur(0.7)))
    return vignette(plate, 40)


def create_ending_wanderer():
    plate = bg("annex_dawn")
    plate = tint(plate, (235, 204, 145), 24)
    layer = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    draw.rounded_rectangle((1180, 615, 1515, 845), 34, fill=(89, 57, 39, 238), outline=(202, 166, 105, 225), width=7)
    draw.rectangle((1210, 825, 1255, 1030), fill=(66, 45, 35, 220))
    draw.rectangle((1440, 825, 1485, 1030), fill=(66, 45, 35, 220))
    draw.ellipse((1030, 835, 1165, 900), fill=(224, 201, 161, 245), outline=(144, 111, 72, 230), width=5)
    draw.ellipse((1064, 845, 1130, 880), fill=(134, 78, 48, 220))
    draw.ellipse((1510, 835, 1645, 900), fill=(224, 201, 161, 245), outline=(144, 111, 72, 230), width=5)
    draw.ellipse((1544, 845, 1610, 880), fill=(134, 78, 48, 220))
    plate = Image.alpha_composite(plate, layer.filter(ImageFilter.GaussianBlur(1.2)))
    plate = place_sprite_at(plate, "wanderer", "soft", 650, 1060, (750, 1010))
    plate = glow(plate, (1330, 660), 210, (246, 207, 132), 50)
    return vignette(plate, 70)


def create_ending_scaramouche():
    plate = bg("annex_evening")
    plate = tint(plate, (38, 31, 63), 88)
    plate = glow(plate, (1370, 390), 360, (215, 169, 99), 125)
    plate = place_sprite_at(plate, "echo", "smile", 780, 1050, (760, 990))
    # The hat is set aside as the Echo begins his new life among the archive lamps.
    layer = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    draw.ellipse((1190, 820, 1745, 935), fill=(34, 28, 39, 242), outline=(190, 146, 76, 245), width=8)
    draw.polygon(((1320, 830), (1410, 710), (1575, 710), (1665, 840)), fill=(48, 36, 49, 246), outline=(190, 146, 76, 240))
    draw.arc((1220, 820, 1715, 915), 8, 172, fill=(225, 188, 106, 230), width=6)
    # One newly lit lamp; its light reaches the open page but not the whole room.
    draw.line(((1630, 690), (1630, 815)), fill=(70, 48, 34, 245), width=18)
    draw.polygon(((1568, 700), (1692, 700), (1664, 625), (1598, 625)), fill=(77, 56, 44, 245), outline=(213, 176, 109, 230))
    draw.ellipse((1590, 606, 1672, 670), fill=(255, 224, 156, 220))
    plate = Image.alpha_composite(plate, layer.filter(ImageFilter.GaussianBlur(1.5)))
    plate = glow(plate, (1630, 645), 180, (255, 212, 128), 85)
    return vignette(plate, 84)


def create_ending_true():
    plate = bg("annex_day")
    plate = tint(plate, (213, 192, 145), 30)
    plate = place_sprite_at(plate, "wanderer", "soft", 550, 1025, (610, 960), 255)
    plate = place_sprite_at(plate, "echo", "smile", 1370, 1025, (610, 960), 255)
    # A shared warm table anchors the two selves in one ordinary, hopeful moment.
    table = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(table)
    draw.polygon(((210, 960), (1710, 960), (1880, 1080), (60, 1080)), fill=(88, 56, 39, 218))
    draw.line(((245, 970), (1675, 970)), fill=(218, 176, 107, 175), width=7)
    draw.ellipse((875, 905, 1015, 960), fill=(235, 219, 183, 225), outline=(148, 108, 70, 200), width=5)
    draw.ellipse((902, 914, 988, 948), fill=(126, 78, 48, 210))
    plate = Image.alpha_composite(plate, table.filter(ImageFilter.GaussianBlur(2.0)))
    plate = glow(plate, (960, 380), 420, (255, 231, 174), 55)
    return vignette(plate, 60)


def create_folio_black():
    plate = bg("white_page_dark")
    plate = tint(plate, (12, 10, 20), 122)
    plate = glow(plate, (960, 590), 400, (116, 78, 159), 75)
    folio = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(folio)
    draw.rounded_rectangle((480, 160, 1450, 950), 58, fill=(14, 13, 20, 248), outline=(171, 138, 83, 230), width=8)
    draw.rounded_rectangle((530, 205, 1400, 905), 32, outline=(83, 70, 57, 190), width=5)
    draw.line(((690, 190), (690, 920)), fill=(118, 94, 60, 220), width=10)
    for y in range(300, 830, 58):
        draw.line(((565, y), (635, y + 8)), fill=(192, 159, 101, 190), width=5)
    draw.ellipse((940, 460, 1090, 610), fill=(111, 78, 147, 118), outline=(217, 188, 123, 230), width=8)
    draw.ellipse((982, 502, 1048, 568), outline=(229, 208, 162, 205), width=4)
    for x in range(900, 1120, 32):
        draw.line(((x, 690), (x + 18, 733)), fill=(206, 177, 117, 100), width=3)
    plate = Image.alpha_composite(plate, folio.filter(ImageFilter.GaussianBlur(1)))
    plate = glow(plate, (1010, 525), 170, (125, 82, 186), 75)
    return vignette(plate, 130)


def create_margin_door(open_door):
    plate = bg("corridor_mist")
    if open_door:
        plate = tint(plate, (32, 28, 49), 56)
        # Reveal the Annex through the opening instead of filling it with a flat color.
        annex_view = bg("annex_dawn").resize((235, 470), Image.Resampling.LANCZOS)
        reveal = Image.new("RGBA", SIZE, (0, 0, 0, 0))
        reveal.paste(annex_view, (830, 304))
        reveal_mask = Image.new("L", SIZE, 0)
        ImageDraw.Draw(reveal_mask).polygon(
            ((850, 318), (1050, 326), (1045, 754), (851, 761)), fill=255)
        reveal.putalpha(reveal_mask.filter(ImageFilter.GaussianBlur(1.2)))
        plate = Image.alpha_composite(plate, reveal)
        door = Image.new("RGBA", SIZE, (0, 0, 0, 0))
        draw = ImageDraw.Draw(door)
        # Door leaf swings toward camera while the revealed room remains visible.
        draw.polygon(((1054, 326), (1160, 360), (1170, 800), (1048, 754)), fill=(36, 29, 43, 246), outline=(171, 138, 83, 230))
        draw.line(((1072, 350), (1068, 735)), fill=(205, 169, 103, 145), width=5)
        draw.line(((1145, 380), (1153, 780)), fill=(205, 169, 103, 110), width=4)
        draw.line(((1085, 410), (1133, 425)), fill=(116, 95, 71, 130), width=3)
        draw.line(((1082, 690), (1140, 708)), fill=(116, 95, 71, 120), width=3)
        draw.ellipse((1108, 548, 1127, 567), fill=(223, 184, 101, 245))
        plate = Image.alpha_composite(plate, door.filter(ImageFilter.GaussianBlur(1.4)))
        plate = glow(plate, (890, 540), 260, (248, 219, 153), 90)
        threshold = Image.new("RGBA", SIZE, (0, 0, 0, 0))
        td = ImageDraw.Draw(threshold)
        td.polygon(((842, 770), (1060, 770), (1260, 940), (660, 940)), fill=(241, 205, 129, 52))
        plate = Image.alpha_composite(plate, threshold.filter(ImageFilter.GaussianBlur(26)))
    else:
        plate = tint(plate, (18, 16, 29), 100)
        door = Image.new("RGBA", SIZE, (0, 0, 0, 0))
        draw = ImageDraw.Draw(door)
        # Match the distant arch size from the open-door image; fine grain lets the
        # native corridor texture show through instead of reading like a flat card.
        draw.polygon(((835, 300), (1068, 310), (1060, 770), (842, 776)), fill=(25, 22, 34, 230), outline=(111, 91, 62, 185))
        draw.polygon(((862, 324), (1043, 333), (1036, 746), (868, 751)), fill=(24, 21, 31, 225), outline=(170, 138, 88, 170))
        draw.line(((882, 350), (884, 724)), fill=(220, 176, 91, 155), width=4)
        draw.line(((1026, 355), (1019, 722)), fill=(220, 176, 91, 140), width=4)
        draw.line(((902, 400), (1004, 405)), fill=(115, 93, 66, 92), width=3)
        draw.line(((899, 650), (1000, 654)), fill=(115, 93, 66, 80), width=3)
        draw.ellipse((1008, 525, 1028, 545), fill=(171, 127, 66, 235))
        draw.ellipse((1012, 529, 1024, 541), outline=(235, 196, 121, 190), width=2)
        plate = Image.alpha_composite(plate, door.filter(ImageFilter.GaussianBlur(1.6)))
    return vignette(plate, 88)


def create_page_together():
    plate = bg("white_page")
    plate = tint(plate, (239, 227, 194), 12)
    plate = place_sprite_at(plate, "wanderer", "soft", 475, 1000, (500, 820), 190)
    plate = place_sprite_at(plate, "echo", "smile", 1445, 1000, (500, 820), 190)
    folio = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(folio)
    draw.polygon(((300, 740), (1620, 740), (1700, 1010), (220, 1010)), fill=(240, 231, 209, 218), outline=(163, 127, 77, 190))
    draw.line(((390, 800), (1535, 800)), fill=(188, 154, 103, 135), width=4)
    # Two strokes meet at the binding like hands sharing one line.
    draw.line(((550, 875), (910, 840), (960, 850)), fill=(72, 94, 145, 190), width=11)
    draw.line(((1370, 875), (1010, 840), (960, 850)), fill=(117, 83, 155, 190), width=11)
    draw.line(((960, 850), (1085, 792)), fill=(68, 57, 49, 235), width=13)
    draw.ellipse((1070, 778, 1100, 808), fill=(191, 148, 79, 255))
    draw.line(((1092, 794), (1105, 787)), fill=(249, 223, 163, 230), width=5)
    plate = Image.alpha_composite(plate, folio.filter(ImageFilter.GaussianBlur(0.5)))
    plate = glow(plate, (960, 535), 240, (228, 193, 113), 80)
    return vignette(plate, 42)


def create_blank_dot_file():
    plate = bg("white_page")
    plate = ImageEnhance.Contrast(plate).enhance(0.72)
    plate = vignette(plate, 24)
    dot = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    ImageDraw.Draw(dot).ellipse((951, 531, 969, 549), fill=(35, 32, 39, 255))
    return Image.alpha_composite(plate, dot)


def main():
    requested = {
        "blank_dot": create_blank_dot_file,
        "ending_scaramouche": create_ending_scaramouche,
        "ending_true": create_ending_true,
        "ending_wanderer": create_ending_wanderer,
        "folio_black": create_folio_black,
        "margin_door_shut": lambda: create_margin_door(False),
        "margin_door": lambda: create_margin_door(True),
        "wanderer_echo_on_page": create_page_together,
    }
    for name, create in requested.items():
        save(name, create())


if __name__ == "__main__":
    main()