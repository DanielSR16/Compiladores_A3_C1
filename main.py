from dataclasses import replace
from hashlib import new
from posixpath import split
import sys
from tokenize import String
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
import string
valor = ''
listaPrimaria = []
mayusculas = list(string.ascii_uppercase)
minusculas = list(string.ascii_lowercase)
letra = minusculas.extend(mayusculas)
encontrados = {
    'coma': [],
    'parentesis' : [],
    'palabraReservada':[],
    'letra': [],
    'numero' : []
    }
tokens = {
    
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
    print('ok ')
    for linea in listaPrimaria:

        auxString = ''
        for valores in linea:
            if valores != ':':
                auxString = auxString + valores
         
                if len(linea) == len(auxString):
                    print('soy normal xd')

            elif  valores == ':' :
                palabra = palabrasReservadas(auxString)
                print(palabra)
                if(palabra == 'BaseDeDatos'):
                    print('Soy base de datos')
                elif(palabra == 'NombreTabla'):
                    print('NombreTabla')
                elif(palabra == 'ListaCampo'):
                    print('ListasCampo')
                elif(palabra == 'LavePrimaria'):
                    print('PrimariKEY')
                    
        



def palabrasReservadas (palabra):
    print('a')
    for reservadas in tokens['palabraReservada']:
        if(palabra == reservadas):
            encontrados['palabraReservada'].append(palabra)

    return palabra


    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = index()
    GUI.show()
    sys.exit(app.exec_())