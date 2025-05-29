#!/usr/bin/env python
import pprint

import dateutil.parser

import common

print("Procesando listado general de actividades")
actividadesjson = common.readjson(filename="actividades")

actividades = {}
# Procesar las actividades para generar lista de horarios y años de nacimiento, así como plazas e inscritos
for interes in actividadesjson:
    idactividad = f'{int(interes["idActivitat"])}'
    try:
        horario = int(interes["idNivell"])
    except:
        horario = 0

    if horario in {7, 8, 9, 10}:
        try:
            edatMax = int(interes["edatMax"])
        except Exception:
            edatMax = 9000

        try:
            edatMin = int(interes["edatMin"])
        except Exception:
            edatMin = 0000

        # Rellenar diccionario
        actividades[idactividad] = {
            "maxplazas": int(interes["maxPlaces"]),
            "inscritos": [],
            "edatMax": edatMax,
            "edatMin": edatMin,
            "horario": horario,
        }

idsactividad = list(actividades)
# Ordenar las actividades por ID
idsactividad = sorted(set(idsactividad))


# TEST, leer lista de socios y procesar los activos y de alta
print("Procesando fichero general de socios")
mis_socios = {}
sociosjson = common.readjson(filename="socios")

for socio in sociosjson:
    id_socio = f'{int(socio["idColegiat"])}'

    if (
        "estat" in socio
        and socio["estat"] == "COLESTVAL"
        and "estatColegiat" in socio
        and socio["estatColegiat"]["nom"] == "ESTALTA"
    ):
        if "colegiatHasModalitats" in socio:
            # Iterate over all categories for the socio
            for modalitat in socio["colegiatHasModalitats"]:
                if "modalitat" in modalitat:
                    # Save name for comparing the ones we target
                    modalitat_nombre = modalitat["modalitat"]["nom"].lower()

                    if (
                        "socio principal".lower() in modalitat_nombre
                        or "deudor".lower() in modalitat_nombre
                        or "hermano de socio".lower() in modalitat_nombre
                    ):
                        mis_socios[id_socio] = {}
                        fecha = dateutil.parser.parse(socio["persona"]["dataNaixement"])
                        mis_socios[id_socio]["nacim"] = fecha.year

# Salvar lista para la futura ejecución
common.writejson(filename="sorteo-socios", data=mis_socios)

# Procesar inscripciones

# Leer inscripciones desde disco para cada iteración
try:
    inscripciones_por_actividad = common.readjson(
        filename="sorteo-inscripciones_por_actividad"
    )
except:
    print("Fallo leyendo inscripciones por actividad previos")
    inscripciones_por_actividad = {}

try:
    inscripciones_por_socio = common.readjson(filename="sorteo-inscripciones_por_socio")

except:
    print("Fallo leyendo inscripciones por socio previas")
    inscripciones_por_socio = {}

try:
    horarios_por_socio = common.readjson(filename="sorteo-horarios_por_socio")
except:
    print("Fallo leyendo horarios por socio previos")
    horarios_por_socio = {}


# Asignar plazas actualmente en playoff

print("Procesando actividades...")

usuariosyactividad = {}
actividadyusuarios = {}
usuariosyhorarios = {}


for actividad in actividades:
    inscritos = common.readjson(filename=f"{actividad}")

    for inscrito in inscritos:
        if inscrito["estat"] == "INSCRESTNOVA":
            socio = inscrito["colegiat"]["idColegiat"]

            if socio not in inscripciones_por_socio:
                inscripciones_por_socio[socio] = []

            if socio not in horarios_por_socio:
                horarios_por_socio[socio] = []

            if actividad not in inscripciones_por_actividad:
                inscripciones_por_actividad[actividad] = []

            # No hay conflicto de horario con otras inscripciones
            actividades[actividad]["inscritos"].append(socio)
            inscripciones_por_actividad[actividad].append(socio)

            inscripciones_por_socio[socio].append(actividad)
            horarios_por_socio[socio].append(actividades[actividad]["horario"])

for actividad in inscripciones_por_actividad:
    inscripciones_por_actividad[actividad] = sorted(
        set(inscripciones_por_actividad[actividad])
    )

for socio in inscripciones_por_socio:
    inscripciones_por_socio[socio] = sorted(set(inscripciones_por_socio[socio]))


# Salvar datos
common.writejson(
    filename="sorteo-inscripciones_por_actividad", data=inscripciones_por_actividad
)
common.writejson(
    filename="sorteo-inscripciones_por_socio", data=inscripciones_por_socio
)
common.writejson(filename="sorteo-horarios_por_socio", data=horarios_por_socio)
common.writejson(filename="sorteo-actividades", data=actividades)


# Resultados de inscripciones por actividad e inscripcones por socio
print("Inscripciones por actividad")
pprint.pprint(inscripciones_por_actividad)
print("Inscripciones por socio")
pprint.pprint(inscripciones_por_socio)
