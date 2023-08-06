from clangast.data_structures.tree import BaseTree as Tree
from clangast.algorithms.utility import (
    all_function_declarations_generator
)
from clangast.algorithms.__parsing__ import (
    __parse_function__, __cursor_index__
)

from typing import List, Any, Generator

TranslationUnit = __cursor_index__.TranslationUnit


def get_translation_unit_index(path_to_file: str, **kwargs) -> TranslationUnit:
    return __cursor_index__.Index.create().parse(path_to_file, **kwargs)


def parse_translation_unit_generator(unit: TranslationUnit) -> Generator[Tree, Any, None]:
    for function_declaration in all_function_declarations_generator(unit.cursor):
        yield __parse_function__(function_declaration)


def parse_translation_unit(unit: TranslationUnit) -> List[Tree]:
    return list(parse_translation_unit_generator(unit))
