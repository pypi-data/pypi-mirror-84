from clang.cindex import CursorKind, Cursor, Index, TranslationUnit
from clang import cindex

from typing import Any, List

CLANG_INIT = False


def init_clang(_path_to_lib: str):
    global CLANG_INIT
    if not CLANG_INIT:
        cindex.Config.set_library_file(_path_to_lib)
        CLANG_INIT = True


def not_none(value: Any) -> bool:
    return value is not None


def all_as_kinds_generator(kinds: List[CursorKind], cursor: Cursor):
    for element in list(cursor.get_children())[::-1]:
        if element.kind in kinds:
            yield element


def get_translation_unit_index(path_to_file: str, **kwargs) -> TranslationUnit:
    return Index.create().parse(path_to_file, **kwargs)
