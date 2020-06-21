#!/usr/bin/env python3

"""
Create a 15x16 image of the letter 'A' (codepoint 65), in black on a white background.
"""

from PIL import Image
from bmtext.meta import parse_file
from bmtext.pil import BMText

def main():
    im = Image.new('RGB', (300, 300), color='white')
    bm = BMText(im)
    font = parse_file("tests/fixtures/raleway-30/raleway-thin-32.fnt")
    bm.text((0, 0), "Hiya\nGoodbya\nThing", font, fill='red')
    im.show()

if __name__ == "__main__":
    main()
