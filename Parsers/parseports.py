#!/usr/bin/python
import re

f = open('results.csv')

for line in f:
    p = line.split(',')
    f2 = open(str(re.sub('[\'\"]', '', p[2])), "w+")
    f2.write(p[0])
    f2.close()

f.close()
