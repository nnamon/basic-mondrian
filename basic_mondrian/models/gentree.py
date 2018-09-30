#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module provides an implementation of a generalisation tree.
"""


class GenTree(object):

    """Class for Generalization hierarchies (Taxonomy Tree).

    Store tree node in instances.

    Attributes:
        value (str): node value
        level (int): tree level (top is 0)
        leaf_num (int): number of leaf node covered
        parent (list): ancestor node list
        child (list): direct successor node list
        cover (dict): all nodes covered by current node
    """

    def __init__(self, value=None, parent=None, isleaf=False):
        self.value = ''
        self.level = 0
        self.leaf_num = 0
        self.parent = []
        self.child = []
        self.cover = {}
        if value is not None:
            self.value = value
            self.cover[value] = self
        if parent is not None:
            self.parent = parent.parent[:]
            self.parent.insert(0, parent)
            parent.child.append(self)
            self.level = parent.level + 1
            for t in self.parent:
                t.cover[self.value] = self
                if isleaf:
                    t.leaf_num += 1

    def node(self, value):
        """Search tree with value, return GenTree node.

        Returns:
            GenTree: requested node, or None if it does not exist
        """
        try:
            return self.cover[value]
        except Exception:
            return None

    def __len__(self):
        """
        Returns:
            int: number of leaf nodes covered by current node
        """
        return self.leaf_num

    def __repr__(self):
        return '@%s: %s' % (self.value, self.child)
