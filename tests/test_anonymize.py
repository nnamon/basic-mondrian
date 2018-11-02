#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module provides a test of the anonymization classes.
"""

from basic_mondrian.anonymize import Anonymizer
from basic_mondrian.tree import Tree

# import itertools

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

expected = ([['greg', '*', 'AAA'],
             ['greg', '*', 'LLL'],
             ['greg', '*', 'MMM'],
             ['connie', '*', 'BBB'],
             ['connie', '*', 'NNN'],
             ['garnet', 'female', 'CCC'],
             ['garnet', 'female', 'DDD'],
             ['amethyst', '*', 'EEE'],
             ['amethyst', '*', 'FFF'],
             ['pearl', 'male', 'HHH'],
             ['pearl', 'male', 'PPP'],
             ['pearl', 'female', 'GGG'],
             ['pearl', 'female', 'OOO'],
             ['peridot', 'male', 'KKK'],
             ['peridot', 'male', 'QQQ'],
             ['peridot', 'female', 'III'],
             ['peridot', 'female', 'JJJ']], 0.0)

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

expected2 = ([['greg', '*', '2,4', 'AAA'],
              ['greg', '*', '2,4', 'LLL'],
              ['human', '*', '5,6', 'BBB'],
              ['human', '*', '5,6', 'MMM'],
              ['human', '*', '5,6', 'NNN'],
              ['gem', 'female', '1,2', 'CCC'],
              ['gem', 'female', '1,2', 'DDD'],
              ['gem', 'female', '1,2', 'OOO'],
              ['gem', 'male', '2', 'HHH'],
              ['gem', 'male', '2', 'KKK'],
              ['gem', 'male', '2', 'PPP'],
              ['gem', '*', '3,4', 'EEE'],
              ['gem', '*', '3,4', 'FFF'],
              ['gem', '*', '3,4', 'QQQ'],
              ['gem', 'female', '5,9', 'GGG'],
              ['gem', 'female', '5,9', 'III'],
              ['gem', 'female', '5,9', 'JJJ']], 22.54901960784314)


data3 = [['greg', 'male', '2', 'AAA'],
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
         ['pink diamond', 'female', '99', 'QQQ']]


data4 = [['greg', 'male', '2', 'AAA', 'WWW', 'XXX'],
         ['connie', 'female', '5', 'BBB', 'WWW', 'XXX'],
         ['garnet', 'female', '1', 'CCC', 'WWW', 'XXX'],
         ['garnet', 'female', '2', 'DDD', 'WWW', 'XXX'],
         ['amethyst', 'female', '3', 'EEE', 'WWW', 'XXX'],
         ['amethyst', 'male', '4', 'FFF', 'WWW', 'XXX'],
         ['pearl', 'female', '5', 'GGG', 'WWW', 'XXX'],
         ['pearl', 'male', '2', 'HHH', 'WWW', 'XXX'],
         ['peridot', 'female', '6', 'III', 'WWW', 'XXX'],
         ['peridot', 'female', '9', 'JJJ', 'WWW', 'XXX'],
         ['peridot', 'male', '2', 'KKK', 'WWW', 'XXX'],
         ['greg', 'female', '4', 'LLL', 'WWW', 'XXX'],
         ['greg', 'female', '5', 'MMM', 'WWW', 'XXX'],
         ['connie', 'male', '6', 'NNN', 'WWW', 'XXX'],
         ['pearl', 'female', '1', 'OOO', 'WWW', 'XXX'],
         ['pearl', 'male', '2', 'PPP', 'WWW', 'XXX'],
         ['pink diamond', 'female', '99', 'QQQ', 'WWW', 'XXX']]

# def compare_result(obja, objb):
# assert type(obja) == type(objb)
# tuples_a, ncma = obja
# tuples_b, ncmb = objb
# assert ncma == ncmb
# for rowa, rowb in itertools.izip(tuples_a, tuples_b):
# for itema, itemb in itertools.izip(rowa, rowb):
# assert itema == itemb


def test_anonymizer():
    sex_tree_instance = Tree.struct_to_tree(gem_tree)
    gem_tree_instance = Tree.struct_to_tree(sex_tree)

    anon = Anonymizer()
    anon.add_tree(sex_tree_instance)
    anon.add_tree(gem_tree_instance)

    assert anon is not None
    result = anon.process(data, k=2, qi_num=2)
    assert type(result) is tuple


def test_anonymizer_numeral():
    sex_tree_instance = Tree.struct_to_tree(gem_tree)
    gem_tree_instance = Tree.struct_to_tree(sex_tree)

    anon = Anonymizer()
    anon.add_tree(sex_tree_instance)
    anon.add_tree(gem_tree_instance)
    anon.add_numrange(0, 11, 1)

    assert anon is not None
    result = anon.process(data2, k=2, qi_num=3)
    assert type(result) is tuple


def test_anonymizer_non_existent():
    sex_tree_instance = Tree.struct_to_tree(gem_tree)
    gem_tree_instance = Tree.struct_to_tree(sex_tree)

    anon = Anonymizer()
    anon.add_tree(sex_tree_instance)
    anon.add_tree(gem_tree_instance)
    anon.add_numrange(0, 11, 1)

    assert anon is not None
    result = anon.process(data3, k=2, qi_num=3, normalize=True)
    assert type(result) is tuple


def test_anonymizer_more_than_one_si():
    sex_tree_instance = Tree.struct_to_tree(gem_tree)
    gem_tree_instance = Tree.struct_to_tree(sex_tree)

    anon = Anonymizer()
    anon.add_tree(sex_tree_instance)
    anon.add_tree(gem_tree_instance)
    anon.add_numrange(0, 11, 1)

    assert anon is not None
    result = anon.process(data4, k=2, qi_num=3, normalize=True)
    assert type(result) is tuple
