#!/bin/bash
HOST="\
"
WD=/tmp/autoroute
CACHE='ip.list'
CACHE_NEW="$CACHE.new"
SCRIPT='script'
SCRIPT_LOG="$SCRIPT.log"

## Check and Change environment
export IFS=$'\n'
[[ -e $WD ]] || mkdir -p $WD
[[ ! -d $WD ]] && echo "ERROR! ! -d $WD" && exit
cd $WD
[[ -e $CACHE ]] || touch $CACHE
[[ ! -f $CACHE ]] && echo "ERROR! ! -f $CACHE" && exit
# Magic route for checking if ppp0 down
[[ -z $(ip route show 1.1.1.1 | grep 'metric 2358') ]] &&
    ip route add 1.1.1.1 dev ppp0 metric 2358 && :> $CACHE

## Generate new IP List
dig +short $HOST | grep -P '^\d' | sort -h - | uniq - $CACHE_NEW
## Compare & Overwrite Cache
change=$(diff $CACHE $CACHE_NEW)
mv $CACHE_NEW $CACHE

## Generate Script
echo '#!/bin/bash' > $SCRIPT
echo 'ip -force -batch - <<EOF' >>$SCRIPT
for line in $change; do
    [[ -z ${line:2} ]] && continue
    [[ ${line:0:2} = '> ' ]] &&
        sed 's/^> /route add dev ppp0 /' - <<<$line >>$SCRIPT
    [[ ${line:0:2} = '< ' ]] &&
        sed 's/^< /route del /' - <<<$line >>$SCRIPT
done
echo 'EOF' >>$SCRIPT

## Execute Script
[[ -x $SCRIPT ]] || chmod +x $SCRIPT
bash $SCRIPT
