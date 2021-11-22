from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from Mapper import *
from Builder import *
from Ranker import *
from Generator import *


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
        profile = mapping_profilo(id_film_piaciuti)
        recommendation = mapping_profilo(id_film_raccomandati)

        # ESECUZIONE COMPONENTE BUILDER
        print("\nEsecuzione componente Builder...\n")
        G, common_properties = costruisci_grafo(profile, recommendation)
        # visualizza_grafo(G)

        # ESECUZIONE COMPONENTE RANKER
        print("\nEsecuzione componente Ranker...\n")
        sorted_prop = ranking_proprieta(G, common_properties, profile, recommendation, numero_prop_considerate)
        # print("\nEcco le proprietà in comune dei film in ordine decrescente per influenza:\n")
        # for key, value in sorted_prop.items():
        #     print(key, value)
        # print("\n\n")

        # ESECUZIONE COMPONENTE GENERATOR
        print("\nEsecuzione componente Generator...\n")
        NewPreGenArchitecture = inizializzaNewPreGenArchitecture(G, sorted_prop, profile, recommendation)
        explanation = generate_explanation(NewPreGenArchitecture, recommendation, profile, scelta_configurazione, template, html)
        # print(explanation)
        result = {'explanation': explanation}

        return jsonify(result)


api.add_resource(Rec,'/rec/')

if __name__ == "__main__":
    app.run(port=5036)
