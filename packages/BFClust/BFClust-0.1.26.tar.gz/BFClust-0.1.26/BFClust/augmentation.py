#!/usr/bin/env python3

import numpy as np

from BFClust.cluster_de_novo import *
from BFClust.consensus import *
from BFClust.gbk_parsing import *

import pickle
import pandas as pd

def find_closest_on_BT(incoming_seqs, BT, treeseqs):
    n = len(incoming_seqs)
    representatives = np.zeros([n,1])
    
    for i in range(n):
        curr_tree_node_ix = 0
        curr_node_all_children_node_ix = BT[curr_tree_node_ix][1]
        curr_node_score = aligner.score(incoming_seqs[i].seq, treeseqs[curr_tree_node_ix].seq)
        
        path_ixs = [curr_tree_node_ix]
        path_scores = [curr_node_score]
        
        while len(BT[curr_tree_node_ix][1])>0:
            #print(curr_tree_node_ix, BT[curr_tre_node_ix], path_ixs, path_scores)
            max_score = -10000000
            for child_node in curr_node_all_children_node_ix:
                child_score = aligner.score(incoming_seqs[i].seq, treeseqs[child_node].seq)
                if child_score>max_score:
                    max_score = child_score
                    best_child_node_ix = child_node
            path_ixs = path_ixs + [best_child_node_ix]
            path_scores = path_scores + [max_score]
            curr_tree_node_ix = best_child_node_ix
            curr_node_all_children_node_ix = BT[curr_tree_node_ix][1]
            
        best_match_index = np.argmax(path_scores)
        representatives[i] = BT[path_ixs[best_match_index]][0] # index in the input sequence order - should match all_clusters
    return(representatives)


def augment(newseqs, existing_clust_dir, initialbt, threshold = 0.1, maxChild = 10):
    consensus_pickle_name = os.path.join(existing_clust_dir, 'Consensus', 'consensus.p')
    consensus_data = pickle.load(open(consensus_pickle_name,'rb'))
    ntrees = consensus_data['ntrees']
    all_clusters = consensus_data['all_clusters']
    consensus_model = consensus_data['consensus_model']
    
    new_clust_assignments = np.zeros([len(newseqs),ntrees])
    #make BT from incoming sequences
    if initialbt == True: 
        n_newseqs = len(newseqs)
        dataorder = list(range(n_newseqs))
        new_BT, new_BT_refs = make_BT(n_newseqs, newseqs, dataorder, threshold, maxChild)
        
        new_clust_assignments_BT = np.zeros([len(new_BT), ntrees])
        new_BT_seqs = [newseqs[n[0]] for n in new_BT]
        # find representatives on existing forest
        for t in range(ntrees):
            treename = 'BT'+str(t)
            tree_pickle_name = os.path.join(existing_clust_dir, 'Forest', 'pickle', treename+'.p')
            treeseqs_file = os.path.join(existing_clust_dir, 'Forest', 'fasta', treename+'.fasta')
            BT = pickle.load(open(tree_pickle_name,'rb'))
            BT_seqs = list(SeqIO.parse(treeseqs_file, 'fasta'))
            reps = find_closest_on_BT(new_BT_seqs, BT, BT_seqs)
            new_clust_assignments_BT[:,t] = [all_clusters[r, t] for r in range(len(reps))]
        cons_clusters_BT = consensus_model.predict(new_clust_assignments_BT)
        cons_clusters = np.zeros([len(newseqs),1])
        
        #extend consensus to all newseqs
        for i in range(len(new_BT)):
            new_clust_assignments[new_BT[i][0],:] = new_clust_assignments_BT[i,:]
            cons_clusters[new_BT[i][0]] = cons_clusters_BT[i]
        
        for i in range(len(newseqs)):
            treeref = new_BT_refs[i]
            new_clust_assignments[i,:] = new_clust_assignments[treeref,:]
            cons_clusters[i] = cons_clusters[treeref]
        
    #process incoming sequences as is
    else: 
        # find representatives on existing forest
        for t in range(ntrees):
            treename = 'BT'+str(t)
            tree_pickle_name = os.path.join(existing_clust_dir, 'Forest', 'pickle', treename+'.p')
            treeseqs_file = os.path.join(existing_clust_dir, 'Forest', 'fasta', treename+'.fasta')
            BT = pickle.load(open(tree_pickle_name,'rb'))
            BT_seqs = list(SeqIO.parse(treeseqs_file, 'fasta'))
            reps = find_closest_on_BT(newseqs, BT, BT_seqs)
            new_clust_assignments[:,t] = [all_clusters[r, t] for r in range(len(reps))]
        cons_clusters = consensus_model.predict(new_clust_assignments)
    
    all_clusters_merged = np.concatenate((all_clusters, new_clust_assignments), axis=0)
    
    new_cons_df = pd.DataFrame(new_clust_assignments)
    new_cons_df.columns = ['Tree '+str(i) for i in range(ntrees)]
    new_cons_df.index = [r.id for r in newseqs]
    new_cons_df['Consensus Cluster'] = cons_clusters
    
    all_cons_df = pd.concat([consensus_data['consensus_df'], new_cons_df])
    n_total = all_cons_df.shape[0]
    all_cons_df, all_clust_scores = compute_consensus_scores(all_cons_df['Consensus Cluster'],
                                                            all_cons_df, ntrees, n_total, 
                                                            consensus_data['k_final'],
                                                            all_clusters_merged)
    
    return(all_cons_df, all_clust_scores)


def augment_and_output(newseqs, existing_clust_dir, initialbt, threshold = 0.1, maxChild = 10):
    new_cons_df, new_clust_scores = augment(newseqs, existing_clust_dir, initialbt, threshold, maxChild)
    augment_dir = os.path.join(existing_clust_dir, 'Augmentation/')
    check_and_mkdir(augment_dir)
    
    augment_consensus_filename = os.path.join(augment_dir, 'cluster_assignments.csv')
    augment_clustscore_filename = os.path.join(augment_dir, 'cluster_consensus_scores.csv')
    new_cons_df.to_csv(augment_consensus_filename)
    new_clust_scores.to_csv(augment_clustscore_filename)
   