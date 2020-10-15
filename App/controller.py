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

import config as cf
from App import model
import datetime
import csv

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________


def init():
    """
    Llama la funcion de inicializacion del modelo.
    """
    analyzer = model.newAnalyzer()
    return analyzer


# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________

def loadData(analyzer, accidentsfile):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    accidentsfile = cf.data_dir + accidentsfile
    input_file = csv.DictReader(open(accidentsfile, encoding="utf-8"),
                                delimiter=",")
    for accident in input_file:
        model.addAccidents(analyzer, accident)
    return analyzer

# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________


def accidentsSize(analyzer):
    """
    Numero de crimenes leidos
    """
    return model.accidentsSize(analyzer)


def indexHeight(analyzer):
    """
    Altura del indice (arbol)
    """
    return model.indexHeight(analyzer)


def indexSize(analyzer):
    """
    Numero de nodos en el arbol
    """
    return model.indexSize(analyzer)


def minKey(analyzer):
    """
    La menor llave del arbol
    """
    return model.minKey(analyzer)


def maxKey(analyzer):
    """
    La mayor llave del arbol
    """
    return model.maxKey(analyzer)

# Requerimiento 1
def getCrimesByRangeCode(analyzer, initialDate):
    """
    Retorna el total de crimenes en una
    fecha determinada
    """
    initialDate = datetime.datetime.strptime(initialDate, '%Y-%m-%d')
    return model.getCrimesByDate(analyzer, initialDate.date())

# Requerimiento 2
def getAccidentsBeforeDate(analyzer, initialDate):
    """
    Se desea conocer el total de accidentes ocurridos antes de una fecha específica.
    La fecha se debe ingresar siguiente el formato:(YYYYMM DD). 
    Se debe indicar el total de accidentes ocurridos antes de la
    fecha indicada y la fecha en la que más accidentes se reportaron.
    """
    initialDate = datetime.datetime.strptime(initialDate, '%Y-%m-%d')
    return model.getAccidentsBeforeDate(analyzer, initialDate.date())
# Requerimiento 3
def getAccidentsByRange(analyzer, initialDate, finalDate):
    """
    Retorna el total de crimenes en un rango de fechas y indicando la categoría de
    accidentes más reportadas en dicho rango. Se debe responder con el
    número total de accidentes en ese rango de fechas,
    indicando la categoría de accidentes más reportadas en dicho rango. 
    """
    initialDate = datetime.datetime.strptime(initialDate, '%Y-%m-%d')
    finalDate = datetime.datetime.strptime(finalDate, '%Y-%m-%d')
    return model.getAccidentsByRange(analyzer, initialDate.date(),
                                  finalDate.date())
# Requerimiento 4
def getAccidentsByRangeState(analyzer, initialDate, finalDate):
    """
    Se desea conocer para un rango de fechas el estado que más accidentes tiene
    reportados. El usuario ingresa una fecha inicial y una fecha final en formato: YYYY MM DD. Se
    debe retornar la fecha con más accidentes reportados.
    """ 
    initialDate = datetime.datetime.strptime(initialDate, '%Y-%m-%d')
    finalDate = datetime.datetime.strptime(finalDate, '%Y-%m-%d')
    return model.getAccidentsByRangeState(analyzer, initialDate.date(),
                                  finalDate.date())
# Requerimiento 5
def getAccidentsByRangeHours(analyzer, initialDate, finalDate):
    """
    Se desea conocer para un rango de horas dado (hora inicial y hora final), el total de accidentes 
    registrados agrupados por severidad Igualmente se desea conocer el porcentaje que ese número
    representa contra el total de accidentes reportados. 
    """ 
    initialDate = datetime.datetime.strptime(initialDate, '%h-%m-%s')
    finalDate = datetime.datetime.strptime(finalDate, '%h-%m-%s')
    return model.getAccidentsByRangeHours(analyzer, initialDate.date(),
                                  finalDate.date())

# Requerimiento 6
def getAccidentsGeographicalArea(analyzer, length, latitude, radio):
    """
    Dada una latitud y una longitud, tomado como punto central, y un radio dado (por
    ejemplo una milla), informar cuántos accidentes en total se han producido en
    ese radio desde el punto de búsqueda. El resultado se debe presentar
    agrupado por el día de la semana en la que han ocurrido los accidentes y el total de
    accidentes reportados. 
    """
    return model.getAccidentsByRangeHours(analyzer, initialDate.date(),
                                  finalDate.date())



