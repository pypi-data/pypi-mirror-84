from clangast.data_structures.node import BaseNode
from typing import List, Union, DefaultDict
from collections import defaultdict
from functools import wraps

import sys


class BaseTree(object):
    reverse_index_type = DefaultDict[BaseNode, List[List[int]]]

    @staticmethod
    def __not_empty_tree__(method):
        @wraps(method)
        def __check__(self, *args, **kwargs):
            if self.empty():
                raise RuntimeError("Empty tree")
            method(self, *args, **kwargs)

        return __check__

    @staticmethod
    def __child_indexing_after__(method):
        @wraps(method)
        def __perform__(self, element, *args, **kwargs):
            result = method(self, element, *args, **kwargs)
            if result == 1:
                self.__child_indexing__(element, self.__last_inserted_path)
            return result

        return __perform__

    def __init__(self, root: BaseNode = None):
        self._root = root
        self._counter = 0
        self._reverse_index: reverse_index_type = defaultdict(list)

        if self._root is not None:
            self._counter += 1

        self.__last_inserted_path: List[int] = []

    def __len__(self) -> int:
        return self._counter

    @__not_empty_tree__.__get__(object)
    def __merger_reverse_index_modified_paths__(self, another_reverse_index: reverse_index_type,
                                                additional_path: List[int]):
        for element, paths in another_reverse_index.items():
            modified_paths = []
            for path in paths:
                modified_paths.append(path + additional_path)
            self.__add_paths__(element, modified_paths)

    @__not_empty_tree__.__get__(object)
    def __merge_reverse_index__(self, another_reverse_index: reverse_index_type, additional_path: List[int] = None):
        if additional_path is None:
            for element, paths in another_reverse_index.items():
                self.__add_paths__(element, paths)
        else:
            self.__merger_reverse_index_modified_paths__(another_reverse_index, additional_path)

    def __get_reverse_index__(self) -> reverse_index_type:
        return self._reverse_index

    def __get_root__(self) -> BaseNode:
        return self._root

    @BaseNode.__only_node_type__
    @__not_empty_tree__.__get__(object)
    def __child_indexing__(self, element: BaseNode, path_to_element: List[int]):
        for i in range(0, len(element)):
            child = element[i]
            if not child.empty():
                self.__child_indexing__(child, path_to_element + [i])
            self._reverse_index[child].append(path_to_element + [i])

    @BaseNode.__only_node_type__
    def __add_paths__(self, element: BaseNode, paths: List[List[int]]):
        self._counter += len(paths)
        self._reverse_index[element] += paths
        self.__last_inserted_path = paths[-1]

    @BaseNode.__only_node_type__
    def __add_path__(self, element: BaseNode, path: List[int], *args):
        path += args
        self._counter += 1
        self._reverse_index[element].append(path)
        self.__last_inserted_path = path

    def __str__(self):
        if self.empty():
            return ""
        else:
            return f"Root name: {self._root.name()}\nRoot kind: {self._root.kind()}\n--------------------"

    def empty(self):
        return len(self) == 0

    @BaseNode.__only_node_type__
    @__child_indexing_after__.__get__(object)
    def set_root(self, element: BaseNode) -> int:
        """
        Set root element.
        Return 1 if root was set.
        If root was existed, return 0.

        :param element: BaseNode instance
        :return: int
        """
        if self._root is None:
            self._root = element
            self.__add_path__(self._root, [])
            return 1

        return 0

    @__not_empty_tree__.__get__(object)
    def get(self, path: List[int]) -> Union[BaseNode, None]:
        """
        Get BaseNode instance from tree.

        Return None if element isn't in tree or path is wrong.

        :param path: List of integer index
        :return: BaseNode instance or None
        """
        node: BaseNode = self._root
        for ind in path:
            node = node[ind]
            if node is None:
                return None
        return node

    @__not_empty_tree__.__get__(object)
    @__child_indexing_after__.__get__(object)
    def add(self, element: BaseNode, path: List[int]) -> int:
        """
        Adding element to tree.

        Return -1 if path for adding is wrong.

        Return 0 is element with its name is already in tree.

        Else return 1

        :param path: list of indexes
        :param element: BaseNode instance
        :return: int
        """
        node: BaseNode = self._root
        for ind in path:
            node = node[ind]
            if node is None:
                return -1

        index = len(node)
        if node.add(element):
            self.__add_path__(element, path, index)
            return 1
        return 0

    @BaseNode.__only_node_type__
    def paths(self, element: BaseNode) -> List[List[int]]:
        """
        Return all known paths to element in tree

        :param element: BaseNode instance
        :return: list of paths to element
        """
        if element in self._reverse_index:
            return self._reverse_index[element]
        return []

    def paths_generator(self, element: BaseNode):
        """
        Generator for path returning

        :param element: BaseNode instance
        :return: one path on every step
        """
        for path in self.paths(element):
            yield path

    def paths_by_name(self, name: str) -> List[List[int]]:
        """
        Get paths to element by name

        :param name: string
        :return: list of paths
        """
        return self.paths(BaseNode(name, None))

    def paths_generator_by_name(self, name: str):
        """
        Generator for paths to element by name

        :param name: str
        :return: one path on every step
        """
        for path in self.paths(BaseNode(name, None)):
            yield path

    def show(self, target_file=None, **kwargs):
        """
        In depth first tree printing

        :param target_file: if none show in stdout. Else it uses target_file for outputting
        :return: None
        """
        if target_file is None:
            target_file = sys.stdout
        print(self, file=target_file)
        self._root.show(target_file=target_file, **kwargs)
