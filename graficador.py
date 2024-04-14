#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 19:23:17 2022

@author: miguel
"""
import matplotlib.pyplot as plt

class Graficador:
    
    def __init__(self):
        self.ciudades = [[],[],[],[],[],[]]
        self.caminos = [[[],[]]]
        self.figure, self.axes = plt.subplots()
        
    def loadMap(self,mapa):        
        # Obtiene las coordenadas de las ciudades
        for ciudad in mapa:
            coordenada = mapa[ciudad]['coord']
            children = mapa[ciudad]['nodes']
            self.ciudades[0].append(coordenada[0])
            self.ciudades[1].append(795-coordenada[1])
            self.ciudades[2].append(ciudad)
            # grey: inicial
            # red: pos actual
            # orange: visitado
            # darkblue: ruta
            self.ciudades[3].append('grey')
            self.ciudades[4].append(children)
        
        # Grafica las ciudades
        self.axes = plt.scatter(self.ciudades[0], self.ciudades[1], zorder=500, s=20, color='grey')
        
        # Obtiene las conexiones entre ciudades
        for ciudad in mapa:
            #Extrae los datos de cada ciudad
            vecinos = mapa[ciudad]['nodes']
            i_ciudad = self.ciudades[2].index(ciudad)
            x0 = self.ciudades[0][i_ciudad]
            y0 = self.ciudades[1][i_ciudad]
            
            # Agrega el nombre de cada ciudad a la gráfica
            #plt.text(x0, y0, self.ciudades[2][i_ciudad], zorder=501)
            self.axes = plt.text(x0, y0, self.ciudades[2][i_ciudad], zorder=501)
            
            for nodo in vecinos:
                i_nodo = self.ciudades[2].index(nodo)
                x1 = self.ciudades[0][i_nodo]
                y1 = self.ciudades[1][i_nodo]
                
                # Agrega los caminos al arreglo self.caminos
                if ([[x0,x1],[y0,y1]] not in self.caminos or 
                    [[x1,x0],[y1,y0]] not in self.caminos):
                    self.caminos.append([[x0,x1],[y0,y1]])
                    # Dibuja los caminos
                    self.axes = plt.plot([x0,x1], [y0,y1], 'r', lw=1, color='lightgrey')
                
        self.axes = plt.axis('off')
        self.axes = plt.title('Mapa')
        #plt.draw()
        plt.pause(0.01)
        #plt.show(block=False)
    
    def redrawMap(self):
        #print("redraw")
        self.figure.clf()
        
       
        for i in range(len(self.ciudades[0])):
            x0 = self.ciudades[0][i]
            y0 = self.ciudades[1][i]
            c = self.ciudades[3][i]
            size = 20
            if (c != 'grey'):
                size = 40
            
            
            # Grafica las ciudades
            self.axes = plt.scatter(x0, y0, zorder=500, s=size, color=c)
            # Agrega el nombre de cada ciudad a la gráfica
            self.axes = plt.text(x0, y0, self.ciudades[2][i], zorder=501)
            
        # Grafica las conexiones entre ciudades
        for camino in self.caminos:
           self.axes = plt.plot(camino[0], camino[1], 'r', lw=1, color='lightgrey')
                
        self.axes = plt.axis('off')
        self.axes = plt.title('Mapa')
        #plt.show()
        plt.pause(0.01)

    # grey: inicial
    # red: pos actual
    # yellow: visitado
    # darkblue: ruta
    
    def resetAgents(self):
        for i in range(len(self.ciudades[3])):
            self.ciudades[3][i] = 'grey'
    
    def setCurrent(self, key, agente):
        colors = ['red','blue','green','yellow','black','orange']
        if (key != ""):
            i = self.ciudades[2].index(key)
            self.ciudades[3][i] = colors[agente]
            return
    
    def setVisited(self, key):
        if (key != ""):
            i = self.ciudades[2].index(key)
            self.ciudades[3][i] = 'orange'
        
    def setRuta(self, key):
        if (key != ""):
            i = self.ciudades[2].index(key)
            self.ciudades[3][i] = 'green'
            
        
    def getNodes(self, key):
        i = self.ciudades[2].index(key)
        return self.ciudades[4][i].copy()
    
    def getTotalCiudades(self):
        return len(self.ciudades[2])
    
