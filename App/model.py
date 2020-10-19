"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """
import config
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as m
import datetime
assert config

"""
En este archivo definimos los TADs que vamos a usar,
es decir contiene los modelos con los datos en memoria


"""

# -----------------------------------------------------
# API del TAD Catalogo de accidentes
# -----------------------------------------------------


def newAnalyzer():
    """ Inicializa el analizador

    Crea una lista vacia para guardar todos los crimenes
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas

    Retorna el analizador inicializado.
    """
    analyzer = {'accidents': None,
                'dateIndex': None
                }

    analyzer['accidents'] = lt.newList('SINGLE_LINKED', compareIds)
    analyzer['dateIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
    return analyzer

# Funciones para agregar informacion al catalogo


def addAccidents(analyzer, accident):
    """
    """
    lt.addLast(analyzer['accidents'], accident)
    updateDateIndex(analyzer['dateIndex'], accident)
    return analyzer


def updateDateIndex(map, accident):
    """
    Se toma la fecha del crimen y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de crimenes
    y se actualiza el indice de tipos de crimenes.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de crimenes
    """
    occurreddate = accident['Start_Time']
    crimedate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, crimedate.date())
    if entry is None:
        datentry = newDataEntry(accident)
        om.put(map, crimedate.date(), datentry)
    else:
        datentry = me.getValue(entry)
    addDateIndex(datentry, accident)
    return map


def addDateIndex(datentry, accident):
    """
    Actualiza un indice de tipo de crimenes.  Este indice tiene una lista
    de crimenes y una tabla de hash cuya llave es el tipo de crimen y
    el valor es una lista con los crimenes de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datentry['lstaccidents']
    lt.addLast(lst, accident)
    offenseIndex = datentry['offenseIndex']
    offentry = m.get(offenseIndex, accident['Description'])
    if (offentry is None):
        entry = newOffenseEntry(accident['Description'], accident)
        lt.addLast(entry['lstoffenses'], accident)
        m.put(offenseIndex, accident['Description'], entry)
    else:
        entry = me.getValue(offentry)
        lt.addLast(entry['lstoffenses'], accident)
    return datentry


def newDataEntry(accident):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'offenseIndex': None, 'lstaccidents': None}
    entry['offenseIndex'] = m.newMap(numelements=30,
                                     maptype='PROBING',
                                     comparefunction=compareOffenses)
    entry['lstaccidents'] = lt.newList('SINGLE_LINKED', compareDates)

    return entry


def newOffenseEntry(offensegrp, accident):
    """
    Crea una entrada en el indice por tipo de crimen, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    ofentry = {'offense': None, 'lstoffenses': None}
    ofentry['offense'] = offensegrp
    ofentry['lstoffenses'] = lt.newList('SINGLELINKED', compareOffenses)
    return ofentry

# ==============================
# Funciones de consulta
# ==============================


def accidentsSize(analyzer):
    """
    Número de libros en el catago
    """
    return lt.size(analyzer['accidents'])


def indexHeight(analyzer):
    """Numero de autores leido
    """
    return om.height(analyzer['dateIndex'])


def indexSize(analyzer):
    """Numero de autores leido
    """
    return om.size(analyzer['dateIndex'])


def minKey(analyzer):
    """Numero de autores leido
    """
    return om.minKey(analyzer['dateIndex'])


def maxKey(analyzer):
    """Numero de autores leido
    """
    return om.maxKey(analyzer['dateIndex'])


# Requerimiento 1
# ["first"]["info"]["offenseIndex"]
def getCrimesByDate(analyzer, initialDate):
    mapa = om.newMap(omaptype='RBT', comparefunction=compareDates)
    lista_1 = lt.newList('SINGLE_LINKED', compareDates)
    lista_2 = lt.newList('SINGLE_LINKED', compareDates)
    lista_3 = lt.newList('SINGLE_LINKED', compareDates)
    lista_4 = lt.newList('SINGLE_LINKED', compareDates)
    obtener_2 = om.get(analyzer["dateIndex"], initialDate)
    lista_2 = me.getValue(obtener_2)["lstaccidents"]
    cantidad_2 = lista_2["size"]
    v = om.valueSet(obtener_2)
    iterator = it.newIterator(v)
    dicc = {}
    while (it.hasNext(iterator)):
        lista_values = it.next(iterator)
        pri = lista_values["lstaccidents"]
        seg = pri["first"]
        ter = seg["info"]
        if ter["Severity"] == "1":
            lt.addLast(lista_1, lista_values)
            # dicc[seg["info"]["Severity"]] = agregar_1

        elif ter["Severity"] == "2":
            lt.addLast(lista_2, lista_values)
            # dicc[seg["info"]["Severity"]] = agregar_2

        elif ter["Severity"] == "3":
            lt.addLast(lista_3, lista_values)
            # dicc[seg["info"]["Severity"]] = agregar_3

        else:
            lt.addLast(lista_4, lista_values)
            # dicc[seg["info"]["Severity"]] = agregar_4

    if lt.size(lista_1) > 0:
        dicc["1"] = lt.size(lista_1)
    if lt.size(lista_2) > 0:
        dicc["2"] = lt.size(lista_2)
    if lt.size(lista_3) > 0:
        dicc["3"] = lt.size(lista_3)
    if lt.size(lista_4) > 0:
        dicc["4"] = lt.size(lista_4)
    return (cantidad_2, dicc)


# Requerimiento 2
def getAccidentsBeforeDate(analyzer, initialDate):
    """
    Se desea conocer el total de accidentes ocurridos antes de una fecha específica.
    La fecha se debe ingresar siguiente el formato:(YYYYMM DD).
    Se debe indicar el total de accidentes ocurridos antes de la
    fecha indicada y la fecha en la que más accidentes se reportaron.

    """
    number_date = om.rank(analyzer['dateIndex'], initialDate)
    date_last = om.select(analyzer['dateIndex'], number_date-1)
    menor_llave = om.minKey(analyzer['dateIndex'])  # obtenemos la menor fecha
    # obtenemos el numero de accidentes
    total = 0
    total_keys = om.keys(analyzer['dateIndex'], menor_llave, date_last)
    iterador = it.newIterator(total_keys)
    date = ""  # fecha en la que ocurren más accidentes
    mayor_cantidad_accidentes = 0  # mayor numero de accidentes en una fecha
    while (it.hasNext(iterador)):  # iteramos las llaves
        llave = it.next(iterador)
        # obtenemos la cantidad de accidentes en una fecha
        obtener = om.get(analyzer["dateIndex"], llave)
        lista = (me.getValue(obtener))["lstaccidents"]
        cantidad = lista["size"]
        total += cantidad
        if cantidad > mayor_cantidad_accidentes:
            mayor_cantidad_accidentes = cantidad  # asignamos el numero de accidentes
            date = str(llave)  # asiganamos la fecha
    return (total, date)  # valor retornado


# Requerimiento 3

def getAccidentsByRange(analyzer, initialDate, finalDate):
    """
    Retorna el total de crimenes en un rango de fechas y indicando la categoría de
    accidentes más reportadas en dicho rango. Se debe responder con el
    número total de accidentes en ese rango de fechas,
    indicando la categoría de accidentes más reportadas en dicho rango.
    """
    l = om.values(analyzer['dateIndex'], initialDate, finalDate)
    iterator = it.newIterator(l)
    diccionario = {}
    accidents = 0
    while (it.hasNext(iterator)):
        lista_values = it.next(iterator)
        accidents += lt.size(lista_values["lstaccidents"])

        if lista_values["lstaccidents"]["first"]["info"]["Severity"] in diccionario:
            diccionario[lista_values["lstaccidents"]
                        ["first"]["info"]["Severity"]] += 1
        else:
            diccionario[lista_values["lstaccidents"]
                        ["first"]["info"]["Severity"]] = 1
    return (accidents, diccionario)


# Requerimiento 4
def getAccidentsByRangeState(analyzer, initialDate, finalDate):
    """
    Se desea conocer para un rango de fechas el estado que más accidentes tiene
    reportados. El usuario ingresa una fecha inicial y una fecha final en formato: YYYY MM DD. Se
    debe retornar la fecha con más accidentes reportados.
    """
    l = om.values(analyzer['dateIndex'], initialDate, finalDate)
    iterator = it.newIterator(l)
    diccionario = {}
    accidents = 0
    while (it.hasNext(iterator)):
        lista_values = it.next(iterator)
        accidents += lt.size(lista_values["lstaccidents"])

        if lista_values["lstaccidents"]["first"]["info"]["State"] in diccionario:
            diccionario[lista_values["lstaccidents"]
                        ["first"]["info"]["State"]] += 1
        else:
            diccionario[lista_values["lstaccidents"]
                        ["first"]["info"]["State"]] = 1
    return (accidents, diccionario)
# Requerimiento 5


def getAccidentsByRangeHours(analyzer, initialDate, finalDate):
    """
    Se desea conocer para un rango de horas dado (hora inicial y hora final), el total de accidentes
    registrados agrupados por severidad Igualmente se desea conocer el porcentaje que ese número
    representa contra el total de accidentes reportados.
    """
    pass
# Requerimiento 6


def getAccidentsGeographicalArea(analyzer, length, latitude, radio):
    """
    Dada una latitud y una longitud, tomado como punto central, y un radio dado (por
    ejemplo una milla), informar cuántos accidentes en total se han producido en
    ese radio desde el punto de búsqueda. El resultado se debe presentar
    agrupado por el día de la semana en la que han ocurrido los accidentes y el total de
    accidentes reportados.
    """
    pass

# ==============================
# Funciones de Comparacion
# ==============================


def compareIds(id1, id2):
    """
    Compara dos crimenes
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1


def compareDates(date1, date2):
    """
    Compara dos ids de libros, id es un identificador
    y entry una pareja llave-valor
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1


def compareOffenses(offense1, offense2):
    """
    Compara dos ids de libros, id es un identificador
    y entry una pareja llave-valor
    """
    offense = me.getKey(offense2)
    if (offense1 == offense):
        return 0
    elif (offense1 > offense):
        return 1
    else:
        return -1
