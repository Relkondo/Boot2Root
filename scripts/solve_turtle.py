#! /usr/bin/env v_turtle

import re
import os
import time
from turtle import *

directions_collec = {
            'avance': re.compile(r'^Avance (\d+) spaces'),
            'recule': re.compile(r'^Recule (\d+) spaces'),
            'droite': re.compile(r'^Tourne droite de (\d+) degrees'),
            'gauche': re.compile(r'^Tourne gauche de (\d+) degrees'),
        }

letters = []
order = []
file = open(os.path.dirname(os.path.abspath(__file__))+'/../Downloads/turtle', 'r')
for line in file.readlines():
    if line == "\n":
        letters.append(order.copy())
        order.clear()
    for direction, str_collec in directions_collec.items():
        line_match = str_collec.search(line)
        if line_match:
            order.append((direction, line_match.group(1)))
file.close()

for oneletter in letters:
    left(90)
    for oneorder in oneletter:
        if oneorder[0] == 'avance':
            forward(int(oneorder[1]))
        elif oneorder[0] == 'recule':
            backward(int(oneorder[1]))
        elif oneorder[0] == 'droite':
            right(int(oneorder[1]))
        elif oneorder[0] == 'gauche':
            left(int(oneorder[1]))
        print(oneorder[0], oneorder[1])
    time.sleep(2)
    reset()
done()
