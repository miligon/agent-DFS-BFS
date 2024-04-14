#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 18:23:17 2022

@author: miguel
"""
from graficador import Graficador 
from agente import Agente
import threading, time
import sys


mapa3={
"Arad":{"nodes":["Sibiu","Timisoara","Zerind"],"coord":[67,133]},
"Zerind":{"nodes":["Oradea","Arad"],"coord":[92,80]},
"Oradea":{"nodes":["Zerind","Sibiu"],"coord":[122,25]},
"Timisoara":{"nodes":["Lugoj","Arad"],"coord":[72,245]},
"Lugoj":{"nodes":["Timisoara","Mehadia"],"coord":[168,287]},
"Dobreta":{"nodes":["Mehadia","Craiova"],"coord":[169,395]},
"Mehadia":{"nodes":["Lugoj","Dobreta"],"coord":[173,340]},
"Sibiu":{"nodes":["Arad","Oradea","Rimnicu Vilcea","Fagaras"],"coord":[227,181]},
"Fagaras":{"nodes":["Sibiu","Bucharest"],"coord":[362,191]},
"Rimnicu Vilcea":{"nodes":["Sibiu","Pitesti","Craiova"],"coord":[261,244]},
"Craiova":{"nodes":["Pitesti","Rimnicu Vilcea","Dobreta"],"coord":[287,410]},
"Pitesti":{"nodes":["Rimnicu Vilcea","Craiova","Bucharest"],"coord":[381,302]},
"Bucharest":{"nodes":["Fagaras","Pitesti","Giurgiu","Urziceni"],"coord":[488,356]},
"Urziceni":{"nodes":["Bucharest","Hirsova","Vaslui"],"coord":[565,325]},
"Vaslui":{"nodes":["Urziceni","Iasi"],"coord":[636,197]},
"Iasi":{"nodes":["Neamt","Vaslui"],"coord":[587,114]},
"Neamt":{"nodes":["Iasi"],"coord":[495,71]},
"Hirsova":{"nodes":["Urziceni","Eforie"],"coord":[669,326]},
"Eforie":{"nodes":["Hirsova"],"coord":[707,402]},
"Giurgiu":{"nodes":["Bucharest"],"coord":[453,433]}
}

def showFinalRoute(self, ruta):
    for ciudad in ruta:
        self.graficador.setRuta(ciudad)
        time.sleep(1)
        # Refresca el mapa
        self.graficador.redrawMap()

def refreshMap():
    global graph
    global agentes
    graph.resetAgents()
    for agente in agentes:
        graph.setCurrent(agente.getCurPos(), agente.id)
        #graph.setVisited(agente.getPrevPos())
    graph.redrawMap()

def refreshData():
    global graph
    global agentes
    for agente in agentes:
        #print("procesando: ",agente.id)
        if (agente.state == 'waiting for nodes' or 
            agente.state == "wait_returnOne" or 
            agente.state == "wait_forwardOne"):
            if (agente.getCurPos() != ""):
                posicion = agente.getCurPos()
                print("Actualizando agente: ",agente.id, posicion, graph.getNodes(posicion))
                agente.setNewVecinos(graph.getNodes(posicion))
    
    refreshMap()
    return True

def isFinished(agentes):
    for agente in agentes:
        print(agente.state)
        if ('finished' not in agente.state):
            return False
    return True

def tickAgents(agentes, tiempo):
    for agente in agentes:
        agente.runAgent()
    if ( isFinished(agentes) ):
        sys.exit()
        return
    threading.Timer(tiempo, tickAgents, (agentes, tiempo)).start()

def setAgent(agent, inicio, vecinos, final, modo):
    agent.setInicio(inicio, vecinos)
    agent.setFinal(final)                    
    agent.setBehavior(modo) 

if __name__ == '__main__':
    graph = Graficador()
    graph.loadMap(mapa3)
    
    agentes = []
    agregar_agentes = True
    agente_id = 1
    opciones = "Arad, Zerind, Oradea, Timisoara, Lugoj, Dobreta, Mehadia, Sibiu, Fagaras, Rimnicu Vilcea, Craiova, Pitesti, Bucharest, Urziceni, Vaslui, Iasi, Neamt, Hirsova, Eforie, Giurgiu"
    print("Cities available: " + opciones)
    while agregar_agentes:
        start = input("Define start:")
        destination = input("Define destination:")
        method = 'profundidad' if input("Select search method (DFS, BFS)") == 'DFS' else 'BFS'
        # Se crean los agentes y se agregan a la lista
        agent = Agente(agente_id)
        setAgent(agent, start, graph.getNodes(start), destination, method)
        agentes.append(agent)
        if input("Add another Agent?(Y/N)") == 'Y':
            agente_id = agente_id + 1
        else:
            agregar_agentes = False
    
    # Se establece el tiempo para el timer
    tiempo = 0.1
    timer = threading.Timer(tiempo, tickAgents, (agentes, tiempo))
    timer.start()
    
    while (True):
        
        refreshData()
        
        # Tiempo de refresco de la grafica
        time.sleep(tiempo/2.0)
        
        if ( isFinished(agentes) ):
            input("Presione ENTER para salir")
            sys.exit()
    
    
    
