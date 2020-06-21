import os.path
from pathlib import Path

import pytest
from bmtext import meta


FIXTURE_DIR = Path(__file__).resolve(True).parent / 'fixtures'


def test_parse_line_tokens():
    # assert meta.parse_line_tokens("") == ("", {})
    assert meta.parse_line_tokens("a") == ("a", {})
    assert meta.parse_line_tokens("a b=c") == ("a", {"b": "c"})
    assert meta.parse_line_tokens("a b=c=d") == ("a", {"b": "c=d"})
    assert meta.parse_line_tokens("a b==d") == ("a", {"b": "=d"})
    assert meta.parse_line_tokens("a b==d") == ("a", {"b": "=d"})
    assert meta.parse_line_tokens("a b=c d=e") == ("a", {"b": "c", "d": "e"})
    assert meta.parse_line_tokens("a  b=c   d=e") == ("a", {"b": "c", "d": "e"})


def test_parse_info():
    parsed = meta.parse_line(
        'info face="Raleway" size=32 bold=0 italic=0 charset="" unicode=1 stretchH=100 smooth=0 aa=1 padding=0,0,0,0 spacing=1,1 outline=0'
    )

    assert parsed == meta.Info(
        face="Raleway",
        size=32,
        bold=0,
        italic=0,
        charset="",
        unicode=1,
        stretchH=100,
        smooth=0,
        aa=1,
        padding=(0, 0, 0, 0),
        spacing=(1, 1),
        outline=0,
    )

    assert parsed.face == "Raleway"
    assert parsed.size == 32


def test_parse_common():
    parsed = meta.parse_line(
        "common lineHeight=32 base=27 scaleW=256 scaleH=256 pages=1 packed=0 alphaChnl=1 redChnl=0 greenChnl=0 blueChnl=0"
    )
    assert parsed == meta.Common(
        lineHeight=32,
        base=27,
        scaleW=256,
        scaleH=256,
        pages=1,
        packed=0,
        alphaChnl=1,
        redChnl=0,
        greenChnl=0,
        blueChnl=0,
    )

    assert parsed.lineHeight == 32


def test_parse_page():
    parsed = meta.parse_line('page id=0 file="raleway-thin-32_0.png"')
    assert parsed == meta.Page(id=0, file="raleway-thin-32_0.png")
    assert parsed.id == 0
    assert parsed.file == "raleway-thin-32_0.png"


def test_parse_kerning():
    parsed = meta.parse_line("kerning first=65  second=218 amount=-1")

    assert parsed == meta.Kerning(first=65, second=218, amount=-1)

    assert parsed.first == 65
    assert parsed.second == 218
    assert parsed.amount == -1


def test_parse_char():
    parsed = meta.parse_line(
        "char id=246  x=150   y=43    width=12    height=17    xoffset=1     yoffset=10    xadvance=14    page=0  chnl=15"
    )

    assert parsed == meta.Char(
        id=246,
        x=150,
        y=43,
        width=12,
        height=17,
        xoffset=1,
        yoffset=10,
        xadvance=14,
        page=0,
        chnl=15,
    )

    assert parsed.height == 17


def test_Char_char():
    c = meta.Char(
        id=246,
        x=150,
        y=43,
        width=12,
        height=17,
        xoffset=1,
        yoffset=10,
        xadvance=14,
        page=0,
        chnl=15,
    )

    assert c.char() == "ö"
    assert str(c) == "<Char 246 - 'ö'>"


def test_parse_file():
    path = FIXTURE_DIR / 'raleway-30/raleway-thin-32.fnt'
    with path.open() as f:
        font = meta.parse_file(f)
    
    assert font.info.face == 'Raleway'
    assert len(font.char_map) == 193
    assert len(font.kerning_map) == 1085
    assert font.char_map[246].char() == "ö"


@pytest.mark.skip("Test not implemented")
def test_invalid_input_file():
    pass