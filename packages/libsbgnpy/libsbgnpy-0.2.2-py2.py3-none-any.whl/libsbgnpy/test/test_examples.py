#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test the example scripts in the examples folder.
"""
import os

from libsbgnpy.examples.info_example import info_example
from libsbgnpy.examples.read_example import read_sbgn_01
from libsbgnpy.examples.write_example import write_sbgn_01, write_sbgn_02, write_sbgn_03


directory = os.path.dirname(os.path.realpath(__file__))


def test_read_examples():
    """ Parse SBGN file test. """
    files = [
        "sbgn/adh.sbgn",
        "sbgn/glycolysis.sbgn",
        "sbgn/test-output-01.sbgn",
        "sbgn/test-output-02.sbgn",
    ]
    for f_in in files:
        f = os.path.join(directory, "../examples/{0}".format(f_in))
        sbgn = read_sbgn_01(f)
        assert sbgn is not None


def test_write_example_01():
    """ Write SBGN file test. """
    f_out = "sbgn/test-output-01.sbgn"
    f = os.path.join(directory, "../examples/{0}".format(f_out))
    write_sbgn_01(f)


def test_write_example_02():
    f_out = "sbgn/test-output-02.sbgn"
    f = os.path.join(directory, "../examples/{0}".format(f_out))
    write_sbgn_02(f)


def test_write_example_03():
    f_out = "sbgn/test-output-03.sbgn"
    f = os.path.join(directory, "../examples/{0}".format(f_out))
    write_sbgn_03(f)


def test_write_read_example_01():
    f_out = "sbgn/test-output-01.sbgn"
    f = os.path.join(directory, "../examples/{0}".format(f_out))
    write_sbgn_01(f)
    sbgn = read_sbgn_01(f)
    assert sbgn is not None


def test_write_read_example_02():
    f_out = "sbgn/test-output-02.sbgn"
    f = os.path.join(directory, "../examples/{0}".format(f_out))
    write_sbgn_02(f)
    sbgn = read_sbgn_01(f)
    assert sbgn is not None


def test_write_read_example_03():
    f_out = "sbgn/test-output-03.sbgn"
    f = os.path.join(directory, "../examples/{0}".format(f_out))
    write_sbgn_03(f)
    sbgn = read_sbgn_01(f)
    assert sbgn is not None


def test_info_example():
    info_example()
