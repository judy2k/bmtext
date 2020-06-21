#!/usr/bin/env python3

"""
Create a 15x16 image of the letter 'A' (codepoint 65), in black on a white background.
"""

from PIL import Image, ImageChops

def main():
    original = Image.open("tests/fixtures/raleway-30/raleway-thin-32_0.png")
    bg = Image.new('RGB', (19, 31), 'yellow')
    fg = Image.new('RGB', (19, 31), 'red')
    mask = Image.new('L', (19, 31), 'black')
    letter_mask = original.crop((48, 81, 48+15, 81+16))
    mask.paste(letter_mask, (2, 2+11))
    bg.paste(fg, mask=mask)
    bg.save('raleway-A.png')

if __name__ == "__main__":
    main()
