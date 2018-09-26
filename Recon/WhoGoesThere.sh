#!/bin/bash
#
# A simple bash script to look up
# who owns an IP Address based on
# the IP address's whois data
#
# Author: Liam Haworth <liam@haworth.id.au>
#

IPADDR=$1
WHOIS_DATA=$(whois $IPADDR)
FIELDS=("org-name" "OrgName" "descr" "owner")

for field in ${FIELDS[@]}; do
	OWNER=$(echo "$WHOIS_DATA" | awk -v whoisField="$field:" '$0 ~ whoisField {$1 = ""; sub(/^[ \t\r\n]+/, "", $0); print $0}')

	if [ ! -z "${OWNER}" ]; then
		break
	fi
done

if [ -z "${OWNER}" ]; then
	OWNER="UNKNOWN"
fi

echo $IPADDR:$OWNER
