#!/usr/bin/env python
from xunitparser import parse


def test_read():
    with open('penguin-1352619250.xml') as f:
        ts, tr = parse(f)
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
