import argparse
from BHQuery import BHQuery

argparser = argparse.ArgumentParser()

argparser.add_argument('--input', help="input file containing usernames", required=False)
argparser.add_argument('-g', '--groups', action='store_true', help="unrolled group memberships for input object(s)")
argparser.add_argument('-m', '--groupmembers', action='store_true', help="get group members")
argparser.add_argument('-f', '--firstdegree-localadmin', action='store_true', help="group delegated local admin")
argparser.add_argument('-a', '--groupdelegated-admin', action='store_true', help="group delegated local admin")
argparser.add_argument('-d', '--derivadmin', action='store_true', help="derivitive local admin rights for input object(s)")
#argparser.add_argument('-o', '--outbound', action='store_true', help="outbound ACLs for input object(s)")
#argparser.add_argument('-i', '--inbound', action='store_true', help="inbound ACLs for input object(s)")
argparser.add_argument('-s', '--sessions', action='store_true', help="sessions for input object(s)")
argparser.add_argument('object', type=str, metavar='objects', nargs='*', help='object(s) to run the operation on')
arguments = argparser.parse_args()



if arguments.input: 
    try: 
        print "file"
        objects = open(arguments.input, 'r')
    except Exception as e:
        print "[-] ERROR opening input file"
        print e
        sys.exit(1)
else: 
    objects = arguments.object

queryType = ""
if arguments.groups:
    queryType = "groups"
    
if arguments.firstdegree_localadmin: 
    queryType = "firstdegree_localadmin"
if arguments.groupdelegated_admin: 
    queryType = "groupdelegated_localadmin"
if arguments.derivadmin:
	queryType = "deriv-admin"
if arguments.sessions: 
    queryType = "sessions"
if arguments.groupmembers:
    queryType = "groupmembers"


results = BHQuery().runQuery(queryType, arguments.object)
for result in results:
    print result
