#!/usr/bin/env python

import sys

count = int(sys.argv[1])

f = open('generated-policy.yml', 'w')

for i in range(0, count / 10 + 1):
  f.write("- !group group-%s\n" % i)

f.write("\n")

for i in range(0, count):
  f.write("""- !user user-%s
- !grant
  role: !group group-%s
  member: !user user-%s
\n""" % ( i, i / 10, i))

f.close()
