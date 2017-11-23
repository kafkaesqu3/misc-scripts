import requests
import json
import argparse
import sys

def doCurl(statement):
    headers = { "Accept": "application/json; charset=UTF-8",
                "Content-Type": "application/json",
                "Authorization": "bmVvNGo6Qmxvb2RIb3VuZA==" }
    data = {"statements": [{'statement': statement}]}
    url = 'http://localhost:7474/db/data/transaction/commit'
    r = requests.post(url=url,headers=headers,json=data)
    return r.text


argparser = argparse.ArgumentParser()
argparser.add_argument("-i", "--input", help="input file containing usernames", required=True)
argparser.add_argument("-o", "--output", help="output file csv (default results.csv", required=True)
argparser.add_argument("-v", "--verbose", help="write to stdout", action="store_true")
arguments = argparser.parse_args()

try: 
    infile = open(arguments.input, 'r')
except Exception as e:
    print "[-] ERROR opening input file"
    print e
    sys.exit(1)

try: 
    outfile = open(arguments.output, 'w')
except Exception as e:
    print "[-] ERROR opening output file"
    print e
    sys.exit(1)

for user in infile: 
    user = user.upper().strip('\n')
    first_degree_query = "MATCH p = (n:User {name:'%s'})-[r:AdminTo]->(c:Computer) RETURN count(p)" % user
    group_delegated_query = "MATCH p=(n:User {name:'%s'})-[r1:MemberOf*1..]->(g:Group)-[r2:AdminTo]->(c:Computer) RETURN count(p)" % user 
    derivitive_query = "MATCH (c:Computer) WHERE NOT c.name='%s' WITH c MATCH p = shortestPath((n:User {name:'%s'})-[r:HasSession|AdminTo|MemberOf*1..]->(c)) RETURN count(p)" % (user, user)

    first_degree_results = json.loads(doCurl(first_degree_query))
    group_delegated_results = json.loads(doCurl(group_delegated_query))
    derivitive_results = json.loads(doCurl(derivitive_query))
    line = user.rstrip('\n') + ","
    line = line + str(first_degree_results['results'][0]['data'][0]['row'])[1:-1]
    line = line + ","
    line = line + str(group_delegated_results['results'][0]['data'][0]['row'])[1:-1]
    line = line + ","
    line = line + str(derivitive_results['results'][0]['data'][0]['row'])[1:-1]
    if arguments.verbose: 
        print(line)
    outfile.write(line)

outfile.write('\n')
infile.close()
outfile.close()