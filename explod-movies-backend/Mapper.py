import sys


# Funzione che legge il file di mapping dei film e crea due dizionari contenenti tutti i film mappati
# Il primo dizionario ha per chiave l'id e per valore il titolo
# Il secondo ha per chiave il titolo e per valore l'URI del film
def lettura_file(file_path):
    id_key_dictionary = {} #dizionario (k id, val titolo)
    name_key_dictionary = {} #dizionari (k titolo, val uri film)
    numero_film = 0
    with open(file_path, 'r') as f:
        for line in f:
            numero_film += 1
            if line == '\n':
                break
            else:
                line = line.split('\t')
                id_key_dictionary[line[0]] = line[1]
                name_key_dictionary[line[1]] = line[2]

    return id_key_dictionary, name_key_dictionary, numero_film


# Funzione che prende in input una lista contenente id di film (piaciuti o raccomandati) e con i dizionari di mapping
# creati da lettura_file costruisce un dizionario avente per chiave il titolo dei film selezionati e per valore l'URI
#INPUT: id_film insieme degli id dei film contenuti nel profile dell'utente, nel formato [I:<number>, I:<number>, ..., ecc]
def mapping_profilo(id_film):
    profile_prov = {} #dizionario profilo provvisorio
    profile = {}
    id_key_dictionary, id_name_dictionary, numero_film = lettura_file("list_items_movies.mapping")
    """for key, value in id_key_dictionary.items():
        for item in id_film:
            if item == key:
                profile_prov[item] = value
    for key1, value1 in profile_prov.items():
        for key2, value2 in id_name_dictionary.items():
            if value1 == key2:
                profile[value1] = value2"""
    for item in id_film:
        if item in id_key_dictionary.keys():
            profile_prov[item] = id_key_dictionary[item]
    for key, value in profile_prov.items():
        profile[value] = id_name_dictionary[value]


    return profile, numero_film

# Funzione che prende in input un dizionario di film e attraverso il confronto degli uri con le proprieta di ogni film
# all'interno del file di mapping seleziona e ritorna solo le proprieta dei film di interesse nel dizionario
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


def cmd_mapper(profilo, racc):
    if "[" not in sys.argv[2] or "]" not in sys.argv[2] or " " in sys.argv[2] or "[" not in sys.argv[3] or "]" not in sys.argv[3] or " " in sys.argv[3]:
        print("I dati inseriti non sono corretti!\nAssicurarsi di aver inserito gli id tra parentesi quadre e senza lasciare spazi.")
    else:
        print("\nEsecuzione componente Mapper...\n")
        profile, numero_film1 = mapping_profilo(profilo)
        recommendation, numero_film2 = mapping_profilo(racc)
        print("Numero totale di film mappati: ", numero_film1)
        print("\nMappatura del profilo utente realizzata:\n")
        for key, value in profile.items():
            print(key, "\t", value)
        print("\nMappatura delle raccomandazioni realizzata:\n")
        for key1, value1 in recommendation.items():
            print(key1, "\t", value1)


if __name__ == "__main__":
    globals()[sys.argv[1]](sys.argv[2][1:-1].split(','), sys.argv[3][1:-1].split(','))