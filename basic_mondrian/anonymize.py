#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy

from . import mondrian
from .tree import NumTree, Tree

X_ELEMENT = 0
Y_ELEMENT = 1
FIRST_ELEMENT = 0


class Anonymizer:

    def __init__(self, trees=None):
        if trees is None:
            trees = []
        self.trees = trees

    def add_tree(self, tree):
        self.trees.append(tree)

    def add_numrange(self, start, end, step):
        self.trees.append(NumTree(start, end, step))

    def normalize_tree_rows(self, data, current_tree, index):
        for row in data:
            value = row[index]
            if not current_tree.covers(value):
                current_tree.extend(value)

    def normalize_numtree_rows(self, data, current_tree, index):
        for row in data:
            value = row[index]
            if not current_tree.covers(value):
                current_tree.extend(value)

    def normalize_data(self, data, qi_num):
        '''Normalizes a two-dimensional data set by suppressing unknown categories or adding them.

        This occurs in place.
        '''
        for index in range(qi_num):
            current_tree = self.trees[index]
            if isinstance(current_tree, Tree):
                self.normalize_tree_rows(data, current_tree, index)
            elif isinstance(current_tree, NumTree):
                self.normalize_numtree_rows(data, current_tree, index)
            else:
                raise Exception('Unknown tree type during normalization.')

    def list_shape(self, data):
        if type(data) != list:
            raise Exception('Cannot tell a shape from a non-list.')

        ptr = data
        shape_list = []

        while True:
            length = len(ptr)
            shape_list.append(length)
            if length == 0 or type(ptr[FIRST_ELEMENT]) is not list:
                break
            ptr = ptr[FIRST_ELEMENT]

        return tuple(shape_list)

    def validate_shape(self, data, rows, columns):
        '''Validate a two-dimensional list.

        Args:
            data (list): a list to validate.
            rows (int): the number of rows.
            columns (int): the number of columns.

        Returns:
            bool: indicates if the data passes.
        '''
        if len(data) != rows:
            return False

        for row in data:
            if len(row) != columns:
                return False

        return True

    def process(self, data, k=10, qi_num=-1, normalize=False):
        '''Anonymize a two-dimensional tuple.

        Args:
            data (list): a two-dimensional list of values to anonymize.
            k (int): the k-value to satisfy.
            qi_num (int): the number of quasi-identifiable columns to the left.
            normalize (bool): determine whether to automatically generalize non-existent categories.

        Returns:
            list: a two-dimensional list of anonymized data.
        '''
        if qi_num > len(self.trees):
            raise Exception('Insufficient number of generalization trees.')

        shape = self.list_shape(data)

        if len(shape) != 2:
            raise Exception('Data is not a two-dimensional list.')

        if not self.validate_shape(data, shape[X_ELEMENT], shape[Y_ELEMENT]):
            raise Exception('Data is not a uniform two-dimensional list.')

        if qi_num < 0:
            qi_num = shape[Y_ELEMENT]

        data_copy = copy.deepcopy(data)

        if normalize:
            self.normalize_data(data_copy, qi_num)

        active_trees = []
        for i in self.trees:
            active_trees.append(i.process())

        mondrian_instance = mondrian.BasicMondrian(active_trees, data_copy, k, qi_num)
        results = mondrian_instance.mondrian()

        return results
