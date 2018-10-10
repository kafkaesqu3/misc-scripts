#!/usr/bin/python

# takes CSV export results of ports table from recon-ng, and parses the results into files containing IP addresses grouped by port

import re

f = open('results.csv')

for line in f:
    p = line.split(',')
    f2 = open(str(re.sub('[\'\"]', '', p[2])), "a+")
    f2.write(str('{0}\n'.format(re.sub('[\'\"]', '', p[0]))))
    f2.close()

f.close()
