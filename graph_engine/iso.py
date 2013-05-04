#!/usr/bin/env python

import json
import networkx as nx
import networkx.algorithms.isomorphism as iso

def init():
    """ ss """
    with open("ggg.json") as f1:
        j1 = f1.read()

    with open("hhh.json") as f2:
        j2 = f2.read()

    print(check_isomorphism(j1, j2))


# najebat jsony do g1 a g2
def check_isomorphism(json_1, json_2):
    g1 = json.loads(json_1)
    g2 = json.loads(json_2)

    nodes_1 = [(i['id'], {'type': i['type']}) for i in g1['nodes']]
    edges_1 = [(i['from'],i['to'], {'type': i['type']}) for i in g1['edges']]


    nodes_2 = [(i['id'], {'type': i['type']}) for i in g2['nodes']]
    edges_2 = [(i['from'],i['to'], {'type': i['type']}) for i in g2['edges']]


    graph_1 = nx.Graph()
    graph_1.add_nodes_from(nodes_1)
    graph_1.add_edges_from(edges_1)

    graph_2 = nx.Graph()
    graph_2.add_nodes_from(nodes_2)
    graph_2.add_edges_from(edges_2)

    nm = iso.numerical_node_match('type',-1)
    em = iso.numerical_edge_match('type',-1)

    return nx.is_isomorphic(graph_1, graph_2, node_match=nm, edge_match=em)


if __name__ == '__main__':
    init()
