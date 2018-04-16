while true; do
	p1=$(netstat -tlpn | grep 127.0.0.1:8081)
	p2=$(netstat -tlpn | grep 127.0.0.1:8082)
	p3=$(netstat -tlpn | grep 127.0.0.1:8083)
	p4=$(netstat -tlpn | grep 127.0.0.1:8084)
	p5=$(netstat -tlpn | grep 127.0.0.1:8085)
	
	if [ -z "$p1" ] ; then 
		echo "Lost proxy 1 at $(date)"
		ssh -i /home/david/.ssh/id_rsa -N -f -D 8081 root@ip
	fi
	
	if [ -z "$p2" ] ; then 
		echo "Lost proxy 2 at $(date)"
		ssh -i /home/david/.ssh/id_rsa -N -f -D 8082 root@ip
	fi
	
	if [ -z "$p3" ] ; then 
		echo "Lost proxy 3 at $(date)"
		ssh -i /home/david/.ssh/id_rsa -N -f -D 8083 root@ip
	fi
	
	if [ -z "$p4" ] ; then 
		echo "Lost proxy 4 at $(date)"
		ssh -i /home/david/.ssh/id_rsa -N -f -D 8084 root@IP	
	fi
	
	if [ -z "$p5" ] ; then 
		echo "Lost proxy 5 at $(date)"
		ssh -i /home/david/.ssh/id_rsa -N -f -D 8085 root@IP
	fi

	sleep 60
done
