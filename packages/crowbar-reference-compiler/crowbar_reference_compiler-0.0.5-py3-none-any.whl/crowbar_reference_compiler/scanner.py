from dataclasses import dataclass
from typing import Optional, List

import regex as re  # type: ignore


@dataclass
class Token:
    type: str
    data: Optional[str] = None

    def __repr__(self) -> str:
        if self.data is not None:
            return "{}: {}".format(self.type, repr(self.data))
        else:
            return repr(self.type)


class GenerousTokenList(List[Token]):
    def __getitem__(self, i):
        try:
            return super(GenerousTokenList, self).__getitem__(i)
        except IndexError:
            return Token('')


KEYWORD = re.compile(r"""
    bool|break|
    case|char|const|continue|
    default|do|
    else|enum|
    false|float32|float64|for|fragile|function|
    if|include|int8|int16|int32|int64|intmax|intsize|
    opaque|
    return|
    sizeof|struct|switch|
    true|
    uint8|uint16|uint32|uint64|uintaddr|uintmax|uintsize|union|
    void|
    while""", re.VERBOSE)
IDENTIFIER = re.compile(r"[\p{L}\p{Pc}\p{Sk}\p{Mn}][\p{L}\p{Pc}\p{Sk}\p{Mn}\p{N}]*")
DECIMAL_CONSTANT = re.compile(r"[0-9_]+")
BINARY_CONSTANT = re.compile(r"0[bB][01_]+")
OCTAL_CONSTANT = re.compile(r"0o[0-7_]+")
HEX_CONSTANT = re.compile(r"0[xX][0-9a-fA-F]+")
FLOAT_CONSTANT = re.compile(r"[0-9_]+\.[0-9_]+([eE][+-]?[0-9_]+)?")
HEX_FLOAT_CONSTANT = re.compile(r"0(fx|FX)[0-9a-fA-F_]+\.[0-9a-fA-F_]+[pP][+-]?[0-9_]+")

_ESCAPE_SEQUENCE = r"""\\['"\\rnt0]|\\x[0-9a-fA-F]{2}|\\u[0-9a-fA-F]{4}|\\U[0-9a-fA-F]{8}"""
CHAR_CONSTANT = re.compile(r"'([^'\\]|" + _ESCAPE_SEQUENCE + r")'")
STRING_LITERAL = re.compile(r'"([^"\\]|' + _ESCAPE_SEQUENCE + r')+"')
PUNCTUATOR = re.compile(r"->|\+\+|--|>>|<<|<=|>=|&&|\|\||[=!+\-*/%&|^]=|[\[\](){}.,+\-*/%;!&|^~><=]")
WHITESPACE = re.compile(r"[\p{Z}\p{Cc}]+")
COMMENT = re.compile(r"(//[^\n]*\n)|(/\*.*?\*/)", re.DOTALL)


def scan(code):
    result = []
    remaining = code

    while len(remaining) > 0:
        match = COMMENT.match(remaining)
        if match:
            remaining = remaining[match.end():]
            continue
        match = WHITESPACE.match(remaining)
        if match:
            remaining = remaining[match.end():]
            continue
        kw_match = KEYWORD.match(remaining)
        id_match = IDENTIFIER.match(remaining)
        if kw_match and ((not id_match) or len(kw_match.group()) == len(id_match.group())):
            result.append(Token(kw_match.group()))
            remaining = remaining[kw_match.end():]
            continue
        if id_match:
            result.append(Token('identifier', id_match.group()))
            remaining = remaining[id_match.end():]
            continue
        was_constant = False
        for constant in [DECIMAL_CONSTANT, BINARY_CONSTANT, OCTAL_CONSTANT, HEX_CONSTANT, FLOAT_CONSTANT, HEX_FLOAT_CONSTANT, CHAR_CONSTANT]:
            match = constant.match(remaining)
            if match:
                result.append(Token('constant', match.group()))
                remaining = remaining[match.end():]
                was_constant = True
                break
        if was_constant:
            continue
        match = STRING_LITERAL.match(remaining)
        if match:
            result.append(Token('string_literal', match.group()))
            remaining = remaining[match.end():]
            continue
        match = PUNCTUATOR.match(remaining)
        if match:
            result.append(Token(match.group()))
            remaining = remaining[match.end():]
            continue
        raise ValueError("unrecognized code in scanner: {}".format(repr(remaining[:20])))

    return GenerousTokenList(result)
