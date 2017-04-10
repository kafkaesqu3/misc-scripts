file=$1

if [ $# -eq 0 ]
then
	echo "massresolve.sh takes a list of IPs (or IP:ports), and will attempt a reverse dns query for each IP. If none is found, the IP is printed"
	echo "USAGE: ./massresolve.sh [file containing IP:[port]] [--remove-duplicates]"
	echo "--remove-duplicates will only print the first PTR record if multiple are found, and will not warn you it did so"
	exit
fi

if [ $2="--remove-duplicates" ] ; then
	removeduplicates=true
else
	removeduplicates=false
fi

for ip in $(cat $file | cut -d ":" -f 1 | sort -u | uniq); do 
	name=$(dig +noall +answer -x $ip | cut -d$'\t' -f 3)
	if [ -n "$name" ] ; then
		if echo $name | grep -q ' ' && $removeduplicates -eq "true"; then
			echo $name | cut -d " " -f 1
		else
			echo $name
		fi
	else 
		echo $ip
	fi
done
