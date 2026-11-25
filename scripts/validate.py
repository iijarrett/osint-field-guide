#!/usr/bin/env python3
"""Check data/*.yml against the rules in osintlib.validate. Exit 1 on any error."""
import sys

from osintlib import load, load_ignore, load_pivots, real_tools, validate, validate_ignore, validate_pivots


def main():
    sections, tools, skips = load()
    pivots = load_pivots()
    errs = (validate(sections, tools, skips) + validate_ignore(load_ignore())
            + validate_pivots(pivots, sections, tools))
    for e in errs:
        print("error:", e)
    if errs:
        print("%d problem(s)" % len(errs))
        return 1
    print("ok: %d sections, %d tools, %d workflow steps, %d skip entries, %d pivots between %d data types"
          % (len(sections), len(real_tools(tools)), len(tools) - len(real_tools(tools)), len(skips),
             len(pivots["edges"]), len(pivots["nodes"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
