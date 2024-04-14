#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 21 10:23:17 2022

@author: miguel
"""

class Agente:
    def __init__(self, id):
        self.id = id
        self.inicio = ""
        self.final = ""
        self.posicion_actual = [0, 0]  # ruta, profundidad
        self.prev_pos = ""
        self.cambios_de_ruta = [[],[]]
        self.ruta = [[""]]
        self.visitados = []
        self.vecinos = []
        self.modoBusqueda = 'profundidad'
        self.buffer_busqueda = []
        self.padres = []
        self.movimientos = []
        self.destino = ""
        self.move_pending = ""
        self.move_pending2 = ""
        self.change_route = False
        self.state = 'idle'
        self.busqueda_state = 'busqueda_1'
        self.padre = ""
        self.try_node = ""
        print("Agente creado!")

    def reset(self):
        self.id = id
        self.inicio = ""
        self.final = ""
        self.posicion_actual = [0, 0]  # ruta, profundidad
        self.prev_pos = ""
        self.cambios_de_ruta = [[],[]]
        self.ruta = [[""]]
        self.visitados = []
        self.vecinos = []
        self.modoBusqueda = 'profundidad'
        self.buffer_busqueda = []
        self.padres = []
        self.movimientos = []
        self.destino = ""
        self.move_pending = ""
        self.move_pending2 = ""
        self.change_route = False
        self.state = 'idle'
        self.busqueda_state = 'busqueda_1'
        self.padre = ""
        self.try_node = ""
        print("Agente reinicializado!")
        
    def getFinalRoute(self):
        if (self.state == 'finished'):
            return self.ruta[self.posicion_actual[0]]
        return False
    
    def getCurPos(self):
        return self.ruta[self.posicion_actual[0]][self.posicion_actual[1]]
    
    def getPrevPos(self):
        return self.prev_pos
        
    def setInicio(self, inicio, vecinos):
        print("Ciudad inicial:", inicio)
        print("Vecinos:", vecinos)
        self.setNewVecinos(vecinos)
        self.inicio = inicio
        self.ruta = [[inicio]]
        self.setPos([0, 0])
        self.buffer_busqueda = self.vecinos.copy()
        self.padres = len(self.buffer_busqueda) * [self.inicio]

    def setFinal(self, final):
        print("Ciudad final:", final)
        self.final = final

    def setBehavior(self, modo):
        if (modo == 'amplitud'):
            self.modoBusqueda = 'amplitud'
        else:
            self.modoBusqueda = 'profundidad'
            
    def setNewVecinos(self,vecinos):
        self.vecinos = vecinos

    def setPos(self, pos):
        if (pos != self.posicion_actual):
            pos_ant = self.posicion_actual
            self.posicion_actual = pos
            key = self.ruta[pos[0]][pos[1]]
            key_anterior = self.ruta[pos_ant[0]][pos_ant[1]]
            #Mantiene un registro unico de lugares visitados
            if (key_anterior not in self.visitados):
                self.visitados.append(key_anterior)
            self.prev_pos = key_anterior
            self.vecinos = []
            print("setpos: ", self.state)
            if (self.state == "returnOne"):
                self.state = "wait_returnOne"
                print("Nueva posicion: ", key, self.state)
                return
            
            if (self.state == "forwardOne"):
                self.state = "wait_forwardOne"
                print("Nueva posicion: ", key, self.state)
                return
            
            self.state = "waiting for nodes"
            print("Nueva posicion: ", key, self.state)
        else:
            if (pos == self.posicion_actual):
                key = self.ruta[pos[0]][pos[1]]
                self.state = "idle"
                print("No cambio mi posición: ", key)


    def move(self, destino):
        #self.state = 'moving'
        print("Moviendo a: ", destino)
        pos = self.posicion_actual
        if (destino in self.vecinos and destino not in self.ruta[pos[0]]):
            # Down
            #print("move: ", len(self.ruta[pos[0]]), (pos[1]+1))
            if (len(self.ruta[pos[0]]) == (pos[1]+1)):
                # Dive in to node
                self.ruta[pos[0]].append(destino)
                print("agregue: ", destino)
            new_pos = [pos[0], (pos[1] + 1)]
            self.setPos(new_pos)
            return True
        
        if(pos[1] > 0):
            if (destino == self.ruta[pos[0]][pos[1]-1]):
                # Up
                new_pos = [pos[0], (pos[1] - 1)]
                self.setPos(new_pos)
                return True
        
        if(pos[1]+1 < len(self.ruta[pos[0]])):
            if (destino == self.ruta[pos[0]][pos[1]+1]):
                # Down existente
                new_pos = [pos[0], (pos[1] + 1)]
                self.setPos(new_pos)
                return True
        
        return False
    
    def __returnOne(self):
        self.state = "returnOne"
        print("return: ", self.destino, self.vecinos, self.getCurPos())
        if (self.destino not in self.vecinos):
            
            if (self.posicion_actual[1] > 0):
                new_depth = self.posicion_actual[1]-1
                key = self.ruta[self.posicion_actual[0]][new_depth]
                print("regresando a:", key)
                self.move(key)
            else:
                print("Llegue a inicio sin encontrar la ciudad en vecinos")
            
            self.__changeRoute2()
        else:
            self.__changeRoute1()
            
    def __changeRoute2(self):
        #print("__changeRoute2")
        if (self.destino not in self.vecinos):
            for route in self.ruta:
                depth_i = self.posicion_actual[1]
                key = self.ruta[self.posicion_actual[0]][depth_i]
                # Verifica si en la ciudad actual existen bifurcaciones
                # y si el destino se encuentre en dichas bifurcaciones
                if ((depth_i+1) < len(route)):
                    if (key == route[depth_i] and self.destino in route[depth_i+1:]):
                        print("Cambiando a ruta existente")
                        route_num = self.ruta.index(route)
                        self.posicion_actual[0]=route_num
                        self.state = 'moveTo'
                        return
        self.status = "returnOne"
        
    def __changeRoute1(self):
        #print("__changeRoute1")
        self.state = "changeRoute1"
        if (self.destino in self.vecinos):
                # Si el destino se encuentra en los vecinos de la ciudad
                # Se crea una nueva ruta
                print("CAMBIANDO A NUEVA RUTA :D")
                depth_i = self.posicion_actual[1] + 1
                route = self.posicion_actual[0]
                nueva_ruta = self.ruta[route][:depth_i]
                self.ruta.append(nueva_ruta)
                print("nueva ruta: ", nueva_ruta)
                self.posicion_actual[0] = len(self.ruta)-1
                self.move(self.destino)
                
    def __forwardOne(self):
        self.state = "forwardOne"
        print("forward: ", self.destino, self.vecinos, self.getCurPos())
        if (self.destino != self.getCurPos()):
            if (self.destino not in self.vecinos):
                if (self.posicion_actual[1] < (len(self.ruta[self.posicion_actual[0]])-1)):
                    new_depth = self.posicion_actual[1]+1
                    key = self.ruta[self.posicion_actual[0]][new_depth]
                    print("avanzando a:", key)
                    self.move(key)
                else:
                    print("Llegue al final sin encontrar la rama")
                    return False
            else:
                self.state = "idle"
                self.move(self.destino)
        else:
            self.state = "idle"
        
    def moveTo(self):
        #self.state = 'calculating'
        print("Calculando movimientos ...", self.destino, self.vecinos, 
              self.ruta[self.posicion_actual[0]], 
              self.ruta[self.posicion_actual[0]][self.posicion_actual[1]])
        if (self.destino not in self.vecinos and
                self.destino not in self.ruta[self.posicion_actual[0]]):
            
            self.move_pending = self.destino
            self.__returnOne()
        else:
            if (self.destino in self.vecinos):
                    self.move(self.destino)
                    
            else:
                if (self.destino in self.ruta[self.posicion_actual[0]]):
                    # Descender en una ruta en la que se encuentra el destino
                    self.move_pending = self.destino
                    self.__forwardOne()
                    

    def __busqueda_2(self):
        nodes = self.vecinos.copy()
        if len(nodes) != 0:
            for child in nodes:
                if (child not in self.visitados and child != self.padre):
                    if (self.modoBusqueda == 'amplitud'):
                        self.buffer_busqueda.insert(0, child)
                        self.padres.insert(0,self.try_node)
                        
                    else:
                        self.buffer_busqueda.append(child)
                        self.padres.append(self.try_node)
                        # print(try_node)                    

    def runSearch(self): 
        if (self.state == 'moveTo'):
            self.moveTo()    
            return
            
        if (self.state == 'returnOne'):
            self.__returnOne()
            return
            
        if (self.state == 'forwardOne'):
            self.__forwardOne()
            return
        
        if (self.state == 'changeRoute2'):
            self.__changeRoute2()
            return
            
        if (self.state == 'changeRoute1'):
            self.__changeRoute1()
            return
            
        if (self.state == 'idle'):
            
            print("idle:", self.move_pending,",", self.move_pending2, len(self.buffer_busqueda), self.destino)
            
            if ( self.move_pending != ""):
                
                if (self.getCurPos() == self.move_pending):
                    self.move_pending = ""
                    print(1)
                else:
                    self.destino = self.move_pending
                    self.moveTo()
                    print(2)
                return
            
            if ( self.move_pending2 != "" and self.move_pending == ""):
                self.move_pending = self.move_pending2
                self.move_pending2 = ""
                return
                
            if (self.final == self.getCurPos()):
                print("ENCONTRE: ", self.getCurPos())
                self.state = 'finished'
                return
            
            if (self.busqueda_state == 'busqueda_1'):
                if ( len(self.buffer_busqueda) > 0 and 
                    self.move_pending == "" and self.move_pending2 == "" ):
                    
                    self.try_node = self.buffer_busqueda.pop()
                    self.padre = self.padres.pop()
                    
                    if (self.padre not in self.ruta[self.posicion_actual[0]]):
                        self.destino = self.padre
                        self.moveTo()
                        self.move_pending2 = self.try_node
                    else:
                        self.destino = self.try_node
                        self.moveTo()
                        
                    self.busqueda_state = 'busqueda_2'
                return
                    
            if (self.busqueda_state == 'busqueda_2'):
                if ( self.move_pending == "" and self.move_pending2 == ""):
                    self.__busqueda_2()
                    self.busqueda_state = 'busqueda_1'
                    return
                                    
                                    
        if (self.state == 'finished'):
            print("Trabajo finalizado, agente: ", self.id,", ruta final: ", self.getFinalRoute())
            return
            
        if (self.state == 'wait_returnOne'):
            if (self.vecinos != []):
                self.state = 'returnOne'
            else:
                print("returnOne, Esperando información acerca del nuevo nodo . . .")
            return
                
        if (self.state == 'wait_forwardOne'):
            if (self.vecinos != []):
                self.state = 'forwardOne'
            else:
                print("forwardOne, Esperando información acerca del nuevo nodo . . .")
            return
            
        if (self.state == 'waiting for nodes'):
            if (self.vecinos != []):
                self.state = 'idle'
            else:
                print("waiting, Esperando información acerca del nuevo nodo . . .")
            return
        
        
    def runAgent(self):
        print("Tick agente: ", self.id, self.state)
        self.runSearch()
        
