#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mondrian


class Anonymizer:

    def __init__(self, trees=[]):
        self.trees = trees

    def add_tree(self, tree):
        self.trees.append(tree)

    def process(self, data, qi_num=-1):
        if qi_num > len(self.trees):
            return None

        mondrian_instance = mondrian.BasicMondrian(self.trees, data, qi_num)
        results = mondrian_instance.mondrian()

        return results
