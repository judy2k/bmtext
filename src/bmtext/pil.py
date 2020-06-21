import attr
from PIL import Image
from typing import Dict

from . import meta


class LoadedFont:
    def __init__(self, font: meta.Font):
        self._images = [Image.open(page) for page in font.pages]
    
    def char_image(self, char: meta.Char):
        return self._images[char.page].crop(char.bounds)


class BMText:
    def __init__(self, image: Image):
        self._image: Image = image
        self._loaded_fonts: Dict[meta.Font, Image] = {}

    def textsize(self, text: str, font: meta.Font):
        # TODO: You _could_ actually implement this.
        return 

    def _load_font(self, font):
        # TODO: Font has no good hash (check attrs) - should find a better way to do this.
        loaded_font = self._loaded_fonts.get(font, None)
        if loaded_font is None:
            self._loaded_fonts[font] = loaded_font = LoadedFont(font)
        return loaded_font

    def text(self, xy, text, font: meta.Font, kerning=True, fill='black'):
        # TODO: Optimize by pre-calculating mask and fill image sizes to text bounds, not image bounds.
        mask = Image.new('L', self._image.size, 'black')
        loaded_font = self._load_font(font)
        for g in font.glyph_positions(text, kerning):
            mask.paste(
                loaded_font.char_image(g.char),
                g.dest_location)
        self._image.paste(Image.new('RGB', mask.size, color=fill), xy, mask=mask)