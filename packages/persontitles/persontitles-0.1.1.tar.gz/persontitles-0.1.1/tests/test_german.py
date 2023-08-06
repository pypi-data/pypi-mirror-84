#!/usr/bin/env python
# test_german.py
"""Tests for academic_german module."""
import os

from context import academic_german


def test_filenotfound():
    os.remove('./persontitles/academic_german.txt')
    ACADEMIC = academic_german.degrees_ger()
    assert isinstance(ACADEMIC, set)


def test_academic_is_set():

    ACADEMIC = academic_german.degrees_ger()
    assert isinstance(ACADEMIC, set)


def test_degree_in_list():

    ACADEMIC = academic_german.degrees_ger()
    assert 'MBA' in ACADEMIC
    assert 'Dr. e. h.' in ACADEMIC
    assert 'Dr. e. h' not in ACADEMIC
