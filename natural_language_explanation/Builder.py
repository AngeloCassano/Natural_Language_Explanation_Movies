import networkx as nx
import matplotlib.pyplot as plt


def costruisci_grafo(profile, recommendation):
    profile1 = {}
    recommendation1 = {}

    with open('movies_stored_prop.mapping', 'r') as f:
        for line in f:
            line = line.rstrip().split('\t')
            for key, value in profile.items():
                if line[0] == value:
                    profile1[line[2]] = value

    with open('movies_stored_prop.mapping', 'r') as f:
        for line in f:
            line = line.rstrip().split('\t')
            for key, value in recommendation.items():
                if line[0] == value:
                    recommendation1[line[2]] = value

    profile2 = {}
    recommendation2 = {}

    for key, value in profile1.items():
        for key1, value1 in recommendation1.items():
            if key == key1:
                profile2[key] = value
                recommendation2[key1] = value1

    common_proprierties = list(profile2.keys())
    G = nx.DiGraph()
    for key, value in profile2.items():
        G.add_edge(value, key)
    for key, value in recommendation2.items():
        G.add_edge(key, value)

    return G, common_proprierties


def visualizza_grafo(G):
    nx.draw(G, with_labels=True)
    plt.show()