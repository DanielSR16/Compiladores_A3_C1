from dataclasses import replace
from hashlib import new
from operator import le
from posixpath import split
from re import T
import sys
from tokenize import String
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
import string
valor = ''
listaPrimaria = []
mayusculas = list(string.ascii_uppercase)
minusculas = list(string.ascii_lowercase)
letra = minusculas + mayusculas

encontrados = {
    'dosPuntos' : [],
    'coma': [],
    'parentesis' : [],
    'palabraReservada':[],
    'letra': [],
    'numero' : [],
    'error' : []
    }
tokens = {
    'dosPuntos' : [':'],
    'coma': [','],
    'parentesis' : ['(',')'],
    'palabraReservada':['BaseDeDatos','NombreTabla','ListaCampo','LavePrimaria','entero','enteroSuperPequeño','enteroPequeño'
                         'fecha','fechaHora','hora','textoPequeño','texto','textoMediano','textoLargo','textoLargo','dobleFlotante'
                         'cadenaDefinida','noVacio','autoIncremento','cadena','enteroMediano','enteroGande','enteroDecimal','decimalDoble'
                         'decimal','año'],
    'letra': letra,
    'numero' : ['1','2','3','4','5','6','7','8','9','0']
    
}
class index(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("vista3.ui", self)
      
        self.boton.clicked.connect(self.input_to_List)
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
 






def validarTokens():
   
    for numLinea in range(0,len(listaPrimaria)):
        
        auxString = ''
        for valores in listaPrimaria[numLinea]:
            if valores != ':':
                auxString = auxString + valores
         
                if len(listaPrimaria[numLinea]) == len(auxString):
                    print('soy normal xd')

            elif  valores == ':' :
                existe_in_list_dosPuntos = ':' in encontrados['dosPuntos']
                if( existe_in_list_dosPuntos == False):
                    encontrados['dosPuntos'].append(':')

                palabra = palabrasReservadas(auxString)
                
                if(palabra == 'BaseDeDatos'):
                    dataBD = listaPrimaria[numLinea][len(palabra)+1:len( listaPrimaria[numLinea])]
                    listaPrimaria[numLinea] = dataBD
                    print('Soy base de datos')
                    verificarTokens(listaPrimaria[numLinea])
                elif(palabra == 'NombreTabla'):
                    dataNT = listaPrimaria[numLinea][len(palabra)+1:len( listaPrimaria[numLinea])]
                    listaPrimaria[numLinea] = dataNT
                    verificarTokens(listaPrimaria[numLinea])
                    print('NombreTabla')
                elif(palabra == 'ListaCampo'):
                    dataLC = listaPrimaria[numLinea][len(palabra)+1:len( listaPrimaria[numLinea])]
                    listaPrimaria[numLinea] = dataLC
                    print('ListasCampo')
                elif(palabra == 'LavePrimaria'):
                    dataLP = listaPrimaria[numLinea][len(palabra)+1:len( listaPrimaria[numLinea])]
                    listaPrimaria[numLinea] = dataLP
                    print('PrimariKEY')
                else:
                   print()

    print(encontrados)     
    print('listaPrimaria')
    print(listaPrimaria)           
        



def palabrasReservadas (palabra):
    for reservadas in tokens['palabraReservada']:
        if(palabra == reservadas):
            existe_in_list_reservada = palabra in  encontrados['palabraReservada'] 
            if existe_in_list_reservada == False:
                encontrados['palabraReservada'].append(palabra)
    

    return palabra

def verificarTokens(palabra):

    print('soy lo proximo a verificar: ',palabra)
    for letra in palabra:
        bandera = False
        if letra in tokens['dosPuntos']:
            existe_in_list_dosPuntos = letra in encontrados['dosPuntos']
            if existe_in_list_dosPuntos == False:
                encontrados['dosPuntos'].append(letra)
            bandera = True
        elif letra in tokens['coma']:
            existe_in_list_dosPuntos = letra in encontrados['coma']
            if existe_in_list_dosPuntos == False:
                encontrados['coma'].append(letra)
            bandera = True
        elif letra in tokens['parentesis']:
            existe_in_list_parentesis = letra in encontrados['parentesis']
            if existe_in_list_parentesis == False:
                encontrados['parentesis'].append(letra)
            bandera = True
        elif letra in tokens['letra']:
            existe_in_list_letra = letra in encontrados['letra']
            if existe_in_list_letra == False:
                encontrados['letra'].append(letra) 
            bandera = True
        elif letra in tokens['numero']:
            existe_in_list_numero = letra in encontrados['numero']
            if existe_in_list_numero == False:
                encontrados['numero'].append(letra) 
            bandera = True
        if bandera == False:
            encontrados['error'].append(letra)
            
        



    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = index()
    GUI.show()
    sys.exit(app.exec_())


    