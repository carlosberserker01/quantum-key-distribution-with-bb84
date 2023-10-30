import tkinter as tk
from pandastable import Table
import pandas as pd
import random as rd
import pyperclip
import re

longitudDf = 0
qubitsAlice= 0
qubitsEva = 0
dfBob = 0
dfEva = 0
dfImpresion = 0
banderaEva = 0
numAlteraciones = 0
claveFinal = 0

def generarClave():
    botonCopiar.config(state="normal")

    textoBlanco.grid_remove()
    longitudDf = entryLongitud.get()
    dfAlice = pd.DataFrame(ArrAleatorio(longitudDf))
    dfAlice.columns = ['Bit']
    dfAlice['Base'] = ArrAleatorio(longitudDf)
    dfAlice['Qubit Alice'] = dfAlice.apply(CalcularQubit, axis=1)
    dfAlice.columns = ['Bit Alice', 'Base Alice', 'Qubit Alice']
    qubitsAlice = dfAlice['Qubit Alice']

    if banderaEva == True:
        # SI está espiando Eva
        dfEva = pd.DataFrame(ArrAleatorio(longitudDf))
        dfEva.columns = ['Base elegida']
        dfEva['Qubit recibido'] = qubitsAlice
        dfEva = dfEva[['Qubit recibido', 'Base elegida']]
        dfEva['Qubit Eva'] = dfEva.apply(CalcularBitMedido, axis=1)
        dfEva.columns = ['Qubit recibido', 'Base Eva', 'Qubit Eva']
        qubitsEva = dfEva['Qubit Eva']
        dfBob = generarBob(qubitsEva)
        dfImpresion = dfAlice
        dfImpresion = pd.concat([dfImpresion, dfEva.drop('Qubit recibido', axis=1)], axis=1)
        dfImpresion = pd.concat([dfImpresion, dfBob.drop('Qubit recibido', axis=1)], axis=1)
    else:
        dfBob = generarBob(qubitsAlice)
        dfImpresion = dfAlice
        dfImpresion = pd.concat([dfImpresion, dfBob.drop('Qubit recibido', axis=1)], axis=1)

    tabla = Table(frame, dataframe=dfImpresion, showtoolbar=True, showstatusbar=True)
    tabla.show()
    tabla.editable = False

    mostrarClave(dfAlice, dfBob)

def mostrarClave(dfRecibidoA, dfRecibidoB):
    dfComparacion = pd.DataFrame(dfRecibidoA['Bit Alice'])
    dfComparacion['Base Alice'] = dfRecibidoA['Base Alice']
    dfComparacion['Bit Bob'] = dfRecibidoB['Qubit Bob']
    dfComparacion['Base Bob'] = dfRecibidoB['Base Bob']
    dfComparacion['Bit Bob'] = dfComparacion['Bit Bob'].replace({"|0>": 0, "|1>": 1, "|+>": 0, "|->": 1})
    dfFiltroBases = dfComparacion[(dfComparacion['Base Alice'] == dfComparacion['Base Bob'])]

    dfFiltroBitsDistintos = dfFiltroBases[(dfFiltroBases['Bit Alice'] != dfFiltroBases['Bit Bob'])]
    global numAlteraciones
    numAlteraciones = dfFiltroBitsDistintos.shape[0]

    labelEva.config(text="Se han detectado " + str(numAlteraciones) + " alteraciones en los bits enviados")
    labelEva.config(foreground='black') 
    
    dfFiltroBitsIguales = dfFiltroBases[(dfFiltroBases['Bit Alice'] == dfFiltroBases['Bit Bob'])]
    dfClaveBit = pd.DataFrame(dfFiltroBitsIguales['Bit Bob'])
    dfClaveBit = dfClaveBit.rename(columns={'Bit Bob': 'Clave'})
    dfClaveBit = dfClaveBit.reset_index(drop=True)
    dfClaveBit.index = range(len(dfClaveBit))

    if(dfClaveBit.shape[0] == 0):
        dfClaveBit = 0
    else:
        global claveFinal
        clave = dfClaveBit.to_string(index=False)
        claveFinal = ''.join(re.findall(r'\d', clave))

    mostradorClave.config(state="normal")
    mostradorClave.delete("1.0", "end")
    mostradorClave.insert("1.0", claveFinal)
    mostradorClave.config(state="disabled")

def generarBob(qubitsRecibidos):
    longitudDf = entryLongitud.get()
    dfBob = pd.DataFrame(ArrAleatorio(longitudDf))
    dfBob.columns = ['Base elegida']
    dfBob['Qubit recibido'] = qubitsRecibidos
    dfBob = dfBob[['Qubit recibido', 'Base elegida']]
    dfBob['Qubit Bob'] = dfBob.apply(CalcularBitMedido, axis=1)
    dfBob.columns = ['Qubit recibido', 'Base Bob', 'Qubit Bob']
    return dfBob

def verificarContenido(event):
    if not entryLongitud.get() and event.char:
        botonMaestro.config(state="normal")

def ArrAleatorio(long):
    arr= []
    for i in range(1,int(long)+1):
        arr.append(rd.randint(0,1))
    return arr

def CalcularQubit(fila):
    if fila['Bit'] == 0 and fila['Base'] == 0:
        return "|0>"
    if fila['Bit'] == 0 and fila['Base'] == 1:
        return "|+>"
    if fila['Bit'] == 1 and fila['Base'] == 0:
        return "|1>"
    if fila['Bit'] == 1 and fila['Base'] == 1:
        return "|->"

def CalcularBitMedido(fila):
    if fila['Qubit recibido']=="|0>" and fila['Base elegida']==0:
        return "|0>"
    if fila['Qubit recibido']=="|0>" and fila['Base elegida']==1:
        tmp = rd.randint(0,1)
        return "|+>" if tmp==0 else "|->"
    if fila['Qubit recibido']=="|1>" and fila['Base elegida']==0:
        return "|1>"
    if fila['Qubit recibido']=="|1>" and fila['Base elegida']==1:
        tmp = rd.randint(0,1)
        return "|+>" if tmp==0 else "|->"
    
    if fila['Qubit recibido']=="|+>" and fila['Base elegida']==0:
        tmp = rd.randint(0,1)
        return "|0>" if tmp==0 else "|1>"
    if fila['Qubit recibido']=="|+>" and fila['Base elegida']==1:
        return "|+>"
    if fila['Qubit recibido']=="|->" and fila['Base elegida']==0:
        tmp = rd.randint(0,1)
        return "|0>" if tmp==0 else "|1>"
    if fila['Qubit recibido']=="|->" and fila['Base elegida']==1:
        return "|->"

def FuncionEva():
    global banderaEva
    if var.get() == 1:
        banderaEva = True
    else:
        banderaEva = False

def CopiarClave():
    pyperclip.copy(claveFinal)

ventana = tk.Tk()
ventana.title("Protocolo BB84")
ventana.geometry("1100x700")
ventana.columnconfigure(0, weight=1)
ventana.columnconfigure(1, weight=1)
ventana.columnconfigure(2, weight=1)
ventana.rowconfigure(0, weight=1)
ventana.rowconfigure(1, weight=1)
ventana.rowconfigure(2, weight=1)
ventana.rowconfigure(3, weight=1)
ventana.grid_rowconfigure(4, minsize=25)
ventana.resizable(width=False, height=False)

labelLongitud = tk.Label(ventana, text="Número de bits para generar:")
labelLongitud.grid(row=0, column=0)

entryLongitud = tk.Entry(ventana)
entryLongitud.grid(row=0, column=0)
entryLongitud.place(x=240, y=29)
longitudDF = entryLongitud.get()

entryLongitud.bind("<Key>", verificarContenido)

var = tk.IntVar()
checkbuttonEva = tk.Checkbutton(ventana, text="Incluir Eva", variable=var, command=FuncionEva)
checkbuttonEva.grid(row=0, column=2)

labelProcesamiento = tk.Label(ventana, text="Tablas de los qubits:")
labelProcesamiento.grid(row=1, column=0)

botonMaestro = tk.Button(ventana, text="Generar tabla", width=25, command=generarClave)
botonMaestro.grid(row=1, column=2)
botonMaestro.config(state="disabled")

labelClave = tk.Label(ventana, text="Clave:")
labelClave.grid(row=3, column=0, sticky='n')

mostradorClave = tk.Text(ventana, wrap=tk.WORD, bg="white", width=85, height=1, font=('Arial', 10))
mostradorClave.grid(row=3, column=0, columnspan=2, sticky="n")
mostradorClave.place(x=210, y=617)
mostradorClave.config(state="disabled")

botonCopiar = tk.Button(ventana, text="Copiar clave", width=25, command=CopiarClave)
botonCopiar.grid(row=3, column=2, sticky="n")
botonCopiar.config(state="disabled")

frame = tk.Frame(ventana)
frame.grid(row=2, column=0, columnspan=3)

textoBlanco = tk.Text(ventana, wrap=tk.WORD, bg=ventana.cget('background'), width=70, height=30, font=('Arial', 10))
textoBlanco.grid(row=2, column=0, columnspan=3, sticky="n")
textoBlanco.config(highlightbackground=ventana.cget('background'))
textoBlanco.config(highlightthickness=0)
textoBlanco.config(state="disabled")

labelEva = tk.Label(ventana, text="Se han detectado " + str(numAlteraciones) + " alteraciones en los bits enviados")
labelEva.grid(row=3, column=1, sticky="w")
labelEva.config(foreground=ventana.cget('background'))

ventana.mainloop()