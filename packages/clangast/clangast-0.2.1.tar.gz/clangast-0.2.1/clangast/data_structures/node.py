from clang import cindex
from typing import List, Dict, Hashable, Any
from functools import wraps

import sys


class BaseNode(object):
    index_type = List[Any]
    reverse_index_type = Dict[Hashable, int]

    @staticmethod
    def __first_argument_is_string__(method):
        @wraps(method)
        def __check__(self, arg, *args, **kwargs):
            if type(arg) != str:
                raise TypeError(f"First argument must be string; type of first element: {type(arg)}")
            return method(self, arg, *args, **kwargs)

        return __check__

    @__first_argument_is_string__.__get__(object)
    def __init__(self, spelling: str, kind: cindex.CursorKind):
        """
        Base class for trees nodes

        :param spelling: Name of element; str
        :param kind: kind of element; clang.cindex.CursorKind
        """
        self._index: index_type = []
        self._reverse_index: reverse_index_type = {}

        self._name: str = spelling
        self._kind: cindex.CursorKind = kind

        self._additional = list()

        self._pretty_print_offset = ""

    @staticmethod
    def __node_type__(element):
        return type(element) == BaseNode

    @staticmethod
    def __only_node_type__(method):
        @wraps(method)
        def __check_type__(self, element, *args, **kwargs):
            if not BaseNode.__node_type__(element):
                raise TypeError(f"Must be Node type; type of element: {type(element)}")
            return method(self, element, *args, **kwargs)

        return __check_type__

    def __hash__(self):
        return self._name.__hash__()

    def __next__(self):
        for something in self._additional:
            yield something

    @__only_node_type__.__get__(object)
    def __eq__(self, element):
        return self._name == element.name()

    def __ne__(self, element):
        return not (self.__eq__(element))

    def __getitem__(self, key: int):
        """
        If index in child return child by index.
        Else return None

        :param key: int
        :return: BaseNode instance or None
        """
        if 0 <= key < len(self):
            return self._index[key]
        return None

    def __len__(self):
        return len(self._index)

    def __str__(self):
        self_description = f"{self._pretty_print_offset}Kind:\t{self._kind}\n{self._pretty_print_offset}Name:\t{self._name}\n"
        end_line = f"{self._pretty_print_offset}--------------"
        storage = self._pretty_print_offset + f"\n{self._pretty_print_offset}".join(
            (str(store_element) for store_element in self._additional))
        storage = f"{self._pretty_print_offset}Store:\n{storage}\n"
        return f"{self_description}{storage}{end_line}"

    def empty(self) -> bool:
        """
        Return true is node has not child

        :return: bool
        """
        return len(self) == 0

    def name(self) -> str:
        """
        Get name of element

        :return: string
        """
        return self._name

    def kind(self) -> cindex.CursorKind:
        """
        Get cursor kind of element

        :return: clang.cindex.CursorKind
        """
        return self._kind

    @__only_node_type__.__get__(object)
    def has(self, element) -> bool:
        """
        Return True if element has in children of elements

        :param element: BaseNode instance
        :return: bool
        """
        return element in self._reverse_index

    def has_by_name(self, name: str) -> bool:
        """
        Return True if element with name in child of elements

        :param name: string
        :return: bool
        """
        return self.has(BaseNode(name, None))

    @__only_node_type__.__get__(object)
    def add(self, element) -> bool:
        """
        Adding new element to child if it isn't in.
        Return true if adding has finished success.

        :param element: BaseNode instance
        :return: bool
        """
        if self.has(element):
            return False

        index = len(self)
        self._index.append(element)
        self._reverse_index[element] = index

        return True

    @__only_node_type__.__get__(object)
    def index(self, element) -> int:
        """
        Get integer index of element

        :param element: BaseNode instance
        :return: int
        """
        if self.has(element):
            return self._reverse_index[element]
        return len(self)

    def index_by_name(self, name: str) -> int:
        """
        Get integer index of element by name. Searching uses only name.
        Useful with get item by []

        :param name: string
        :return: int
        """
        return self.index(BaseNode(name, None))

    def store(self, something):
        """
        Store something to additional storage of node

        :param something: Any
        :return: None
        """
        self._additional.append(something)

    def get_from_store(self, index: int) -> Any:
        """
        Get element from additional storage element by index.
        For iterating over this storage better use iterating over node with `for <> in <>`.

        :param index: int
        :return: Any if element in storage. None another.
        """
        if index < len(self._additional):
            return self._additional[index]
        return None

    def show(self, offset: str = None, offset_block: str = None,
             target_file=None):
        """
        Pretty output current node info and its childs info with offset

        :param offset: symbols before line, default is 2 space
        :param offset_block: step for offset increasing, default is 2 space
        :param target_file: descriptor for printing, default is stdout
        :return: None
        """
        prev_offset = self._pretty_print_offset
        if offset is None:
            offset = prev_offset
        self._pretty_print_offset = offset

        if offset_block is None:
            offset_block = "  "

        if target_file is None:
            target_file = sys.stdout

        print(self, file=target_file)
        print(f"{offset}[", file=target_file)
        for i in range(0, len(self)):
            self._index[i].show(offset + offset_block, offset_block, target_file)
        print(f"{offset}]", file=target_file)

        self._pretty_print_offset = prev_offset
