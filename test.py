#!/usr/bin/env python
from xunitparser import parse

def test_read():
    with open('penguin-1352619250.xml') as f:
        tr, ts = parse(f)
        print ts
