#!/usr/bin/python

import os
import argparse
import hashlib

home = os.path.expanduser("~")
if not os.path.isfile(home+'/.reader_rc'):
  open(home+'/.reader_rc', 'w').close()

parser = argparse.ArgumentParser()
parser.add_argument("filename", help="the file containing the book")
parser.add_argument("-n", nargs=1, help="number of lines", required=False)
args = parser.parse_args()

if(args.n is not None):
  num_lines = int(args.n[0])
else:
  num_lines = 40

md5 = hashlib.md5()
with open(args.filename, 'r') as book:
  for line in book:
    md5.update(line)
checksum = md5.hexdigest()
with open(home+'/.reader_rc', 'r') as bookmark:
  found = False
  for line in bookmark:
    if checksum in line:
      found = True
      break
if not found:
  with open(home+'/.reader_rc', 'a') as bookmark:
    bookmark.write(checksum + ',0\n')

def flip(lines, n):
  """Flips the page.
  n = -1, 0, 1 for previous, current, next page respectively"""
  with open(home+'/.reader_rc', 'r') as bookmark:
    bookmarklines = bookmark.readlines()
  for i in range(len(bookmarklines)):
    parts = bookmarklines[i].split(',')
    if parts[0] == checksum:
      num = int(parts[1]) + n * num_lines
      if num < 0:
        num = 0
      if num > len(lines):
        num = len(lines)
      bookmarklines[i] = str(checksum) + ',' + str(num) + '\n'
      with open(home+'/.reader_rc', 'w') as bookmark:
        bookmark.writelines(bookmarklines)
      break

  print 40*'-'
  for i in range(num, min(num + num_lines, len(lines))):
    print lines[i],
  print 40*'-'

def main():
  with open(args.filename, 'r') as book:
    booklines = book.readlines()
  flip(booklines, 0)
  while True:
    key = raw_input()
    if key == 'q':
      break
    elif key == 'n':
      flip(booklines, 1)
    elif key == 'p':
      flip(booklines, -1)

main()
