from clangast.data_structures.generator import EndlessPipeline
from clangast.algorithms.tools.utility import not_none
from clang.cindex import Token

from typing import Generator, Any

from functools import partial

left_borders = ('(', '[', '{')
right_borders = (')', ']', '}')

borders_index = {
    **dict(zip(left_borders, right_borders)),
    **dict(zip(right_borders, left_borders))
}

filter_none = partial(filter, not_none)


def gathering_tokens_until_border(token_generator: EndlessPipeline,
                                  border_token_spelling: str) -> Generator[Token, Any, None]:
    for token in filter_none(token_generator):
        if token.spelling == border_token_spelling:
            break
        yield token


def gathering_statement_open_spelling(token_generator: EndlessPipeline,
                                      open_border_spelling: str) -> Generator[Token, Any, None]:
    close_border_spelling = borders_index[open_border_spelling]
    return gathering_statement(token_generator, close_border_spelling)


def gathering_statement(token_generator: EndlessPipeline,
                        close_border_spelling: str) -> Generator[Token, Any, None]:
    open_borders = 1
    for token in filter_none(token_generator):
        if open_borders == 1 and not mismatch_spelling(token, close_border_spelling):
            break

        if token.spelling in left_borders:
            open_borders += 1
        elif token.spelling in right_borders:
            open_borders -= 1

        yield token


def mismatch_spelling(token: Token, spelling: str) -> bool:
    return token.spelling == spelling
