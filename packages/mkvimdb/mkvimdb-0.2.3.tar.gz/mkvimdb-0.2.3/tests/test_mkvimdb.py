#!/usr/bin/env python

"""Tests for `mkvimdb` package."""


import unittest

from mkvimdb import mkvimdb


class TestMkvimdb(unittest.TestCase):
    """Tests for `mkvimdb` package."""

    def setUp(self):
        """Give us an IMDB browser object"""
        self.m = mkvimdb.moviecursor()

    def tearDown(self):
        """Tear down test fixtures, if any."""
        pass

    def test_default_query(self):
        """We should see the right canonical name for Pulp Fiction (1994)."""
        self.assertEqual(self.m.tagdata['filename'], 'tarantino,quentin-pulp_fiction-1994', 'Misidentified film!')
