#!/usr/bin/env python
from xunitparser import parse
from unittest import TestCase


class XupTest(TestCase):
    def setUp(self):
        """ read the default file """
        with open('penguin-1352619250.xml') as f:
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
