#!/bin/bash
# copia los datos del escenario de prueba y ejecuta la asignacion
# ojo! borra los datos actuales en data/ y los sorteo/*.log
# ejemplo:
# ./run-scenario.sh test/simple

if [ -z "$1" ]; then
  if command -v fzf &> /dev/null; then
    # find directories under test/ and let user select one with fzf
    selected_scenario=$(find test -mindepth 1 -maxdepth 1 -type d | fzf --prompt="Select a scenario > ")

    # if user cancels fzf, exit
    if [ -z "$selected_scenario" ]; then
      echo "No scenario selected. Exiting."
      exit 1
    fi

    # set the selected scenario as the first positional parameter
    set -- "$selected_scenario"
  else
    echo "Usage: $0 <scenario_path>"
    echo "fzf is not installed. Please provide a scenario path as an argument."
    exit 1
  fi
fi

echo "Running scenario: $1"
echo "echo 32768 > ~/.sorteoseed"
echo 32768 > ~/.sorteoseed
rm -f data/*
rm sorteo/*
cp $1/data/* data/
#cp $1/sorteo/* sorteo/
uv run python3 asignar.py 
if [ -f "$1/sorteo-inscripciones_por_actividad.json" ]; then
  echo "Diff: sorteo-inscripciones_por_actividad"
  diff "$1/sorteo-inscripciones_por_actividad.json" data/sorteo-inscripciones_por_actividad.json
fi
if [ -f "$1/sorteo-inscripciones_por_socio.json" ]; then
  echo "Diff: sorteo-inscripciones_por_socio"
  diff "$1/sorteo-inscripciones_por_socio.json" data/sorteo-inscripciones_por_socio.json
fi
