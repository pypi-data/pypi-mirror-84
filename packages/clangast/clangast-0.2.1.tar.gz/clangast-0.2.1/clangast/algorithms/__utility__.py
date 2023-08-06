from clang import cindex as __cursor_index__

__token_kind__ = __cursor_index__.TokenKind
__cursor_kind__ = __cursor_index__.CursorKind

from typing import Any as __Any__

__CLANG_INIT__ = False

from typing import List as __List__


def __init_clang__(_path_to_lib: str):
    global __CLANG_INIT__
    if not __CLANG_INIT__:
        __cursor_index__.Config.set_library_file(_path_to_lib)
        __CLANG_INIT__ = True


def __not_none__(_any: __Any__) -> bool:
    return _any is not None


def __all_as_kinds_generator__(kinds: __List__[__cursor_index__.CursorKind], cursor: __cursor_index__.Cursor):
    for element in list(cursor.get_children())[::-1]:
        if element.kind in kinds:
            yield element
