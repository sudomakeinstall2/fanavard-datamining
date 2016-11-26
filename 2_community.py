# this script reads a weighted graph from an excel file and finds it's communities
# requirements: igraph, pandas

from igraph import *

import pandas as pd

df = pd.read_excel('_2.xlsx')
vertex_to_id = {}
id_to_vertex = {}
edges = {}


def id_of_vertex(vertex):
    if vertex in vertex_to_id:
        return vertex_to_id[vertex]
    else:
        id_ = len(vertex_to_id)
        vertex_to_id[vertex] = id_
        id_to_vertex[id_] = vertex
        return id_


def add_edge(e,w):
    if e in edges:
        edges[e]+=w
    else:
        edges[e]=w


for index,row in df.iterrows():
    id1 = id_of_vertex(row['u'])
    id2 = id_of_vertex(row['v'])
    if id1 > id2:
        id1,id2 = id2,id1
    add_edge( (id1,id2), row['weight'] )

n = len(vertex_to_id)
g = Graph()
g.add_vertices(n)
weights = []
for e in edges:
    g.add_edge(e[0],e[1])
    weights.append(edges[e])
v = g.community_fastgreedy(weights=weights)
clusters = v.as_clustering()

with open('result.txt','w') as f:
    print >>f, 'vertex_id', 'cluster_id'
    for idx,c in enumerate(clusters):
        for id_ in c:
            v = id_to_vertex[id_]
            print >>f, v,idx

# algorithm     modularity
#fastgreedy         0.97
#walktrap           0.90
#multilevel         0.97
#labelpropagation   0.84
