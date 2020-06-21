#!/usr/bin/env python3

"""
Create a 15x16 image of the letter 'A' (codepoint 65), in black on a white background.
"""

from PIL import Image
from bmtext.meta import parse_file
from bmtext.pil import BMText

def main():
    im = Image.new('RGB', (320, 180), color=(160, 160, 255))
    bm = BMText(im)
    font = parse_file("tests/fixtures/raleway-30/raleway-thin-32.fnt")
    # FIXME: Overlapping glyphs remove part of previous char.
    bm.text((5, 5), "Antidisestablishmentarianism\nThorough\nSHOUTING!!!\nTomato?", font, fill='blue')
    im.save('assets/rendered_text.png')
    im.show()

if __name__ == "__main__":
    main()
