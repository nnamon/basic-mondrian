#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mondrian


class Anonymizer:

    def __init__(self, trees=[]):
        self.trees = trees

    def add_tree(self, tree):
        self.trees.append(tree)

    def process(self, data, k=10, qi_num=-1):
        if qi_num > len(self.trees):
            return None

        active_trees = []
        for i in self.trees:
            active_trees.append(i.process())

        mondrian_instance = mondrian.BasicMondrian(active_trees, data, k, qi_num)
        results = mondrian_instance.mondrian()

        return results
