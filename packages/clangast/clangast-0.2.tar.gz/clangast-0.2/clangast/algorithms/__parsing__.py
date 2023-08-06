from typing import Union as __Union__
from typing import Generator as __Generator__

from clangast.data_structures.tree import BaseTree as __Tree__
from clangast.data_structures.node import BaseNode as __Node__
from clangast.algorithms.__utility__ import (
    __not_none__, __cursor_kind__, __cursor_index__, __token_kind__
)

from typing import Any as __Any__

from functools import partial as __partial__

__left_borders__ = ('(', '[', '{', 'new_line')
__right_borders__ = (')', ']', '}', ';')

__borders_index__ = {
    **dict(zip(__left_borders__, __right_borders__)),
    **dict(zip(__right_borders__, __left_borders__))
}


class __MainGenerator__:
    def __init__(self, token_generator: __Generator__[__cursor_index__.Token, __Any__, None]):
        self.generator = token_generator
        self.tokens = []

    def __next__(self):
        for token in self.generator:
            while len(self.tokens) != 0:
                return self.tokens.pop()
            return token

    def __iter__(self):
        for t in self.generator:
            while len(self.tokens) != 0:
                yield self.tokens.pop()
            yield t

    def stack(self, value: __cursor_index__):
        self.tokens.append(value)


def __element_pretty_format__(element: __Union__[__cursor_index__.Cursor,
                                                 __cursor_index__.Token],
                              preamble: str = None) -> str:
    if preamble is not None:
        preamble = f"{preamble}\n"
    else:
        preamble = ""
    return f"{preamble}Name:\t{element.spelling}\nKind:\t{element.kind}\n----------------"


def __mismatch_spelling__(_token: __cursor_index__.Token, _spelling: str) -> bool:
    if _token is not None:
        return not _token.spelling == _spelling
    return True


def __parse_statement_stacked_generator__(token_generator: __MainGenerator__
                                          ) -> __Generator__[__Node__, __Any__, None]:
    # statement type: in brackets or single line
    token = next(token_generator)

    close_token = '}'

    if __mismatch_spelling__(token, '{'):
        close_token = ';'
        token_generator.stack(token)

    parser = __partial__(__parse_statement_to_stop_token__, close_token)
    for _node in filter(__not_none__,
                        parser(token_generator)):
        yield _node


def __parse_statement_to_stop_token__(stop_token_spelling: str,
                                      token_generator: __MainGenerator__) -> __Generator__[__Node__,
                                                                                           __Any__,
                                                                                           None]:
    for token in filter(__not_none__, token_generator):
        if token.spelling == stop_token_spelling:
            break
        node = __kind_switch__(token, token_generator)
        if node is not None:
            yield node
    yield None


def __gathering_tokens_between_borders__(token_generator: __MainGenerator__,
                                         close_token_spelling: str) -> __Generator__[__cursor_index__.Token,
                                                                                     __Any__,
                                                                                     None]:
    if close_token_spelling not in __borders_index__:
        return

    open_token_spelling = __borders_index__[close_token_spelling]
    inner_open_borders = 0

    for token in filter(__not_none__, token_generator):
        if token.spelling == open_token_spelling:
            inner_open_borders += 1

        if token.spelling == close_token_spelling:
            if inner_open_borders == 0:
                break
            else:
                inner_open_borders -= 1

        yield token


def __parse_id__(token: __cursor_index__.Token,
                 token_generator: __MainGenerator__
                 ) -> __Node__:
    node = __Node__(token.spelling, token.cursor.kind)
    node.store(
        something=" ".join((
            _token.spelling for _token in __gathering_tokens_between_borders__(token_generator, ';')
        ))
    )
    return node


def __parse_if_case__(token: __cursor_index__.Token,
                      token_generator: __MainGenerator__
                      ) -> __Node__:
    # set "if" as name for node
    node = __Node__(token.spelling, token.cursor.kind)

    # condition
    if __mismatch_spelling__(next(token_generator), '('):
        return node
    condition = " ".join(
        (token.spelling
         for token in __gathering_tokens_between_borders__(token_generator, ')'))
    )
    node.store(condition)

    # inner statement on if branch
    for _node in __parse_statement_stacked_generator__(token_generator):
        node.add(_node)

    # else
    token = next(token_generator)
    if __mismatch_spelling__(token, "else"):
        token_generator.stack(token)
        return node
    node.add(__parse_else__(token, token_generator))

    return node


def __parse_else__(token: __cursor_index__.Token,
                   tokens_generator: __MainGenerator__) -> __Node__:
    node = __Node__(token.spelling, token.cursor.kind)
    for _node in __parse_statement_stacked_generator__(tokens_generator):
        node.add(_node)
    return node


def __parse_switch_case__(token: __cursor_index__.Token,
                          token_generator: __MainGenerator__

                          ) -> __Node__:
    node = __Node__(token.spelling, token.cursor.kind)

    # condition
    if __mismatch_spelling__(next(token_generator), '('):
        return node
    node.store(
        something=" ".join((
            _token.spelling for _token in __gathering_tokens_between_borders__(token_generator, ')')
        ))
    )
    return node


def __parse_return__(token: __cursor_index__.Token,
                     token_generator: __MainGenerator__

                     ) -> __Node__:
    node = __Node__(token.spelling, token.cursor.kind)
    node.store(
        something=" ".join((
            token.spelling for token in __gathering_tokens_between_borders__(token_generator, ';')
        ))
    )
    return node


def __keyword_case__(token: __cursor_index__.Token,
                     token_generator: __MainGenerator__

                     ) -> __Union__[__Node__, None]:
    name = token.spelling
    if name == "if":
        return __parse_if_case__(token, token_generator)
    elif name == "switch":
        return __parse_switch_case__(token, token_generator)
    elif name == "return":
        return __parse_return__(token, token_generator)
    else:
        return None


def __id_case__(token: __cursor_index__.Token,
                token_generator: __MainGenerator__
                ) -> __Node__:
    return __parse_id__(token, token_generator)


def __kind_switch__(token: __cursor_index__.Token,
                    token_generator: __MainGenerator__
                    ) -> __Union__[__Node__, None]:
    kind = token.kind
    if kind == __token_kind__.IDENTIFIER:
        return __id_case__(token, token_generator)
    elif kind == __token_kind__.KEYWORD:
        return __keyword_case__(token, token_generator)
    else:
        return None


def __parse_statement_generator__(token_generator: __MainGenerator__) -> __Generator__[__Node__,
                                                                                       __Any__,
                                                                                       None]:
    for token in token_generator:
        node = __kind_switch__(token, token_generator)
        if node is not None:
            yield node
    yield None


def __parse_function_body__(main_generator: __MainGenerator__) -> __Generator__[__Node__, __Any__, None]:
    for node in __parse_statement_generator__(main_generator):
        yield node


def __parse_function__(cursor: __cursor_index__.Cursor) -> __Tree__:
    main_generator = __MainGenerator__(cursor.get_tokens())

    root_node = __Node__(cursor.spelling, cursor.kind)
    root_node.store(
        something=" ".join((
            token.spelling for token in __gathering_tokens_between_borders__(main_generator, '{')
        ))
    )

    tree = __Tree__(root=root_node)
    for node in filter(__not_none__, __parse_function_body__(main_generator)):
        tree.add(node, [])
    return tree
