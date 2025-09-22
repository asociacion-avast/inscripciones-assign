- [Preparación](#preparación)
- [Descripción de los scripts](#descripción-de-los-scripts)
- [Funcionamiento](#funcionamiento)
- [Probar el funcionamiento](#probar-el-funcionamiento)
  - [Ejemplo de preferencias de socios y ejecución](#ejemplo-de-preferencias-de-socios-y-ejecución)
  - [Listado de socios](#listado-de-socios)
  - [Ejecución](#ejecución)
    - [1ª sorteo](#1ª-sorteo)
    - [2º sorteo](#2º-sorteo)
    - [3er Sorteo y 4º sorteo](#3er-sorteo-y-4º-sorteo)
  - [Conclusiones](#conclusiones)

## Preparación

Crea un fichero llamado `.sorteoseed` con la información del número escogido como semilla para el generador de números aleatorio.

```sh
echo '32768' > .sorteoseed
```

## Descripción de los scripts

| Script                  | Función                                                                                                                       |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `3-importa-talleres.py` | para uso INTERNO: Importa talleres actualmente inscritos para pre-rellenar la lista de inscritos y saber las vacantes reales. |
| `4-asignar.py`          | Procesa la lista de socios, actividades e intereses para hacer las asignaciones de grupos                                     |
| `TEST-interes-fill.py`  | para uso INTERNO: Crea entradas para simular la selección de los socios en cuanto a actividades.                              |

`asignar.py` lee a cada ejecución los datos y realiza la asignación de un grupo a cada ejecución siguiendo el orden de preferencias indicado.

Tras cuatro ejecuciones, en caso de haber plazas, el usuario tendrá cuatro talleres de su lista asignados.

## Funcionamiento

El script utiliza un método de ordenación `Durstenfeld` para aleatorizar la lista de identificadores de socios.

## Probar el funcionamiento

- Rellenar `.sorteoseed` con el número premiado del día escogido
- Descargar el fichero con las selecciones de socios y el fichero de actividades
- Ejecutar el script `asignar.py` para que se realice la primera ronda de asignaciones y repetir alterando las selecciones de socios y semillas para cada ejecución.

El código del programa `asignar.py` está documentado para que con mínimas nociones se entienda lo que se hace en cada paso

### Ejemplo de preferencias de socios y ejecución

Son dos socios con distinto año de nacimiento y con las mismas preferencias

```sh
cat sorteo/851.txt
701
675
628
592
678
620
640
561
580
542
650
586
573
678
690
611
655
```

```sh
cat sorteo/811.txt
701
675
628
592
678
620
640
561
580
542
650
586
573
678
690
611
655
```

### Listado de socios

Listado parcial

```json
{
  "811": {
    "nacim": 2010
  },
  "813": {
    "nacim": 2007
  },
  "823": {
    "nacim": 2010
  },
  "824": {
    "nacim": 2010
  },
  "832": {
    "nacim": 2008
  },
  "851": {
    "nacim": 2008
  }
}
```

### Ejecución

#### 1ª sorteo

```sh
./asignar.py
Procesando listado general de actividades
Procesando fichero general de socios
Total socios a asignar:  979
Leyendo preferencias de socios
Inscripciones por actividad
{'542': [],
 '561': [],
 '573': [],
 '580': [],
 '586': [],
 '592': ['851'],
 '611': [],
 '620': [],
 '628': ['811'],
 '640': [],
 '650': [],
 '655': [],
 '675': [],
 '678': [],
 '690': [],
 '701': []}
Inscripciones por socio
{'811': ['628'], '851': ['592']}

```

En esta primera iteración se ha asignado un taller a cada socio y se ha salido de la ejecución...

En ambos socios la primera preferencia asignada no es la primera del listado, se han asignado la `592` y la `628`... y la causa es esta:

```json
{

    "592": {
        "maxplazas": 35,
        "inscritos": [
            "851"
        ],
        "edatMax": 2009,
        "edatMin": 2003,
        "horario": 10
    },

    "628": {
        "maxplazas": 25,
        "inscritos": [
            "811"
        ],
        "edatMax": 2012,
        "edatMin": 2010,
        "horario": 7
    },
```

Como podemos ver, aunque ambos socios la hubieran puesto en su lista de preferencias, la actividad `592`, es para nacidos entre `2003` y `2009` mientras que la actividad `628` es para nacidos entre `2010` y `2012`.

#### 2º sorteo

Repitiendo las rondas

```sh
Total socios a asignar:  979
Leyendo preferencias de socios
Inscripciones por actividad
{'542': [],
 '561': ['851'],
 '573': [],
 '580': [],
 '586': [],
 '592': ['851'],
 '611': [],
 '620': ['811'],
 '628': ['811'],
 '640': [],
 '650': [],
 '655': [],
 '675': [],
 '678': [],
 '690': [],
 '701': []}
Inscripciones por socio
{'811': ['628', '620'], '851': ['592', '561']}
```

Como vemos, se han asignado otros dos talleres, y el resumen final, muestra que el socio `811` tiene 2 talleres, y el socio `851` tiene otros dos.

#### 3er Sorteo y 4º sorteo

```sh
Total socios a asignar:  979
Leyendo preferencias de socios
Inscripciones por actividad
{'542': [],
 '561': ['851'],
 '573': [],
 '580': [],
 '586': [],
 '592': ['851'],
 '611': ['811'],
 '620': ['811'],
 '628': ['811'],
 '640': [],
 '650': [],
 '655': [],
 '675': [],
 '678': [],
 '690': [],
 '701': []}
Inscripciones por socio
{'811': ['628', '620', '611'], '851': ['592', '561']}
```

En esta ronda, el socio `811` ha reccibido un nuevo taller, mientras que el `851` no ha tenido nuevo taller asignado

En el cuarto sorteo, los resultados no han variado para ninguno...

### Conclusiones

¿La causa? ¿Qué ha pasado con todas las actividades que aparecen y no tienen socios?

```json
In [3]: actividades["542"]
Out[3]:
{'maxplazas': 30,
 'inscritos': [],
 'edatMax': 2019,
 'edatMin': 2013,
 'horario': 10}

In [4]: actividades["573"]
Out[4]:
{'maxplazas': 25,
 'inscritos': [],
 'edatMax': 2015,
 'edatMin': 2010,
 'horario': 8}

In [5]: actividades["580"]
Out[5]:
{'maxplazas': 20,
 'inscritos': [],
 'edatMax': 2015,
 'edatMin': 2013,
 'horario': 9}

In [6]: actividades["586"]
Out[6]:
{'maxplazas': 30,
 'inscritos': [],
 'edatMax': 2015,
 'edatMin': 2013,
 'horario': 8}

In [7]: actividades["640"]
Out[7]:
{'maxplazas': 25,
 'inscritos': [],
 'edatMax': 2015,
 'edatMin': 2013,
 'horario': 9}

In [8]: actividades["650"]
Out[8]:
{'maxplazas': 25,
 'inscritos': [],
 'edatMax': 2015,
 'edatMin': 2013,
 'horario': 7}

In [9]: actividades["655"]
Out[9]:
{'maxplazas': 25,
 'inscritos': [],
 'edatMax': 2012,
 'edatMin': 2010,
 'horario': 10}

```

Como vemos con el ejemplo, las actividades sin socios, obviamente no están sin plazas, pero tienen unos rango de edades incompatibles con nuestros socios de ejemplo, por lo que... llegados a este punto, aunque repitieramos miles de veces la asignación, no se añadirían los talleres.

De igual modo, si los talleres fueran en el mismo horario que los ya asignados, tampoco se podrían usar por concidir en el mismo hueco.

¿Y por qué salen actividades sin inscripciones?

Por que los usuarios las habían puesto en su lista de intereses... pero como no han satisfecho los requisitos (edad, plazas, horario, etc), no se ha añadido su inscripción.

En la carpeta `data/` existen los ficheros generados que contienen los datos obtenidos a cada iteración, mientras que en `sorteo/` están las preferencias de talleres de cada socio.
