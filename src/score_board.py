# SPDX-FileCopyrightText: 2020 Phillip Burgess for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
RASTER EYES for Adafruit Matrix Portal: animated spooky eyes.
"""

# pylint: disable=import-error
import math
import random
import time
import displayio
import adafruit_imageload
from adafruit_matrixportal.matrix import Matrix
import terminalio
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
import vectorio

font = bitmap_font.load_font("/font/forkawesome-42.pcf")

# ONE-TIME INITIALIZATION --------------------------------------------------

MATRIX = Matrix(bit_depth=6)
DISPLAY = MATRIX.display

# Order in which sprites are added determines the 'stacking order' and
# visual priority. Lower lid is added before the upper lid so that if they
# overlap, the upper lid is 'on top' (e.g. if it has eyelashes or such).
SPRITES_SCORE = displayio.Group()

# --- Gray background ---
bg_bitmap = displayio.Bitmap(DISPLAY.width, DISPLAY.height, 1)
bg_palette = displayio.Palette(1)
bg_palette[0] = 0x000000  # gray
bg_tilegrid = displayio.TileGrid(bg_bitmap, pixel_shader=bg_palette)
SPRITES_SCORE.append(bg_tilegrid)

shape_palette = displayio.Palette(1)
shape_palette[0] = 0x000800   # green rectangle

shape_palette2 = displayio.Palette(1)
shape_palette2[0] = 0x000000   # green rectangle

shape_palette3 = displayio.Palette(1)
shape_palette3[0] = 0x101010   # green rectangle

max_score = 25


default_color=0x008000
highlight_color=0x808080
race_color=0x800000

# Filled rectangle
rect_a1 = vectorio.Rectangle(
    pixel_shader=shape_palette,
    x=0,
    y=0,
    width=32,
    height=2
)
SPRITES_SCORE.append(rect_a1)

# Filled rectangle
rect_a2 = vectorio.Rectangle(
    pixel_shader=shape_palette,
    x=0,
    y=0,
    width=2,
    height=16
)
SPRITES_SCORE.append(rect_a2)

# Filled rectangle
rect_b1 = vectorio.Rectangle(
    pixel_shader=shape_palette,
    x=32,
    y=30,
    width=32,
    height=2
)
SPRITES_SCORE.append(rect_b1)

# Filled rectangle
rect_b2 = vectorio.Rectangle(
    pixel_shader=shape_palette,
    x=62,
    y=16,
    width=2,
    height=16
)
SPRITES_SCORE.append(rect_b2)


####
field_a = vectorio.Rectangle(
    pixel_shader=shape_palette2,
    x=2,
    y=2,
    width=28,
    height=19
)
SPRITES_SCORE.append(field_a)

field_b = vectorio.Rectangle(
    pixel_shader=shape_palette2,
    x=34,
    y=11,
    width=28,
    height=19
)
SPRITES_SCORE.append(field_b)



# --- Add text ---
score_a = label.Label(
    terminalio.FONT,
    text=f"{0:2d}",
    color=default_color,
    x=4,
    y=11,
    scale=2
)

score_b = label.Label(
    terminalio.FONT,
    text=f"{0:2d}",
    color=default_color,
    x=38,
    y=21,
    scale=2,
)

SPRITES_SCORE.append(score_a)
SPRITES_SCORE.append(score_b)

# NEW API — assign root group
DISPLAY.root_group = SPRITES_SCORE

# MAIN LOOP ----------------------------------------------------------------

a = 0
b = 0


while True:

    score_a.text = f"{a:2d}"
    score_b.text = f"{b:2d}"

    time.sleep(5)

    while True:

        #step = random.choice([0, 1])
        side = random.choice([0, 1])

        if side:
            a += 1
            score_a.text = f"{a:2d}"
            score_a.color=highlight_color
            #field_a.pixel_shader=shape_palette3
            rect_a1.pixel_shader=shape_palette3
            rect_a2.pixel_shader=shape_palette3

        else:
            b += 1
            score_b.text = f"{b:2d}"
            score_b.color=highlight_color
            #field_b.pixel_shader=shape_palette3
            rect_b1.pixel_shader=shape_palette3
            rect_b2.pixel_shader=shape_palette3

        time.sleep(0.5)

        if a % 5 == 0 and a > 5:
            score_a.color=race_color
        else:
            score_a.color=default_color

        if b % 5 == 0 and b > 5:
            score_b.color=race_color
        else:
            score_b.color=default_color

        field_a.pixel_shader=shape_palette2
        field_b.pixel_shader=shape_palette2

        rect_a1.pixel_shader=shape_palette
        rect_a2.pixel_shader=shape_palette

        rect_b1.pixel_shader=shape_palette
        rect_b2.pixel_shader=shape_palette

        if (a >= max_score or b >= max_score) and (a-b >= 2 or b-a >= 2):
            break;

        wait = random.choice([1, 3])

        time.sleep(wait)

    # match finished

    a = 0
    b = 0

    for i in range(20):
        score_a.color=highlight_color
        score_b.color=highlight_color
        time.sleep(0.25)
        score_a.color=default_color
        score_b.color=default_color
        time.sleep(0.25)


    SPRITES_SCORE.hidden = True

