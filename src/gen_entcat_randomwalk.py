import networkx as nx
import numpy as np
import pandas as pd
import torch
from sklearn.preprocessing import LabelEncoder

from torchProp import LabelSpreadinger

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', -1)

def randomwalk(edges, all_ents, wiki_cats, labels):
    print('building graph')
    B = nx.Graph()
    B.add_nodes_from(wiki_cats, bipartite=1)
    B.add_nodes_from(all_ents, bipartite=0)
    B.add_weighted_edges_from(edges)
    components = sorted(nx.connected_components(B), key=len, reverse=True)
    c = components[0]
    B = B.subgraph(c)
    print('giant size', len(B.nodes()))
    A = nx.adjacency_matrix(B).toarray()

    LE = LabelEncoder()
    labels['code'] = LE.fit_transform(labels['wiki_cluster'])
    keyfits = labels[['wiki_cluster', 'code']]
    keyfits.drop_duplicates(inplace=True)
    print('keyfit', keyfits)
    labels = labels.set_index('cats_clean')['code'].to_dict()

    y = np.array([labels[x] if x in labels else -1 for x in B.nodes()])
    print(np.unique(y))
    adj_matrix_t = torch.FloatTensor(A)
    labels_t = torch.LongTensor(y)
    print('shapes', adj_matrix_t.shape, labels_t.shape)

    # Learn with Label Spreading
    label_spreading = LabelSpreadinger(adj_matrix_t)
    label_spreading.fit(labels_t, alpha=0.9)
    y_probs = label_spreading.predict().max(dim=1).values.numpy()
    print('y_probs', y_probs)
    label_spreading_output_labels = label_spreading.predict_classes().numpy()
    # print(label_spreading_output_labels)

    idx = list(zip(label_spreading_output_labels, y_probs, B.nodes()))
    dfidx = pd.DataFrame(idx, columns=['code', 'y_prob', 'node'])
    dfidx = pd.merge(dfidx, keyfits, on='code', how='left')
    dfidx = dfidx[dfidx['node'].isin(all_ents)]
    print(dfidx.head())
    print('length', len(dfidx.index))

    return dfidx