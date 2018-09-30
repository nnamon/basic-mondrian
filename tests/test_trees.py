#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module provides a test of the abstract tree format.
"""

from basic_mondrian.tree import Tree

tree_data = {'Never-married': [], 'Married': ['Married-civ-spouse', 'Married-AF-spouse'],
             'leave': ['Divorced', 'Separated'], 'alone': ['Widowed', 'Married-spouse-absent']}
keys = ['Separated', 'leave', 'Widowed', '*', 'Divorced', 'Married', 'Married-spouse-absent',
        'Never-married', 'Married-AF-spouse', 'alone', 'Married-civ-spouse']


def test_data_to_tree():
    tree = Tree.struct_to_tree(tree_data)
    result = tree.process()
    assert len(result.keys()) == len(keys)
    assert set(result.keys()) == set(keys)
