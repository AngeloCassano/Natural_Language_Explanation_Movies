import sys
from Mapper import *
from Builder import *
from Ranker import *
from Generator import *

id_film_piaciuti = sys.argv[1][1:-1].split(',')
id_film_raccomandati = sys.argv[2][1:-1].split(',')
scelta_configurazione = sys.argv[3]
template = int(sys.argv[4])
html = sys.argv[5]
if html == "True":
    html = True
elif html == "False":
    html = False


# ESECUZIONE COMPONENTE MAPPER

profile = mapping_profilo(id_film_piaciuti)
recommendation = mapping_profilo(id_film_raccomandati)


# ESECUZIONE COMPONENTE BUILDER

G, common_properties = costruisci_grafo(profile, recommendation)
visualizza_grafo(G)


# ESECUZIONE COMPONENTE RANKER

sorted_prop = ranking_proprieta(G, common_properties, profile, recommendation)
print("\nEcco le proprietà in comune dei film in ordine decrescente per influenza:\n")
for key, value in sorted_prop.items():
    print(key, value)
print("\n\n")


# ESECUZIONE COMPONENTE GENERATOR

NewPreGenArchitecture = inizializzaNewPreGenArchitecture(G, sorted_prop, profile, recommendation)
explanation = generate_explanation(NewPreGenArchitecture, recommendation, profile, scelta_configurazione, template, html)
print(explanation)
