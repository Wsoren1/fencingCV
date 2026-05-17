#!/usr/bin/env sh

runid=$(date +"%Y%m%d%H%M%S")
mkdir "runs/$runid"

python pose.py $1 "runs/$runid"

python analyze.py "runs/$runid"

rm -r runs/latest
cp -r "runs/$runid" runs/latest
