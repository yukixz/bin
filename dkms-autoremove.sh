#!/bin/bash

USAGE='Usage $0 <kernel version> [more]'

# Checking environment.
[[ -n "$@" ]] && KERNELS="$@" || exit 2

dkms=$(which dkms)
[[ $? != 0 ]] &&
    echo "!! ERROR! \`dkms\` not found!" && exit 1

if [[ $EUID != 0 ]]; then
    sudo="$(which sudo)"
    [[ $? != 0 ]] && 
        echo "!! ERROR! \`sudo\` not found! Please run as root." && exit 1
fi


# Generate modules list.
for kernel in $KERNELS; do
    tmp=$($dkms status -k $kernel | 
        grep -P "(installed|built)" |
        sed -r "s|^([0-9a-zA-Z-]+), ([0-9.]+), ($kernel),.+|\1/\2 \3|")
    [[ -n "$tmp" ]] &&
        list=$(echo -e "$list\n$tmp")
done


# Confirm
echo "==> Modules below will be removed."
while read module kernel; do
    [[ -n "$module" ]] && [[ -n "$kernel" ]] || continue
    echo "$kernel: $module"
done <<<"$list"
read -r -p "==> Continue? [Y/n] " prompt
[[ ! $prompt =~ ^[Yy]?$ ]] && exit 0


# Processing
while read module kernel; do
    [[ -n "$module" ]] && [[ -n "$kernel" ]] || continue
    echo "==> Removing $kernel: $module"
    $sudo $dkms remove $module -k $kernel
done <<<"$list"
