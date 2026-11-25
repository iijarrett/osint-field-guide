#!/usr/bin/env python3
"""Check data/*.yml against the rules in osintlib.validate. Exit 1 on any error."""
import sys

from osintlib import load, real_tools, validate


def main():
    sections, tools, skips = load()
    errs = validate(sections, tools, skips)
    for e in errs:
        print("error:", e)
    if errs:
        print("%d problem(s)" % len(errs))
        return 1
    print("ok: %d sections, %d tools, %d workflow steps, %d skip entries"
          % (len(sections), len(real_tools(tools)), len(tools) - len(real_tools(tools)), len(skips)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
