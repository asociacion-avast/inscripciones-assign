#!/usr/bin/bash

date
echo ./run-scenario.sh test/1-socio-edad-incorrecta
./run-scenario.sh test/1-socio-edad-incorrecta
date
echo ./run-scenario.sh test/1-socio-pide-misma-actividad-4-turnos
./run-scenario.sh test/1-socio-pide-misma-actividad-4-turnos
date
echo ./run-scenario.sh test/1-socio-repite-2-turnos
./run-scenario.sh test/1-socio-repite-2-turnos
date
echo ./run-scenario.sh test/11-socios-1-actividad
./run-scenario.sh test/11-socios-1-actividad
date
echo ./run-scenario.sh test/11-socios-4-actividades
./run-scenario.sh test/11-socios-4-actividades
date
echo ./run-scenario.sh test/40-socios-4-actividades
./run-scenario.sh test/40-socios-4-actividades
date
echo ./run-scenario.sh test/40-socios-4-actividades-distinta-edad
./run-scenario.sh test/40-socios-4-actividades-distinta-edad
