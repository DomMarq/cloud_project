#!/usr/bin/env python

import os
import sys

num = 400

f = open("load_400.sh", "w")
f.write("#!/bin/sh")
f.write("\n")
f.write("\n")

for x in range (num):
    if x < num - 1:     
        f.write("time(curl -i -X POST -H \"Content-Type: multipart/form-data\" -F \"file=@00000003_000.png\" https://bp90jzkqgf.execute-api.us-east-1.amazonaws.com/dev/v1/uploadfile) &")
        f.write("\n")
    else: 
        f.write("time(curl -i -X POST -H \"Content-Type: multipart/form-data\" -F \"file=@00000003_000.png\" https://bp90jzkqgf.execute-api.us-east-1.amazonaws.com/dev/v1/uploadfile)")
f.close()
