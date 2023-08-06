from clangast.algorithms.elements_parsing import UnitParser
from clangast.algorithms.tools import get_translation_unit_index


def parse_file(path_to_file: str, **kwargs) -> UnitParser:
    parser = UnitParser(get_translation_unit_index(path_to_file, **kwargs))
    parser.parse()
    return parser
