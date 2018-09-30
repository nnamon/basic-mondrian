#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module provides a test of the anonymization classes.
"""

from basic_mondrian.anonymize import Anonymizer


def test_anonymizer():
    anon = Anonymizer()
    assert anon is not None
