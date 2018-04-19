# pip install ipwhois==0.10.3

from ipwhois import IPWhois
import csv
import argparse
import json
import sys

#argparser = argparse.ArgumentParser()

#argparser.add_argument('-i', '--input', help="input file containing usernames", required=True)
#arguments = argparser.parse_args()

print(['IP Address', 'Country', 'State', 'City', 'Description', 'Name', 'Emails', 'Range'])

try:
    fileOpen = open('22', 'r')
    #fileOpen = open(arguments.input, 'r')
    lines = fileOpen.read().strip().split()

    for ip in lines:
        obj = IPWhois(ip)
        out = obj.lookup()
        row = []
        row.append(ip)
        row.append(out['asn_registry'])
        row.append(out['asn_cidr'])
        row.append(out["nets"][-1]['city'])
        row.append(out["nets"][-1]['name'])
        row.append(out["nets"][-1]['description'])
        row.append(out["nets"][-1]['tech_emails'])

        if len(out["nets"]) > 1:
            print("HAS PARENT")
#        row.append(out["nets"][0]['range'])
#        country = out["nets"][0]['country']
#        state = out["nets"][0]['state']
        print row
        
    fileOpen.close()
except Exception as an:
    print "Error in input file :", an
