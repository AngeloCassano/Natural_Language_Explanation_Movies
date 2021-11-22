# Funzione che legge il file di mapping dei film e crea due dizionari contenenti tutti i film mappati
# Il primo dizionario ha per chiave l'id e per valore il titolo
# Il secondo ha per chiave il titolo e per valore l'URI del film
def lettura_file(file_path):
    id_key_dictionary = {}
    name_key_dictionary = {}
    with open(file_path, 'r') as f:
        for line in f:
            if line == '\n':
                break
            else:
                line = line.split('\t')
                id_key_dictionary[line[0]] = line[1]
                name_key_dictionary[line[1]] = line[2]
    return id_key_dictionary, name_key_dictionary


# Funzione che prende in input una lista contenente id di film (piaciuti o raccomandati) e con i dizionari di mapping
# creati da lettura_file costruisce un dizionario avente per chiave il titolo dei film selezionati e per valore l'URI
def mapping_profilo(id_film):
    profile_prov = {}
    profile = {}
    id_key_dictionary, id_name_dictionary = lettura_file("list_items_movies.mapping")
    for key, value in id_key_dictionary.items():
        for item in id_film:
            if item == key:
                profile_prov[item] = value
    for key1, value1 in profile_prov.items():
        for key2, value2 in id_name_dictionary.items():
            if value1 == key2:
                profile[value1] = value2
    return profile


# Funzione che prende in input un dizionario di film e attraverso il confronto degli uri con le proprietà di ogni film
# all'interno del file di mapping seleziona e ritorna solo le proprietà dei film di interesse nel dizionario
def get_property_movies(item_raccom):
    property_movies = []
    property = []
    with open('movies_stored_prop.mapping', 'r') as f:
        for line in f:
            line = line.rstrip().split('\t')
            property_movies.append(line)

    for name, uri in item_raccom.items():
        for line in property_movies:
            if uri == line[0]:
                property.append(line)

    return property
