import pickle
from random import randint, choice, shuffle
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import filedialog, messagebox

import copy

from Combinaciones import *

tablero, matrizTablero, matrizF = [], [], []
tamanioCuadricula = 0


def verificar(fila, tamanio):
    cont = 0
    inicio = -1
    for i in range(tamanio):
        if(fila[i] == 0):
            if(cont == 0):
                inicio = i
            cont += 1
        if(fila[i] != 0 and cont <= 9):
            inicio = -1
            cont = 0
    if cont > 9:
        return inicio
    else:
        return -1


def separarDigitos(num):
    lista = []
    while(num != 0):
        dig = num % 10
        lista += [str(dig)]
        num = num // 10
    shuffle(lista)
    return lista


def verificarRepetidosAbajo(i, j, valor, tamanio):
    while(matrizTablero[i][j] != "&"):
        if(matrizTablero[i][j] == valor):
            return False
        if(i+1 < tamanio):
            i += 1
        else:
            return True
    return True


def verificarRepetidosArriba(i, j, valor):
    while(matrizTablero[i][j] != "&"):
        if(matrizTablero[i][j] == valor):
            return False
        if(i-1 >= 0):
            i -= 1
        else:
            return True
    return True


def ultimosNegros(tamanio):
    for i in range(tamanio):
        for j in range(tamanio):
            if(matrizTablero[i][j] == 0):
                matrizTablero[i][j] = "&"
                tablero[i][j].set_background("black")
    for i in range(tamanio):
        for j in range(tamanio):
            try:
                if (matrizTablero[i - 1][j] == "&" and matrizTablero[i + 1][j] == "&"
                    and matrizTablero[i][j - 1] == "&" and matrizTablero[i][j + 1] == "&"):
                    matrizTablero[i][j] = "&"
                    tablero[i][j].set_background("black")
            except:
                matrizTablero[i][j] = "&"
                tablero[i][j].set_background("black")
                # print(matrizTablero)


def sumaHorizontal(tamanio):
    for i in range(tamanio):
        cont = 1
        for j in range(tamanio):
            if(matrizTablero[i][j] == "&"):
                suma = 0
                cont = 1
                if (j + cont < tamanio):
                    while(matrizTablero[i][j+cont] != "&"):
                        # print(i, "i", j, "j")
                        suma += int(matrizTablero[i][j+cont])
                        if(j+cont+1 < tamanio):
                            cont += 1
                        else:
                            break
                    # print(suma)
                    if(suma != 0 and suma < 46):
                        if(suma == 2 and cont > 2):
                            pass
                        else:
                            matrizTablero[i][j] = str(suma)+"&"
                            tablero[i][j].set_nHorizontal(suma)
                            tablero[i][j].set_foreground("white")
                            tablero[i][j].set_text(True, "H")


def validarAmp(string):
    if("&" in string):
        return True
    else:
        return False


def sumaVertical(tamanio):
    for i in range(tamanio):
        cont = 1
        for j in range(tamanio):
            if(matrizTablero[j][i] == "&" or validarAmp(matrizTablero[j][i]) == True):
                suma = 0
                cont = 1
                if (j + cont < tamanio):
                    while(validarAmp(matrizTablero[j+cont][i]) == False):
                        # print(i, "i", j, "j")
                        suma += int(matrizTablero[j+cont][i])
                        if(j+cont+1 < tamanio):
                            cont += 1
                        else:
                            break
                    # print(suma)
                    if(suma != 0):
                        matrizTablero[j][i] += str(suma)
                        tablero[j][i].set_nVertical(suma)
                        tablero[j][i].set_foreground("white")
                        tablero[j][i].set_text(True, "H")


def crearMatrizTablero(tamanio):
    global matrizF
    matrizF = copy.deepcopy(matrizTablero)
    for i in range(tamanio):
        for j in range(tamanio):
            if(validarAmp(matrizTablero[i][j]) == False):
                matrizF[i][j] = "0"
    # print(matrizF)


def valoresHorizontal(tamanio):
    try:
        global tablero, matrizTablero, ventanaKakuro
        cont = 1
        for i in range(1, tamanio):
            j = 0
            while(j < tamanio):
                if(j+1 < tamanio):
                    if(matrizTablero[i][j] == "&"):
                        while(j+cont < tamanio and matrizTablero[i][j+cont] == 0):
                            cont += 1  #Cuenta cuantos espacios disponibles hay
                        if(matrizTablero[i][j+1] == 0): #Verificacion para ver si el que sigue no es tambien negro
                            valor = choice(listaDopciones[cont-2]) #Escoge un valor aleatorio de una lista
                            matrizTablero[i][j] = "&" #Asigna ese valor al lugar de la matriz en negro
                            ##Asigna el color y el texto del espacio en negro
                            # tablero[i][j].set_foreground("white")
                            # tablero[i][j].set_nHorizontal(valor)
                            # tablero[i][j].set_text(True, "H")

                            lista = listaDcombinaciones[valor] #Escoge la lista de las posibles combinaciones para el valor

                            size = len(lista) #Cant de combinaciones disponibles para escoger

                            num = lista[randint(0, size-1)] #Escoge una combinacion de manera aleatoria
                            combAleatoria = len(str(num)) #Cuenta el tamaño de esa posible combinacion
                            if(cont-1 > 1): #Sí hay mas de una casilla disponible
                                # Esto se hace hasta que el tamaño de la combinacion sea igual al del num de casillas diponibles
                                while(combAleatoria != cont-1):
                                    #Si no es igual vuelve a elegir aleatoriamente
                                    num = lista[randint(0, size - 1)]
                                    combAleatoria = len(str(num))
                            else:
                                num = valor

                            lista = separarDigitos(num) #Separa la el numero y lo añade como str a una lista
                            # print(lista)

                            pos = 0 #Contador para ir iterando sobre la lista de la combinacion
                            for h in range(cont-1):
                                tablero[i][j+h+1].set_foreground("black") #Color de letra = negro
                                c = 0 #Contador de la cantidad de iteraciones permitidas
                                #El while se hace hasta que no hayan repetidos en la misma columna
                                while(verificarRepetidosAbajo(i, j+h+1, lista[pos], tamanio) == False
                                      or verificarRepetidosArriba(i, j+h+1, lista[pos]) == False):
                                    if(c > 50): #50 = Cant de iteraciones permitidas
                                        #Se realiza el mismo proceso anterior
                                        valor = choice(listaDopciones[cont - 2])
                                        matrizTablero[i][j] = "&"
                                        # tablero[i][j].set_foreground("white")
                                        # tablero[i][j].set_nHorizontal(valor)
                                        # tablero[i][j].set_text(True, "H")
                                        lista = listaDcombinaciones[valor]
                                        size = len(lista)
                                        num = lista[randint(0, size - 1)]
                                        combAleatoria = len(str(num))
                                        if (cont - 1 > 1):
                                            while (combAleatoria != cont - 1):
                                                num = lista[randint(0, size - 1)]
                                                combAleatoria = len(str(num))
                                        else:
                                            num = valor

                                        lista = separarDigitos(num)
                                        for h in range(cont - 1):
                                            tablero[i][j + h + 1].set_foreground("black")
                                    if(c > 75): #Detener el while con más de 75 iteraciones
                                        break

                                    c += 1 #Cont de iteraciones
                                #Sale del while
                                # tablero[i][j+h+1].set_text(False, lista[pos]) #Se van colocando los valores en las casillas disponibles
                                matrizTablero[i][j+h+1] = lista[pos] #Se van colocando los valores en la matriz

                                pos += 1 #Cont de cantidad
                            j += cont-2

                    cont = 1
                j += 1
        ultimosNegros(tamanio)
        sumaHorizontal(tamanio)
        sumaVertical(tamanio)
        crearMatrizTablero(tamanio)
    except:
        print("Intento fallido, recalculando...")
        # valoresHorizontal(tamanio)


class LabelTablero:
    def __init__(self, ventana, background, xi, yi, ancho, alto):
        self.ventana = ventana
        self.background = background
        self.xi = xi
        self.yi = yi
        self.ancho = ancho
        self.alto = alto
        self.numVertical = 0
        self.numHorizontal = 0
        self.label = Label(ventana)
        self.label.config(bg=background, width=ancho, height=alto)
        self.label.place(x=xi, y=yi)

    def set_nVertical(self, numVertical):
        self.numVertical = numVertical

    def set_nHorizontal(self, numHorizontal):
        self.numHorizontal = numHorizontal

    def set_text(self, tipo, texto):
        if(tipo):
            if(self.numVertical == 0):
                num = "\\" + str(self.numHorizontal)
            elif(self.numHorizontal == 0):
                num = str(self.numVertical) + "\\"
            else:
                num = str(self.numVertical)+"\\"+str(self.numHorizontal)
            self.label.configure(text=num)
        else:
            self.label.configure(text=texto)

    def set_background(self, background):
        self.background = background
        self.label.configure(bg=background)

    def set_foreground(self, foreground):
        self.foreground = foreground
        self.label.config(fg=foreground)


def resolverRapidoPeroNo(tamanio):
    for i in range(tamanio):
        for j in range(tamanio):
            if(validarAmp(matrizTablero[i][j]) == False):
                tablero[i][j].set_foreground("black")
                tablero[i][j].set_text(False, matrizTablero[i][j])


def guardaKakuro(tamanio):
    try:
        global matrizF
        ftypes = [('.txt file', "*.txt")]
        archivo = filedialog.asksaveasfile(mode='w', filetypes=ftypes, defaultextension=".txt")

        if archivo is None:  # En caso de cerrar la ventana y no hacer nada
            return
        cadena = ""
        for i in range(tamanio):
            for j in range(tamanio):
                if(validarAmp(matrizF[i][j]) == True):
                    cadena += matrizF[i][j]
                    cadena += "*"
                if(matrizF[i][j] == "0"):
                    cadena += "0"
                    cadena += "*"
            cadena += "#"

        contenido = str(tamanio)+"\n"+cadena
        archivo.write(contenido)
        archivo.close()
    except:
        advertencia = messagebox.showerror("Error", 'No se pudo guardar la partida')


class Tablero:
    def __init__(self, tamanio, wDimentions, f_width, f_height, x, cargar=False):
        global tablero, matrizTablero, ventanaKakuro, matrizF

        fila = []
        columna = []

        index_X = 7
        index_Y = 6 + x

        ventanaKakuro = Tk()
        ventanaKakuro.geometry(wDimentions)
        ventanaKakuro.configure(bg="light blue")
        ventanaKakuro.resizable(FALSE, FALSE)
        cuadricula = Frame(ventanaKakuro, bg="Black", width=f_width, height=f_height)
        cuadricula.place(x=10, y=25)

        for i in range(tamanio):
            for j in range(tamanio):
                label = LabelTablero(cuadricula, "white", index_X, index_Y, 3, 1)
                index_X += 30
                fila += [label]
            index_Y += 25
            index_X = 7
            tablero += [fila]
            fila = []

        btnResolver = Button(ventanaKakuro, text="Resolver", width=20, relief=FLAT,
                             command=lambda: resolverRapidoPeroNo(tamanio))

        btnGuardar = Button(ventanaKakuro, text="Guardar Kakuro", width=20, relief=FLAT,
                            command=lambda: guardaKakuro(tamanio))

        btnResolver.place(x=index_X+f_width+10, y=f_height)
        btnGuardar.place(x=index_X+f_width+10, y=f_height-30)

        if(cargar == False):

            for i in range(tamanio):
                for j in range(tamanio):
                    fila += [0]
                matrizTablero += [fila]
                fila = []

            for i in range(tamanio): #Para bloquear la fila y la columna 0
                tablero[0][i].set_background("black")
                matrizTablero[0][i] = "&"
                tablero[i][0].set_background("black")
                matrizTablero[i][0] = "&"

            cantBloqueadas = tamanio*3 #Porcentaje del tablero que quiero bloquear, puede variar

            for h in range(cantBloqueadas):
                rand_x = randint(0,tamanio-1)
                rand_y = randint(0, tamanio-1)
                while(matrizTablero[rand_x][rand_y] == "&"):
                    rand_x = randint(0, tamanio - 1)
                    rand_y = randint(0, tamanio - 1)
                matrizTablero[rand_x][rand_y] = "&"
                tablero[rand_x][rand_y].set_background("black")

            for i in range(tamanio):
                for j in range(tamanio//5):
                    #No esta verificando en vertical
                    inicio = verificar(matrizTablero[i], tamanio)

                    if(inicio != -1):
                        x = randint(inicio, tamanio-1)
                        while(matrizTablero[i][x] == "&"):
                            x = randint(inicio, tamanio-1)
                        matrizTablero[i][x] = "&"
                        tablero[i][x].set_background("black")
                        # tablero[i][x].configure(fg="white", text="0#")

            for i in range(tamanio):
                for j in range(tamanio):
                    columna += [matrizTablero[j][i]]
                for h in range(tamanio//5):
                    inicio = verificar(columna, tamanio)
                    if(inicio != -1):
                        x = randint(inicio, tamanio-1)
                        while(matrizTablero[x][i] == "&"):
                            x = randint(inicio, tamanio-1)
                        matrizTablero[x][i] = "&"
                        tablero[x][i].set_background("black")
                        # tablero[x][i].configure(fg="white", text="1#")
                columna = []

            for i in range(tamanio):
                for j in range(tamanio):
                    try:
                        if(matrizTablero[i-1][j] == "&" and matrizTablero[i+1][j] == "&"
                           and matrizTablero[i][j-1] == "&" and matrizTablero[i][j+1] == "&"):
                            matrizTablero[i][j] = "&"
                            tablero[i][j].set_background("black")
                    except:
                        matrizTablero[i][j] = "&"
                        tablero[i][j].set_background("black")

            valoresHorizontal(tamanio)

        else:
            matrizTemp = []
            matrizTemp2 = []
            matrizTemp = matrizF.split("#")
            for i in range(len(matrizTemp)):
                matrizTemp2 += [matrizTemp[i].split("*")]
            matrizF = copy.deepcopy(matrizTemp2)
            # print(matrizF)
            for i in range(tamanio):
                for j in range(tamanio):
                    if(validarAmp(matrizF[i][j]) == True):
                        matrizTemp = matrizF[i][j].split("&")
                        if(matrizTemp[0] != "" or matrizTemp[1] != ""):
                            if(matrizTemp[1] == "" and matrizTemp[0] != ""):
                                tablero[i][j].set_nHorizontal(matrizTemp[0])
                                tablero[i][j].set_text(True, "H")
                            elif(matrizTemp[1] != "" and matrizTemp[0] == ""):
                                tablero[i][j].set_nVertical(matrizTemp[1])
                                tablero[i][j].set_text(True, "H")
                            else:
                                tablero[i][j].set_nHorizontal(matrizTemp[0])
                                tablero[i][j].set_nVertical(matrizTemp[1])
                                tablero[i][j].set_text(True, "H")
                        tablero[i][j].set_foreground("white")
                        tablero[i][j].set_background("Black")




            #Para generarlo puedo hacer una funcion que recorra el kakuro y por cadda uno llama a
            #a otra para verificar la fila y la columna que recibe una fila o columna y el numero que queremos
            #colocar y que retorme true o false, puede ser ¿?"""


def cargarP():
    global tamanioCuadricula
    try:
        global matrizF
        ftypes = [('.txt file', "*.txt")]
        ttl = "Buscar Kakuro..."
        dir1 = 'C:\\'
        direccionArchivo = askopenfilename(filetypes=ftypes, initialdir=dir1, title=ttl)

        if (direccionArchivo is ""):  # En caso de cerrar la ventana y no abrir nada
            return

        with open(direccionArchivo, 'r') as Partida:
            tamanioCuadricula = int(Partida.readline())-9
            matrizF = Partida.readline()
            # print(tamanioCuadricula)
            # print(matrizF)
            dimension = tamanioCuadricula
            desp_w = 30 * dimension
            desp_h = 26 * dimension
            _w = 470 + desp_w
            _h = 270 + desp_w
            _x = 400 - desp_w
            _y = 50
            wDimention = str(_w) + "x" + str(_h) + "+" + str(_x) + "+" + str(_y)
            _wf = 282 + desp_w
            _hf = 230 + desp_h
            cuadricula = 9 + dimension
            x = dimension % 6
            if dimension <= 3:
                x = -1
            if dimension == 4 or dimension == 5:
                x = 0
            # print(x)
            ventanaMenu.destroy()
            ventana = Tablero(cuadricula, wDimention, _wf, _hf, x, True)
    except:
        advertencia = messagebox.showerror("Error", 'No se pudo abrir la partida')


def menu():
    global  ventanaMenu, tamanioCuadricula
    ventanaMenu = Tk()

    ventanaMenu.title("Menú Kakuro")
    ventanaMenu.geometry("205x300+550+150")
    ventanaMenu.configure(bg="light blue")
    ventanaMenu.resizable(FALSE, FALSE)
    tamanioCuadricula = IntVar()

    lblTamanio = Label(ventanaMenu, text="Seleccione el tamaño del Kakuro:")

    Rb10 = Radiobutton(ventanaMenu, text="10x10", value=1, variable=tamanioCuadricula)
    Rb11 = Radiobutton(ventanaMenu, text="11x11", value=2, variable=tamanioCuadricula)
    Rb12 = Radiobutton(ventanaMenu, text="12x12", value=3, variable=tamanioCuadricula)
    Rb13 = Radiobutton(ventanaMenu, text="13x13", value=4, variable=tamanioCuadricula)
    Rb14 = Radiobutton(ventanaMenu, text="14x14", value=5, variable=tamanioCuadricula)
    Rb15 = Radiobutton(ventanaMenu, text="15x15", value=6, variable=tamanioCuadricula)
    Rb16 = Radiobutton(ventanaMenu, text="16x16", value=7, variable=tamanioCuadricula)
    Rb17 = Radiobutton(ventanaMenu, text="17x17", value=8, variable=tamanioCuadricula)
    Rb18 = Radiobutton(ventanaMenu, text="18x18", value=9, variable=tamanioCuadricula)
    Rb19 = Radiobutton(ventanaMenu, text="19x19", value=10, variable=tamanioCuadricula)
    Rb20 = Radiobutton(ventanaMenu, text="20x20", value=11, variable=tamanioCuadricula)

    btnGenerar = Button(ventanaMenu, text="Generar Nuevo", bg="#001848", fg="white", width="20",
                        relief=FLAT, command=lambda: generar())

    btnCargarP = Button(ventanaMenu, text="Cargar Kakuro", bg="#001848", fg="white", width="20",
                        relief=FLAT, command= lambda: cargarP())

    Rb14.select()

    lblTamanio.place(x=10, y=10)
    Rb10.place(x=30, y=40)
    Rb11.place(x=30, y=70)
    Rb12.place(x=30, y=100)
    Rb13.place(x=30, y=130)
    Rb14.place(x=30, y=160)
    Rb15.place(x=30, y=190)
    Rb16.place(x=100, y=40)
    Rb17.place(x=100, y=70)
    Rb18.place(x=100, y=100)
    Rb19.place(x=100, y=130)
    Rb20.place(x=100, y=160)

    btnGenerar.place(x=25, y=225)
    btnCargarP.place(x=25, y=260)

    ventanaMenu.mainloop()

def generar():
    global ventanaKakuro, tamanioCuadricula
    dimension = tamanioCuadricula.get()
    desp_w = 30 * dimension
    desp_h = 26 * dimension
    _w = 470 + desp_w
    _h = 270 + desp_w
    _x = 400 - desp_w
    _y = 50
    wDimention = str(_w)+"x"+str(_h)+"+"+str(_x)+"+"+str(_y)
    _wf = 282 + desp_w
    _hf = 230 + desp_h
    cuadricula = 9 + dimension
    x = dimension % 6
    if dimension <= 3:
        x = -1
    if dimension == 4 or dimension == 5:
        x = 0
    # print(x)
    ventanaMenu.destroy()
    ventana = Tablero(cuadricula, wDimention, _wf, _hf, x)

menu()