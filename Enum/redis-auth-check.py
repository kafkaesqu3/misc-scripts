import redis
import sys

if len(sys.argv) != 2: 
	exit()

targets = sys.argv[1]
try:
	f = open(targets, 'r')
except: 
	print("Can't open targets file")

for target in f.readlines():
	hostname = target.split(":")[0]
	port = target.split(":")[1]

	r = redis.Redis(
	    host=hostname,
	    port=port)

	if r: 
		print("Connected to {} without password".format(target.strip("\n")))
		scan = r.scan()
		print("{}: {}".format(target.strip("\n"), scan))
	else: 
		print("Authentication required: {}".format(target.strip("\n")))

f.close()