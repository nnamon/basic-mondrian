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


def test_anonymizer():
    sex_tree_instance = Tree.struct_to_tree(gem_tree)
    gem_tree_instance = Tree.struct_to_tree(sex_tree)

    anon = Anonymizer()
    anon.add_tree(sex_tree_instance)
    anon.add_tree(gem_tree_instance)

    assert anon is not None
    result = anon.process(data, k=2, qi_num=2)
    assert type(result) is tuple
