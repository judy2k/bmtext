#!/usr/bin/env python3

"""
Create a 15x16 image of the letter 'A' (codepoint 65), in black on a white background.
"""

from PIL import Image
from bmtext.meta import parse_file
from bmtext.pil import LoadedFont

def main():
    font = parse_file("tests/fixtures/raleway-30/raleway-thin-32.fnt")
    loaded = LoadedFont(font)
    letters = {}
    chars = {}
    for letter in 'To':
        char = font.char_map[ord(letter)]
        im = loaded.char_image(char)
        letters[letter] = im
        chars[letter] = char
    t = letters['T']
    o = letters['o']
    ct = chars['T']
    to = chars['o']


    # width=2 height=16 xoffset=2 yoffset=11 xadvance=6

    # T width=14 height=16 xoffset=0 yoffset=11 xadvance=14
    # o width=12 height=12 xoffset=1 yoffset=15 xadvance=14
    # first=84  second=111 amount=-3

    mask = Image.new('L', (300, 100), 'black')
    x = 0
    mask.paste(t, (x, 11))
    x += 14 -3
    mask.paste(o, (x + 1, 15))
    x += 14 -3
    mask.paste(t, (x, 11))
    x += 14 -3 + 1
    mask.paste(o, (x, 15))

    yellow = Image.new('RGB', mask.size, 'yellow')
    red = Image.new('RGB', mask.size, 'red')

    yellow.paste(red, (0, 0), mask=mask)
    yellow.show()

if __name__ == "__main__":
    main()
