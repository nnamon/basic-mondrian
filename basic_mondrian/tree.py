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

        self.dictionary = self.__flatten(self.struct)
        return self.dictionary

    @classmethod
    def struct_to_tree(cls, data):
        return cls(data)

    @classmethod
    def json_to_tree(cls, json_data):
        working = json.loads(json_data)
        return cls.struct_to_tree(working)

    @classmethod
    def __flatten(cls, struct, parent=None, working={}):
        if parent is None:
            parent = GenTree('*')
            working['*'] = parent

        if type(struct) is dict:
            for i, v in struct.iteritems():
                node = GenTree(i, parent, False)
                cls.__flatten(v, node, working)
                working.setdefault(i, node)
        elif type(struct) is list:
            for i in struct:
                leaf = GenTree(i, parent, True)
                working.setdefault(i, leaf)

        return working
