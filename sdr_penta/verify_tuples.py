#!/usr/bin/env python3
"""PENTA-CL tuple verification: canonical form = json.dumps(tuples, separators=(',',':')).encode(), sha256.
Expected: 3254a8a8c586f678408d702d429005da9f23648e34d489c21f0527aaef330d0d"""
import json, hashlib, sys
expected = json.load(open('expected_tuples_rule_pure.json'))
exp_hash = hashlib.sha256(json.dumps(expected, separators=(',',':')).encode()).hexdigest()
for path in sys.argv[1:]:
    got = json.load(open(path))
    h = hashlib.sha256(json.dumps(got, separators=(',',':')).encode()).hexdigest()
    print(path, "->", h, "MATCH" if h == exp_hash else "DIVERGED")
