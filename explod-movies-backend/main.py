from Mapper import *
from Builder import *
from Ranker import *
from Generator import *
import sys

# CODICE PER ESEGUIRE IL FRAMEWORK DA RIGA DI COMANDO

#id_film_p1 = sys.argv[1]
#id_film_r1 = sys.argv[2]

#spielberg-lucas
#id_film_p1 = ['I:14234',"I:80136","I:9221","I:8586","I:10402","I:16","I:11570","I:6027","I:8652","I:331","I:18462","I:9949","I:21168","I:36141","I:8396","I:48867","I:5749"]
#id_film_r1 =  ["I:8589","I:8942","I:656","I:1659","I:8889"]

# film random
"""id_film_p1 =["I:20517","I:67531","I:55608","I:64081","I:27301","I:2310","I:12110","I:12021","I:25015","I:75171",
                    "I:10013","I:14680","I:831","I:37789","I:15681","I:12050","I:30189","I:36498","I:6454","I:1889",
                    "I:69532","I:3419","I:39921","I:24048","I:336","I:68098","I:49348","I:164","I:1243","I:65101",
                    "I:48178","I:50495","I:11860","I:32697","I:49175","I:61508","I:54599","I:3874","I:64321","I:75454",
                    "I:71354","I:59497","I:7991","I:507092","I:71292","I:35340","I:26013","I:62529","I:116",
                    "I:13909","I:41444","I:8207","I:5189","I:55360"]"""
#id_film_r1 = ["I:1500","I:9643","I:1030","I:24918","I:32576","I:62627"]

#film connery
id_film_p1 = ['I:19077', 'I:11193', 'I:13481', 'I:21067', 'I:8400', 'I:11238', 'I:20958', 'I:20188', 'I:515', 'I:17737', 'I:20737', 'I:32316', 'I:9434', 'I:16690', 'I:17279']
id_film_r1 = ['I:8981', 'I:62528', 'I:19099', 'I:8984']

#film spielberg-lucas-connery
#id_film_r1 = ['I:8400','I:21067','I:20188','I:19099','I:80136','I:8981','I:11570']
#id_film_p1 = ['I:331','I:1659','I:10402','I:8586','I:8589','I:18462','I:16','I:11238','I:9949','I:16690','I:8652','I:21168','I:8889','I:62528']

#film Domenico
#id_film_p1 = ['I:8493','I:11188','I:8439','I:41763','I:11033','I:8457','I:1500','I:55352','I:42922','I:8414']
#id_film_r1 = ['I:12635','I:51243','I:67331','I:4451','I:67270','I:51230','I:12524']


graph = "False"
    #sys.argv[3]
numero_prop_considerate = 20
    #int(sys.argv[4])
idf = "True"
    #sys.argv[5]
scelta_configurazione = sys.argv[6]
template = int(sys.argv[7])
html = sys.argv[8]

#id_film_p1.replace("" ,'')
#if "[" not in id_film_p1 or "]" not in id_film_p1 or " " in id_film_p1 or "[" not in id_film_r1 or "]" not in id_film_r1 or " " in id_film_r1:
    #print("\nI dati inseriti non sono corretti!\nAssicurarsi di aver inserito gli id tra parentesi quadre e senza lasciare spazi.")
#el
if (graph != "True" and graph != "False") or (idf != "True" and idf != "False") or (html != "True" and html != "False"):
    print("\nI dati inseriti non sono corretti!\nAssicurarsi di aver scelto True o False per la visualizzazione del grafo, il ranking con o senza IDF e l'utilizzo dei tag HTML.")
elif scelta_configurazione != "baseline" and scelta_configurazione != "schema" and scelta_configurazione != "primolivello":
    print("\nI dati inseriti non sono corretti!\nAssicurarsi di aver inserito una tipologia di spiegazione tra quelle previste (baseline, schema, primolivello).")
else:
    #id_film_piaciuti = id_film_p1[1:-1].split(',')
    #id_film_raccomandati = id_film_r1[1:-1].split(',')
    id_film_piaciuti = id_film_p1
    id_film_raccomandati = id_film_r1
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
    print("\n")


    # ESECUZIONE COMPONENTE RANKER
    #print("\nEsecuzione componente Ranker NO-idf...\n")
    #ranked_prop = ranking_proprieta(G, common_properties, profile, recommendation, idf=False)
    #sorted_prop = proprieta_da_considerare(ranked_prop, numero_prop_considerate)
    #stampa_proprieta(sorted_prop)
    print("\nEsecuzione componente Ranker con IDF...\n")
    ranked_prop_idf = ranking_proprieta(G, common_properties, profile, recommendation, idf=True)
    sorted_prop_idf = proprieta_da_considerare(ranked_prop_idf, numero_prop_considerate)
    stampa_proprieta(sorted_prop_idf)

    # ESECUZIONE COMPONENTE GENERATOR
    #print("\nEsecuzione componente Generator  NO-idf...\n")
    #triple_structure = build_triple_structure(G, sorted_prop, profile, recommendation)
    #explanation = generate_explanation(triple_structure, recommendation, profile, scelta_configurazione, template, html)
    #print(explanation)
    print("\nEsecuzione componente Generator CON IDF...\n")
    triple_structure = build_triple_structure(G, sorted_prop_idf, profile, recommendation)
    explanation = generate_explanation(triple_structure, recommendation, profile, scelta_configurazione, template, html)
    print(explanation)

