import abc
import attr
import itertools
from operator import attrgetter
from pathlib import Path
import typing
from typing import Tuple, Optional, Mapping, List


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


@attr.s(auto_attribs=True)
class Kerning:
    first: int = attr.ib(converter=int)
    second: int = attr.ib(converter=int)
    amount: int = attr.ib(converter=int)


@attr.s(auto_attribs=True)
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

    def __str__(self):
        return f"<Char {self.id} - {self.char()!r}>"


class Kernings:
    def __init__(self, **kwargs):
        pass


class Chars:
    def __init__(self, **kwargs):
        pass


class Font:
    def __init__(self, items):
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
            elif k == "Page":
                self.pages = [i.file for i in sorted(g, key=attrgetter("id"))]


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


def parse_file(f: typing.TextIO):
    items = [parse_line(line) for line in f]
    return Font(items)
