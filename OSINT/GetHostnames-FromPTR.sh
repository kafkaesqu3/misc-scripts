file=$1

if [ $# -eq 0 ]
then
	echo "massresolve.sh takes a list of IPs, and will attempt a reverse dns query for each IP. If none is found, the IP is printed"
	echo "USAGE: ./massresolve.sh [file containing IP:[port]]"
	exit
fi


for ip in $(cat $file); do 
	name=$(dig +noall +answer -x $ip | cut -d$'\t' -f 3)
	for name_entry in $(echo "$name"); do
		echo "$ip":"$name_entry"
	done
done
