#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module provides a test of the anonymization classes.
"""

from basic_mondrian.anonymize import Anonymizer
from basic_mondrian.tree import Tree
from prettytable import PrettyTable

sex_tree = {'male': [], 'female': []}
gem_tree = {'gem': ['garnet', 'amethyst', 'pearl', 'peridot'], 'human': ['greg', 'connie']}

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


def main():
    # Print the original data
    original = PrettyTable(['Name', 'Sex', 'Age', 'Sensitive Data'])
    for row in data3:
        original.add_row(row)
    print 'Original Data'
    print original

    # Construct the anonymizer
    sex_tree_instance = Tree.struct_to_tree(gem_tree)
    gem_tree_instance = Tree.struct_to_tree(sex_tree)

    anon = Anonymizer()
    anon.add_tree(sex_tree_instance)
    anon.add_tree(gem_tree_instance)
    anon.add_numrange(0, 11, 1)

    # Print when k=2
    result1, ncp1 = anon.process(data3, k=2, qi_num=3, normalize=True)
    k2 = PrettyTable(['Name', 'Sex', 'Age', 'Sensitive Data'])
    for row in result1:
        k2.add_row(row)
    print '\nAnonymized k=2 (ncp = %.2f%%)' % ncp1
    print k2

    # Print when k=3
    result2, ncp2 = anon.process(data3, k=3, qi_num=3, normalize=True)
    k3 = PrettyTable(['Name', 'Sex', 'Age', 'Sensitive Data'])
    for row in result2:
        k3.add_row(row)
    print '\nAnonymized k=3 (ncp = %.2f%%)' % ncp2
    print k3


if __name__ == '__main__':
    main()
