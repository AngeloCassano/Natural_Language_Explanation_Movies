import networkx as nx
import matplotlib.pyplot as plt
from Mapper import mapping_profilo
import sys


# Funzione che prende in input i due dizionari di mapping dei film piaciuti e dei film raccomandati e crea il grafo
# che li collega attraverso le proprietà in comune
def costruisci_grafo(profile, recommendation):
    profile1 = {}
    recommendation1 = {}
    numero_proprieta = 0

    with open('movies_stored_prop.mapping', 'r') as f:
        for line in f:                                    # scorro le righe del file con le triple RDF
            numero_proprieta += 1
            line = line.rstrip().split('\t')
            for key, value in profile.items():            # scorro i film piaciuti nel dizionario
                if line[0] == value:                      # quando trovo l'URI del film piaciuto in una tripla RDF
                    profile1[line[2]] = value             # inserisco la proprietà come chiave e il film come valore in un nuovo dizionario

    with open('movies_stored_prop.mapping', 'r') as f:
        for line in f:                                    # scorro le righe del file con le triple RDF
            line = line.rstrip().split('\t')
            for key, value in recommendation.items():     # scorro i film raccomandati nel dizionario
                if line[0] == value:                      # quando trovo l'URI del film piaciuto in una tripla RDF
                    recommendation1[line[2]] = value      # inserisco la proprietà come chiave e il film come valore in un nuovo dizionario di appoggio

    profile2 = {}
    recommendation2 = {}

    for key, value in profile1.items():                   # scorro entrambi i dizionari appena creati
        for key1, value1 in recommendation1.items():
            if key == key1:                               # se film piaciuti e film raccomandati hanno proprietà in comune
                profile2[key] = value                     # inserisco proprietà e film in un dizionario (solo quelle in comune)
                recommendation2[key1] = value1

    common_proprierties = list(profile2.keys())           # creo una lista con solo le proprietà in comune
    G = nx.DiGraph()                                      # creo un grafo orientato
    for key, value in profile2.items():
        G.add_edge(value, key)                            # aggiungo come nodi i film piaciuti e i film raccomandati
    for key, value in recommendation2.items():            # aggiungo come nodi le proprietà in comune
        G.add_edge(key, value)                            # collego i nodi attraverso le proprietà in comune con archi

    return G, common_proprierties, numero_proprieta


# Funzione che disegna e visualizza il grafo creato
def visualizza_grafo(G):
    nx.draw(G, with_labels=True)
    plt.show()


# Funzione che prende in input il grafo creato e l'URI di una proprietà e stampa gli archi entranti (film piaciuti)
# e gli archi uscenti (film raccomandati) di quella spcifica proprietà
def stampa_vicini(G, item):
    archi_entranti = G.in_edges(item)
    print("Archi entranti per il nodo ", item, " (film piaciuti):")
    for archi_entranti_spec in archi_entranti:
        print(archi_entranti_spec[0])

    archi_uscenti = G.out_edges(item)
    print("Archi uscenti per il nodo ", item, " (film raccomandati):")
    for archi_uscenti_spec in archi_uscenti:
        print(archi_uscenti_spec[1])


def cmd_builder(profilo, racc):
    profile, numero_film1 = mapping_profilo(profilo)
    recommendation, numero_film2 = mapping_profilo(racc)
    print("\nEsecuzione componente Builder...\n")
    G, common_properties, numero_proprieta = costruisci_grafo(profile, recommendation)
    visualizza_grafo(G)
    print("Numero di proprietà mappate: ", numero_proprieta)
    print("\nGrafo creato con successo!\n")
    print("Numero di nodi del grafo: ", G.number_of_nodes())
    print("Numero di archi del grafo: ", G.number_of_edges())
    print("\nEcco le proprietà in comune tra film piaciuti e raccomandazioni:\n")
    for item in common_properties:
        print(item)


if __name__ == "__main__":
    globals()[sys.argv[1]](sys.argv[2][1:-1].split(','), sys.argv[3][1:-1].split(','))

