from Mapper import get_property_movies


def calcola_IDF(prop):
    IDF = ''
    with open("list_idf_prop_movies", 'r') as f:
        for line in f:
            line = line.rstrip().split('\t')
            if prop == line[0]:
                IDF = line[1]
                IDF = float(IDF)
                break
    return IDF


def ranking_proprieta(G, proprietà_comuni, item_piaciuti, item_raccom):
    alfa = 0.5
    beta = 0.5
    score_prop = {}

    for prop in proprietà_comuni:
        if prop in G.nodes():
            num_in_edges = G.in_degree(prop)
            num_out_edges = G.out_degree(prop)
            score_prop[prop] = ((alfa * num_in_edges / len(item_piaciuti)) + (beta * num_out_edges / len(item_raccom))) * calcola_IDF(prop)

    sorted_values = sorted(score_prop.values())
    sorted_values.reverse()
    sorted_prop = {}
    for i in sorted_values:
        for k in score_prop.keys():
            if score_prop[k] == i:
                sorted_prop[k] = score_prop[k]
                break

    return sorted_prop


def inizializzaNewPreGenArchitecture(G, score_IDF, profile, recommendation):
    NewPreGenArchitecture = []
    profile_prov = get_property_movies(profile)
    recommendations_prov = get_property_movies(recommendation)
    profile = []
    recommendations = []
    for line in profile_prov:
        profile.append(line[0])

    for line in recommendations_prov:
        recommendations.append(line[0])

    for proprieta, score in score_IDF.items():
        prop = proprieta
        opposite_nodes = estraiNodiOpposti_item_prop(G, prop)
        profile_nodes = []
        recomm_nodes = []
        for current in opposite_nodes:
            if current in profile and current not in profile_nodes:
                profile_nodes.append(current)
            elif current in recommendations and current not in recomm_nodes:
                recomm_nodes.append(current)

        if len(profile_nodes) != 0 and len(recomm_nodes) != 0:
            NewPreGenArchitecture.append(str(recomm_nodes) + "\t" + prop + "\t" + str(profile_nodes))

    return NewPreGenArchitecture


def estraiNodiOpposti_item_prop(G, item):
    lista_item_prop = []
    map_prop = {}
    archi_item_user_prop_in = G.in_edges(item)
    for archi_itemURI_user_prop_in in archi_item_user_prop_in:
        nodo_prop_in = archi_itemURI_user_prop_in[0]
        map_prop[nodo_prop_in] = ""

    archi_item_user_prop_out = G.out_edges(item)
    for archi_itemURI_user_prop_out in archi_item_user_prop_out:
        nodo_prop_out = archi_itemURI_user_prop_out[1]
        map_prop[nodo_prop_out] = ""

    for prop, n in map_prop.items():
        lista_item_prop.append(prop)

    return lista_item_prop