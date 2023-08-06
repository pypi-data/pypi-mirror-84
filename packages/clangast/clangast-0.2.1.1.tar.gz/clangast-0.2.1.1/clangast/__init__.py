from clangast.data_structures import Tree, StackingPipeline
from clangast.algorithms import parse_file

from clangast.algorithms.tools import init_clang

default_path_to_library = "/usr/lib/libclang.so"

init_clang(default_path_to_library)

__all__ = [
    "Tree", "StackingPipeline", "parse_file"
]
