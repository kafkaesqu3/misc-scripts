# Variables - Set these
pth=`pwd`
# HOST DISCOVERY
targets=$1

# Nmap - Pingsweep using ICMP echo
nmap -sP -PE -iL $pth/$targets -oA $pth/icmpecho
cat $pth/icmpecho.gnmap | grep Up | cut -d ' ' -f 2 > $pth/live

# Nmap - Pingsweep using ICMP timestamp
nmap -sP -PP -iL $pth/$targets -oA $pth/icmptimestamp
cat $pth/icmptimestamp.gnmap | grep Up | cut -d ' ' -f 2 >> $pth/live

# Nmap - Pingsweep using ICMP netmask
nmap -sP -PM -iL $pth/$targets -oA $pth/icmpnetmask
cat $pth/icmpnetmask.gnmap | grep Up | cut -d ' ' -f 2 >> $pth/live

# Systems that respond to ping (finding)
cat $pth/live | sort | uniq > $pth/pingresponse

# Nmap - Pingsweep using TCP SYN and UDP
nmap -sP -PS21,22,23,25,53,80,88,110,111,135,139,443,445,8080 -iL $pth/$targets -oA $pth/pingsweepTCP
nmap -sP -PU53,111,135,137,161,500 -iL $pth/$targets -oA $pth/pingsweepUDP
cat $pth/pingsweepTCP.gnmap | grep Up | cut -d ' ' -f 2 >> $pth/live
cat $pth/pingsweepUDP.gnmap | grep Up | cut -d ' ' -f 2 >> $pth/live

# Create unique live hosts file
cat $pth/live | sort | uniq > $pth/livehosts

# Empty file cleanup
find $pth -size 0c -type f -exec rm -rf {} \;
