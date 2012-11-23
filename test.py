#!/usr/bin/env python
from xunitparser import parse


def test_read():
    with open('penguin-1352619250.xml') as f:
        # the lib already does some sanity checks;
        # passing this is already a good test in itself
        ts, tr = parse(f)

        # check some expected results
        for test in ts:
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

        # assert hashes are unique
        assert len(list(hash(t) for t in ts)) == len(set(hash(t) for t in ts))
