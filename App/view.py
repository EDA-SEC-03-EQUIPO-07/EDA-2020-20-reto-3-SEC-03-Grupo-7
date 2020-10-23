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

import sys
import config
from App import controller
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Ruta a los archivos
# ___________________________________________________
# C:\Users\home\Desktop\LABORATORIOS\Reto3-202020-Template\Data\us_accidents_dis_2017.csv
# C:\Users\home\Desktop\LABORATORIOS\Reto3-202020-Template\Data\us_accidents_dis_2016.csv
# us_accidents_small.csv
# us_accidents_dis_2017.csv
# us_accidents_dis_2016.csv
# US_Accidents_Dec19.csv
accidentsfile = 'us_accidents_small.csv'

# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de accidentes")
    print("3- Accidentes en una fecha determinada")
    print("4- Accidentes antes de una fechas determinada")
    print("5- Accidentes en un rango de fechas determinada")
    print("6- Accidentes en un Estado en un rango de fechas determinada")
    print("7- Accidentes por rango de horas")
    print("8- Accidente de una zona")
    print("0- Salir")
    print("*******************************************")


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()
    elif int(inputs[0]) == 2:
        if controller.accidentsSize(cont) < 2:
            print("\nCargando información de accidentes ....")
            controller.loadData(cont, accidentsfile)
            print('Accidentes cargados: ' + str(controller.accidentsSize(cont)))
            print('Altura del arbol: ' + str(controller.indexHeight(cont)))
            print('Elementos en el arbol: ' + str(controller.indexSize(cont)))
            print('Menor Llave: ' + str(controller.minKey(cont)))
            print('Mayor Llave: ' + str(controller.maxKey(cont)))
        else:
            print('Los datos ya fueron cargados.\n')

    elif int(inputs[0]) == 3:
        print("\nBuscando accidentes en un fecha determinada: ")
        accidents_date = input("Ingrese la fecha para conocer los accidentes")
        number = controller.getCrimesByRangeCode(cont, accidents_date)
        print("\n Total de accidentes en la fecha " +
              accidents_date + " es: " + str(number))

    elif int(inputs[0]) == 4:
        print("\nBuscando accidentes en un fecha determinada: ")
        accidents_date = input("Ingrese la fecha para conocer los accidentes")
        number = controller.getAccidentsBeforeDate(cont, accidents_date)
        print("\n Total de accidentes antes de la fecha " +
              accidents_date + " es: " + str(number))

    elif int(inputs[0]) == 5:
        print("\nBuscando accidentes en un fecha determinada: ")
        accidents_date = input("Ingrese la fecha inicial")
        accidents_date_1 = input("Ingrese la fecha final")
        number = controller.getAccidentsByRange(
            cont, accidents_date, accidents_date_1)
        print("\n Total de accidentes entre la fecha " +
              accidents_date + " y la fecha " + accidents_date_1 + " es: " + str(number))

    elif int(inputs[0]) == 6:
        print("\nBuscando accidentes en un Estado en un fecha determinada: ")
        accidents_date = input("Ingrese la fecha inicial")
        accidents_date_1 = input("Ingrese la fecha final")
        number = controller.getAccidentsByRangeState(
            cont, accidents_date, accidents_date_1)
        print("\n Total de accidentes en un Estado entre la fecha " +
              accidents_date + " y la fecha " + accidents_date_1 + " es: " + str(number))
    elif int(inputs[0]) == 7:
        print("\nBuscando accidentes en un rango horario: ")
        accidents_date = input("Ingrese la hora inicial\n")
        accidents_date_1 = input("Ingrese la hora final\n")
        uno,dos,tres,cuatro,porcentaje = controller.getAccidentsByRangeHours(
            cont, accidents_date, accidents_date_1)
        print(f"\nTotal de accidentes entre el rango horario {accidents_date} y la fecha {accidents_date_1}" 
        + f" es:\nTipo 1: {uno}\nTipo 2: {dos}\nTipo 3: {tres}\nTipo 4: {cuatro}\nLos cuales representan un {porcentaje}% de los accidentes totales.\nNOTA: Los rangos de horas usados fueron aproximados.\n")
    elif int(inputs[0]) == 8:
        print("\nBuscando accidentes en un zona demeterminada: ")
        latitud = input("Ingrese la latitud\n")
        longitud = input("Ingrese la longitud\n")
        radio = input("Ingrese el radio de busqueda en Kilometros\n")
        l,m,w,j,v,s,d = controller.getAccidentsGeographicalArea(cont, latitud, longitud, radio)
        print(f"\nEn esta zona se han presentado los siguientes accidentes:\nLunes: {l}\nMartes: {m}\nMiercoles: {w}\nJueves: {j}\nViernes: {v}\nSabado: {s}\nDomingo: {d}\nTotal de accidentes: {l+m+w+j+v+s+d}.\n")
    else:
        sys.exit(0)


sys.exit(0)