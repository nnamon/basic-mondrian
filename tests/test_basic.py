#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module provides a test of the internal Basic Mondrian algorithm.
"""

import basic_mondrian.mondrian
from basic_mondrian.models.gentree import GenTree
from basic_mondrian.models.numrange import NumRange

expected = ([['4', '1,2', 'hha'], ['4', '1,2', 'hha'], ['4', '3,4', 'hha'], ['4', '3,4', 'hha'],
             ['6', '1', 'haha'], ['6', '1', 'test'], ['8', '2', 'haha'], ['8', '2', 'test']],
            2.7777777777777777)

expected2 = ([['1,5', '1', 'hha'], ['1,5', '1', 'hha'], ['1,5', '1', 'hha'], ['1,5', '1', 'hha'],
              ['6', '1', 'haha'], ['6', '1', 'test'], ['8', '2', 'haha'], ['8', '2', 'test']], 12.5)


def test_basic_one():
    """Tests that the results match the expected result.
    """
    ATT_TREE = []
    tree_temp = {}
    tree = GenTree('*')
    tree_temp['*'] = tree
    lt = GenTree('1,5', tree)
    tree_temp['1,5'] = lt
    rt = GenTree('6,10', tree)
    tree_temp['6,10'] = rt
    for i in range(1, 11):
        if i <= 5:
            t = GenTree(str(i), lt, True)
        else:
            t = GenTree(str(i), rt, True)
        tree_temp[str(i)] = t
    numrange = NumRange(['1', '2', '3', '4', '5',
                         '6', '7', '8', '9', '10'], dict())
    ATT_TREE.append(tree_temp)
    ATT_TREE.append(numrange)

    data = [['6', '1', 'haha'],
            ['6', '1', 'test'],
            ['8', '2', 'haha'],
            ['8', '2', 'test'],
            ['4', '1', 'hha'],
            ['4', '2', 'hha'],
            ['4', '3', 'hha'],
            ['4', '4', 'hha']]

    mondrian_instance = basic_mondrian.mondrian.BasicMondrian(ATT_TREE, data, 2)
    result = mondrian_instance.mondrian()
    assert result == expected


def test_basic_two():
    """Tests that the results match the expected result.
    """
    ATT_TREE = []
    tree_temp = {}
    tree = GenTree('*')
    tree_temp['*'] = tree
    lt = GenTree('1,5', tree)
    tree_temp['1,5'] = lt
    rt = GenTree('6,10', tree)
    tree_temp['6,10'] = rt
    for i in range(1, 11):
        if i <= 5:
            t = GenTree(str(i), lt, True)
        else:
            t = GenTree(str(i), rt, True)
        tree_temp[str(i)] = t
    numrange = NumRange(['1', '2', '3', '4', '5',
                         '6', '7', '8', '9', '10'], dict())
    ATT_TREE.append(tree_temp)
    ATT_TREE.append(numrange)

    data = [['6', '1', 'haha'],
            ['6', '1', 'test'],
            ['8', '2', 'haha'],
            ['8', '2', 'test'],
            ['4', '1', 'hha'],
            ['4', '1', 'hha'],
            ['1', '1', 'hha'],
            ['2', '1', 'hha']]

    mondrian_instance = basic_mondrian.mondrian.BasicMondrian(ATT_TREE, data, 2)
    result = mondrian_instance.mondrian()
    assert result == expected2
