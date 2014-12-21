#!/bin/bash
EXTENSIONS="jpg png"
TAGS="DateTimeOriginal DateTimeDigitized DateTime"

## Checking exif exist
which exif 1>/dev/null
[ $? -ne 0 ] && exit

## Loop
for file in "$@"; do
    ## File Extension
    ext="${file##*.}"
    ext="${ext,,}"
    [[ $EXTENSIONS =~ $ext ]] || continue

    ## Image Datetime
    for tag in $TAGS; do
        datetime=$(exif -mt $tag "$file" 2>/dev/null)
        [ $? -eq 0 ] && break
    done
    datetime=$(sed 's/:/./g' - <<<$datetime)
    [ -n "$datetime" ] || continue

    ## Rename
    #echo "$file" '=>' "$datetime.$ext"
    mv -n "$file" "$datetime.$ext"
done
