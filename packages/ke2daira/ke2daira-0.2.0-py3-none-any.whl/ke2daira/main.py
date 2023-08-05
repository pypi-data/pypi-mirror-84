from janome.tokenizer import Tokenizer, Token  # type: ignore
from functools import reduce
from operator import add
from .kana2mora import katakana2mora

t = Tokenizer()

TANGO_SEPARATOR = " "
NO_READING = "*"


def get_reading_from_token(token: Token) -> str:
    if token.reading == NO_READING:
        return token.surface
    return token.reading


def tango2yomi(tango: str) -> str:
    tokens = t.tokenize(tango)
    yomi = reduce(add, map(get_reading_from_token, tokens))
    return yomi


def ke2dairanize(text: str) -> str:
    tangos = text.split(TANGO_SEPARATOR)

    yomis = list(map(tango2yomi, tangos))

    if len(tangos) == 1:
        return tangos[0]

    first_tango_moras = katakana2mora(yomis[0])
    first_tango_head = first_tango_moras[0]
    first_tango_tail_moras = first_tango_moras[1:]

    last_tango_moras = katakana2mora(yomis[-1])
    last_tango_head = last_tango_moras[0]
    last_tango_tail_moras = last_tango_moras[1:]

    new_first_tango_moras = [last_tango_head] + first_tango_tail_moras
    new_last_tango_moras = [first_tango_head] + last_tango_tail_moras

    yomis[0] = "".join(new_first_tango_moras)
    yomis[-1] = "".join(new_last_tango_moras)

    return TANGO_SEPARATOR.join(yomis)
