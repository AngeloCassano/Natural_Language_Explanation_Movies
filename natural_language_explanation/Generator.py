import random
from Mapper import get_property_movies

item_spiegati = 0
used_verboIniziale = {}
used_avverbio = {}
used_avverbioFinale = {}
used_verboIniziale2 = {}
used_incipitRacc = {}


def generate_explanation(NewPreGenArchitecture, item_raccom, profile, scelta_configurazione, template, html):
    explanation = ""

    if scelta_configurazione == "baseline":
        if len(item_raccom) == 1:
            simple_explanation = "I suggest this movie because many people like it and it's very popular."
        else:
            simple_explanation = "I suggest these movies because many people like them and they are very popular."
        explanation = simple_explanation

    elif scelta_configurazione == "schema":
        schema_explanation = ""
        if len(item_raccom) == 1:
            value = item_raccom.values()
            schema_explanation = get_descrizione_film(value[0], item_raccom)
        else:
            for key, value in item_raccom.items():
                schema_explanation += get_descrizione_film(value, item_raccom)
                schema_explanation += "\n\n"
        explanation = schema_explanation

    elif scelta_configurazione == "primolivello":
        if len(item_raccom) == 1:
            if len(NewPreGenArchitecture) > 0:
                NewPreGenArchitecture = optimize_new_architecture(NewPreGenArchitecture, item_raccom, 15)
        elif len(NewPreGenArchitecture) > 0:
            NewPreGenArchitecture = optimize_new_architecture_groups(NewPreGenArchitecture, item_raccom)

        explanation = get_explanation_primo_livello(template, item_raccom, NewPreGenArchitecture, profile, html)

    return explanation


def get_descrizione_film(item_raccomandato, recommendation):
    explanation = ""
    property_movies = get_property_movies(recommendation)
    property_item = []
    subject_prop = []
    subject_prop_provv = {}
    for line in property_movies:
        if item_raccomandato == line[0]:
            property_item.append(line)

    if len(property_item) > 0:
        explanation += "Info: " + pulisci_uri_item(item_raccomandato) + "\n\n"
        for prop_corrente in property_item:
            subject = prop_corrente[1]
            subject = pulisci_subject(subject)
            if subject != "rdf-schema#seeAlso" and subject != "openingFilm" and subject != "soundRecording" and subject != "subject" and subject != "film" and subject != "closingFilm" and subject != "owl#differentFrom" and subject != "releaseLocation":
                prop_corrente_pulita = pulisci_uri_prop(prop_corrente[2])
                list = [subject, prop_corrente_pulita]
                subject_prop.append(list)
                subject_prop_provv[subject] = prop_corrente_pulita

        for key, value in subject_prop_provv.items():
            prop_subject = []
            for items in subject_prop:
                if key == items[0]:
                    prop_subject.append(items[1])
            prop_with_subject = ""
            for propCorrente in prop_subject:
                prop_with_subject += propCorrente + ", "
            prop_with_subject += "."
            prop_with_subject = prop_with_subject.replace(", .", ";\n")

            explanation += "- " + key + ": " + prop_with_subject

    explanation = pulisci_explanation(explanation)

    return explanation


def optimize_new_architecture(NewPreGenArchitecture, item_raccom, numero_prop):
    new_architecture_cleaned_all = []
    for current in NewPreGenArchitecture:
        current = current.replace("['", "")
        current = current.replace("']", "")
        new_architecture_cleaned_all.append(current)

    new_architecture_cleaned = []
    for s in new_architecture_cleaned_all:
        splitted = s.split('\t')
        items_racc = splitted[0].split(', ')
        for i in items_racc:
            for name, uri in item_raccom.items():
                if i == uri:
                    new_architecture_cleaned.append(i + "\t" + splitted[1] + "\t" + splitted[2])

    new_architecture_cleaned_2 = []
    if len(new_architecture_cleaned) > 0:
        considered_items = []
        limit = numero_prop
        list_prop_cons = []
        list_prop_cons.append(new_architecture_cleaned[0])
        if limit >= len(new_architecture_cleaned):
            limit = len(new_architecture_cleaned)
        if len(new_architecture_cleaned) > 1:
            for i in range(1, limit):
                add = True
                splitline = new_architecture_cleaned[i].split('\t')
                current_property = splitline[1]
                current_property = pulisci_property(current_property)
                for j in range(i):
                    splitlineJ = new_architecture_cleaned[j].split('\t')
                    old_property = splitlineJ[1]
                    old_property = pulisci_property(old_property)
                    if current_property == old_property:
                        add = False
                if add:
                    list_prop_cons.append(new_architecture_cleaned[i])
                elif limit < len(new_architecture_cleaned):
                    limit = limit + 1
        for k in range(len(list_prop_cons)):
            splitlineI = list_prop_cons[k].split('\t')
            recI = splitlineI[0]
            properties = splitlineI[1]
            profI = splitlineI[2]
            for j in range(k + 1, len(list_prop_cons)):
                splitlineK = list_prop_cons[j].split('\t')
                recK = splitlineK[0]
                properties1 = splitlineK[1]
                profK = splitlineK[2]
                if recI == recK and profI == profK and profI not in considered_items:
                    properties += "-and-" + properties1
            if profI not in considered_items:
                considered_items.append(profI)
                profI_pulito = ""
                prof_splitted = profI.split(', ')
                for z in range(len(prof_splitted)):
                    profI_pulito += pulisci_uri_item(prof_splitted[z]) + ", "
                profI_pulito = profI_pulito[0:-2]
                new_architecture_cleaned_2.append(pulisci_uri_item(recI) + "\t" + properties + "\t" + profI_pulito)

    NewPreGenArchitecture = new_architecture_cleaned_2

    return NewPreGenArchitecture


def optimize_new_architecture_groups(NewPreGenArchitecture,item_raccom):
    new_architecture_cleaned = []
    for current in NewPreGenArchitecture:
        current = current.replace("['", "")
        current = current.replace("']", "")
        new_architecture_cleaned.append(current)

    new_architecture_cleaned_2 = []
    considered_items = []
    limit = len(item_raccom)
    list_prop_cons = []
    covered_items = []
    if limit >= len(NewPreGenArchitecture):
        limit = len(NewPreGenArchitecture)
    i = 0
    while i < limit:
        splitline = new_architecture_cleaned[i].split('\t')
        movies = splitline[0].split(', ')
        add = False
        found = []
        for j in range(len(movies)):
            if movies[j] in covered_items:
                found.insert(j, False)
            else:
                found.insert(j, True)
                covered_items.append(movies[j])

        items = ""
        for s in range(len(found)):
            if found[s] == True:
                add = True
                items += movies[s] + ", "

        if len(items) != 0:
            items = items[0:-2]
        if add:
            list_prop_cons.append(items + "\t" + splitline[1] + "\t" + splitline[2])
        elif limit < len(NewPreGenArchitecture):
            limit = limit + 1
        i = i + 1

    for i in range(len(list_prop_cons)):
        splitlineI = list_prop_cons[i].split('\t')
        recI = splitlineI[0]
        properties = splitlineI[1]
        profI = splitlineI[2]
        for m in range(i + 1, len(list_prop_cons)):
            splitlineJ = list_prop_cons[m].split('\t')
            recJ = splitlineJ[0]
            properties1 = splitlineJ[1]
            profJ = splitlineJ[2]
            if profI == profJ and profI not in considered_items and recI == recJ:
                properties += "-and-" + properties1
        if profI not in considered_items:
            considered_items.append(profI)
        profI_pulito = ""
        prof_splitted = profI.split(', ')
        for n in range(len(prof_splitted)):
            profI_pulito += pulisci_uri_item(prof_splitted[n]) + ", "
        profI_pulito = profI_pulito[0:-2]
        recI_pulito = ""
        rec_splitted = recI.split(', ')
        for p in range(len(rec_splitted)):
            recI_pulito += pulisci_uri_item(rec_splitted[p]) + ", "
        recI_pulito = recI_pulito[0:-2]
        new_architecture_cleaned_2.append(recI_pulito + "\t" + properties + "\t" + profI_pulito)

    NewPreGenArchitecture = new_architecture_cleaned_2

    return NewPreGenArchitecture


def get_explanation_primo_livello(template, item_raccom, NewPreGenArchitecture, profile, html):
    natural_language_explanation = ""
    global item_spiegati

    if template == 1:
        if len(item_raccom) == 1:
            if len(NewPreGenArchitecture) > 0:
                natural_language_explanation = verboIniziale_getRandom() + " " + get_item_raccomandato(NewPreGenArchitecture, 0, html) + " because " + get_frasi(NewPreGenArchitecture, profile, html)
                natural_language_explanation = natural_language_explanation.replace("_", " ")
                while "  " in natural_language_explanation:
                    natural_language_explanation = natural_language_explanation.replace("  ", " ")
            else:
                natural_language_explanation = "Your preferences are really particular! Sorry, but I can't still explain why you received such a recommendation."

        else:
            if len(NewPreGenArchitecture) > 0:
                for i in range(len(NewPreGenArchitecture)):
                    natural_language_explanation += verboIniziale_getRandom() + " " + get_item_raccomandato(NewPreGenArchitecture, i, html) + " because " + get_group_frasi(NewPreGenArchitecture, i, profile, html)
                natural_language_explanation = natural_language_explanation.replace("_", " ")
                while "  " in natural_language_explanation:
                    natural_language_explanation = natural_language_explanation.replace("  ", " ")

                if item_spiegati != 0 and item_spiegati < 5:
                    natural_language_explanation += "\nThe other recommendations are really particular, I can't still explain why you received them."
            else:
                natural_language_explanation = "Your preferences are really particular! Sorry, but I can't still explain why you received such a recommendation."

    elif template == 2:
        if len(item_raccom) == 1:
            if len(NewPreGenArchitecture) > 0:
                natural_language_explanation = verboIniziale2_getRandom() + " " + get_frasi(NewPreGenArchitecture, profile, html) + " "
                frasi_raccomandazione = incipitRacc_getRandom()
                if "So_why_don$t_you" not in frasi_raccomandazione:
                    natural_language_explanation += frasi_raccomandazione + " watch " + get_item_raccomandato(NewPreGenArchitecture, 0, html)
                else:
                    natural_language_explanation += frasi_raccomandazione + " watch " + get_item_raccomandato(NewPreGenArchitecture, 0, html) + " ?"

                natural_language_explanation = natural_language_explanation.replace("_", " ")
                natural_language_explanation = natural_language_explanation.replace("  ", " ")
                natural_language_explanation = natural_language_explanation.replace("$", "\'")
                while "  " in natural_language_explanation:
                    natural_language_explanation = natural_language_explanation.replace("  ", " ")
                if not natural_language_explanation.endswith(".") and not natural_language_explanation.endswith("?"):
                    natural_language_explanation += "."
            else:
                natural_language_explanation = "Your preferences are really particular! Sorry, but I can't still explain why you received such a recommendation."

        else:
            if len(NewPreGenArchitecture) > 0:
                for n in range(len(NewPreGenArchitecture)):
                    if n + 1 < len(NewPreGenArchitecture) and n != 0:
                        natural_language_explanation += get_avverbio(NewPreGenArchitecture) + " " + verboIniziale2_getRandom() + " " + get_group_frasi_2(NewPreGenArchitecture, n, profile, html) + ". "
                    elif n < len(NewPreGenArchitecture) and n != 0:
                        natural_language_explanation += get_avverbio_finale(NewPreGenArchitecture) + " " + verboIniziale2_getRandom() + " " + get_group_frasi_2(NewPreGenArchitecture, n, profile, html) + ". "
                    else:
                        natural_language_explanation += verboIniziale2_getRandom() + " " + get_group_frasi_2(NewPreGenArchitecture, n, profile, html) + ". "

                    frasi_raccomandazione = incipitRacc_getRandom()
                    if "So_why_don$t_you" not in frasi_raccomandazione:
                        natural_language_explanation += "\n" + frasi_raccomandazione + " watch " + get_item_raccomandato(NewPreGenArchitecture, n, html) + ".\n"
                    else:
                        natural_language_explanation += "\n" + frasi_raccomandazione + " watch " + get_item_raccomandato(NewPreGenArchitecture, n, html) + "?\n"

                natural_language_explanation = natural_language_explanation.replace("_", " ")
                natural_language_explanation = natural_language_explanation.replace("$", "\'")
                while "  " in natural_language_explanation:
                    natural_language_explanation = natural_language_explanation.replace("  ", " ")
                if item_spiegati != 0 and item_spiegati < 5:
                    natural_language_explanation += "\nThe other recommendations are really particular, I can't still explain why you received them."
            else:
                natural_language_explanation = "Your preferences are really particular! Sorry, but I can't still explain why you received such a recommendation."

    return natural_language_explanation


def pulisci_uri_item(item_corrente):
    item_corrente = item_corrente.replace("http://dbpedia.org/resource/", "")
    item_corrente = item_corrente.replace("/", " ")

    item_pulito = ""
    splitted = item_corrente.split("_")
    for x in range(len(splitted)):
        if not splitted[x].startswith("(") and not splitted[x].endswith(")"):
            item_pulito += splitted[x] + " "

    item_pulito += "."
    item_pulito = item_pulito.replace(" .", "")

    return item_pulito


def pulisci_subject(subject):
    subject = subject.replace("http://dbpedia.org/ontology/", "")
    subject = subject.replace("http://purl.org/dc/terms/", "")
    subject = subject.replace("http://www.w3.org/2002/07/", "")
    subject = subject.replace("http://www.w3.org/2000/01/", "")

    return subject


def pulisci_uri_prop(prop_corrente):
    prop_corrente = prop_corrente.replace("http://dbpedia.org/resource/Category:", "")
    prop_corrente = prop_corrente.replace("http://dbpedia.org/resource/", "")

    prop_pulita = ""
    splitted = prop_corrente.split("_")
    for x in range(len(splitted)):
        if not splitted[x].startswith("(") and not splitted[x].endswith(")"):
            prop_pulita += splitted[x] + " "

    prop_pulita += "."
    prop_pulita = prop_pulita.replace(" .", "")

    return prop_pulita


def pulisci_explanation(explanation):
    explanation = explanation.replace(", ;", ";")
    explanation = explanation.replace(", .", ".")
    explanation = explanation.replace("; .", ".")
    explanation = explanation.replace(" and .", ".")
    explanation = explanation.replace(" as   _", " ")
    explanation = explanation.replace("_", " ")
    explanation = explanation.replace("@", " ")
    explanation = explanation.replace("  ", "")
    explanation = explanation.replace("and you like also movies .", ".")
    explanation = explanation.replace(" as and", " and")
    explanation = explanation.replace(", .", ".")
    explanation = explanation.replace(" as .", ".")
    explanation = explanation.replace("movies Films", " Films")
    explanation = explanation.replace("movies Film", " Films")
    explanation = explanation.replace("alsoFilms", "also Films")

    return explanation


def pulisci_property(property):
    property = property.replace("http://dbpedia.org/resource/Category:Films_based_on_works_by_", "")
    property = property.replace("http://dbpedia.org/resource/Category:Films_directed_by_", "")
    property = property.replace("http://dbpedia.org/resource/Category:Screenplays_by_", "")
    property = property.replace("http://dbpedia.org/resource/Category:Film_scores_by_", "")
    property = property.replace("http://dbpedia.org/resource/Category:Films_produced_by_", "")
    property = property.replace("http://dbpedia.org/resource/Category:Compositions_by_", "")
    property = property.replace("http://dbpedia.org/resource/Category:Works_by_", "")
    property = property.replace("http://dbpedia.org/resource/Category:Plays_by_", "")
    property = property.replace("http://dbpedia.org/resource/Category:", "")
    property = property.replace("http://dbpedia.org/resource/Template:", "")
    property = property.replace("http://dbpedia.org/resource/", "")

    return property


def verboIniziale_getRandom():
    verbo_iniziale = ["I_suggest_you", "I_propose_you", "I_recommend_you"]
    global used_verboIniziale
    if len(used_verboIniziale) == len(verbo_iniziale):
        used_verboIniziale.clear()

    verbo = random.choice(verbo_iniziale)
    while verbo in used_verboIniziale.keys():
        verbo = random.choice(verbo_iniziale)

    used_verboIniziale[verbo] = ""
    return verbo


def avverbio_getRandom():
    avverbio = ["Furthermore", "In_addition", "Besides", "Next", "Moreover"]
    global used_avverbio
    if len(used_avverbio) == len(avverbio):
        used_avverbio.clear()

    avv = random.choice(avverbio)
    while avv in used_avverbio.keys():
        avv = random.choice(avverbio)

    used_avverbio[avv] = ""
    return avv


def avverbioFinale_getRandom():
    avverbio_finale = ["Finally", "At_last", "Lastly"]
    global used_avverbioFinale
    if len(used_avverbioFinale) == len(avverbio_finale):
        used_avverbioFinale.clear()

    avv = random.choice(avverbio_finale)
    while avv in used_avverbioFinale.keys():
        avv = random.choice(avverbio_finale)

    used_avverbioFinale[avv] = ""
    return avv


def get_item_raccomandato(NewPreGenArchitecture, i, html):
    items = NewPreGenArchitecture[i].split('\t')[0].split(', ')
    item = ""
    global item_spiegati
    if html:
        if len(items) == 1:
            item = "<b>" + items[0] + "</b>"
            item_spiegati = item_spiegati + 1
        elif len(items) == 2:
            item += "<b>" + items[0] + "</b> and <b>" + items[1] + "</b>"
            item_spiegati = item_spiegati + 2
        else:
            for z in range(len(items) - 2):
                item += "<b>" + items[z] + "</b>, "
                item_spiegati = item_spiegati + 1
            item += "<b>" + items[len(items) - 2] + "</b> and <b>" + items[len(items) - 1] + "</b>"
            item_spiegati = item_spiegati + 2
    else:
        if len(items) == 1:
            item = items[0]
            item_spiegati = item_spiegati + 1
        elif len(items) == 2:
            item += items[0] + "and" + items[1]
            item_spiegati = item_spiegati + 2
        else:
            for z in range(len(items) - 2):
                item += items[z] + ", "
                item_spiegati = item_spiegati + 1
            item += items[len(items) - 2] + "and" + items[len(items) - 1]
            item_spiegati = item_spiegati + 2

    return item


def verboIniziale2_getRandom():
    verbo_iniziale_2 = ["I_note", "It_seems", "I_see"]
    global used_verboIniziale2
    if len(used_verboIniziale2) == len(verbo_iniziale_2):
        used_verboIniziale2.clear()

    verbo = random.choice(verbo_iniziale_2)
    while verbo in used_verboIniziale2.keys():
        verbo = random.choice(verbo_iniziale_2)

    used_verboIniziale2[verbo] = ""
    return verbo


def incipitRacc_getRandom():
    incipit_racc = ["So_I_suggest_you_to", "Thus_I_suggest_you_to", "This_is_why_I_suggest_you_to", "So_I_recommend_you_to", "So_I_think_you_should", "This_is_why_you_should", "Thus_you_should", "This_is_why_I_recommend_you_to", "This_is_why_I_think_you_should", "So_why_don$t_you", "Thus_it_could_be_that_you_like_to"]
    global used_incipitRacc
    if len(used_incipitRacc) == len(incipit_racc):
        used_incipitRacc.clear()

    incipit = random.choice(incipit_racc)
    while incipit in used_incipitRacc.keys():
        incipit = random.choice(incipit_racc)

    used_incipitRacc[incipit] = ""
    return incipit


def get_frasi(NewPreGenArchitecture, profile, html):
    frasi = ""
    for i in range(len(NewPreGenArchitecture)):
        frasi += costruisci_frase(NewPreGenArchitecture, i, profile, html)

    return frasi


def get_group_frasi(NewPreGenArchitecture, i, profile, html):
    return costruisci_frase(NewPreGenArchitecture, i, profile, html)


def costruisci_frase(NewPreGenArchitecture, i, profile, html):
    frase = ""
    if i + 2 < len(NewPreGenArchitecture):
        frase += "you " + get_avverbio_gradimento(NewPreGenArchitecture, i, profile) + "like " + get_lista_proprieta(NewPreGenArchitecture, i, html) + ".\n " + get_avverbio(NewPreGenArchitecture)
    elif i + 1 < len(NewPreGenArchitecture):
        frase += "you " + get_avverbio_gradimento(NewPreGenArchitecture, i, profile) + "like " + get_lista_proprieta(NewPreGenArchitecture, i, html) + ".\n " + get_avverbio_finale(NewPreGenArchitecture)
    else:
        frase += "you " + get_avverbio_gradimento(NewPreGenArchitecture, i, profile) + "like " + get_lista_proprieta(NewPreGenArchitecture, i, html) + ".\n "

    return frase


def get_group_frasi_2(NewPreGenArchitecture, i, profile, html):
    return costruisci_frase_2(NewPreGenArchitecture, i, profile, html)


def costruisci_frase_2(NewPreGenArchitecture, i, profile, html):
    frase = ""
    frase += "you " + get_avverbio_gradimento(NewPreGenArchitecture, i, profile) + "like " + get_lista_proprieta(NewPreGenArchitecture, i, html)

    return frase


def get_lista_proprieta(NewPreGenArchitecture, i, html):
    splitted = NewPreGenArchitecture[i].split('\t')
    properties = splitted[1].split('-and-')
    lista_proprieta = ""
    domain = "movies"

    for j in range(len(properties)):
        natural_language_property = get_subject_prop(properties[j]).replace("_", "") + " "
        if "ovie" in natural_language_property or "film" in natural_language_property or "Film" in natural_language_property or "films" in natural_language_property or "creenplay" in natural_language_property or "franchise" in natural_language_property or "serie" in natural_language_property:
            domain = ""
        natural_language_property = domain + " " + natural_language_property

        if html:
            if len(natural_language_property) > 0:
                lista_proprieta += "<i>" + natural_language_property[0:-1] + "</i>"
            if j + 2 < len(properties):
                lista_proprieta += ", "
            elif j + 1 < len(properties):
                lista_proprieta += " and "
        else:
            if len(natural_language_property) > 0:
                lista_proprieta += natural_language_property[0:-1]
            if j + 2 < len(properties):
                lista_proprieta += ", "
            elif j + 1 < len(properties):
                lista_proprieta += " and "

    lista_film = splitted[2].split(',')
    films = ""
    if html:
        if len(lista_film) == 1:
            films += "<b>" + lista_film[0] + "</b>"
        elif len(lista_film) == 2:
            films += "<b>" + lista_film[0] + "</b> and <b>" + lista_film[1] + "</b>"
        else:
            for z in range(len(lista_film) - 2):
                films += "<b>" + lista_film[z] + "</b>, "
            films += "<b>" + lista_film[len(lista_film) - 2] + "</b> and <b>" + lista_film[len(lista_film) - 1] + "</b>"
    else:
        if len(lista_film) == 1:
            films += lista_film[0]
        elif len(lista_film) == 2:
            films += lista_film[0] + " and " + lista_film[1]
        else:
            for x in range(len(lista_film) - 2):
                films += lista_film[x] + ", "
            films += lista_film[len(lista_film) - 2] + " and " + lista_film[len(lista_film) - 1]
    lista_proprieta += ", "

    return lista_proprieta + "as " + films


def get_quantificatore(property, movies_user_rated):
    movies_with_prop_only_one = {}
    property_movies = []
    with open('movies_stored_prop.mapping', 'r') as f:
        for line in f:
            line = line.rstrip().split('\t')
            property_movies.append(line)
    for line in property_movies:
        if property == line[2]:
            movies_with_prop_only_one[line[0]] = ""

    film_with_property = 0
    for movie_curr in movies_with_prop_only_one.keys():
        for key, value in movies_user_rated.items():
            if movie_curr == value:
                film_with_property = film_with_property + 1

    score = film_with_property / len(movies_user_rated)
    if score == 1.0:
        quantificatore = "always "
    elif score < 1.0 and score >= 0.6:
        quantificatore = "often "
    elif score < 0.6 and score >= 0.3:
        quantificatore = "sometimes "
    else:
        quantificatore = " "

    return  quantificatore


def get_avverbio_gradimento(NewPreGenArchitecture, i, profile):
    property = NewPreGenArchitecture[i].split('\t')[1].split('-and-')[0]
    return get_quantificatore(property, profile)


def get_avverbio(NewPreGenArchitecture):
    if len(NewPreGenArchitecture) == 1:
        return ""
    else:
        return "\n" + avverbio_getRandom() + ", "


def get_avverbio_finale(NewPreGenArchitecture):
    if len(NewPreGenArchitecture) == 1:
        return ""
    elif len(NewPreGenArchitecture) == 2:
        return "\n" + avverbio_getRandom() + ", "
    else:
        return "\n" + avverbioFinale_getRandom() + ", "


def carica_properties_item():
    properties_items = []
    with open('properties_subject_movies.mapping', 'r') as f:
        for line in f:
            line = line.split('\t')
            if len(line) == 2:
                splitline = [line[0], line[1]]
                properties_items.append(splitline)
            else:
                splitline = [line[0], "N.D."]
                properties_items.append(splitline)

    return properties_items


def carica_properties_text():
    predicate_text = []
    with open('subject_movies.mapping', 'r') as f:
        for line in f:
            line = line.split('\t')
            if len(line) == 2:
                splitline = [line[0], line[1]]
                predicate_text.append(splitline)
            else:
                splitline = [line[0], "N.D."]
                predicate_text.append(splitline)

    return predicate_text


def get_subject_prop(prop_corrente):
    properties_items = carica_properties_item()
    predicate_text = carica_properties_text()
    predicate = ""
    text = ""
    for items in properties_items:
        if prop_corrente == items[0]:
            predicate += items[1]
            break
    for elem in predicate_text:
        if predicate == elem[0]:
            text += elem[1]
            break
    prop_corrente = prop_corrente.replace("http://dbpedia.org/resource/Category:", "")
    prop_corrente = prop_corrente.replace("http://dbpedia.org/resource/Template:", "")
    prop_corrente = prop_corrente.replace("http://dbpedia.org/resource/", "")

    prop_pulita = ""
    splitted = prop_corrente.split('_')
    for i in range(len(splitted)):
        prop_pulita += splitted[i] + " "

    prop_pulita += "."
    prop_pulita = prop_pulita.replace(" .", "")
    prop_pulita = prop_pulita.replace("(director)", "")
    prop_pulita = prop_pulita.replace("(composer)", "")
    prop_pulita = prop_pulita.replace("(", "")
    prop_pulita = prop_pulita.replace(")", "")
    if text is None:
        text = ""
    prop_corrente1 = text + " " + prop_pulita

    return prop_corrente1
