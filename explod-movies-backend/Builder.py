import networkx as nx
import matplotlib.pyplot as plt


# Funzione che prende in input i due dizionari di mapping dei film piaciuti e dei film raccomandati e crea il grafo
# che li collega attraverso le proprietà in comune
def costruisci_grafo(profile, recommendation):
    profile1 = {}
    recommendation1 = {}

    with open('movies_stored_prop.mapping', 'r') as f:
        for line in f:                                    # scorro le righe del file con le triple RDF
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

    print("\nGrafo creato con successo!\n")

    return G, common_proprierties


# Funzione che disegna e visualizza il grafo creato
def visualizza_grafo(G):
    nx.draw(G, with_labels=True)
    plt.show()