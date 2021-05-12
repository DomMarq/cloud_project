#!/usr/bin/env python

import os
import sys

file_name = sys.argv[1]
summation = 0.0
count = 0.0

f = open(file_name, "r")
for line in f: 
    if line[:4] == "real":
        if line[-8].isdigit():
            minutes = float(line[-10])
            seconds = float(line[-8:-2])
        else: 
            minutes = float(line[-9])
            seconds = float(line[-7:-2])
        total = minutes * 60 + seconds
        summation = summation + total
        count = count + 1

# return average
print(summation/count)
