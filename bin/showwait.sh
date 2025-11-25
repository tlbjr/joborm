#!/bin/bash
if [ "$1" != "" ];
then
    TIME=$1
else
    TIME=10
fi

for (( count = $TIME; count > 0; count-- ))
do
    printf "%02d" "$count"
    echo -ne "\r"
    #echo -ne "${count}\r"
    sleep 1
done
