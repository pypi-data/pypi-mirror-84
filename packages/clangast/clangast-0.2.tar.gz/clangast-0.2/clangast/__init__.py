from clangast.data_structures.node import BaseNode as Node
from clangast.data_structures.tree import BaseTree as Tree

from clangast.algorithms.parsing import (
    get_translation_unit_index, parse_translation_unit,
    parse_translation_unit_generator
)

from clangast.algorithms.__utility__ import __init_clang__

__default_path_to_library = "/usr/lib/libclang.so"
__file_with_path = "clangast/path_to_so.txt"

__init_clang__(__file_with_path, __default_path_to_library)

__all__ = [
    "Node", "Tree",
    "get_translation_unit_index", "parse_translation_unit",
    "parse_translation_unit_generator"
]
