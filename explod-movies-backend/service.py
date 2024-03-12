from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from Mapper import *
from Builder import *
from Ranker import *
from Generator import *

# CODICE PER ESEGUIRE IL FRAMEWORK COME API SU UN SERVER IN ASCOLTO DI RICHIESTE

app = Flask(__name__)
api = Api(app)


class Rec(Resource):
    def get(self):
        id_film_piaciuti = request.args.get('film_piaciuti')[1:-1].split(',')
        id_film_raccomandati = request.args.get('film_raccomandati')[1:-1].split(',')
        numero_prop_considerate = int(request.args.get('num_proprieta'))
        scelta_configurazione = request.args.get('tipo_spiegazione')
        template = int(request.args.get('template'))
        html = request.args.get('html')
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
        print("Numero di proprieta mappate: ", numero_proprieta)
        print("\nGrafo creato con successo!\n")
        print("Numero di nodi del grafo: ", G.number_of_nodes())
        print("Numero di archi del grafo: ", G.number_of_edges())
        print("\n")

        # ESECUZIONE COMPONENTE RANKER
        print("\nEsecuzione componente Ranker...\n")
        ranked_prop_idf = ranking_proprieta(G, common_properties, profile, recommendation, idf=True)
        sorted_prop_idf = proprieta_da_considerare(ranked_prop_idf, numero_prop_considerate)
        stampa_proprieta(sorted_prop_idf)

        # ESECUZIONE COMPONENTE GENERATOR
        print("\nEsecuzione componente Generator...\n")
        triple_structure = build_triple_structure(G, sorted_prop_idf, profile, recommendation)
        explanation = generate_explanation(triple_structure, recommendation, profile, scelta_configurazione, template, html)
        print(explanation)
        result = {'explanation': explanation}

        return jsonify(result)


api.add_resource(Rec,'/rec/')

if __name__ == "__main__":
    app.run(port=5036)