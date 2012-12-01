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
                assert test.time is not None
            if test.basename == 'YouTubeTest':
                assert test.good
                assert not test.skipped
            if test.basename == 'PastebinTest':
                assert not test.skipped
                if test.methodname == 'test_post':
                    assert test.bad
                    assert 'backend.pastebin_loggedin' in test.message

    def test_hashes(self):
        """ assert hashes are unique """
        assert len(list(hash(t) for t in self.ts)) == len(set(hash(t) for t in self.ts))

    def test_testresult(self):
        assert len(self.tr.failures)
        for f in self.tr.failures:
            if 'pastebin.test.PastebinTest' in repr(f[0]):
                assert 'backend.pastebin_loggedin' in f[1]


class Test1(X, TestCase):
    FILENAME = 'test1.xml'

    def test_notime(self):
        assert self.tr.time is None

    def test_name(self):
        assert self.ts.name == 'nosetests'


class Test2(X, TestCase):
    FILENAME = 'test2.xml'

    def test_time(self):
        assert self.tr.time is not None
        assert str(self.tr.time).startswith('0:00:05.')
