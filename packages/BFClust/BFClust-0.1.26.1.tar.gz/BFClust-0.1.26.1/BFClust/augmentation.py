#!/usr/bin/env python3

import numpy as np

from BFClust.BoundaryForest import *
from BFClust.cluster_de_novo import *
from BFClust.consensus import *
from BFClust.gbk_parsing import *

import pickle
import pandas as pd

def find_closest_on_BT(incoming_seqs, BT, treeseqs):
    n = len(incoming_seqs)
    representatives = np.zeros([n,1])
    
    for i in range(n):
       representatives[i] = find_rep(incoming_seqs[i], BT, treeseqs)
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
        
        new_clust_assignments_BT = np.zeros([new_BT.treeSize, ntrees])
        tree_ixs_dict = new_BT.traverse()
        new_BT_size = new_BT.treeSize
        new_BT_seqs = [newseqs[tree_ixs_dict[i]] for i in  range(new_BT_size)]
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
        for i in range(new_BT.treeSize):
            new_clust_assignments[tree_ixs_dict[i],:] = new_clust_assignments_BT[i,:]
            cons_clusters[tree_ixs_dict[i]] = cons_clusters_BT[i]
        
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
   