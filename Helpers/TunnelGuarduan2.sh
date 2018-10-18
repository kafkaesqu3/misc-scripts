# config format
# username:keyfile:ip:port
# for each tunnel you want to keep alive

config="$(cat TunnelGuardian.conf)"
while true; do 
	for i in $(echo "$config"); do 
		username=echo $i | cut -d":" -f 1
		keyfile=echo $i | cut -d":" -f 2
		ip=echo $i | cut -d":" -f 3
		port=echo $i | cut -d":" -f 4

		proc=$(netstat -tlpn | grep 127.0.0.1:$port)

		if [ -z "$proc" ] ; then
			echo "Lost proxy $ip:$port at $(date)"
			ssh -i $keyfile -N -f -D $port $username@$ip
		fi
	done
	sleep 30
done