from typing import Generator, Any, NoReturn, Union, Callable

from clang.cindex import Cursor, Token, TokenKind

from clangast.data_structures import StackingPipeline, Tree, Node
from clangast.algorithms.elements_parsing.utility import (
    gathering_tokens_until_border, gathering_statement, gathering_statement_open_spelling,
    filter_none, mismatch_spelling
)


def parse_error(t: Token) -> RuntimeError:
    return RuntimeError(
        f"Unexpected token; {t.cursor.translation_unit}:{t.cursor.location}:{t.cursor.kind}:{t.spelling}")


def expected_token(t: Token, spelling: str) -> NoReturn:
    if mismatch_spelling(t, spelling):
        raise parse_error(t)


class ObjectParser(object):
    def __init__(self, cursor: Cursor):
        self.cursor: Cursor = cursor
        self.tokens_pipeline: StackingPipeline = StackingPipeline(self.cursor.get_tokens())
        self.result_tree: Tree = Tree()

    def _get_statement_as_pipeline(self, source: StackingPipeline,
                                   border_spelling: str, gathering_method: Callable) -> StackingPipeline:
        return StackingPipeline(
            filter_none(gathering_method(source,
                                         border_spelling))
        )

    def _get_statement_as_string(self, source: StackingPipeline,
                                 border_spelling: str, gathering_method: Callable) -> str:
        return " ".join((
            token.spelling for token in self._get_statement_as_pipeline(source, border_spelling, gathering_method)
        ))

    def _parse_statement(self, source: StackingPipeline) -> Generator[Node, Any, None]:
        t = source.pop()
        if mismatch_spelling(t, '{'):
            source += t
            tokens = self._get_statement_as_pipeline(source, ';', gathering_statement)
        else:
            tokens = self._get_statement_as_pipeline(source, '{', gathering_statement_open_spelling)
        for node in self._parse_from(filter_none(tokens)):
            yield node

    def _parse_if_case(self, token: Token, source: StackingPipeline) -> Node:
        node = Node(token.spelling, token.cursor.kind)

        t: Token = source.pop()
        expected_token(t, '(')
        condition = self._get_statement_as_string(source, '(', gathering_statement)
        node.store(condition)

        for _node in self._parse_statement(source):
            node.add(_node)

        t = source.pop()
        if mismatch_spelling(t, "else"):
            source += t
            return node

        else_node = Node(t.spelling, t.cursor.kind)
        for _node in self._parse_statement(source):
            else_node.add(_node)
        node.add(else_node)

        return node

    def _parse_switch_case(self, token: Token, source: StackingPipeline) -> Node:
        node = Node(token.spelling, token.cursor.kind)

        t = source.pop()
        expected_token(t, '(')
        condition = self._get_statement_as_string(source, '(', gathering_statement)
        node.store(condition)

        t = source.pop()
        expected_token(t, '{')
        source += t

        for _node in self._parse_statement(source):
            node.add(_node)

        return node

    def _parse_case_in_switch(self, token: Token, source: StackingPipeline) -> Node:
        name = self._get_statement_as_string(source, ':', gathering_tokens_until_border)
        full_name = f"{token.spelling}_{name}"
        node = Node(full_name, token.cursor.kind)

        for token in source:
            spelling = token.spelling
            if spelling == "case":
                source += token
                node.store("fall_trough")
                return node
            elif spelling == "default":
                source += token
                node.store("fall_trough")
                return node
            elif spelling == "break":
                node.store("break")
                return node
            elif spelling == "return":
                node.store("return")
                return_node = self._parse_return_case(token, source)
                node.add(return_node)
                return node
            else:
                for _node in self._parse_statement(source):
                    node.add(node)

        expected_token(token, "end_of_case")

    def _parse_default_in_switch(self, token: Token, source: StackingPipeline) -> Node:
        node = Node(token.spelling, token.cursor.kind)
        t = source.pop()
        expected_token(t, ':')

        spelling = token.spelling
        if spelling == "break":
            node.store("break")
            return node
        elif spelling == "return":
            node.store("return")
            return_node = self._parse_return_case(token, source)
            node.add(return_node)
            return node
        else:
            for _node in self._parse_statement(source):
                node.add(node)

        expected_token(token, "end_of_default_case")

    def _parse_return_case(self, token: Token, source: StackingPipeline) -> Node:
        node = Node(token.spelling, token.cursor.kind)
        what = self._get_statement_as_string(source, ';', gathering_tokens_until_border)
        node.store(what)
        return node

    def _parsing_keyword(self, token: Token, source: StackingPipeline) -> Union[Node, None]:
        spelling = token.cursor.spelling
        if spelling == "if":
            return self._parse_if_case(token, source)
        elif spelling == "switch":
            return self._parse_switch_case(token, source)
        elif spelling == "case":
            return self._parse_case_in_switch(token, source)
        elif spelling == "default":
            return self._parse_default_in_switch(token, source)
        elif spelling == "return":
            return self._parse_return_case(token, source)
        else:
            return None

    def _parsing_identifier(self, token: Token, source: StackingPipeline) -> Union[Node, None]:
        node = Node(token.spelling, token.cursor.kind)
        rest_of_line = self._get_statement_as_string(source, ';', gathering_tokens_until_border)
        node.store(rest_of_line)

        return node

    def _parse_from(self, source: StackingPipeline) -> Generator[Node, Any, None]:
        for token in filter_none(source):
            kind = token.kind
            if kind == TokenKind.KEYWORD:
                yield self._parsing_keyword(token, source)
            elif kind == TokenKind.IDENTIFIER:
                yield self._parsing_identifier(token, source)

    def _parse(self) -> Generator[Node, Any, None]:
        for node in filter_none(self._parse_from(self.tokens_pipeline)):
            yield node

    def parse(self) -> NoReturn:
        root_node = Node(self.cursor.spelling, self.cursor.kind)
        object_prototype = self._get_statement_as_string(self.tokens_pipeline, '{', gathering_tokens_until_border)
        root_node.store(object_prototype)
        self.result_tree.set_root(root_node)

        for node in filter_none(self._parse()):
            self.result_tree.add(node, [])

    def name(self) -> str:
        return self.result_tree.root_name()

    def show(self, target_file, **kwargs):
        self.result_tree.show(target_file, **kwargs)
