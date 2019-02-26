#!/usr/bin/env python3

import argparse

def fix(f):
    f.seek(0, 2)
    length = f.tell()
    f.seek(length - 2)
    if f.read(1) == ']':
        return
    read_from = max(0, length - (4096))
    f.seek(read_from)
    s = f.read(length - read_from)
    last_comma = read_from + 2 + s.rindex('}},\n')
    f.seek(last_comma)
    f.write('\n]\n')
    f.truncate()

def main():
    parser = argparse.ArgumentParser(description='Fix up traces captured from Firefox with MOZ_LOG=MSGTracing:5,raw')
    parser.add_argument('file', type=argparse.FileType('r+'), nargs='+', help='Files to fix up')
    args = parser.parse_args()
    for f in args.file:
        try:
            fix(f)
        except Exception as e:
            print(type(e).__name__, '->', e)
        finally:
            f.close()

if __name__ == "__main__":
    main()
