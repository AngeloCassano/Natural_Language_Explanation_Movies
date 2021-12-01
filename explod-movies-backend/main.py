from Mapper import *
from Builder import *
from Ranker import *
from Generator import *
import sys

# CODICE PER ESEGUIRE IL FRAMEWORK DA RIGA DI COMANDO

id_film_piaciuti = sys.argv[1][1:-1].split(',')
id_film_raccomandati = sys.argv[2][1:-1].split(',')
numero_prop_considerate = int(sys.argv[3])
scelta_configurazione = sys.argv[4]
template = int(sys.argv[5])
html = sys.argv[6]
if html == "True":
    html = True
elif html == "False":
    html = False

# ESECUZIONE COMPONENTE MAPPER
print("\nEsecuzione componente Mapper...\n")
profile, numero_film1 = mapping_profilo(id_film_piaciuti)
recommendation, numero_film2 = mapping_profilo(id_film_raccomandati)
print("Numero di film mappati: ", numero_film1)
print("\n")

# ESECUZIONE COMPONENTE BUILDER
print("\nEsecuzione componente Builder...\n")
G, common_properties, numero_proprieta = costruisci_grafo(profile, recommendation)
visualizza_grafo(G)
print("Numero di proprietà mappate: ", numero_proprieta)
print("\nGrafo creato con successo!\n")
print("Numero di nodi del grafo: ", G.number_of_nodes())
print("Numero di archi del grafo: ", G.number_of_edges())
print("\n")

# ESECUZIONE COMPONENTE RANKER
print("\nEsecuzione componente Ranker...\n")
ranked_prop = ranking_proprieta(G, common_properties, profile, recommendation)
sorted_prop = proprieta_da_considerare(ranked_prop, numero_prop_considerate)
stampa_proprieta(ranked_prop)

# ESECUZIONE COMPONENTE GENERATOR
print("\nEsecuzione componente Generator...\n")
NewPreGenArchitecture = inizializzaNewPreGenArchitecture(G, sorted_prop, profile, recommendation)
explanation = generate_explanation(NewPreGenArchitecture, recommendation, profile, scelta_configurazione, template, html)
print(explanation)
