#!/usr/bin/env python
from xunitparser import parse
from unittest import TestCase


class X(object):
    def setUp(self):
        with open(self.FILENAME) as f:
            # the lib already does some sanity checks;
            # passing this is already a good test in itself
            self.ts, self.tr = parse(f)

    def test_results(self):
        """ check some expected results """
        for test in self.ts:
            if test.basename == 'ArteTest':
                assert test.good
                assert test.skipped
            if test.basename == 'YouTubeTest':
                assert test.good
                assert not test.skipped
            if test.basename == 'PastebinTest':
                assert not test.skipped
                if test.methodname == 'test_post':
                    assert test.bad

    def test_hashes(self):
        """ assert hashes are unique """
        assert len(list(hash(t) for t in self.ts)) == len(set(hash(t) for t in self.ts))


class Test1(X, TestCase):
    FILENAME = 'test1.xml'


class Test2(X, TestCase):
    FILENAME = 'test2.xml'
