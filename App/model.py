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
import math
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
                'dateIndex': None,
                'timeIndex': None
                }

    analyzer['accidents'] = lt.newList('SINGLE_LINKED', compareIds)
    analyzer['dateIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
    analyzer['timeIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
    return analyzer

# Funciones para agregar informacion al catalogo


def addAccidents(analyzer, accident):
    """
    """
    lt.addLast(analyzer['accidents'], accident)
    updateDateIndex(analyzer['dateIndex'], accident)
    updateTimeIndex(analyzer['timeIndex'], accident)
    return analyzer


def updateTimeIndex(map, accident):
    accidentTime = getTime(accident['Start_Time'])
    entry = om.get(map, accidentTime)
    if entry is None:
        timeentry = newDataEntry()
        om.put(map, accidentTime, timeentry)
    else:
        timeentry = me.getValue(entry)
    addDateIndex(timeentry, accident)
    return map



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
        datentry = newDataEntry()
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
    lt.addLast(datentry['lstaccidents'], accident)
    datentry[str(accident['Severity'])] += 1
    datentry['total'] += 1
    return datentry

def newDataEntry():
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'lstaccidents': None,'1':0,'2':0,'3':0,'4':0,'total':0}
    entry['lstaccidents'] = lt.newList('SINGLE_LINKED', compareDates)
    return entry

#Función para fijar una fecha en intervalos de 30 minutos
def getTime(date):
    time = datetime.datetime.strptime(date,'%Y-%m-%d %H:%M:%S')
    hour = time.hour
    minute = time.minute
    sMinute = ''
    if minute >= 20 and minute <= 40:
        sMinute = '30'
    elif minute < 20:
        sMinute = '00'
    elif minute > 40:
        if hour < 23:
            sMinute = '00'
            hour += 1
        else:
            sMinute = '59'

    
    if hour >= 10:
        sHour = str(hour)
    else:
        sHour = '0' + str(hour)

    return sHour+':'+sMinute


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
def getCrimesByDate(analyzer, initialDate):
    obtener = om.get(analyzer["dateIndex"], initialDate)
    value = me.getValue(obtener)
    dicc = {'1':value['1'],'2':value['2'],'3':value['3'],'4':value['4']}
    return dicc


# Requerimiento 2
def getAccidentsBeforeDate(analyzer, initialDate):
    """
    Se desea conocer el total de accidentes ocurridos antes de una fecha específica.
    La fecha se debe ingresar siguiente el formato:(YYYYMM DD).
    Se debe indicar el total de accidentes ocurridos antes de la
    fecha indicada y la fecha en la que más accidentes se reportaron.

    """
    present = om.contains(analyzer['dateIndex'], initialDate)
    if present == True:
        number_date = om.rank(analyzer['dateIndex'], initialDate)
        date_last = om.select(analyzer['dateIndex'], number_date)
        # obtenemos la menor fecha
        menor_llave = om.minKey(analyzer['dateIndex'])
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
        re = (total, date)
    else:
        re = "Ingrese otra fecha"
    return re  # valor retornado


# Requerimiento 3

def getAccidentsByRange(analyzer, initialDate, finalDate):
    """
    Retorna el total de crimenes en un rango de fechas y indicando la categoría de
    accidentes más reportadas en dicho rango. Se debe responder con el
    número total de accidentes en ese rango de fechas,
    indicando la categoría de accidentes más reportadas en dicho rango.
    """

    l = om.keys(analyzer['dateIndex'], initialDate, finalDate)
    iterator = it.newIterator(l)
    dicc_Severity = {'1':0,'2':0,'3':0,'4':0}
    accidents = 0
    while (it.hasNext(iterator)):
        lista_keys = it.next(iterator)
        keys = om.get(analyzer["dateIndex"], lista_keys)
        value = me.getValue(keys)
        accidents += value['total']
        dicc_Severity['1'] += value['1']
        dicc_Severity['2'] += value['2']
        dicc_Severity['3'] += value['3']
        dicc_Severity['4'] += value['4']
        
    dic = {}
    name = ""
    number = 0
    for re in dicc_Severity:
        if dicc_Severity[re] > number:
            name = re
            number = dicc_Severity[re]
    dic[name] = number
    return (accidents, dic)

# Requerimiento 4


def getAccidentsByRangeState(analyzer, initialDate, finalDate):
    """
    Se desea conocer para un rango de fechas el estado que más accidentes tiene
    reportados. El usuario ingresa una fecha inicial y una fecha final en formato: YYYY MM DD. Se
    debe retornar la fecha con más accidentes reportados.
    """
    dicc_State = {}
    total_keys = om.keys(analyzer['dateIndex'], initialDate, finalDate)
    iterador = it.newIterator(total_keys)
    date = ""  # fecha en la que ocurren más accidentes
    mayor_cantidad_accidentes = 0  # mayor numero de accidentes en una fecha
    while (it.hasNext(iterador)):  # iteramos las llaves
        llave = it.next(iterador)
        # obtenemos la cantidad de accidentes en una fecha
        obtener = om.get(analyzer["dateIndex"], llave)
        values = (me.getValue(obtener))["lstaccidents"]
        cantidad = values["size"]
        ite = it.newIterator(values)
        while (it.hasNext(ite)):
            valor = it.next(ite)
            if valor["State"] in dicc_State:
                dicc_State[valor["State"]] += 1
            else:
                dicc_State[valor["State"]] = 1

        if cantidad > mayor_cantidad_accidentes:
            mayor_cantidad_accidentes = cantidad  # asignamos el numero de accidentes
            date = str(llave)  # asiganamos la fecha

    diccionario = {}
    name = ""
    number = 0
    for re in dicc_State:
        if dicc_State[re] > number:
            name = re
            number = dicc_State[re]
    diccionario[name] = number
    return (date, diccionario)  # valor retornado


# Requerimiento 5
def getAccidentsByRangeHours(analyzer, initialDate, finalDate):
    """
    Se desea conocer para un rango de horas dado (hora inicial y hora final), el total de accidentes
    registrados agrupados por severidad Igualmente se desea conocer el porcentaje que ese número
    representa contra el total de accidentes reportados.
    """
    l = om.keys(analyzer['timeIndex'], str(initialDate), str(finalDate)) #Se obtiene las llaves del arbol que se cubren ese rando de horas
    iterator = it.newIterator(l)
    dicc_Severity = {'1':0,'2':0,'3':0,'4':0}
    accidents = 0
    while (it.hasNext(iterator)): #Recorremos las llaves de nuestro rango de horas
        lista_keys = it.next(iterator)
        keys = om.get(analyzer["timeIndex"], lista_keys) #Obtenemos la pareja llave-valor

        value = me.getValue(keys)   #Obtenemos el valor (diccionario) perteneciente a esa llave
        dicc_Severity['1'] += value['1']
        dicc_Severity['2'] += value['2']
        dicc_Severity['3'] += value['3']
        dicc_Severity['4'] += value['4']
        accidents += value["total"]

    total = analyzer['accidents']['size']
    return dicc_Severity['1'], dicc_Severity['2'], dicc_Severity['3'], dicc_Severity['4'], (accidents/total)*100

# Requerimiento 6
def getAccidentsGeographicalArea(analyzer, latitude, length, radio):
    """
    Dada una latitud y una longitud, tomado como punto central, y un radio dado (por
    ejemplo una milla), informar cuántos accidentes en total se han producido en
    ese radio desde el punto de búsqueda. El resultado se debe presentar
    agrupado por el día de la semana en la que han ocurrido los accidentes y el total de
    accidentes reportados.
    """
    dayDicc = {'Sunday':0,'Monday':0,'Tuesday':0,'Wednesday':0,'Thursday':0,'Friday':0,'Saturday':0}
    iterator = it.newIterator(analyzer['accidents'])
    while (it.hasNext(iterator)): #Se recorre toda la lista accidentes
        valor = it.next(iterator)
        latp = valor['Start_Lat']
        lonp = valor['Start_Lng']
        if pointCircle(radio, latitude, length, latp, lonp): #Revisa si el accidente se encuntra dentro del radio
            date = valor['Start_Time']
            day = datetime.datetime.strptime(date,'%Y-%m-%d %H:%M:%S').strftime('%A') #Obtenemos el dia de la semana de la fecha
            dayDicc[day] += 1
    return dayDicc['Monday'], dayDicc['Tuesday'], dayDicc['Wednesday'], dayDicc['Thursday'], dayDicc['Friday'], dayDicc['Saturday'], dayDicc['Sunday']

def pointCircle(radio, latc, lonc, latp, lonp):
    # Formula de Haversine
    R = 6371 # Radio de la tierra en Km
    dLat = aRadianes(float(latp)-float(latc)) # Pasar a radianes
    dLon = aRadianes(float(lonp)-float(lonc))
    a = math.sin(dLat/2)**2 + math.cos(aRadianes(float(latc))) * math.cos(aRadianes(float(latp))) * math.sin(dLon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c # Distancia en km
    return d <= float(radio)

def aRadianes(deg):
    return deg * (float(math.pi)/180.0)

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