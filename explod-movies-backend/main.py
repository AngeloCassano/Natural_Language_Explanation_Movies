from Mapper import *
from Builder import *
from Ranker import *
from Generator import *
import sys

# CODICE PER ESEGUIRE IL FRAMEWORK DA RIGA DI COMANDO

id_film_p1 = sys.argv[1]
id_film_r1 = sys.argv[2]
graph = sys.argv[3]
numero_prop_considerate = int(sys.argv[4])
idf = sys.argv[5]
scelta_configurazione = sys.argv[6]
template = int(sys.argv[7])
html = sys.argv[8]

id_film_p1.replace("" ,'')
if "[" not in id_film_p1 or "]" not in id_film_p1 or " " in id_film_p1 or "[" not in id_film_r1 or "]" not in id_film_r1 or " " in id_film_r1:
    print("\nI dati inseriti non sono corretti!\nAssicurarsi di aver inserito gli id tra parentesi quadre e senza lasciare spazi.")
elif (graph != "True" and graph != "False") or (idf != "True" and idf != "False") or (html != "True" and html != "False"):
    print("\nI dati inseriti non sono corretti!\nAssicurarsi di aver scelto True o False per la visualizzazione del grafo, il ranking con o senza IDF e l'utilizzo dei tag HTML.")
elif scelta_configurazione != "baseline" and scelta_configurazione != "schema" and scelta_configurazione != "primolivello":
    print("\nI dati inseriti non sono corretti!\nAssicurarsi di aver inserito una tipologia di spiegazione tra quelle previste (baseline, schema, primolivello).")
else:
    id_film_piaciuti = id_film_p1[1:-1].split(',')
    id_film_raccomandati = id_film_r1[1:-1].split(',')
    if graph == "True":
        graph = True
    elif graph == "False":
        graph = False

    if idf == "True":
        idf = True
    elif idf == "False":
        idf = False

    if html == "True":
        html = True
    elif html == "False":
        html = False

    # ESECUZIONE COMPONENTE MAPPER
    print("\nEsecuzione componente Mapper...\n")
    profile, numero_film1 = mapping_profilo(id_film_piaciuti)
    recommendation, numero_film2 = mapping_profilo(id_film_raccomandati)
    print("Numero di film mappati: ", numero_film1)
    print("\nMappatura del profilo utente realizzata:\n")
    for key, value in profile.items():
        print(key, "\t", value)
    print("\nMappatura delle raccomandazioni realizzata:\n")
    for key1, value1 in recommendation.items():
        print(key1, "\t", value1)
    print("\n")

    # ESECUZIONE COMPONENTE BUILDER
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
    print("\n")


    # ESECUZIONE COMPONENTE RANKER
    if idf:
        print("\nEsecuzione componente Ranker con IDF...\n")
    else:
        print("\nEsecuzione componente Ranker NO-idf...\n")
    ranked_prop_idf = ranking_proprieta(G, common_properties, profile, recommendation, idf)
    sorted_prop_idf = proprieta_da_considerare(ranked_prop_idf, numero_prop_considerate)
    stampa_proprieta(sorted_prop_idf)

    # ESECUZIONE COMPONENTE GENERATOR
    if idf:
        print("\nEsecuzione componente Generator CON IDF...\n")
    else:
        print("\nEsecuzione componente Generator  NO-idf...\n")
    triple_structure = build_triple_structure(G, sorted_prop_idf, profile, recommendation)
    explanation = generate_explanation(triple_structure, recommendation, profile, scelta_configurazione, template, html)
    print("\nLa tua spiegazione personalizzata è:\n")
    print(explanation)

