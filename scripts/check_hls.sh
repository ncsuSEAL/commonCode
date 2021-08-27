#!/bin/bash
S30="S30/*.hdf"
L30="L30/*.hdf"

echo "Checking Sent 2"
for s in $S30
do
  if ! [ "$(gdalinfo $s | grep SUBDATASET | wc -l)" == 28 ]; then
    echo $s
  fi
done

echo "Checking Landsat 8"
for l in $L30
do
  if ! [ "$(gdalinfo $l | grep SUBDATASET | wc -l)" == 22 ]; then
    echo $l
  fi
done
