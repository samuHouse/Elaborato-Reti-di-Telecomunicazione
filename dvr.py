# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 14:12:12 2024

@author: Samuele Casadei

matricola: 0001097772

IMPLEMENTAZIONE DEL PROTOCOLLO DISTANCE VECTOR ROUTING
"""

# importo random per generare i collegamenti tra i nodi in modo casuale
import random

# la classe Nodo rappresenta l'istanza del nodo di commutazione
class Node:
    # costruttore di classe
    def __init__(self, name):
        # Inizializza un nodo con un nome specifico e una tabella di routing.
        self.name = name
        """
        la routing table è utilizzata come dictionary, dove:
        le key sono i nomi delle destinazioni, e ad ogni key è associata una
        coppia di valori (distanza, nextHop).
        Ovviamente, per ogni nodo, viene inizializzato con distanza 0 da se stesso
        """
        self.routingTable = {name: (0, name)}  # Formato: {destinazione: (distanza, next_hop)}
        """
        Neighbors è una dictionary dove le chiavi sono i nodi adiacenti, e il valore
        corrispondenete ad ogni chiave è la distanza da esso.
        """
        self.neighbors = {}

    # funzione che aggiunge un nuovo nodo alla lista di adiacenza di un altro nodo
    def addNeighbor(self, neighbor, distance):
        # Aggiunge un nodo vicino con una distanza specifica.
        self.neighbors[neighbor] = distance
        self.routingTable[neighbor.name] = (distance, neighbor.name)

    def updateNode(self):
        """
        Aggiorna la tabella di routing utilizzando il protocollo Distance Vector.
        Restituisce True se la tabella è stata aggiornata, False altrimenti.
        """
        # flag che descrive se l'update è avvenuto o meno
        updated = False
        # per ogni vicino
        for neighbor, distance_to_neighbor in self.neighbors.items():
            # esamino la routing table
            neighbor_table = neighbor.routingTable
            """
            se il vicino riesce a raggiungere una destinazione nota percorrendo
            una distanza minore, oppure riesce a raggiungere una destinazione non nota,
            aggiorno la mia routing table con il nuovo percorso (tramite il vicino).
            """
            for dest, (dist, next_hop) in neighbor_table.items():
                new_distance = distance_to_neighbor + dist
                if dest not in self.routingTable or new_distance < self.routingTable[dest][0]:
                    self.routingTable[dest] = (new_distance, neighbor.name)
                    # se faccio modifiche alla routing table, update diventa True
                    updated = True
        return updated

    def printTable(self):
        # Stampa la tabella di routing del nodo.
        print(f"Routing table for {self.name}:")
        print("dest\t\t  dist\t\t\tnextHop")
        for dest, (dist, next_hop) in self.routingTable.items():
            print(f"{dest}\t\t|\t\t{dist}\t\t|\t\t{next_hop}")
        print()

def randomNetwork(num_nodes, max_distance=10):
    """
    Genera una rete casuale con un dato numero di nodi e distanze massime,
    garantendo che ogni nodo abbia almeno un collegamento.
    """
    # crea nodi per il numero indicato, dando a ciascuno (come nome) una lettera (A, B, C, ...)
    nodes = [Node(chr(65 + i)) for i in range(num_nodes)]  # Nodi con nomi A, B, C, ...
    
    # crea collegamenti random tra i nodi, con probabilità del 50%
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if random.random() < 0.5:
                distance = random.randint(1, max_distance)
                nodes[i].addNeighbor(nodes[j], distance)
                nodes[j].addNeighbor(nodes[i], distance)
    
    '''
    Dato un nodo isolato non sarebbe utile per il test, questo ciclo fa sì che ogni nodo
    abbia al meno un collegamento, scelto sempre in modo casuale.
    '''
    for node in nodes:
        if not node.neighbors:  # Nodo isolato
            # Collega il nodo a un altro nodo casuale
            other_node = random.choice([n for n in nodes if n != node])
            distance = random.randint(1, max_distance)
            node.addNeighbor(other_node, distance)
            other_node.addNeighbor(node, distance)
    
    return nodes

def tablesUpdate(nodes, iterations=10):
    '''
    Simula l'aggiornamento delle tabelle di routing tra i nodi
    per un dato numero di iterazioni.
    '''
    for i in range(iterations):
        print(f"---------- Iteration {i + 1} ----------")
        # flage che indica se viene raggiunta la convergenza
        updated = False
        for node in nodes:
            if node.updateNode():
                # se almeno una tabella viene aggiornata, updated è true
                updated = True
        for node in nodes:
            # per ogni nodo stampa la sua routing table
            node.printTable()
        # se in questa iterazione nessuna tabella viene aggiornata, ferma il loop
        if not updated:
            print("Convergence accomplished.\n")
            break

# Configurazione della rete
num_nodes = 6  # Cambia per avere più o meno nodi
max_distance = 15  # Cambia per variare le distanze massime

# Generazione della rete
nodes = randomNetwork(num_nodes, max_distance)

# Simulazione del routing
tablesUpdate(nodes)

