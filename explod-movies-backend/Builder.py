import networkx as nx
import matplotlib.pyplot as plt
from Mapper import mapping_profilo
import sys


# Funzione che prende in input i due dizionari di mapping dei film piaciuti e dei film raccomandati e crea il grafo
# che li collega attraverso le proprieta in comune
def costruisci_grafo(profile, recommendation):
    list_profile_properties = []
    profile_properties: dict[str, list[str]] = {}
    recommendation_properties = {}
    profile_properties_temp = {}
    numero_proprieta = 0

    with open('movies_stored_prop.mapping', 'r') as f:
        for line in f:  # scorro le righe del file con le triple RDF
            numero_proprieta += 1
            line2 = line.rstrip().split('\t')
            if line2[0] in profile.values():  # scorro i film piaciuti nel dizionario
                if line2[2] not in profile_properties.keys():  # quando trovo l'URI del film piaciuto in una tripla RDF
                    list_item =[line2[0]]
                    profile_properties[line2[2]] = list_item
                else:
                    list_item2: list[str] = profile_properties.pop(line2[2])
                    list_item2.append(line2[0])
                    profile_properties[line2[2]] = list_item2
                # profile_properties[line2[2]] = value             # inserisco la proprieta come chiave e il film come valore in un nuovo dizionario

    with open('movies_stored_prop.mapping', 'r') as f:
        for line in f:  # scorro le righe del file con le triple RDF
            numero_proprieta += 1
            line2 = line.rstrip().split('\t')
            if line2[0] in recommendation.values():  # scorro i film piaciuti nel dizionario
                if line2[2] not in recommendation_properties.keys():  # quando trovo l'URI del film piaciuto in una tripla RDF
                    list_item = [line2[0]]
                    recommendation_properties[line2[2]] = list_item
                else:
                    list_item2: list[str] = recommendation_properties.pop(line2[2])
                    list_item2.append(line2[0])
                    recommendation_properties[line2[2]] = list_item2

    print("proprieta profilo: " + str(len(profile_properties)))
    print("proprieta raccomandati: " + str(len(recommendation_properties)))
    print("numero proprieta mappate: " + str(numero_proprieta))

    profile_common_prop = {}
    recomm_common_prop = {}

    for key, value in profile_properties.items():  # scorro entrambi i dizionari appena creati
        if key in recommendation_properties.keys():  # se film piaciuti e film raccomandati hanno proprieta in comune
            profile_common_prop[key] = value  # inserisco proprieta e film in un dizionario (solo quelle in comune)
            recomm_common_prop[key] = recommendation_properties[key]

    common_properties = list(profile_common_prop.keys())  # creo una lista con solo le proprieta in comune
    G = nx.DiGraph()  # creo un grafo orientato
    for key, value in profile_common_prop.items():

        for v in value:
            conteggio = value.count(v)
            G.add_edge(v, key, count=conteggio)  # aggiungo come nodi i film piaciuti e i film raccomandati

    for key, value in recomm_common_prop.items():  # aggiungo come nodi le proprieta in comune
        for v in value:
            G.add_edge(key, v, count=value.count(v))  # collego i nodi attraverso le proprieta in comune con archi
    print("proprieta comuni: " + str(len(common_properties)))

    print("stampa dei nodi del grafo")
    for n in G.nodes:
        print(n)

    print("stampa degli archi del grafo: ")
    for e in G.edges:
        print(e)

    return G, common_properties, numero_proprieta


# Funzione che disegna e visualizza il grafo creato
def visualizza_grafo(G):
    nx.draw(G, with_labels=True)
    plt.show()


# Funzione che prende in input il grafo creato e l'URI di una proprieta e stampa gli archi entranti (film piaciuti)
# e gli archi uscenti (film raccomandati) di quella spcifica proprieta
def stampa_vicini(G, item):
    archi_entranti = G.in_edges(item)
    print("Archi entranti per il nodo ", item, " (film piaciuti):")
    for archi_entranti_spec in archi_entranti:
        print(archi_entranti_spec[0])

    archi_uscenti = G.out_edges(item)
    print("Archi uscenti per il nodo ", item, " (film raccomandati):")
    for archi_uscenti_spec in archi_uscenti:
        print(archi_uscenti_spec[1])


def cmd_builder(profilo, racc, graph):
    if "[" not in sys.argv[2] or "]" not in sys.argv[2] or " " in sys.argv[2] or "[" not in sys.argv[3] or "]" not in \
            sys.argv[3] or " " in sys.argv[3] or (sys.argv[4] != "True" and sys.argv[4] != "False"):
        print(
            "\nI dati inseriti non sono corretti!\nAssicurarsi di aver inserito gli id tra parentesi quadre e senza lasciare spazi.")
        print("\nAssicurarsi di aver scelto True o False per la visualizzazione del grafo.")
    else:
        if graph == "True":
            graph = True
        elif graph == "False":
            graph = False
        profile, numero_film1 = mapping_profilo(profilo)
        recommendation, numero_film2 = mapping_profilo(racc)
        print("\nEsecuzione componente Builder...\n")
        G, common_properties, numero_proprieta = costruisci_grafo(profile, recommendation)
        if graph:
            visualizza_grafo(G)
        print("Numero di proprieta mappate: ", numero_proprieta)
        print("\nGrafo creato con successo!\n")
        print("Numero di nodi del grafo: ", G.number_of_nodes())
        print("Numero di archi del grafo: ", G.number_of_edges())
        print("\nEcco le proprieta in comune tra film piaciuti e raccomandazioni:\n")
        for item in common_properties:
            print(item)


if __name__ == "__main__":
    globals()[sys.argv[1]](sys.argv[2][1:-1].split(','), sys.argv[3][1:-1].split(','), sys.argv[4])
