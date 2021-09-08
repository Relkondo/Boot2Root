#! /usr/bin/env python3
import os, re

#Parameter
pathtofun = "../Downloads/ft_fun"
filescontent = {}

for file in os.listdir(pathtofun):
    with open(pathtofun + "/%s" % file, 'r') as f:
        onefile = f.read()
        f.close()
    onefilenumber = re.findall('//file([0-9]*)', onefile)
    if len(onefilenumber) == 1:
        filescontent[int(onefilenumber[0])] = onefile
    else:
        print("ERROR : more or less than one match was found in " + file + ". File wasn't taken into account.")

if os.path.exists("read_fun.c"):
    os.remove("read_fun.c")
with open("read_fun.c", 'w') as f:
    for key in sorted(filescontent.keys()):
        f.write(filescontent[key] + "\n")
    f.close()
