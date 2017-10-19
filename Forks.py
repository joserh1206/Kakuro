import pickle
from random import randint, choice, shuffle
from itertools import *
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import filedialog, messagebox
from copy import *
from Combinaciones import *
from time import time

from multiprocessing import Pool, freeze_support

tablero, matrizTablero, matrizF, listaThread = [], [], [], []
tamanioCuadricula = 0

def verificar(fila, tamanio):
    cont = 0
    inicio = -1
    for i in range(tamanio):
        if (fila[i] == 0):
            if (cont == 0):
                inicio = i
            cont += 1
        if (fila[i] != 0 and cont <= 9):
            inicio = -1
            cont = 0
    if cont > 9:
        return inicio
    else:
        return -1


def separarDigitos(num):
    lista = []
    while (num != 0):
        dig = num % 10
        lista += [str(dig)]
        num = num // 10
    shuffle(lista)
    return lista


def verificarRepetidosAbajo(i, j, valor, tamanio):
    while (matrizTablero[i][j] != "&"):
        if (matrizTablero[i][j] == valor):
            return False
        if (i + 1 < tamanio):
            i += 1
        else:
            return True
    return True


def verificarRepetidosArriba(i, j, valor):
    while (matrizTablero[i][j] != "&"):
        if (matrizTablero[i][j] == valor):
            return False
        if (i - 1 >= 0):
            i -= 1
        else:
            return True
    return True


def ultimosNegros(tamanio):
    for i in range(tamanio):
        for j in range(tamanio):
            if (matrizTablero[i][j] == 0):
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
            if (matrizTablero[i][j] == "&"):
                suma = 0
                cont = 1
                if (j + cont < tamanio):
                    while (matrizTablero[i][j + cont] != "&"):
                        # print(i, "i", j, "j")
                        suma += int(matrizTablero[i][j + cont])
                        if (j + cont + 1 < tamanio):
                            cont += 1
                        else:
                            break
                    # print(suma)
                    if (suma != 0 and suma < 46):
                        # print(suma)
                        if (suma == 2 and cont > 2):
                            pass
                        else:
                            matrizTablero[i][j] = str(suma) + "&"
                            tablero[i][j].set_nHorizontal(suma)
                            tablero[i][j].set_foreground("white")
                            tablero[i][j].set_text(True, "H")
                            # for i in range(1, tamanio):
                            #     cont = 1
                            #     for j in range(tamanio):
                            #         if(validarAmp(matrizTablero[i][j]) == True):
                            #             comb = []
                            #             suma = 0
                            #             cont = 1
                            #             if (j + cont < tamanio):
                            #                 while(validarAmp(matrizTablero[i][j+cont]) == False):
                            #                     # print(i, "i", j, "j")
                            #                     num = int(matrizTablero[i][j+cont])
                            #                     if(num not in comb):
                            #                         comb += [num]
                            #                         suma += num
                            #                     else:
                            #                         temp = 0
                            #                         num = 1
                            #                         while(num < 10):
                            #                             if(num not in comb):
                            #                                 if(verificarRepetidosAbajo(i, j+cont, num, tamanio) == False
                            #                                    or verificarRepetidosArriba(i, j+cont, num) == False):
                            #                                     num += 1
                            #                                 else:
                            #                                     comb += [num]
                            #                                     suma += num
                            #                                     matrizTablero[i][j + cont] = str(num)
                            #                                     num = 10
                            #                             else:
                            #                                 comb += [num]
                            #                                 suma += num
                            #                                 matrizTablero[i][j + cont] = str(num)
                            #                                 num = 10
                            #                         # print(num)
                            #
                            #
                            #                     if(j+cont+1 < tamanio):
                            #                         cont += 1
                            #                     else:
                            #                         break
                            #                 # print("suma: ", suma)
                            #                 # print("cont: ", cont)
                            #
                            #                 if(suma != 0 and suma < 46 and cont >= 2):
                            #                     try:
                            #                         if(validarAmp(matrizTablero[i][j+2]) == False):
                            #                             matrizTablero[i][j] = str(suma)+"&"
                            #                             tablero[i][j].set_nHorizontal(suma)
                            #                             tablero[i][j].set_foreground("white")
                            #                             tablero[i][j].set_text(True, "H")
                            #                     except:
                            #                         pass
                            #                 else:
                            #                     matrizTablero[i][j] = "&"


def validarAmp(string):
    if ("&" in str(string)):
        return True
    else:
        return False


def sumaVertical(tamanio):
    for i in range(tamanio):
        cont = 1
        for j in range(tamanio):
            if (matrizTablero[j][i] == "&" or validarAmp(matrizTablero[j][i]) == True):
                suma = 0
                cont = 1
                if (j + cont < tamanio):
                    while (validarAmp(matrizTablero[j + cont][i]) == False):
                        # print(i, "i", j, "j")
                        suma += int(matrizTablero[j + cont][i])
                        if (j + cont + 1 < tamanio):
                            cont += 1
                        else:
                            break
                    # print(suma)
                    if (suma != 0):
                        matrizTablero[j][i] += str(suma)
                        tablero[j][i].set_nVertical(suma)
                        tablero[j][i].set_foreground("white")
                        tablero[j][i].set_text(True, "H")


def kakuroValido(tamanio):
    global matrizTablero
    for i in range(tamanio):
        lst = []
        for j in range(tamanio):
            if (validarAmp(matrizTablero[i][j]) == False):
                if (matrizTablero[i][j] in lst):
                    print("Kakuro no válido")
                    return False
                else:
                    lst.append(matrizTablero[i][j])
            else:
                lst = []
    for i in range(tamanio):
        lst = []
        for j in range(tamanio):
            if (validarAmp(matrizTablero[j][i]) == False):
                if (matrizTablero[j][i] in lst):
                    print("Kakuro no válido")
                    return False
                else:
                    lst.append(matrizTablero[j][i])
            else:
                lst = []
    return True


def crearMatrizTablero(tamanio):
    global matrizF
    if (kakuroValido(tamanio)):
        matrizF = deepcopy(matrizTablero)
        for i in range(tamanio):
            for j in range(tamanio):
                if (validarAmp(matrizTablero[i][j]) == False):
                    matrizF[i][j] = "0"
    else:
        print("No tiene solucion valida")


def crearValido(tamanio):
    global matrizTablero
    for i in range(tamanio):
        lst = []
        for j in range(tamanio):
            if (validarAmp(str(matrizTablero[i][j])) == False):
                # print("Y")

                if (str(matrizTablero[i][j]) in lst):
                    matrizTablero[i][j] = 0
                else:
                    lst.append(matrizTablero[i][j])
            else:
                lst = []
    for i in range(tamanio):
        lst = []
        for j in range(tamanio):
            if (validarAmp(str(matrizTablero[j][i])) == False):
                # print("Y")

                if (str(matrizTablero[j][i]) in lst):
                    matrizTablero[j][i] = 0
                else:
                    lst.append(matrizTablero[j][i])
            else:
                lst = []


def valoresHorizontal(tamanio):
    # try:
    global tablero, matrizTablero, ventanaKakuro
    cont = 1
    for i in range(1, tamanio):
        j = 0
        while (j < tamanio):
            if (j + 1 < tamanio):
                if (matrizTablero[i][j] == "&"):
                    while (j + cont < tamanio and matrizTablero[i][j + cont] == 0):
                        cont += 1  # Cuenta cuantos espacios disponibles hay
                    # print("Cont: ", cont-1)
                    if (matrizTablero[i][j + 1] == 0):  # Verificacion para ver si el que sigue no es tambien negro

                        valor = choice(listaDopciones[cont - 2])  # Escoge un valor aleatorio de una lista

                        matrizTablero[i][j] = "&"  # Asigna ese valor al lugar de la matriz en negro

                        lista = listaDcombinaciones[
                            valor]  # Escoge la lista de las posibles combinaciones para el valor

                        size = len(lista)  # Cant de combinaciones disponibles para escoger

                        num = lista[randint(0, size - 1)]  # Escoge una combinacion de manera aleatoria
                        combAleatoria = len(str(num))  # Cuenta el tamaño de esa posible combinacion
                        if (cont - 1 > 1):  # Sí hay mas de una casilla disponible
                            # Esto se hace hasta que el tamaño de la combinacion sea igual al del num de casillas diponibles
                            while (combAleatoria != cont - 1):
                                # Si no es igual vuelve a elegir aleatoriamente
                                num = lista[randint(0, size - 1)]
                                combAleatoria = len(str(num))
                        else:
                            num = valor

                        lista = separarDigitos(num)  # Separa la el numero y lo añade como str a una lista
                        # print(lista)

                        pos = 0  # Contador para ir iterando sobre la lista de la combinacion
                        for h in range(cont - 1):
                            tablero[i][j + h + 1].set_foreground("black")  # Color de letra = negro
                            c = 0  # Contador de la cantidad de iteraciones permitidas
                            # El while se hace hasta que no hayan repetidos en la misma columna
                            while (verificarRepetidosAbajo(i, j + h + 1, lista[pos], tamanio) == False
                                   or verificarRepetidosArriba(i, j + h + 1, lista[pos]) == False):
                                if (c > 50):  # 50 = Cant de iteraciones permitidas
                                    # Se realiza el mismo proceso anterior
                                    valor = choice(listaDopciones[cont - 2])
                                    matrizTablero[i][j] = "&"  # llaveVer & llaveHo

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
                                if (c > 75):  # Detener el while con más de 75 iteraciones
                                    break

                                c += 1  # Cont de iteraciones
                            # Sale del while
                            # tablero[i][j+h+1].set_text(False, lista[pos]) #Se van colocando los valores en las casillas disponibles
                            matrizTablero[i][j + h + 1] = lista[pos]  # Se van colocando los valores en la matriz

                            pos += 1  # Cont de cantidad
                        j += cont - 2

                cont = 1
            j += 1
    # print(matrizTablero)
    crearValido(tamanio)
    ultimosNegros(tamanio)
    sumaHorizontal(tamanio)
    sumaVertical(tamanio)
    crearMatrizTablero(tamanio)
    # except:
    #     print("Intento fallido, recalculando...")
        # valoresHorizontal(tamanio)


def casillasH(tamanio, i, j):
    global matrizF
    cont = 0
    while (validarAmp(j < tamanio and matrizF[i][j]) == False):
        cont += 1
        j += 1
    return cont


def is_distinct(list):

    used = []
    for i in list:
        if i == 0:
            continue
        if i in used:
            return False
        used.append(i)
    return True


def is_valid(brd, tamanio):
    '''Checks if a 3x3 mini-Sudoku is valid.'''
    lst = []
    for i in range(tamanio):
        for j in range(tamanio):
            if(validarAmp(brd[i][j]) == False):
                if(int(brd[i][j]) == 0):
                    # print("FALSE")
                    continue
                else:
                    if(int(brd[i][j]) in lst):
                        return False
                    else:
                        lst.append(int(brd[i][j]))
            else:
                lst = []
    lst = []
    for i in range(tamanio):
        for j in range(tamanio):
            if(validarAmp(brd[j][i]) == False):
                if(int(brd[j][i]) == 0):
                    # print("FALSE")
                    continue
                else:
                    if(int(brd[j][i]) in lst):
                        return False
                    else:
                        lst.append(int(brd[j][i]))
            else:
                lst = []
    return True


def disponibles(tamanio):
    global matrizF
    cont = 0
    for i in range(tamanio):
        for j in range(tamanio):
            if(validarAmp(matrizF[i][j]) == False):
                if(int(matrizF[i][j]) == 0):
                    cont += 1
    return cont


def verifca(prueba, cont, i, j, tamanio):
    print("i:", i, " j:", j)

    c = 0
    cantperm = int(prueba)*tamanio
    pos = matrizTablero[i][j]
    while(c < cantperm):
        if(verificarRepetidosArriba(i, j, pos) == True):
            return False
        if(verificarRepetidosAbajo(i, j, pos, tamanio) == True):
            return False
        c += 1
    return pos


def is_posible(posible):
    # print("Posible", posible)
    global matrizF #, listaThread
    prueba, objetivo, i, j, tamanio = 0, 0, 0, 0, 0
    # print("Hilo numero: ", prueba)
    lstPos = posible.split("*")
    # print("Posblelst", lstPos)
    prueba = int(lstPos[0])
    objetivo = int(lstPos[1])
    i = int(lstPos[2])
    j = int(lstPos[3])
    tamanio = int(lstPos[4])
    lst = listaDcombinaciones[objetivo]
    # print(lst, objetivo, "OBJ")
    cont = 0
    h = j
    lstOptima = []

    print("LLEGA")
    for opt in lst:
        if(len(str(opt)) == cont):
            lstOptima.append(opt)
    if(len(lstOptima) == 0):
        lstOptima = copy(lst)
    # print(lstOptima, "OPT")
    # print(lst, "NOOP")
    # print("Hilo numeroF: ", prueba)
    print("prueba:", prueba)
    for opt2 in lst:
        if(str(prueba) in str(opt2)):
            if(str(prueba) == verifca(prueba, cont, i, j, tamanio)):
                return True
    return False


def backtracking(brd, tamanio, empties):
    # global listaThread
    # print(empties, "EMP")
    if empties == 0:
        # print("I")
        # print(is_valid(brd, tamanio))
        return is_valid(brd, tamanio)
    objetivo = 0
    for row, col in product(range(tamanio), repeat=2):
        cell = brd[row][col]
        if(validarAmp(brd[row][col]) == True):
            if(len(brd[row][col]) > 1):
                lst = brd[row][col].split("&")
                if(lst[0] != ""):
                    objetivo = int(lst[0])
            continue
        if (validarAmp(brd[row][col]) == False):
            if(int(brd[row][col]) == 0):
                brd2 = copy(brd)
                listaPosibilidades = ["1"+"*"+str(objetivo)+"*"+str(row)+"*"+str(col)+"*"+str(tamanio),
                                      "2"+"*"+str(objetivo)+"*"+str(row)+"*"+str(col)+"*"+str(tamanio),
                                      "3"+"*"+str(objetivo)+"*"+str(row)+"*"+str(col)+"*"+str(tamanio),
                                      "4"+"*"+str(objetivo)+"*"+str(row)+"*"+str(col)+"*"+str(tamanio),
                                      "5"+"*"+str(objetivo)+"*"+str(row)+"*"+str(col)+"*"+str(tamanio),
                                      "6"+"*"+str(objetivo)+"*"+str(row)+"*"+str(col)+"*"+str(tamanio),
                                      "7"+"*"+str(objetivo)+"*"+str(row)+"*"+str(col)+"*"+str(tamanio),
                                      "8"+"*"+str(objetivo)+"*"+str(row)+"*"+str(col)+"*"+str(tamanio),
                                      "9"+"*"+str(objetivo)+"*"+str(row)+"*"+str(col)+"*"+str(tamanio)]
                # freeze_support()
                fork = Pool(10)
                resultado = fork.map(is_posible, listaPosibilidades)
                # print(resultado)
                for prueba in resultado:
                    # print(prueba[0])
                    if(prueba == True):
                        brd2[row][col] = prueba[1]
                        tablero[row][col].set_text(False, prueba[1])
                        # print(prueba, "Prueba")
                        if(is_valid(brd2, tamanio) == True and backtracking(brd, tamanio, empties-1) == True):
                            return True
                        brd2[row][col] = 0
                    else:
                        # print("not posible")
                        continue
    return False


def fijos2(tamanio):
    global matrizF, tablero
    for i in range(tamanio):
        for j in range(tamanio):
            if (validarAmp(str(matrizF[i][j])) == True and len(matrizF[i][j]) > 1):
                lst = matrizF[i][j].split("&")
                cont = 0
                h = j + 1
                suma = 0
                while (h < tamanio and validarAmp(str(matrizF[i][h])) == False):
                    cont += 1
                    # print(matrizF[i][h], "matriz")
                    if (int(matrizF[i][h]) != 0):
                        suma += int(matrizF[i][h])
                    h += 1
                if (cont == 2):
                    if (lst[0] != "" and suma > 0):
                        num = int(lst[0]) - suma
                        if (int(matrizF[i][j + 1]) == 0):
                            matrizF[i][j + 1] = num
                            tablero[i][j + 1].set_text(False, str(num))
                        else:
                            if (int(matrizF[i][j + 2]) == 0 and num != 0):
                                matrizF[i][j + 2] = num
                                tablero[i][j + 2].set_text(False, str(num))
    for i in range(tamanio):
        for j in range(tamanio):
            if (validarAmp(str(matrizF[j][i])) == True and len(matrizF[j][i]) > 1):
                lst = matrizF[j][i].split("&")
                cont = 0
                h = j + 1
                suma = 0
                while (h < tamanio and validarAmp(str(matrizF[h][i])) == False):
                    cont += 1
                    # print(matrizF[i][h], "matriz")
                    if (int(matrizF[h][i]) != 0):
                        suma += int(matrizF[h][i])
                    h += 1
                if (cont == 2):
                    # print(lst, "LST")
                    # print(suma, "SUM")
                    if (lst[1] != "" and suma > 0):
                        num = int(lst[1]) - suma
                        # print(num, "NUM")
                        # print(matrizF[j+1][i], "MATRIX")
                        if (int(matrizF[j + 1][i]) == 0 and num > 0):
                            matrizF[j + 1][i] = num
                            tablero[j + 1][i].set_text(False, str(num))
                        else:
                            if (int(matrizF[j + 2][i]) == 0 and num != 0):
                                matrizF[j + 2][i] = num
                                tablero[j + 2][i].set_text(False, str(num))

    dis = disponibles(tamanio)
    # print(dis, "dis")
    tiempoini = time()
    backtracking(matrizF, tamanio, dis)
    tiempofin = time()
    print("Con hilos duró: ", tiempofin-tiempoini)


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

    def get_nHorizontal(self):
        return self.numHorizontal

    def get_nVertical(self):
        return self.numVertical

    def set_text(self, tipo, texto):
        if (tipo):
            if (self.numVertical == 0):
                num = "\\" + str(self.numHorizontal)
            elif (self.numHorizontal == 0):
                num = str(self.numVertical) + "\\"
            else:
                num = str(self.numVertical) + "\\" + str(self.numHorizontal)
            self.label.configure(text=num)
        else:
            self.label.configure(fg="black")
            self.label.configure(text=str(texto))

    def set_background(self, background):
        self.background = background
        self.label.configure(bg=background)

    def set_foreground(self, foreground):
        self.foreground = foreground
        self.label.config(fg=foreground)


def ponerFijos(tamanio):
    global matrizF
    # print(matrizF)
    for i in range(tamanio):
        for j in range(tamanio):
            if (validarAmp(matrizF[i][j]) == True and len(matrizF[i][j]) > 1):
                cont = 0
                # print("matriz:", matrizF[i][j])
                if (j + 1 >= tamanio):
                    pass
                else:
                    h = j + 1
                    while (validarAmp(matrizF[i][h]) == False):
                        cont += 1
                        if (h + 1 >= tamanio or cont > 1):
                            break
                        else:
                            h += 1
                    if (cont == 1):
                        num = tablero[i][j].get_nHorizontal()
                        matrizF[i][j + 1] = str(num)
                        tablero[i][j + 1].set_text(False, num)
                        # print("num:", num)
    for fila in range(tamanio):
        for columna in range(tamanio):
            if (validarAmp(matrizF[fila][columna]) == True and len(matrizF[fila][columna]) > 1):
                cont = 0
                if (fila + 1 >= tamanio):
                    pass
                else:
                    f = fila + 1
                    while (validarAmp(matrizF[f][columna]) == False):
                        cont += 1
                        if (f + 1 >= tamanio or cont > 1):
                            break
                        else:
                            f += 1
                    if (cont == 1):
                        num = tablero[fila][columna].get_nVertical()
                        matrizF[fila + 1][columna] = str(num)
                        tablero[fila + 1][columna].set_text(False, num)
    fijos2(tamanio)
    # backtracking(tamanio)
    # backtracking(tamanio, 1, 0, [])
    # for i in range(tamanio):
    #     for j in range(tamanio):
    #         if(validarAmp(matrizTablero[i][j]) == False):
    #             tablero[i][j].set_foreground("black")
    #             tablero[i][j].set_text(False, matrizTablero[i][j])


def guardaKakuro(tamanio):
    try:
        global matrizF, matrizTablero
        ftypes = [('.txt file', "*.txt")]
        archivo = filedialog.asksaveasfile(mode='w', filetypes=ftypes, defaultextension=".txt")

        if archivo is None:  # En caso de cerrar la ventana y no hacer nada
            return
        cadena = ""
        for i in range(tamanio):
            for j in range(tamanio):
                if (validarAmp(matrizF[i][j]) == True):
                    cadena += matrizF[i][j]
                    cadena += "*"
                if (matrizF[i][j] == "0"):
                    cadena += "0"
                    cadena += "*"
            cadena += "#"
        cadena2 = ""
        for i_2 in range(tamanio):
            for j_2 in range(tamanio):
                if(validarAmp(matrizTablero[i_2][j_2]) == False):
                    n = randint(0, 9)
                    n2 = randint(0, 9)
                    cadena2 += str(n)+matrizTablero[i_2][j_2]+str(n2)
                    cadena2 += "*"
                else:
                    cadena2 += "XX"
                    cadena2 += "*"
            cadena2 += "#"

        contenido = str(tamanio) + "\n" + cadena +"\n"+"\n"+"Formato del Tablero"+"\n"+cadena2
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
                             command=lambda: ponerFijos(tamanio))

        btnGuardar = Button(ventanaKakuro, text="Guardar Kakuro", width=20, relief=FLAT,
                            command=lambda: guardaKakuro(tamanio))

        btnResolver.place(x=index_X + f_width + 10, y=f_height)
        btnGuardar.place(x=index_X + f_width + 10, y=f_height - 30)

        if (cargar == False):

            for i in range(tamanio):
                for j in range(tamanio):
                    fila += [0]
                matrizTablero += [fila]
                fila = []

            for i in range(tamanio):  # Para bloquear la fila y la columna 0
                tablero[0][i].set_background("black")
                matrizTablero[0][i] = "&"
                tablero[i][0].set_background("black")
                matrizTablero[i][0] = "&"

            cantBloqueadas = tamanio * 2  # Porcentaje del tablero que quiero bloquear, puede variar

            for h in range(cantBloqueadas):
                rand_x = randint(0, tamanio - 1)
                rand_y = randint(0, tamanio - 1)
                while (matrizTablero[rand_x][rand_y] == "&"):
                    rand_x = randint(0, tamanio - 1)
                    rand_y = randint(0, tamanio - 1)
                matrizTablero[rand_x][rand_y] = "&"
                tablero[rand_x][rand_y].set_background("black")

            for i in range(tamanio):
                for j in range(tamanio // 5):
                    # No esta verificando en vertical
                    inicio = verificar(matrizTablero[i], tamanio)

                    if (inicio != -1):
                        x = randint(inicio, tamanio - 1)
                        while (matrizTablero[i][x] == "&"):
                            x = randint(inicio, tamanio - 1)
                        matrizTablero[i][x] = "&"
                        tablero[i][x].set_background("black")
                        # tablero[i][x].configure(fg="white", text="0#")

            for i in range(tamanio):
                for j in range(tamanio):
                    columna += [matrizTablero[j][i]]
                for h in range(tamanio // 5):
                    inicio = verificar(columna, tamanio)
                    if (inicio != -1):
                        x = randint(inicio, tamanio - 1)
                        while (matrizTablero[x][i] == "&"):
                            x = randint(inicio, tamanio - 1)
                        matrizTablero[x][i] = "&"
                        tablero[x][i].set_background("black")
                        # tablero[x][i].configure(fg="white", text="1#")
                columna = []

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

            # for i in range(1, tamanio):
            #     j = 0
            #     cont = 0
            #     while (j < tamanio):
            #         if (j + 1 < tamanio):
            #             if (matrizTablero[i][j] == "&"):
            #                 cont = 0
            #                 h = j+1
            #                 while (h < tamanio and matrizTablero[i][h] == 0):
            #                     cont += 1  # Cuenta cuantos espacios disponibles hay
            #                     h += 1
            #                     # j += cont - 2
            #                 print(cont)
            #                 if(cont == 1):
            #                     tablero[i][j+1].set_foreground("white")
            #                     tablero[i][j+1].set_background("red")
            #                     tablero[i][j+1].set_text(False, "U")
            #                     print("j")
            #         j += 1


            valoresHorizontal(tamanio)

        else:
            matrizTemp = []
            matrizTemp2 = []
            # print(matrizF, "F")
            matrizTemp = matrizF.split("#")
            for i in range(len(matrizTemp)):
                matrizTemp2 += [matrizTemp[i].split("*")]
            matrizF = deepcopy(matrizTemp2)
            # print(matrizF, "F2")
            # print(matrizTablero, "0")

            matrizTemp = matrizTablero.split("#")
            matrizTemp2 = []
            for i in range(len(matrizTemp)-1):
                matrizTemp2 += [matrizTemp[i].split("*")]

            matrizTablero = deepcopy(matrizTemp2)
            # print(matrizTablero, "1")
            lenT = len(matrizTablero)
            for i_4 in range(lenT):
                for j_4 in range(lenT):
                    if("X" not in matrizTablero[i_4][j_4]):
                        matrizTablero[i_4][j_4] = matrizTablero[i_4][j_4][1]
            # print(matrizTablero, "2")

            # print(matrizTablero)
            # print(matrizF)
            for i in range(tamanio):
                for j in range(tamanio):
                    if (validarAmp(matrizF[i][j]) == True):
                        matrizTemp = matrizF[i][j].split("&")
                        if (matrizTemp[0] != "" or matrizTemp[1] != ""):  # ["",""]  [5, 3]
                            if (matrizTemp[1] == "" and matrizTemp[0] != ""):
                                tablero[i][j].set_nHorizontal(matrizTemp[0])
                                tablero[i][j].set_text(True, "H")
                            elif (matrizTemp[1] != "" and matrizTemp[0] == ""):
                                tablero[i][j].set_nVertical(matrizTemp[1])
                                tablero[i][j].set_text(True, "H")
                            else:
                                tablero[i][j].set_nHorizontal(matrizTemp[0])
                                tablero[i][j].set_nVertical(matrizTemp[1])
                                tablero[i][j].set_text(True, "H")
                        tablero[i][j].set_foreground("white")
                        tablero[i][j].set_background("Black")


def cargarP():
    global tamanioCuadricula, matrizTablero
    try:
        global matrizF
        ftypes = [('.txt file', "*.txt")]
        ttl = "Buscar Kakuro..."
        dir1 = 'C:\\'
        direccionArchivo = askopenfilename(filetypes=ftypes, initialdir=dir1, title=ttl)

        if (direccionArchivo is ""):  # En caso de cerrar la ventana y no abrir nada
            return

        with open(direccionArchivo, 'r') as Partida:
            tamanioCuadricula = int(Partida.readline()) - 9
            matrizF = Partida.readline()
            info = Partida.readline()
            info = Partida.readline()
            matrizTablero = Partida.readline()

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
    global ventanaMenu, tamanioCuadricula
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
                        relief=FLAT, command=lambda: cargarP())

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
    ventana = Tablero(cuadricula, wDimention, _wf, _hf, x)
menu()
