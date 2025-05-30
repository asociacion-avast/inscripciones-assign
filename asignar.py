#!/usr/bin/env python
import os
import pprint
import random
import re

import dateutil.parser

import common

# Inicializar semilla aleatoria con el valor proporcionado
with open(os.path.expanduser(".sorteoseed")) as f:
    seed = f.readlines()[0].strip()

random.seed(seed)


# Función para aleatorizar los id's de socio
def durstenfeld_shuffle(arr):
    # Bucle desde el final de la lista al principio
    for i in range(len(arr) - 1, 0, -1):
        # Escoger un índice aleatorio
        j = random.randint(0, i)
        # intercambiar elementos i y j
        arr[i], arr[j] = arr[j], arr[i]
    return arr


def graba_log(filename, data):
    with open(f"{filename}.log", "a", encoding="utf-8") as f:
        f.write(data)
        return True


actividades_nombre = {}

# Construir diccionario de actividades o reutilizar el anterior
try:
    actividades = common.readjson(filename="sorteo-actividades")
    actividades_nombre = common.readjson(filename="sorteo-actividades-nombre")
except Exception:
    print("Procesando listado general de actividades")
    actividades_json = common.readjson(filename="actividades")

    actividades = {}
    # Procesar las actividades para generar lista de horarios y años de nacimiento, así como plazas e inscritos
    for actividad in actividades_json:
        idactividad = f"{int(actividad['idActivitat'])}"
        actividades_nombre[idactividad] = (
            " ".join(
                re.sub(r"grupo .", "", actividad["nom"].split("(")[0]).rstrip().split()
            )
        ).lower()
        try:
            horario = int(actividad["idNivell"])
        except:
            horario = 0

        if horario in {7, 8, 9, 10}:
            try:
                edatMax = int(actividad["edatMax"])
            except Exception:
                edatMax = 9000

            try:
                edatMin = int(actividad["edatMin"])
            except Exception:
                edatMin = 0000

            # Rellenar diccionario
            actividades[idactividad] = {
                "maxplazas": int(actividad["maxPlaces"]),
                "inscritos": [],
                "edatMax": edatMax,
                "edatMin": edatMin,
                "horario": horario,
            }

ids_actividad = list(actividades)
# Ordenar las actividades por ID
ids_actividad = sorted(set(ids_actividad))


# Leer el listado de socios y edades
try:
    mis_socios = common.readjson(filename="sorteo-socios")
except Exception:
    # TEST, leer lista de socios y procesar los activos y de alta
    print("Procesando fichero general de socios")
    mis_socios = {}
    sociosjson = common.readjson(filename="socios")

    for socio in sociosjson:
        id_socio = f"{int(socio['idColegiat'])}"
        graba_log(filename=f"sorteo/{id_socio}", data="Comienzo del proceso\n")

        if (
            "estat" in socio
            and socio["estat"] == "COLESTVAL"
            and "estatColegiat" in socio
            and socio["estatColegiat"]["nom"] == "ESTALTA"
        ):
            tieneactivi = False
            graba_log(
                filename=f"sorteo/{id_socio}",
                data="Socio está dado de alta y validado\n",
            )
            if "colegiatHasModalitats" in socio:
                # Iterate over all categories for the socio
                for modalitat in socio["colegiatHasModalitats"]:
                    if "modalitat" in modalitat:
                        # Save name for comparing the ones we target
                        modalitat_nombre = modalitat["modalitat"]["agrupacio"][
                            "nom"
                        ].lower()

                        if (
                            "actividades".lower() in modalitat_nombre
                            and "sin actividades".lower() not in modalitat_nombre
                        ):
                            graba_log(
                                filename=f"sorteo/{id_socio}",
                                data="Socio tiene actividades\n",
                            )
                            tieneactivi = True
                            mis_socios[id_socio] = {}
                            fecha = dateutil.parser.parse(
                                socio["persona"]["dataNaixement"]
                            )
                            mis_socios[id_socio]["nacim"] = fecha.year

            else:
                graba_log(
                    filename=f"sorteo/{id_socio}",
                    data="Socio no está dado de alta y/o validado\n",
                )
            if not tieneactivi:
                graba_log(
                    filename=f"sorteo/{id_socio}", data="Socio NO tiene actividades\n"
                )

    # Salvar lista para la futura ejecución
    common.writejson(filename="sorteo-socios", data=mis_socios)


id_socios = list(mis_socios)
id_socios = sorted(set(id_socios))
print("Total socios a asignar: ", len(id_socios))

socios = {}
print("Leyendo preferencias de socios")
for socio in mis_socios:
    # Fill dictionary of interests for each socio

    filename = f"sorteo/{socio}.txt"

    # Validar que el socio ha expresado intereses
    if os.access(filename, os.R_OK):
        if socio not in socios:
            socios[socio] = []
        with open(filename) as f:
            lineas = f.readlines()

            for linea in lineas:
                interes = f"{int(linea.strip())}"
                socios[socio].append(interes)

            graba_log(
                filename=f"sorteo/{socio}",
                data="Preferencias de socio: %s\n" % " ".join(socios[socio]),
            )


socios_a_borrar = [socio for socio, value in socios.items() if value == []]
for socio in socios_a_borrar:
    del socios[socio]

# Ordenar id's de socio usando el algoritmo de ordenación
sorted_socios = durstenfeld_shuffle(id_socios)

common.writejson(filename="sorteo-socios-ordenados", data=sorted_socios)

# Procesar inscripciones

# Leer inscripciones desde disco para cada iteración
try:
    inscripciones_por_actividad = common.readjson(
        filename="sorteo-inscripciones_por_actividad"
    )

except Exception:
    print("Fallo leyendo inscripciones por actividad previos")
    inscripciones_por_actividad = {}

try:
    inscripciones_por_socio = common.readjson(filename="sorteo-inscripciones_por_socio")

except Exception:
    print("Fallo leyendo inscripciones por socio previas")
    inscripciones_por_socio = {}

try:
    horarios_por_socio = common.readjson(filename="sorteo-horarios_por_socio")

except Exception:
    print("Fallo leyendo horarios por socio previos")
    horarios_por_socio = {}


# Asignar plazas
print("Asignando plazas a socios")
for socio in sorted_socios:
    # Validar que el socio está en el listado con intereses
    if socio in socios:
        # Preparar si no existen listado de inscripciones de cada socio y horarios ocupados y las inscripciones de cada actividad
        keep_running = True
        if socio not in inscripciones_por_socio:
            inscripciones_por_socio[socio] = []

        if socio not in horarios_por_socio:
            horarios_por_socio[socio] = []

        graba_log(
            filename=f"sorteo/{socio}",
            data="El socio está inscrito en %s\n" % inscripciones_por_socio[socio],
        )

        for interes in socios[socio]:
            if interes not in inscripciones_por_actividad:
                inscripciones_por_actividad[interes] = []
            if keep_running:
                if interes in actividades and (
                    len(actividades[interes]["inscritos"])
                    < actividades[interes]["maxplazas"]
                ):
                    graba_log(
                        filename=f"sorteo/{socio}",
                        data="El socio tiene interés en %s y hay plazas\n" % interes,
                    )

                    # El socio tiene interés en esta actividad y hay menos inscritos que plazas
                    if socio not in actividades[interes]["inscritos"]:
                        graba_log(
                            filename=f"sorteo/{socio}",
                            data="El socio no está inscrito ya en  %s\n" % interes,
                        )
                        anyo = mis_socios[socio]["nacim"]

                        if (
                            anyo >= actividades[interes]["edatMin"]
                            and anyo <= actividades[interes]["edatMax"]
                        ):
                            # Se puede inscribir (está en rango de edad y hay plazas)
                            graba_log(
                                filename=f"sorteo/{socio}",
                                data="El socio está en el rango de edad para  %s\n"
                                % interes,
                            )

                            if (
                                actividades[interes]["horario"]
                                not in horarios_por_socio[socio]
                            ):
                                graba_log(
                                    filename=f"sorteo/{socio}",
                                    data="El socio no tiene conflictos de horario para %s\n"
                                    % interes,
                                )

                                # Comprobar si hay conflicto de nombre en la actividad
                                conflicto_nombres_actividad = False
                                for activi in inscripciones_por_socio[socio]:
                                    if (
                                        interes in actividades_nombre
                                        and activi in actividades_nombre
                                        and actividades_nombre[interes]
                                        == actividades_nombre[activi]
                                    ):
                                        conflicto_nombres_actividad = True
                                        graba_log(
                                            filename=f"sorteo/{socio}",
                                            data="Actividad %s inscrita con otro nombre %s (%s)\n"
                                            % (
                                                interes,
                                                activi,
                                                actividades_nombre[interes],
                                            ),
                                        )

                                if not conflicto_nombres_actividad:
                                    # No hay conflicto de horario con otras inscripciones
                                    actividades[interes]["inscritos"].append(socio)
                                    inscripciones_por_actividad[interes].append(socio)

                                    inscripciones_por_socio[socio].append(interes)
                                    horarios_por_socio[socio].append(
                                        actividades[interes]["horario"]
                                    )
                                    keep_running = False
                                    graba_log(
                                        filename=f"sorteo/{socio}",
                                        data="Socio %s INSCRITO en %s\n"
                                        % (socio, interes),
                                    )
                            else:
                                graba_log(
                                    filename=f"sorteo/{socio}",
                                    data="El socio TIENE conflictos de horario para %s\n"
                                    % interes,
                                )
                        else:
                            graba_log(
                                filename=f"sorteo/{socio}",
                                data="El socio NO está en el rango de edad para %s\n"
                                % interes,
                            )
                    else:
                        graba_log(
                            filename=f"sorteo/{socio}",
                            data="El socio YA estaba inscrito en  %s\n" % interes,
                        )
                else:
                    graba_log(
                        filename=f"sorteo/{socio}",
                        data="El socio tiene interés en %s pero NO hay plazas\n"
                        % interes,
                    )
            else:
                # Saltando por haber rellenado plaza
                keep_running = False


# Salvar datos
common.writejson(
    filename="sorteo-inscripciones_por_actividad", data=inscripciones_por_actividad
)
common.writejson(
    filename="sorteo-inscripciones_por_socio", data=inscripciones_por_socio
)
common.writejson(filename="sorteo-horarios_por_socio", data=horarios_por_socio)
common.writejson(filename="sorteo-actividades", data=actividades)
common.writejson(filename="sorteo-actividades-nombre", data=actividades_nombre)


# Resultados de inscripciones por actividad e inscripcones por socio
print("Inscripciones por actividad")
pprint.pprint(inscripciones_por_actividad)
print("Inscripciones por socio")
pprint.pprint(inscripciones_por_socio)
