#!/usr/bin/env python
# test_degrees.py
"""Tests for academic degrees."""
import os

from context import academic_degrees


def test_degrees_is_dict():
    os.remove('./persontitles/degrees.json')
    DEGREES = academic_degrees.degrees()
    assert isinstance(DEGREES, dict)


def test_keys():
    DEGREES = academic_degrees.degrees()
    for k, v in DEGREES.items():
        assert k in ['GER', 'UK', 'US']
