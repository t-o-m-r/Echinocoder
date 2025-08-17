#!/bin/sh

( for M in `seq 1 20` ; do { (time python tom_demo.py $M 4) | tail -10 2>&1  ; } done ) > log 2>&1
