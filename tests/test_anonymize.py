#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module provides a test of the anonymization classes.
"""

from basic_mondrian.anonymize import Anonymizer
from basic_mondrian.tree import Tree

sex_tree = {'male': [], 'female': []}
gem_tree = {'gem': ['garnet', 'amethyst', 'pearl', 'peridot'], 'human': ['greg', 'connie']}
data = [['greg', 'male', 'AAA'],
        ['connie', 'female', 'BBB'],
        ['garnet', 'female', 'CCC'],
        ['garnet', 'female', 'DDD'],
        ['amethyst', 'female', 'EEE'],
        ['amethyst', 'male', 'FFF'],
        ['pearl', 'female', 'GGG'],
        ['pearl', 'male', 'HHH'],
        ['peridot', 'female', 'III'],
        ['peridot', 'female', 'JJJ'],
        ['peridot', 'male', 'KKK'],
        ['greg', 'female', 'LLL'],
        ['greg', 'female', 'MMM'],
        ['connie', 'male', 'NNN'],
        ['pearl', 'female', 'OOO'],
        ['pearl', 'male', 'PPP'],
        ['peridot', 'male', 'QQQ']]

expected = ([['greg', '*', 'AAA'], ['greg', '*', 'LLL'], ['greg', '*', 'MMM'],
             ['connie', '*', 'BBB'], ['connie', '*', 'NNN'], ['garnet', 'female', 'CCC'],
             ['garnet', 'female', 'DDD'], ['amethyst', '*', 'EEE'], ['amethyst', '*', 'FFF'],
             ['pearl', 'male', 'HHH'], ['pearl', 'male', 'PPP'], ['pearl', 'female', 'GGG'],
             ['pearl', 'female', 'OOO'], ['peridot', 'male', 'KKK'], ['peridot', 'male', 'QQQ'],
             ['peridot', 'female', 'III'], ['peridot', 'female', 'JJJ']], 0.0)

data2 = [['greg', 'male', '2', 'AAA'],
         ['connie', 'female', '5', 'BBB'],
         ['garnet', 'female', '1', 'CCC'],
         ['garnet', 'female', '2', 'DDD'],
         ['amethyst', 'female', '3', 'EEE'],
         ['amethyst', 'male', '4', 'FFF'],
         ['pearl', 'female', '5', 'GGG'],
         ['pearl', 'male', '2', 'HHH'],
         ['peridot', 'female', '6', 'III'],
         ['peridot', 'female', '9', 'JJJ'],
         ['peridot', 'male', '2', 'KKK'],
         ['greg', 'female', '4', 'LLL'],
         ['greg', 'female', '5', 'MMM'],
         ['connie', 'male', '6', 'NNN'],
         ['pearl', 'female', '1', 'OOO'],
         ['pearl', 'male', '2', 'PPP'],
         ['peridot', 'male', '3', 'QQQ']]


def test_anonymizer():
    sex_tree_instance = Tree.struct_to_tree(gem_tree)
    gem_tree_instance = Tree.struct_to_tree(sex_tree)

    anon = Anonymizer()
    anon.add_tree(sex_tree_instance)
    anon.add_tree(gem_tree_instance)

    assert anon is not None
    result = anon.process(data, k=2, qi_num=2)
    assert type(result) is tuple


def test_anonymizer2():
    sex_tree_instance = Tree.struct_to_tree(gem_tree)
    gem_tree_instance = Tree.struct_to_tree(sex_tree)

    anon = Anonymizer()
    anon.add_tree(sex_tree_instance)
    anon.add_tree(gem_tree_instance)
    anon.add_numrange(0, 11, 1)

    assert anon is not None
    result = anon.process(data2, k=2, qi_num=3)
    assert type(result) is tuple
