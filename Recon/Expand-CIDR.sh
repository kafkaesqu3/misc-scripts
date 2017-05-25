if [ "$#" -ne 2 ]; then
    echo "Usage: ./Expand-CIDR.sh [infile] [outfile]"
	exit
fi

infile=$1
outfile=$2

if [ ! -f $infile ] ; then
	echo "infile \"$infile\" doesnt exist!"
	exit
fi

nmap -iL $infile -sL -oG tmp -n > /dev/null
grep Host tmp | cut -d " " -f 2 > $outfile
rm tmp
