#!/bin/bash

# Checking environment.
KERNELS="$@"

dkms=$(which dkms)
[[ $? != 0 ]] &&
    echo "!! ERROR! \`dkms\` not found!" && exit 1

if [[ $EUID = 0 ]]; then
    dkms_root=$dkms
else
    dkms_root="$(which sudo) $dkms"
    [[ $? != 0 ]] && 
        echo "!! ERROR! \`sudo\` not found! Please run with root." && exit 1
fi


# Generate modules list.
for kernel in $KERNELS; do
    tmp=$($dkms status -k $kernel | 
        grep -P "(installed|built)" |
        sed -r "s|^([0-9a-zA-Z-]+), ([0-9.]+), ($kernel),.+|\1/\2  -k \3|")
    [[ -n "$tmp" ]] &&
        list=$(echo -e "$list\n$tmp")
done


# Confirm
echo -e "$list\n"
read -r -p "==> Continue? [Y/n] " prompt
[[ ! $prompt =~ ^[Yy]?$ ]] && exit 0


# Processing
IFS=$'\n'
for item in $list; do
    [[ -z "$item" ]] && continue
    echo "==> Removing $item"
    $dkms_root remove $module -k $kernel
done
