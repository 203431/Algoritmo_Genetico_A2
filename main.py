import random 
from itertools import combinations 
import math 
import matplotlib.pyplot as plt
from tkinter import *
from functools import partial

import os
from shutil import rmtree

class Individuo():
    def __init__(self, X,Y,bino,dec):
        self.X = X
        self.Y = Y
        self.bino = bino
        self.dec = dec
        
    def __repr__(self):
        rep = 'Individuo(' + str(self.X) +' | '+ str(self.Y) + ' | ' + str(self.bino) +' | ' + str(self.dec) +')'
        return rep

class AlgoritmoGenetico():  

    def __init__(self, Xmin,Xmax, intervalo, rango, puntos, poblacionMaxima, poblacionInicial, generaciones,noBits, Pmi,Pmg, Pc):
        self.Xmin = Xmin
        self.intervalo = intervalo
        self.Xmax = Xmax
        self.rango = rango
        self.puntos = puntos
        self.poblacionInicial = poblacionInicial
        self.poblacionMaxima = poblacionMaxima
        self.generaciones = generaciones
        self.noBits = noBits
        self.individuos = []
        self.probabilidadDeCruce = Pc
        self.Pmi = Pmi
        self.Pmg = Pmg
        
    def generarPoblacionInicial(self):
        individuos = []
        for i in range(0,self.poblacionInicial):
            binary = 0
            decimal = random.uniform(0,self.rango)
            binary = bin(int(decimal))
            binary = binary.removeprefix("0b")
            if(len(binary) < self.noBits):
                binary = binary.zfill(self.noBits)
            x = self.Xmin + (decimal * self.intervalo)
            self.individuos.append(Individuo(x,0,binary,decimal))
        individuos = self.individuos 
        return individuos

    def posiblesParejas(self):
        parejas = []
        temp = combinations(self.individuos,2)
        for i in list(temp):
            parejas.append(i)
        return parejas
    
    def posiblesParejasX(self):
        listCombinaciones = []
        padres = []
        for i in range(len(self.individuos)):
            individuosSeleccionados = random.randint(2, len(self.individuos))
            candidatos = random.sample(self.individuos, individuosSeleccionados)
            ganador = max(candidatos, key = lambda individuo: individuo.Y)
            padres.append(ganador)
        temp = combinations(padres,2)
        for i in list(temp):
            listCombinaciones.append(i)
        return listCombinaciones    

    def cruzaX(self, listParejas):
            listNewgen = []
            if(len(listParejas) > 1):
                for i in range(len(listParejas)):
                    for k in range(0,1):   
                        MascaraDeCruce = ''
                        child1 = ''
                        for y in range(self.noBits):
                            MascaraDeCruce = MascaraDeCruce + "" + str(random.randint(0,1))
                        var = listParejas[i]
                        if(k == 0):
                            gen1 = var[0].bino
                            gen2 = var[1].bino
                        else:
                            gen1 = var[1].bino
                            gen2 = var[0].bino
                        for j in range(len(gen1)):
                            if MascaraDeCruce[j] == '1':
                                child1 = child1 + gen1[j]
                            else:
                                child1 = child1 + gen2[j]
                        listNewgen.append(child1)
            return listNewgen

    def mutacion(self, listCruza):

        listNewInd = []
        listNewBit = []
        listNewBit2 = []
        listAnalizador= []
        listNoCruza= []
        listNew = []
        listGenMutado= []
        for i in range(len(listCruza)):
            var = listCruza[i]
            pmir=float("{:.4f}".format(random.uniform(0.0,1.0)))
            if pmir < self.Pmi:
                listNewInd.append(listCruza[i])
            if pmir > self.Pmi:
                listGenMutado.append(listCruza[i])
        for i in range(len(listNewInd)):
                var =listNewInd[i]
                for y in range(len(var)):
                    listNew.append(var[y])
                for y in range(len(var)):
                    listAnalizador.append(var[y])
                    pmgr= random.randint(0,len(var)-1)
                    listNew[pmgr]
                    lis2=listNew[pmgr]
                    listNewBit.append(lis2)
                # print(listNewBit)
                bit2 = ''.join(listNewBit)
                listGenMutado.append(bit2)
                listAnalizador.clear()
                listNewBit.clear()
                listNew.clear()
        return listGenMutado

    def ConvertirAObjetos(self,mutados):
        for i in range(0,len(mutados)):
            mutadoBinario = mutados[i]
            posicion = 0
            decimal = 0
            binario = mutadoBinario[::-1]            
            for digito in binario:
                # Elevar 2 a la posición actual
                multiplicador = 2**posicion
                decimal += float(digito) * multiplicador
                posicion += 1            
            x = self.Xmin + (decimal * self.intervalo)
            self.individuos.append(Individuo(x,0,mutados[i],decimal))

    def limpiar(self):
        auxIndividuos = []
        # i = 0
        for i in range(len(self.individuos)):
            if(self.individuos[i].X <= self.Xmax):
                auxIndividuos.append(self.individuos[i])
        self.individuos.clear()
        self.individuos = auxIndividuos            
        # for elemento in self.individuos:
        #     if(elemento.X > self.Xmax):
        #         self.individuos.pop(i)
            # i += 1

    def fx(self):
        dataAux =  []
        for i in range(len(self.individuos)):
            x = self.individuos[i].X
            op = float("{:.4f}".format(math.sin(math.radians(x))))
            op2 = float("{:.4f}".format(math.sqrt(2*(pow(x,2))-x-2)))
            if(op2 > 0): 
                resultado = float("{:.4f}".format(op * op2))
                self.individuos[i].Y = resultado
                dataAux.append(self.individuos[i])    
        self.individuos.clear()
        self.individuos = dataAux
        # for elemento in self.individuos:
            
        # print(len(self.individuos))
        
    
    def poda(self):
        uniqueData = []
        if(len(self.individuos) > self.poblacionMaxima):
            while(len(self.individuos) > self.poblacionMaxima):
                posicion = random.randint(0, self.poblacionMaxima)
                self.individuos.pop(posicion)
        for individuo in self.individuos:
            if not any(I.bino == individuo.bino for I in uniqueData):
                uniqueData.append(individuo)
        self.individuos.clear()
        self.individuos = uniqueData


def graficasXiteracion(self,x, fx):
    try:
        rmtree("assets\GraficaHistorial\img")
    except:
        pass
    plt.plot(x,fx, label="Mejores individuo", color="green", linestyle="-",marker ='.')
    plt.legend()
    os.makedirs("assets\GraficaHistorial\img", exist_ok=True)
    plt.savefig("assets\GraficaHistorial\img\GraficaGeneral.png")
    plt.close()

def graficasXgeneracion(self, listNuevaPAptitud,listNuevaFx,index):
    print('Entro a graficas x generacion')
    plt.title("Generacion: "+str(index))
    plt.plot(listNuevaPAptitud,listNuevaFx, label="Generacion "+str(index), color="blue", linestyle="none",marker ='.')
    plt.legend()
    os.makedirs("assets\GraficasIndividuales\img", exist_ok=True)
    plt.savefig("assets\GraficasIndividuales\img\GraficaIndividual "+str(index)+".png")
    plt.close()

if __name__ == "__main__":
    def envioDatos(generaciones, poblacionM, rangoMax, rangoMin, intervalo, mutacionInd, mutacionGen, probCruza):
        print("generaciones :", generaciones.get())
        print("poblacionM :", poblacionM.get())
        print("rangoMaximo :", rangoMax.get())
        print("rangoMinimo :", rangoMin.get())
        print("Intervalo :", intervalo.get())
        print("Mutacion individuo :", mutacionInd.get())
        print("Mutacion gen :", mutacionGen.get())
        print("Probabilida de cruza: ", probCruza.get())

        return
    #window
    tkWindow = Tk()  
    tkWindow.geometry('400x250')  
    tkWindow.title('Obtencion de datos')
    #----
    usernameLabel = Label(tkWindow, text="Generaciones").grid(row=0, column=0)
    generaciones = IntVar()
    generacionesEntry = Entry(tkWindow, textvariable=generaciones).grid(row=0, column=1)      
    #-----
    poblacionMLabel = Label(tkWindow,text="Poblacion Maxima").grid(row=1, column=0)  
    poblacionM = DoubleVar()
    poblacionMEntry = Entry(tkWindow, textvariable=poblacionM).grid(row=1, column=1)
    #-----
    poblacionMLabel = Label(tkWindow,text="Rango maximo").grid(row=2, column=0)  
    rangoMaximo = DoubleVar()
    rangoMaximoEntry = Entry(tkWindow, textvariable=rangoMaximo).grid(row=2, column=1)
    #-----
    poblacionMLabel = Label(tkWindow,text="Rango minimo").grid(row=3, column=0)  
    rangoMinimo = DoubleVar()
    rangoMinimoEntry = Entry(tkWindow, textvariable=rangoMinimo).grid(row=3, column=1)
    #-----
    poblacionMLabel = Label(tkWindow,text="Intervalo").grid(row=4, column=0)  
    intervalo = DoubleVar()
    intervaloEntry = Entry(tkWindow, textvariable=intervalo).grid(row=4, column=1)
    #-----
    poblacionMLabel = Label(tkWindow,text="Mutacion del individuo").grid(row=5, column=0)  
    mutacionIndividuo = DoubleVar()
    mutacionIndividuoEntry = Entry(tkWindow, textvariable=mutacionIndividuo).grid(row=5, column=1)
    #-----
    poblacionMLabel = Label(tkWindow,text="Mutacion del gen").grid(row=6, column=0)  
    mutacionGen = DoubleVar()
    mutacionGenEntry = Entry(tkWindow, textvariable=mutacionGen).grid(row=6, column=1)

    probabilidadCruzaLabel = Label(tkWindow,text="Probabilidad de cruza").grid(row=7, column=0)  
    probCruza = DoubleVar()
    probCruzaEntry = Entry(tkWindow, textvariable=probCruza).grid(row=7, column=1)
    

    envioDatos = partial(envioDatos, generaciones, poblacionM, rangoMaximo, rangoMinimo, intervalo, mutacionIndividuo, mutacionGen, probCruza)
    #login button
    btnEnviar = Button(tkWindow, text="Enviar", command=envioDatos).grid(row=8, column=0)  

    tkWindow.mainloop()


    print("Generaciones: ")
    generaciones = generaciones.get()
    print("Población maxima")
    poblacionMaxima = poblacionM.get()
    poblacionInicial = random.randint(2,poblacionMaxima)
    print("Rango Maximo")
    xMaximo = rangoMaximo.get()
    print("Rango Minimo")
    xMinimo = rangoMinimo.get()
    print("Intervalo")
    intervalo = intervalo.get()
    rango = xMaximo-xMinimo 
    puntos = (rango/intervalo)+1 
    bit= bin(int(puntos))
    bit=bit.removeprefix("0b")
    noBits= len(bit)
    print(noBits)
    print("Ingrese la probabilidad de mutación del inidividuo")
    Pmi= mutacionIndividuo.get()
    print("Ingrese la probabilidad de mutacion de gen")
    Pmg= mutacionGen.get()
    print("Ingrese la probabilidad de cruza")
    Pc= probCruza.get()
    
    ag = AlgoritmoGenetico(xMinimo, xMaximo, intervalo, rango, puntos, poblacionMaxima, poblacionInicial, generaciones, noBits, Pmi,Pmg, Pc)
    
    ag.generarPoblacionInicial()

    MejoresIndividuos = []
    MediaIndividuos = []
    PeoresIndividuos = []

    for i in range(0,generaciones):
        parejas = ag.posiblesParejasX()
        hijos = ag.cruzaX(parejas)
        mutados = ag.mutacion(hijos)
        ag.ConvertirAObjetos(mutados)
        ag.fx()
        # print("_______________________________ya2_________________")
        ag.limpiar()
        ag.poda()        
        MejoresAptitudes = [individuo.Y for individuo in ag.individuos]
        MejoresIndividuos.append(max(MejoresAptitudes))
        aptitudes = [individuo.Y for individuo in ag.individuos]
        promedio = sum(aptitudes)/len(aptitudes)
        MediaIndividuos.append(promedio)
        peoresAptitudes = [individuo.Y for individuo in ag.individuos]
        PeoresIndividuos.append(min(peoresAptitudes))
        print(i)
    # print("_____MEJORES_____\n" , MejoresIndividuos)
    # print("______PROMEDIO_____\n", MediaIndividuos)
    # print("_____PEOR_____\n", PeoresIndividuos)
        
        try:
            os.rmdir("assets")
        except:
            pass 
        os.makedirs("assets\Video", exist_ok=True)

        plt.plot(MejoresIndividuos, label="Mejor individuo", color="red", linestyle="-",)
        plt.plot(MediaIndividuos, label="Promedio", color="blue", linestyle="-",)
        plt.plot(PeoresIndividuos, label="Peor individuo", color="green", linestyle="-")
        plt.legend()
        os.makedirs("assets\Grafica", exist_ok=True)
        plt.savefig("assets\Grafica\GraficaHistorial.png")
        plt.close()


        TodaslasX = [individuo.X for individuo in ag.individuos]
        print(TodaslasX)
        TodaslasY = [individuo.Y for individuo in ag.individuos]
        print(TodaslasY)
        fig, ax = plt.subplots()
        ax.scatter(x = TodaslasX, y = TodaslasY)
        os.makedirs("assets\GraficaxGeneracion", exist_ok=True)
        plt.savefig('assets\GraficaxGeneracion\GraficaHistorial'+str(i)+'.png')
        plt.close()