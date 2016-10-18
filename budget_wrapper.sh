#!/bin/bash

financier_dir="$(dirname "$(readlink "$0")")"
config_dir="~/Desktop/"


while [ -z $balance ]; do
  echo -n "Starting balance: "
  read balance
done
while [ -z $config ]; do
  echo -n "Budget config: $config_dir"
  read config
done

echo -n "Create CSV? (y/n) [default: ENTER for y]: "
read to_csv

if [ $to_csv == "y" ]; then
  echo -n "Output filename [default: ENTER for "$(echo $config | sed 's/.yaml//')"_YYYYMMDD_HHMM.csv]: "
  read filename
fi



echo -n "Format (summary: only EOM, simple: only line items) [default: ENTER for pretty-print]: "
read output
if [ -z $output ]; then
  output='pretty'
fi

if [ $to_csv == 'y' ]; then 
  if [ -z $filename ]; then
    bash $financier_dir/budgetize.sh $HOME"$(echo $config_dir | sed 's/^~//')"$config -b $balance --to_csv=True -o $output
  else
    bash $financier_dir/budgetize.sh $HOME"$(echo $config_dir | sed 's/^~//')"$config -b $balance --to_csv=True -f $filename -o $output
  fi
else
    bash $financier_dir/budgetize.sh $HOME"$(echo $config_dir | sed 's/^~//')"$config -b $balance --to_csv=False -o $output
  fi
