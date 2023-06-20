import numpy as np
import pandas as pd
from sklearn.metrics import adjusted_mutual_info_score, adjusted_rand_score
import community as community_louvain
from itertools import combinations

def graph_community_resolution(G):
    aves = {}
    max_modularity = 0
    for resolution in [0.5, 0.66, 0.75, 1, 1.5, 2, 2.5, 5]:
        # first compute the best partition
        resss = []
        mods = []
        for i in range(10):
            partition = community_louvain.best_partition(G, resolution=resolution, randomize=True)
            partition_lst = list(partition.items())
            resss.append(list(partition.values()))
            modularity = community_louvain.modularity(partition, G)
            mods.append(modularity)
            df_partition = pd.DataFrame(partition_lst, columns = ['node', 'community'])
            df_count = df_partition.groupby('community').agg({'node': 'count'})
            df_count.sort_values(['node'], inplace=True, ascending=False)
        pairs = combinations(resss, 2)
        rand_scores = []
        mi_scores = []
        for p in pairs:
            rand_score = adjusted_rand_score(p[0], p[1])
            rand_scores.append(rand_score)
            mi_score = adjusted_mutual_info_score(p[0], p[1])
            mi_scores.append(mi_score)
        ave_mod = np.mean(mods)
        max_modularity = max(max_modularity, ave_mod)
        print('resulotion=%s, average modularity=%s, average rand score=%s, average mi score=%s'%(resolution, ave_mod, np.mean(rand_scores), np.mean(mi_scores)))
        aves[resolution] = [ave_mod, np.mean([np.mean(rand_scores), np.mean(mi_scores)])]

    best_resolution = 0
    best_score = 0
    print('max modularity', max_modularity)
    for resolution,scores in aves.items():
        modularity, score = scores
        print(resolution, modularity, score, (modularity-max_modularity), 0.1 * max_modularity)
        if score>best_score and (max_modularity-modularity)<=0.1 * max_modularity:
            best_resolution = resolution
            best_score = score

    #get the best
    print('best resolution', best_resolution)
    partition = community_louvain.best_partition(G, resolution=best_resolution, randomize=True)
    partition_lst = list(partition.items())
    df_partition = pd.DataFrame(partition_lst, columns=['node', 'community'])
    df_count = df_partition.groupby('community', as_index=False).agg({'node': 'count'})
    df_count['frac'] = df_count['node']/df_count['node'].sum()
    df_count = df_count[((df_count['frac']>=0.03) & (df_count['node']>=10))| (df_count['frac']>=0.25)]
    df_count.sort_values(['node'], inplace=True, ascending=False)
    # print(df_count)
    df_partition = df_partition[df_partition['community'].isin(df_count['community'].tolist())]
    return df_partition


