from clang.cindex import TranslationUnit, CursorKind
from typing import List, Dict, NoReturn, Generator, Any

from clangast.algorithms.tools.utility import all_as_kinds_generator
from clangast.algorithms.elements_parsing.object_parser import ObjectParser


class UnitParser(object):
    def __init__(self, translation_unit: TranslationUnit):
        self.unit = translation_unit
        self.parsed_objects_index: List[ObjectParser] = []
        self.parsed_objects_reverse_index: Dict[str, int] = {}
        self.target_types: List[CursorKind] = [
            CursorKind.FUNCTION_DECL
        ]

    def append_parsing_target_types(self, *types: List[CursorKind]):
        self.target_types += types

    def set_parsing_target_types(self, *types: List[CursorKind]) -> NoReturn:
        self.target_types = types

    def _all_target_objects_in_translation_unit(self) -> Generator[Any, Any, None]:
        for element in all_as_kinds_generator(self.target_types, self.unit.cursor):
            yield element

    def parse(self) -> NoReturn:
        for element in self._all_target_objects_in_translation_unit():
            if element.spelling in self.parsed_objects_index:
                continue

            parser = ObjectParser(element)
            parser.parse()

            index = len(self.parsed_objects_index)
            self.parsed_objects_index.append(parser)
            self.parsed_objects_reverse_index[parser.name()] = index

    def show(self, target_file, **kwargs) -> NoReturn:
        for parser in self.parsed_objects_index:
            parser.show(target_file, **kwargs)
