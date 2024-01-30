#!/usr/bin/python3
import argparse
import os
import sys
from pycodestyle import StyleGuide

def main():
    parser = argparse.ArgumentParser(description='Check Python code style.')
    parser.add_argument('paths', metavar='path', nargs='+',
                        help='Paths to files or directories to check.')
    parser.add_argument('--exclude', metavar='pattern', default='',
                        help='Exclude files or directories that match this pattern. '
                             'Use a comma-separated list for multiple patterns.')
    args = parser.parse_args()

    exclude_patterns = args.exclude.split(',') if args.exclude else []
    paths = [os.path.abspath(path) for path in args.paths]

    style_guide = StyleGuide(exclude=exclude_patterns)
    report = style_guide.check_files(paths)

    if report.total_errors > 0:
        print(f'Found {report.total_errors} code style errors.')
        sys.exit(1)
    else:
        print('No code style errors found.')

if __name__ == '__main__':
    main()
