for ip in $(cat ip.txt); do whois $ip | echo "$ip $(grep 'OrgName')"; done > whois.txt
