#!/usr/bin/env python
import os
import pprint
import random
import re

import dateutil.parser

import common
import sys

import common

anyo = False
if len(sys.argv) > 1:
    try:
        socio = int(sys.argv[1])
    except Exception:
        socio = False
if not socio:
    print("Indica nº de socio para mostrar intereses")
    sys.exit(-1)


intereses=[]

with open(f"sorteo/{socio}.txt", "r", encoding="utf-8") as f:
    for line in f:
        
        intereses.append(line.rstrip().lstrip())
print(sorted(set(intereses)))


actividades_nombre = common.readjson(filename="sorteo-actividades-nombre")
for interes in intereses:
    print(actividades_nombre[interes])
