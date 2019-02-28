from string import digits, ascii_uppercase, ascii_lowercase
from itertools import product
import argparse

argparser = argparse.ArgumentParser()

argparser.add_argument("-d", "--domain", help="domain you want to print subdomains for. If not specified, will just print the subdomains. ", required=False)
argparser.add_argument("-l", "--length", help="length of subdomain", type=int, required=True)
arguments = argparser.parse_args()

chars = digits + ascii_lowercase

domain = arguments.domain
if domain is None: 
    domain = ""
else: 
    domain = "." + domain

def subdomain_generator(n): 
    for n in range(1, n + 1):
        for comb in product(chars, repeat=n):
            subdomain = ''.join(comb)
            print("{0}{1}".format(subdomain, domain))

subdomain_generator(arguments.length)

"""
name[suffix]
name-[suffix]

"""
# old
# tmp
# temp
# stg
# na
# eu

# option to add 1-9 to each value in wordlist