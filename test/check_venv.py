"""Simple environment check for the repo.

This script tests whether Flask can be imported from the current Python
environment. It no longer mutates sys.path.
"""

import importlib


def main():
    try:
        flask = importlib.import_module('flask')
        print('Flask version:', getattr(flask, '__version__', 'unknown'))
    except Exception as e:
        print('Failed to import Flask:', e)


if __name__ == '__main__':
    main()

