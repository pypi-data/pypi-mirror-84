from functools import partial as __partial__
from clangast.algorithms.__utility__ import (
    __all_as_kinds_generator__, __cursor_kind__,
    __not_none__, __token_kind__
)


def get_available_cursor_kinds():
    return filter(__not_none__,
                  __cursor_kind__.__dict__["_kinds"])


def get_available_token_kinds():
    return filter(__not_none__,
                  __token_kind__.__dict__["_kinds"])


all_function_declarations_generator = __partial__(__all_as_kinds_generator__,
                                                  [__cursor_kind__.FUNCTION_DECL])
