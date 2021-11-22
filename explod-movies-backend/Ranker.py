from Mapper import get_property_movies


# Funzione che prende in input la proprietà e ritorna il rispettivo punteggio IDF preso dal file
# di mapping degli IDF di ogni proprietà precedentemente creato
def calcola_IDF(prop):
    IDF = ''
    with open("list_idf_prop_movies", 'r') as f:    # scorre il file riga per riga
        for line in f:
            line = line.rstrip().split('\t')
            if prop == line[0]:                     # quando trova la proprietà restituisce il rispettivo IDF
                IDF = line[1]
                IDF = float(IDF)
                break
    return IDF


# Funzione che prende in input il grafo costruito, le proprietà in comune, i due dizionari di film piaciuti e
# raccomandati e il numero di proprietà da considerare ed effettua il ranking delle proprietà in comune in ordine di
# influenza attraverso il calcolo di un punteggio (in ordine decrescente)
def ranking_proprieta(G, proprietà_comuni, item_piaciuti, item_raccom, numero_prop_considerate):
    alfa = 0.5
    beta = 0.5
    score_prop = {}

    for prop in proprietà_comuni:                    # per ogni proprietà in comune, calcolo il numero di archi entranti
        if prop in G.nodes():                        # ed uscenti e li uso nella formula, insieme al rispettivo IDF
            num_in_edges = G.in_degree(prop)         # per calcolare il punteggio
            num_out_edges = G.out_degree(prop)
            score_prop[prop] = ((alfa * num_in_edges / len(item_piaciuti)) + (beta * num_out_edges / len(item_raccom))) * calcola_IDF(prop)

    sorted_values = sorted(score_prop.values())      # ordino la lista di punteggi in ordine decrescente in modo da
    sorted_values.reverse()                          # avere per prime le proprietà con più rilevanza
    sorted_prop = {}
    for i in sorted_values:
        for k in score_prop.keys():
            if score_prop[k] == i:
                sorted_prop[k] = score_prop[k]
                break
        if len(sorted_prop) == numero_prop_considerate:          # quando ho raggiunto il numero di proprietà da
            break                                                # considerare mi fermo

    print("\nLe proprietà sono state rankate e ordinate con successo!\n")

    return sorted_prop


# Funzione che prende in input il grafo creato, le proprietà rankate da considerare, i due dizionari dei film piaciuti
# e raccomandati e inizializza la struttura dati che sarà data in input alla funzione che genera la spiegazione
# partendo da questi dati
def inizializzaNewPreGenArchitecture(G, score_IDF, profile, recommendation):
    NewPreGenArchitecture = []
    profile_prov = get_property_movies(profile)                       # prendo le proprietà dei film piaciuti
    recommendations_prov = get_property_movies(recommendation)        # prendo le proprietà dei film raccomandati
    profile = []
    recommendations = []
    for line in profile_prov:
        profile.append(line[0])

    for line in recommendations_prov:
        recommendations.append(line[0])

    for proprieta, score in score_IDF.items():                        # per ogni proprietà in comune considerata
        prop = proprieta
        opposite_nodes = estraiNodiOpposti_item_prop(G, prop)         # estraggo i nodi opposti alla proprietà (film)
        profile_nodes = []
        recomm_nodes = []
        for current in opposite_nodes:
            if current in profile and current not in profile_nodes:       # se il film piaciuto non è stato già inserito
                profile_nodes.append(current)                                 # lo inserisco
            elif current in recommendations and current not in recomm_nodes:
                recomm_nodes.append(current)                                  # faccio lo stesso per i film raccomandati

        if len(profile_nodes) != 0 and len(recomm_nodes) != 0:     # aggiungo alla struttura dati creata gli item
            NewPreGenArchitecture.append(str(recomm_nodes) + "\t" + prop + "\t" + str(profile_nodes))

    return NewPreGenArchitecture


# Funzione che prende in input il grafo creato e una proprietà ed estrae i nodi opposti alla proprietà
def estraiNodiOpposti_item_prop(G, item):
    lista_item_prop = []
    map_prop = {}
    archi_item_user_prop_in = G.in_edges(item)                        # calcola archi entranti nella proprietà
    for archi_itemURI_user_prop_in in archi_item_user_prop_in:
        nodo_prop_in = archi_itemURI_user_prop_in[0]                  # prende il nodo opposto
        map_prop[nodo_prop_in] = ""

    archi_item_user_prop_out = G.out_edges(item)                      # calcola archi uscenti dalla proprietà
    for archi_itemURI_user_prop_out in archi_item_user_prop_out:
        nodo_prop_out = archi_itemURI_user_prop_out[1]                # prende il nodo opposto
        map_prop[nodo_prop_out] = ""

    for prop, n in map_prop.items():
        lista_item_prop.append(prop)

    return lista_item_prop