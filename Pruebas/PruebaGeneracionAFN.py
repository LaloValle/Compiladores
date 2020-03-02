from Automatas import *
from ExpresionRegular import *
from GeneradorAutomatas import *
import sys

expresion = sys.argv[1]

ER = ExpresionRegular(expresion)
ER.reconocerAlfabeto()
error, mensaje = ER.conversionAPostfija()

if error != -1:
    afn,mensaje = GeneradorAFN.generarAFNDePostfija(ER.getExpresionPostfija(),ER.getAlfabeto())

    if afn != -1:
        n,mensaje2 = afn.renombreAutomaticoEstados('e')

        #Probamos la función mover
        generadorAFD = GeneradorAFD()

        conjunto = generadorAFD._cerraduraEpsilon({afn.getEstadoInicial()})

        conjunto2 = generadorAFD._irA(set(conjunto), 'a')
        afnAux = afn

        afd = GeneradorAFD.generarAFDDeAFN(afnAux)

        tabular = ManejadorTabulares.generarTabular(afd, 'nombre')
        ManejadorTabulares.imprimirTablaConsola(tabular)

        tabular = ManejadorTabulares.recuperarTabular('nombre.dat')
        print(tabular,'tabular')
        ManejadorTabulares.imprimirTablaConsola(tabular)

        afd2 = ManejadorTabulares.generarAFDDeTabular(tabular)

else:
    print('Error' + mensaje)
