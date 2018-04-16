#flush
iptables -F

# Set default chain policies to DROP
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# Accept on localhost
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

# Allow established sessions to receive traffic
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Allows lab traffic
iptables -A INPUT -p tcp -m iprange --src-range IPRANGE -j ACCEPT
iptables -A OUTPUT -p tcp -m iprange --dst-range IPRANGE -j ACCEPT

#save rules
iptables-save
