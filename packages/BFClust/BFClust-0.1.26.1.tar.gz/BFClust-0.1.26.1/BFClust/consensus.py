#!/usr/bin/env python3

from BFClust.cluster_de_novo import *

def consensus_cluster(records, cluster_results, ntrees):
    all_clusters = np.transpose(np.array(cluster_results))
    k_values = [len(set(r)) for r in cluster_results]
    k_final = int(np.median(k_values))

    consensus = KMeans(n_clusters=k_final, random_state=0).fit(all_clusters)
    consensus_labels = consensus.predict(all_clusters)
    
    consensus_df = pd.DataFrame(all_clusters)
    consensus_df.columns = ['Tree '+str(i) for i in range(ntrees)]
    consensus_df.index = [r.id for r in records]
    consensus_df['Consensus Cluster'] = consensus_labels
    
    return(consensus_labels, consensus_df, k_final, all_clusters, consensus)

def compute_consensus_scores(consensus_labels, consensus_df, ntrees, n, k_final, all_clusters):
    set_of_clusters = list(set(consensus_labels))
    item_scores = np.zeros([n,1])
    cluster_scores = [0 for i in range(k_final)]

    i = 0
    for cluster in set_of_clusters: 
        #find the cluster members
        clust_ix = consensus_df['Consensus Cluster']==cluster
        thiscluster = consensus_df.loc[clust_ix]
        n_clust = thiscluster.shape[0]
        M = np.zeros([n_clust, n_clust, ntrees])
        for tree in range(ntrees):
            clust_assignments = all_clusters[clust_ix,tree]
            x = np.array([clust_assignments for j in range(n_clust)])
            xt = np.transpose(x)

            M[:,:, tree] = x==xt

        M_cons = np.mean(M, axis=2)
        cluster_scores[i] = np.mean(M_cons)
        i+=1
        clust_ix_array = np.array(clust_ix)==False
        item_scores[~clust_ix_array] = np.mean(M_cons, axis=1, keepdims = True)
        
    consensus_df['Item Consensus Score'] = item_scores
    cluster_scores = pd.DataFrame({'Cluster': set_of_clusters, 'Score': cluster_scores})
    
    return(consensus_df, cluster_scores)

def run_BFC(records, outputdir, ntrees, threshold, maxChild):
    setup_outdir(outputdir)
    
    n = len(records)
    
    results = Parallel(n_jobs=ntrees, backend="multiprocessing")(
             map(delayed(BT_function), list(range(ntrees)), [n]*ntrees, 
                 [records]*ntrees, [threshold]*ntrees, [maxChild]*ntrees, [outputdir]*ntrees))
    
    
    cons_labels, cons_df, k_final, all_clusters, consensus_model = consensus_cluster(records, results, ntrees)
    
    consensus_pickle_dict = {'all_clusters': all_clusters, 'consensus_model': consensus_model, 'k_final': k_final, 'consensus_df': cons_df, 'ntrees': ntrees}
    consensus_picklefile = os.path.join(outputdir, 'Consensus','consensus.p')
    pickle.dump(consensus_pickle_dict, open(consensus_picklefile, 'wb'))
    
    cons_df, clust_scores = compute_consensus_scores(cons_labels, cons_df, ntrees, n, k_final, all_clusters)
    
    outcsvfile = os.path.join(outputdir, 'Consensus','cluster_assignments.csv')
    cons_df.to_csv(outcsvfile)
    
    clustercsvfile = os.path.join(outputdir, 'Consensus', 'cluster_consensus_scores.csv')
    clust_scores.to_csv(clustercsvfile, index=False)