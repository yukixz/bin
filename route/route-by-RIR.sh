#!/bin/sh
add='ip route add'
deth="via `ip route show | grep '^default' | sed -e 's/default via \([^ ]*\).*/\1/'`"
eth="$add $deth"
vpn="$add dev ppp0"
blackhole="$add to blackhole"

#### User-defined ####


#### ARIN ####
# http://www.iana.org/assignments/ipv4-address-space/ipv4-address-space.xml
$vpn   7.0.0.0/8
$vpn  23.0.0.0/8
$vpn  24.0.0.0/8
$vpn  35.0.0.0/8
$vpn  40.0.0.0/8
$vpn  45.0.0.0/8
$vpn  47.0.0.0/8
$vpn  50.0.0.0/8
$vpn  54.0.0.0/8
$vpn  63.0.0.0/8
$vpn  64.0.0.0/8
$vpn  65.0.0.0/8
$vpn  66.0.0.0/8
$vpn  67.0.0.0/8
$vpn  68.0.0.0/8
$vpn  69.0.0.0/8
$vpn  70.0.0.0/8
$vpn  71.0.0.0/8
$vpn  72.0.0.0/8
$vpn  73.0.0.0/8
$vpn  74.0.0.0/8
$vpn  75.0.0.0/8
$vpn  76.0.0.0/8
$vpn  96.0.0.0/8
$vpn  97.0.0.0/8
$vpn  98.0.0.0/8
$vpn  99.0.0.0/8
$vpn 100.0.0.0/8
$eth 100.64.0.0/10	# 100.64.0.0/10 reserved for Shared Address Space [RFC6598].
$vpn 104.0.0.0/8
$vpn 107.0.0.0/8
$vpn 108.0.0.0/8
$vpn 128.0.0.0/4
# 128/8 ~ 143/8
$eth 133.0.0.0/8	# APNIC
#$eth 141.0.0.0/8	# RIPE NCC
$vpn 144.0.0.0/8
$vpn 146.0.0.0/8
$vpn 147.0.0.0/8
$vpn 148.0.0.0/8
$vpn 149.0.0.0/8
$vpn 152.0.0.0/8
$vpn 155.0.0.0/8
$vpn 156.0.0.0/8
$vpn 157.0.0.0/8
$vpn 158.0.0.0/8
$vpn 159.0.0.0/8
$vpn 160.0.0.0/8
$vpn 161.0.0.0/8
$vpn 162.0.0.0/8
$eth 162.105.0.0/16	# Early Registrations, Transferred to APNIC. http://whois.arin.net/rest/net/NET-162-105-0-0-1
$vpn 164.0.0.0/8
$vpn 165.0.0.0/8
$vpn 166.0.0.0/8
$vpn 167.0.0.0/8
$vpn 168.0.0.0/8
$vpn 169.0.0.0/8
$eth 169.254.0.0/16	# 169.254.0.0/16 reserved for Link Local [RFC3927].
$vpn 170.0.0.0/8
$vpn 172.0.0.0/8
$eth 172.16.0.0/12	# 172.16.0.0/12 reserved for Private-Use Networks [RFC1918]. 
$vpn 173.0.0.0/8
$vpn 174.0.0.0/8
$vpn 184.0.0.0/8
$vpn 192.0.0.0/8
$eth 192.0.0.0/24	# 192.0.0.0/24 reserved for IANA IPv4 Special Purpose Address Registry [RFC5736]. 
$eth 192.0.2.0/24	# 192.0.2.0/24  reserved for TEST-NET-1 [RFC5737]. 
$eth 192.88.99.0/24	# 192.88.99.0/24 reserved for 6to4 Relay Anycast [RFC3068]
$eth 192.168.0.0/16	# 192.168.0.0/16 reserved for Private-Use Networks [RFC1918]. 
$vpn 198.0.0.0/8
$eth 198.18.0.0/15	# 198.18.0.0/15 reserved for Network Interconnect Device Benchmark Testing [RFC2544]. 
$eth 198.51.100.0/24	# 198.51.100.0/24 reserved for TEST-NET-2 [RFC5737]. 
$vpn 199.0.0.0/8
$vpn 204.0.0.0/8
$vpn 205.0.0.0/8
$vpn 206.0.0.0/8
$vpn 207.0.0.0/8
$vpn 208.0.0.0/8
$vpn 209.0.0.0/8
$vpn 216.0.0.0/8

#### RIPE NCC ####
# http://www.iana.org/assignments/ipv4-address-space/ipv4-address-space.xml
$vpn   2.0.0.0/8
$vpn   5.0.0.0/8
$vpn  31.0.0.0/8
$vpn  37.0.0.0/8
$vpn  46.0.0.0/8
$vpn  62.0.0.0/8
$vpn  77.0.0.0/8
$vpn  78.0.0.0/8
$vpn  79.0.0.0/8
$vpn  80.0.0.0/4
# 080/8 ~ 095/8
$vpn 109.0.0.0/8
$vpn 141.0.0.0/8
$vpn 145.0.0.0/8
$vpn 151.0.0.0/8
$vpn 176.0.0.0/8
$vpn 178.0.0.0/8
$vpn 185.0.0.0/8
$vpn 188.0.0.0/8
$vpn 193.0.0.0/8
$vpn 194.0.0.0/8
$vpn 195.0.0.0/8
$vpn 212.0.0.0/8
$vpn 213.0.0.0/8
$vpn 217.0.0.0/8
