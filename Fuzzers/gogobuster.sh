#!/bin/bash

gobuster_location=$(which gobuster)
if ! [ -x "$gobuster_location" ] ; then
    echo "You need to have gobuster on your path!"
    exit
fi

if [ "$#" -lt 3 ]; then
    echo "Syntax: $0 <path to file with URLs> <output directory for results> <wordlist to use> <# of threads (default: 5)"
    exit
fi

input=$1
if [ -x "$input" ] ; then
    echo "Input file doesnt exist!"
    exit
fi

output_directory=$2
mkdir -p $output_directory

dictionary=$3
if [ -x "$dictionary" ] ; then
    echo "Dictionary file doesnt exist!"
    exit
fi

threads=$4
if [ -z "threads" ]
  then
    threads=5
fi

for url in $(cat $input); do
	output_file=$(echo $url | cut -d'/' -f3 | cut -d':' -f1)
	command="gobuster -m dir -e -l -k -u $url -w $dictionary -o $output_directory/${output_file}_out"
	$(command)
done; 
