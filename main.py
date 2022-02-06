from dataclasses import replace
from hashlib import new
from json import tool
from operator import le
from posixpath import split
import sys
from tokenize import String
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from tabla import *
import string


valor = ''
listaPrimaria = []
mayusculas = list(string.ascii_uppercase)
minusculas = list(string.ascii_lowercase)
letra = minusculas + mayusculas

encontrados = {
    'guion' : [],
    'dosPuntos' : [],
    'coma': [],
    'parentesis' : [],
    'palabraReservada':[],
    'valor' :[],
    'letra': [],
    'digito' : [],
    'error' : []
    }

tokens = {
    'guion' : ['-'],
    'dosPuntos' : [':'],
    'coma': [','],
    'parentesis' : ['(',')'],

'palabraReservada':['BaseDeDatos','NombreTabla','ListaCampo','LlavePrimaria','noVacio','incrementarse'],
    'valor' : ['entero','enteroSuperPequeño','enteroPequeño'
                         'fecha','fechaHora','hora','textoPequeño','texto','textoMediano','textoLargo','textoLargo','dobleFlotante'
                         'cadenaDefinida','cadena','enteroMediano','enteroGande','enteroDecimal','decimalDoble'
                         'decimal','año'],
    
    'letra': letra,
    'digito' : ['1','2','3','4','5','6','7','8','9','0']
    
}
listaEncontrados = []
auxListaEncontrado = []
encontradosString = []

class index(QMainWindow):
    def __init__(self,data):
        super().__init__()
        self.data = data
        uic.loadUi("vista3.ui", self)
        self.boton.clicked.connect(self.input_to_List)
        self.tablaW.setColumnWidth(0,1500)
        
       

    def input_to_List(self):
        listaPrimaria.clear()
    
        valor:str = self.input.toPlainText()
        newvaL =  valor.replace('\n','*')
        newvaL = newvaL + '*'
        lineaNombreAux = ''
        for i in newvaL:
            # print(i)
            if i != '*' :
                lineaNombreAux = lineaNombreAux + i
            elif i == '*':
                newNombre = lineaNombreAux.replace(' ','')
                listaPrimaria.append(newNombre)
                lineaNombreAux = ''

        validarTokens()
        self.cargarData()
        self.mostrarError()
    def mostrarError(self):
        self.error.setText('')
        stringError = ''
        if(len(encontrados['error'])>0):
            for i in encontrados['error']:
                stringError = stringError + i
            self.error.setText('Error encontrador en: ' + stringError)
        encontrados['error'] = []

    def cargarData(self):
        self.tablaW.setRowCount(len(encontradosString))
        for  i in range(0,len(encontradosString)):
            self.tablaW.setItem(i,0,QtWidgets.QTableWidgetItem(encontradosString[i]))
            
        
      
      
       

    





def validarTokens():
    errorSimbolo = False
    for numLinea in range(0,len(listaPrimaria)):
        if errorSimbolo ==False:
            
            auxString = ''
            for valores in listaPrimaria[numLinea]:
                if valores != ':':
                    auxString = auxString + valores
            
                    if len(listaPrimaria[numLinea]) == len(auxString):
                        print('soy normal xd')
                        palabra = listaPrimaria[numLinea]
                        verificarTokens(palabra)
                        listaPrimaria[numLinea] = []
                elif  valores == ':' :
                    
                    existe_in_list_dosPuntos = ':' in encontrados['dosPuntos']
                    if( existe_in_list_dosPuntos == False):
                        encontrados['dosPuntos'].append(':')

                    palabra = palabrasReservadas(auxString)
                    
                    if(palabra == 'BaseDeDatos'):
                        auxListaEncontrado.append('PalabraReservada')
                        auxListaEncontrado.append('dosPuntos')
                        dataBD = listaPrimaria[numLinea][len(palabra)+1:len( listaPrimaria[numLinea])]
                        listaPrimaria[numLinea] = dataBD
                   
                        verificarTokens(listaPrimaria[numLinea])
                        listaPrimaria[numLinea] = []

                    elif(palabra == 'NombreTabla'):
                        auxListaEncontrado.append('PalabraReservada')
                        auxListaEncontrado.append('dosPuntos')
                        dataNT = listaPrimaria[numLinea][len(palabra)+1:len( listaPrimaria[numLinea])]
                        listaPrimaria[numLinea] = dataNT
                        verificarTokens(listaPrimaria[numLinea])
                        listaPrimaria[numLinea] = []
                  

                    elif(palabra == 'ListaCampo'):
                        auxListaEncontrado.append('PalabraReservada')
                        auxListaEncontrado.append('dosPuntos')
                        dataLC = listaPrimaria[numLinea][len(palabra)+1:len( listaPrimaria[numLinea])]
                        listaPrimaria[numLinea] = dataLC
                        verificarTokensCampo(listaPrimaria[numLinea])
                        listaPrimaria[numLinea] = []
               
                    elif(palabra == 'LlavePrimaria'):
                        auxListaEncontrado.append('PalabraReservada')
                        auxListaEncontrado.append('dosPuntos')
                        dataLP = listaPrimaria[numLinea][len(palabra)+1:len( listaPrimaria[numLinea])]
                        listaPrimaria[numLinea] = dataLP
                        verificarTokens(listaPrimaria[numLinea])
                        listaPrimaria[numLinea] = []
                 

                    else:
                        print('SoyNormal')
                        palabra = listaPrimaria[numLinea]
                        verificarTokens(palabra)
                        listaPrimaria[numLinea] = []
            listaAux= []
            listaAux.extend(auxListaEncontrado)
            listaEncontrados.append(listaAux)
            auxListaEncontrado.clear()
            if len(encontrados['error']) > 0:
               errorSimbolo = True
          
    # print('ListaEnocontrados')
    # print(listaEncontrados)
    listasToString()
    # print(encontradosString)
    for borrarEncontrado in range(0,len(listaEncontrados)):
        listaEncontrados.pop()      


        



def palabrasReservadas (palabra):
    for reservadas in tokens['palabraReservada']:
        if(palabra == reservadas):
            existe_in_list_reservada = palabra in  encontrados['palabraReservada'] 
            if existe_in_list_reservada == False:
                encontrados['palabraReservada'].append(palabra)


    return palabra
#cadena(10)-noVacio-incrementarse,
def verificarTokens(palabra):
 
    for letra in palabra:
        
        bandera = False
        if letra in tokens['dosPuntos'] :
            auxListaEncontrado.append('DosPuntos')
            bandera = True
        elif letra in tokens['coma']:
            auxListaEncontrado.append('coma')
            bandera = True
        elif letra in tokens['parentesis']:
            auxListaEncontrado.append('parentesis')
            bandera = True
        elif letra in tokens['letra']:
            auxListaEncontrado.append('letra')
            bandera = True
        elif letra in tokens['digito']:
            auxListaEncontrado.append('digito')
    
            bandera = True
        elif letra in tokens['guion']:
            auxListaEncontrado.append('guion')
         
            bandera = True
            
        if bandera == False:
            auxListaEncontrado.append('error')
            encontrados['error'].append(letra)

        
def verificarTokensCampo(palabra):
    campoAux = ''
    for letra in palabra:
           
            if letra != '-' and letra != ',' and letra != '(':
                # print(letra)
                campoAux = campoAux + letra
                if len(palabra) == len(campoAux):
               
                    verificarTokens(campoAux)

    
            # print(letra)
            if letra == '-':
    
                existe_in_list_valor = campoAux in tokens['valor']
                existe_in_list_reservadas = campoAux in tokens['palabraReservada']
                if existe_in_list_valor == True:
                    auxListaEncontrado.append('valor')
                    auxListaEncontrado.append('guion')
                elif existe_in_list_reservadas == True:
                    auxListaEncontrado.append('palabraReservada')
                    auxListaEncontrado.append('guion')
                else:
                    verificarTokens(campoAux)
                    auxListaEncontrado.append('guion')
                campoAux = ''
            elif letra == '(':
       
                print(campoAux)
                existe_in_list_reservadas1 = campoAux in tokens['valor']
               
                if existe_in_list_reservadas1 == True:
                    auxListaEncontrado.append('palabraReservada')
                    auxListaEncontrado.append('parentesis')
                else:
                    verificarTokens(campoAux)
                    auxListaEncontrado.append('parentesis')
                campoAux = ''
            
            elif letra == ',':
             
                existe_in_list_reservadas2 = campoAux in tokens['palabraReservada']
          
          
                if existe_in_list_reservadas2 == True:
                    auxListaEncontrado.append('palabraReservada')
                    auxListaEncontrado.append('coma')
                else:
                    verificarTokens(campoAux)
                    auxListaEncontrado.append('coma')
                campoAux = ''    
                        
def listasToString():
    auxEncontradosString = ''
    encontradosString .clear()

    for encontrado in listaEncontrados:
        for datos in encontrado:
            auxEncontradosString = auxEncontradosString + datos + ' '
        encontradosString.append(auxEncontradosString)
        auxEncontradosString = ''



                



        



    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = index(['daniel','juan'])
    GUI.show()
    sys.exit(app.exec_())


    