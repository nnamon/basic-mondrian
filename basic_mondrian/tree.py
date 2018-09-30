#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from .models.gentree import GenTree


class Tree:

    def __init__(self, struct):
        self.struct = struct
        self.dictionary = None

    def process(self):
        if self.dictionary is not None:
            return self.dictionary

        self.dictionary = self.flatten(self.struct)
        return self.dictionary

    @staticmethod
    def struct_to_tree(data):
        return Tree(data)

    @staticmethod
    def json_to_tree(json_data):
        working = json.loads(json_data)
        return Tree.struct_to_tree(working)

    def flatten(self, struct, parent=None, working=None):
        if working is None:
            working = {}

        if parent is None:
            parent = GenTree('*')
            working['*'] = parent

        if type(struct) is dict:
            for i, v in struct.iteritems():
                node = GenTree(i, parent, False)
                self.flatten(v, node, working)
                working[i] = node
        elif type(struct) is list:
            for i in struct:
                leaf = GenTree(i, parent, True)
                working[i] = leaf

        return working
