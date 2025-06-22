# copia los datos del escenario de prueba y ejecuta la asignacion
# ojo! borra los datos actuales en data/ y los sorteo/*.log
# ejemplo:
# ./run-scenario.sh test/simple

rm data/*
rm sorteo/*
cp $1/data/* data/
cp $1/sorteo/* sorteo/
uv run python3 asignar.py
