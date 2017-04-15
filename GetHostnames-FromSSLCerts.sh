
#!/bin/bash

file=$1

if [ $# -eq 0 ]
then
        echo "Given a list of IPs with SSL services, gets the hostname from the SSL certificate"
                echo "If not port is provided in the file, defaults to 443"
        exit
fi

for ip in $(cat $file | cut -d ":" -f 1 | sort -u | uniq); do
        if [[ $ip == *:* ]] ; then
                openssl=$(echo | openssl s_client -showcerts -servername $ip -connect $ip 2>/dev/null | openssl x509 -inform pem -noout -text 2>/dev/null)
        else
                openssl=$(echo | openssl s_client -showcerts -servername $ip:443 -connect $ip:443 2>/dev/null | openssl x509 -inform pem -noout -text 2>/dev/null)
        fi

        dns=$(echo "$openssl" | grep -o 'DNS:[^, }]*')
        cn=$(echo "$openssl" | grep Subject | grep -o 'CN=[^, }]*' | tr = :)

        for dns_entry in $(echo $dns); do
                        echo "$ip:$dns_entry"
        echo "$ip:$cn"

        sleep $((1 + RANDOM % 10))
done

