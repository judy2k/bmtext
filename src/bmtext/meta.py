import abc
import attr
import itertools
from operator import attrgetter
from pathlib import Path
import typing
from typing import Tuple, Optional, Mapping, List, Union


def ParseError(Exception):
    def __init__(self, msg, lineno):
        super().__init__(f"Error parsing line {lineno}: {msg}")


def de_quote(s):
    if s.startswith('"') and s.endswith('"'):
        return s[1:-1]
    return s


def bool_int(s):
    val = int(s)
    if 0 <= val <= 1:
        return val
    raise ValueError(f"Boolean integer {val} should be 0 or 1")


def int_list(s):
    if isinstance(s, str):
        return tuple(int(v) for v in s.split(","))
    return s


@attr.s(auto_attribs=True)
class Info:
    face: str = attr.ib(converter=de_quote)
    size: int = attr.ib(converter=int)
    bold: int = attr.ib(converter=bool_int)
    italic: int = attr.ib(converter=bool_int)
    charset: str = attr.ib(converter=de_quote)
    unicode: int = attr.ib(converter=bool_int)
    stretchH: int = attr.ib(converter=int)
    smooth: int = attr.ib(converter=bool_int)
    aa: int = attr.ib(converter=bool_int)
    padding: Tuple[int] = attr.ib(converter=int_list)
    spacing: Tuple[int] = attr.ib(converter=int_list)
    outline: int = attr.ib(converter=bool_int)


@attr.s(auto_attribs=True)
class Common:
    lineHeight: int = attr.ib(converter=int)
    base: int = attr.ib(converter=int)
    scaleW: int = attr.ib(converter=int)
    scaleH: int = attr.ib(converter=int)
    pages: int = attr.ib(converter=int)
    packed: int = attr.ib(converter=int)
    alphaChnl: int = attr.ib(converter=int)
    redChnl: int = attr.ib(converter=int)
    greenChnl: int = attr.ib(converter=int)
    blueChnl: int = attr.ib(converter=int)


@attr.s(auto_attribs=True)
class Page:
    id: int = attr.ib(converter=int)
    file: str = attr.ib(converter=de_quote)


@attr.s(auto_attribs=True, slots=True)
class Kerning:
    first: int = attr.ib(converter=int)
    second: int = attr.ib(converter=int)
    amount: int = attr.ib(converter=int)

    def __str__(self):
        return f"<Kerning '{chr(self.first)}{chr(self.second)}': {self.amount}>"


@attr.s(auto_attribs=True, slots=True)
class Char:
    id: int = attr.ib(converter=int)
    x: int = attr.ib(converter=int)
    y: int = attr.ib(converter=int)
    width: int = attr.ib(converter=int)
    height: int = attr.ib(converter=int)
    xoffset: int = attr.ib(converter=int)
    yoffset: int = attr.ib(converter=int)
    xadvance: int = attr.ib(converter=int)
    page: int = attr.ib(converter=int)
    chnl: int = attr.ib(converter=int)

    def char(self):
        return chr(self.id)

    @property
    def bounds(self):
        return (self.x, self.y, self.x+self.width, self.y+self.height)

    def __str__(self):
        return f"<Char {self.id} - {self.char()!r}>"


class Kernings:
    def __init__(self, **kwargs):
        pass


class Chars:
    def __init__(self, **kwargs):
        pass


class Font:
    def __init__(self, path: Path, items):
        self.info: Info
        self.char_map: Mapping[int, Char] = {}
        self.kerning_map: Mapping[Tuple[int], Kerning] = {}
        self.pages: List[Page] = []

        classname = lambda x: x.__class__.__name__

        for k, g in itertools.groupby(sorted(items, key=classname), classname):
            if k == "Info":
                self.info = next(g)
            elif k == "Common":
                self.common = next(g)
            elif k == "Char":
                self.char_map = {c.id: c for c in g}
            elif k == "Kerning":
                self.kerning_map = {(k.first, k.second): k.amount for k in g}
                # for k, v in self.kerning_map.items():
                #     print(Kerning(k[0], k[1], v)) # FIXME
            elif k == "Page":
                self.pages = [path.parent / i.file for i in sorted(g, key=attrgetter("id"))]

    def position_char(self, c: Char, prev_c: Optional[Char] = None, kerning=True):
        k = 0
        if prev_c:
            if kerning:
                k = self.kerning_map.get((prev_c.id, c.id), 0)
                dest_location = (k + c.xoffset, c.yoffset)
            else:
                dest_location = (c.xoffset, c.yoffset)
        else:
            dest_location = (0, c.yoffset)
        return GlyphInfo(
            char=c,
            page_index=c.page,
            channel=c.chnl,
            source_bounds=(c.x, c.y, c.x + c.width, c.y + c.height),
            dest_location=dest_location,
            xadvance= c.xadvance + k - (c.xoffset if prev_c is None else 0)
        )

    def glyph_positions(self, text, kerning=True):
        y = 0
        for line in text.split('\n'):
            x = 0
            prev_char = None
            for c in line:
                char = self.char_map[ord(c)]
                # TODO: Handle chars missing from the char_map better
                g = self.position_char(char, prev_char, kerning=kerning)
                g.dest_location = (g.dest_location[0] + x, g.dest_location[1] + y)
                x += g.xadvance
                yield g
                prev_char = char

            y += self.common.lineHeight


LINE_PARSERS = {
    cls.__name__.lower(): cls
    for cls in [Info, Common, Page, Kerning, Char, Kernings, Chars]
}


def parse_line_tokens(line):
    line_type, *pair_tokens = line.split()
    return line_type, dict(pair_token.split("=", 1) for pair_token in pair_tokens)


def parse_line(line):
    line_type, args = parse_line_tokens(line)
    return LINE_PARSERS[line_type](**args)


def parse_file(path: Union[Path, str]):
    path = Path(path)
    with path.open() as f:
        items = [parse_line(line) for line in f]
        return Font(path, items)


@attr.s(auto_attribs=True)
class GlyphInfo:
    char: Char
    page_index: int
    channel: int
    source_bounds: Tuple[int]
    dest_location: Tuple[int]
    xadvance: int