#!/bin/bash
## SETTING
METRIC=16


# Environment
[[ -n $1 ]] && GATEWAY=$1 || exit 1
add="route add"
drt="$add $(ip route show 0/0 | head -n1 | grep -Po 'via \d+\.\d+\.\d+\.\d+') metric $METRIC"
vpn="$add dev $GATEWAY metric $METRIC"
ip_drt="ip $drt"
ip_vpn="ip $vpn"


#### User-defined ####
$ip_drt 193.105.134.117    # btdigg.org


######## Sites ########
# exblog.jp
$ip_vpn 180.235.96.0/21


## Amazon
# http://bgp.he.net/AS14618
# http://whois.arin.net/rest/org/AT-88-Z/nets
# http://wq.apnic.net/apnic-bin/whois.pl?searchtext=54.222.0.0
# $vpn 54.192.0.0/10      # 54.192.0.0/12 54.208.0.0/13 54.216.0.0/14 54.220.0.0/15 54.224.0.0/12 54.240.0.0/12
# $drt 54.222.0.0/15      # Amazon-CN
# http://whois.arin.net/rest/org/AMAZO-4/nets
# $vpn 54.208.0.0/14      # 54.208.0.0/15 54.210.0.0/15
# $vpn 54.216.0.0/15
# $vpn 54.226.0.0/15
# $vpn 54.228.0.0/14      # 54.228.0.0/15 54.230.0.0/15
# $vpn 54.232.0.0/14      # 54.232.0.0/16 54.233.0.0/16 54.234.0.0/15
# $vpn 54.236.0.0/15      # 54.236.0.0/15
# $vpn 54.242.0.0/15
# $vpn 54.247.0.0/16      # 54.247.0.0/16
# $vpn 54.248.0.0/13      # 54.248.0.0/15 54.250.0.0/16 54.251.0.0/16
# $vpn 54.252.0.0/15      # 54.252.0.0/16 54.253.0.0/16
# $vpn 216.182.224.0/20
# Amazon EC2
# $vpn 23.20.0.0/14
# $vpn 50.16.0.0/14
# $vpn 67.202.0.0/18
# $vpn 72.44.32.0/19
# $vpn 75.101.128.0/17
# $vpn 107.20.0.0/14
# $vpn 174.129.0.0/16
# $vpn 184.72.0.0/15
# $vpn 204.236.128.0/17

## Bitly
# http://whois.arin.net/rest/org/BITLY/nets
$ip_vpn 69.58.188.0/24

## Dropbox
# http://bgp.he.net/AS19679#_prefixes
# http://bgp.he.net/AS54372#_prefixes
ip -force -batch - <<EOF
$vpn 108.160.160.0/20
$vpn 199.47.216.0/22
$vpn 205.189.0.0/24
EOF

## Facebook
# http://bgp.he.net/AS32934#_prefixes
# RIPE NCC IPs are ignored.
ip -force -batch - <<EOF
$vpn 66.220.144.0/20
$vpn 69.63.176.0/20
$vpn 69.171.224.0/19
$vpn 74.119.76.0/22
$vpn 103.4.96.0/22
$vpn 173.252.64.0/18
$vpn 204.15.20.0/22
EOF

## Github
# http://bgp.he.net/AS36459#_prefixes
ip -force -batch - <<EOF
$vpn 192.30.252.0/22
EOF

## Google
# http://bgp.he.net/AS15169#_prefixes
ip -force -batch - <<EOF
$vpn 8.34.208.0/21
$vpn 8.34.216.0/21
$vpn 8.35.192.0/21
$vpn 8.35.200.0/21
$vpn 23.236.48.0/20
$vpn 23.251.128.0/19
$vpn 64.233.160.0/19
$vpn 66.102.0.0/20
$vpn 66.249.64.0/19
$vpn 70.32.128.0/19
$vpn 72.14.192.0/18
$vpn 74.125.0.0/16
$vpn 89.207.224.0/21
$vpn 108.59.80.0/20
$vpn 108.170.192.0/18
$vpn 108.177.0.0/17
$vpn 113.197.106.0/24
$vpn 142.250.0.0/15
$vpn 144.188.128.0/24
$vpn 162.216.148.0/22
$vpn 162.222.176.0/21
$vpn 172.217.0.0/16
$vpn 173.194.0.0/16
$vpn 173.255.112.0/20
$vpn 192.158.28.0/22
$vpn 192.178.0.0/15
$vpn 193.142.125.0/24
$vpn 199.192.112.0/22
$vpn 199.223.232.0/21
$vpn 207.223.160.0/20
$vpn 209.85.128.0/17
$vpn 216.58.192.0/19
$vpn 216.239.32.0/19

$vpn 69.46.66.0/24
$vpn 206.169.0.0/16
EOF

## Mediafire
# http://bgp.he.net/AS46179#_prefixes
ip -force -batch - <<EOF
$vpn 199.91.152.0/21
$vpn 205.196.120.0/22
EOF

## Twitter
# http://bgp.he.net/AS13414#_prefixes
ip -force -batch - <<EOF
$vpn 192.133.76.0/22
$vpn 199.16.156.0/22
$vpn 199.59.148.0/22
$vpn 199.96.56.0/21
EOF

## Vimeo
# http://bgp.he.net/AS14829#_prefixes
ip -force -batch - <<EOF
$vpn 66.235.119.0/24
$vpn 74.113.232.0/21
$vpn 192.198.184.0/24
$vpn 199.36.100.0/22
EOF

## Wikimedia
# http://bgp.he.net/AS14907#_prefixes
ip -force -batch - <<EOF
$vpn 198.35.26.0/23
$vpn 208.80.152.0/22
EOF


######## RIPE NCC ########
# http://www.iana.org/assignments/ipv4-address-space/ipv4-address-space.xml
ip -force -batch - <<EOF
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
EOF
