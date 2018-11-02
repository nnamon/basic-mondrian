#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module provides a test of the abstract tree format.
"""

from basic_mondrian.tree import Tree

tree_data = {'Never-married': [], 'Married': ['Married-civ-spouse', 'Married-AF-spouse'],
             'leave': ['Divorced', 'Separated'], 'alone': ['Widowed', 'Married-spouse-absent']}
keys = ['Separated', 'leave', 'Widowed', '*', 'Divorced', 'Married', 'Married-spouse-absent',
        'Never-married', 'Married-AF-spouse', 'alone', 'Married-civ-spouse']

tree_data_3d = {'level1': {'level2': ['one', 'two'], 'level3': []}, 'test2': [], 'test3': []}


def test_data_to_tree():
    tree_instance = Tree.struct_to_tree(tree_data)
    result = tree_instance.process()
    assert len(result.keys()) == len(keys)
    assert set(result.keys()) == set(keys)


def test_data_to_3d_tree():
    tree_instance = Tree.struct_to_tree(tree_data_3d)
    result = tree_instance.process()
    print(result)
    assert len(result.keys()) == 8
