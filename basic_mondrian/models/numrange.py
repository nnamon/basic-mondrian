#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module implements the numerical ranges for the taxonomy tree.
"""


class NumRange(object):

    """Class for Generalization hierarchies (Taxonomy Tree).

    Store numeric node in instances.

    Attributes:
        sort_value (list): sorted values, which may help get the normalized width
        value (str): node value, e.g. '10,20'
        support (): support (frequency) of all values, dict
        range (float): (max-min), used for normalized width
    """

    def __init__(self, sort_value, support):
        self.sort_value = list(sort_value)
        self.support = support.copy()
        # sometimes the values may be str
        self.range = float(sort_value[-1]) - float(sort_value[0])
        self.dict = {}
        for i, v in enumerate(sort_value):
            self.dict[v] = i
        self.value = sort_value[0] + ',' + sort_value[-1]
