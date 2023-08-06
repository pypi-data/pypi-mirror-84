#!/usr/bin/env python3

from Bio import SeqIO
from random import shuffle
import numpy as np
import os
from Bio import Align
from Bio.Align import substitution_matrices
from Bio import pairwise2 as pw2
from joblib import Parallel, delayed
from sklearn.cluster import KMeans
import pandas as pd
import pickle

import time


aligner = Align.PairwiseAligner()
aligner.substitution_matrix = substitution_matrices.load("BLOSUM62")
aligner.open_gap_score = -0.5
aligner.extend_gap_score = -0.1

# percent identity between 2 sequences
def pc_identity(seq1, seq2):
    aln = pw2.align.globalxx(seq1, seq2)
    seq_len = min([len(seq1), len(seq2)])
    matches = aln[0][2]
    return(matches/seq_len)

# jukes cantor distance between 2 sequences
def jc_distance(seq1, seq2):
    p = 1-pc_identity(seq1, seq2)
    if p<0.95:
        jc = (-19/20) * np.log(1 - 20*p/19)
    else:
        jc = np.inf
    return(jc)

# make Boundary Tree
def make_BT(n, records, data_order_ix, threshold, maxChild):

    tree_node_ref = [0 for i in range(n)]
    tree = [[data_order_ix[0],[1]],
           [data_order_ix[1],[]]]

    tree_node_ref[data_order_ix[0]] = data_order_ix[0]
    tree_node_ref[data_order_ix[1]] = data_order_ix[1]

    treesize=2
    for i in range(2,n):
        ele_being_proc_data_ix = data_order_ix[i]
        curr_tree_node_ix = 0
        while True: 

            curr_node_data_ix = tree[curr_tree_node_ix][0]
            curr_node_all_children_node_ix = tree[curr_tree_node_ix][1]

            #print(treesize, i, curr_tree_node_ix, curr_node_data_ix)

            #find the child closest to the ele_being_proc
            highest_score = -10000000
            best_child_node_ix = np.nan
            for child_node_ix in curr_node_all_children_node_ix:
                child_node_data_ix = tree[child_node_ix][0]
                score1 = aligner.score(records[ele_being_proc_data_ix].seq, records[child_node_data_ix].seq)
                if score1 > highest_score: 
                    highest_score = score1
                    best_child_node_ix = child_node_ix
            score2 = aligner.score(records[ele_being_proc_data_ix].seq, records[curr_node_data_ix].seq)
            #if the current node is more similar to element being processed than 
            # any of its children
            if score2 > highest_score and len(tree[curr_tree_node_ix][1]) < maxChild:
                #if the element being processed is sufficiently similar to the current node, 
                #mark element being processed to be represented by current node

                #pc_id2 = pc_identity(records[ele_being_proc_data_ix], records[curr_node_data_ix])
                #if pc_id2 > pc_id_threshold:
                #        tree_node_ref[ele_being_proc_data_ix] = tree[curr_tree_node_ix][0]
                pdist = jc_distance(records[ele_being_proc_data_ix].seq, records[curr_node_data_ix].seq)
                if pdist < threshold:
                    tree_node_ref[ele_being_proc_data_ix] = tree[curr_tree_node_ix][0]

                # otherwise add element being processed as a child
                else: 
                    tree[curr_tree_node_ix][1] = tree[curr_tree_node_ix][1] + [treesize]
                    tree = tree + [[ele_being_proc_data_ix,[]]]
                    tree_node_ref[ele_being_proc_data_ix] = ele_being_proc_data_ix
                    treesize+=1
                break
            # otherwise move onto the best child node
            else: 
                curr_tree_node_ix = best_child_node_ix
                
    print("Boundary Tree size: ", treesize)
    return(tree, tree_node_ref)
    
    

def run_diamond(filestub, outputdir):
    treefasta = filestub+'.fasta'
    treefasta = os.path.join(outputdir,'Forest/fasta',treefasta)
    dbfile = os.path.join(outputdir, 'Forest/diamond/', filestub)
    dblogfilename =  os.path.join(outputdir, 'Forest/diamond/', filestub+'makedb_log.txt')
    makedb_command = 'diamond makedb --in '+treefasta+' -d '+dbfile + ' > '+dblogfilename+' 2>&1'
    os.system(makedb_command)
    
    blastplogfilename =  os.path.join(outputdir, 'Forest/diamond/', filestub+'blastp_log.txt')
    blastp_command = 'diamond blastp --sensitive -q '+treefasta+' -d '+dbfile+' -f 6 qseqid sseqid bitscore -o '+dbfile+'.tsv > '+blastplogfilename+' 2>&1'
    os.system(blastp_command)
    

def run_mcl(filestub, outputdir):
    diamond_out = filestub+'.tsv'
    diamond_out = os.path.join(outputdir, 'Forest/diamond/', diamond_out)
    mcl_out = filestub+'_clusters.tsv'
    mcl_out = os.path.join(outputdir, 'Forest/MCL/', mcl_out)
    logfilename = filestub+'_MCL_log.txt'
    logfilename = os.path.join(outputdir, 'Forest/MCL/', logfilename)
    mcl_command = 'mcl '+diamond_out+' --abc -I 2 -P 10000 -o '+mcl_out+' > '+logfilename+' >&1'
    os.system(mcl_command)

def get_cluster(cluster_dict, record):
    try:
        clust_id = cluster_dict[record.id]
    except KeyError:
        clust_id = -1	
    return(clust_id)

def extend_clusters(records, mcl_output, clust_ref):
    cluster_dict = {}
    with open(mcl_output, 'r') as clustfile: 
        clusters = clustfile.readlines()

    for i in range(len(clusters)): 
        cluster = clusters[i].strip().split('\t')
        for element in cluster:
            cluster_dict[element] = i

    #extended_clusters = [cluster_dict[records[ref].id] for ref in clust_ref]
    extended_clusters = [get_cluster(cluster_dict, records[ref]) for ref in clust_ref]
    return(extended_clusters)


def check_and_mkdir(dirname):
    if not os.path.exists(dirname):
        os.mkdir(dirname)

def setup_outdir(outdirname):
    check_and_mkdir(outdirname)
    forestdir = os.path.join(outdirname, 'Forest/')
    forest_fastadir = os.path.join(forestdir, 'fasta/')
    forest_pickledir = os.path.join(forestdir, 'pickle/')
    forest_diamonddir = os.path.join(forestdir, 'diamond/')
    forest_mcldir = os.path.join(forestdir, 'MCL/')
    consensusdir = os.path.join(outdirname, 'Consensus/')
    for i in [forestdir, forest_fastadir, forest_pickledir, forest_diamonddir, forest_mcldir, consensusdir]:
        check_and_mkdir(i)
		
def BT_function(i, n, records, threshold, maxChild, outputdir):
    filestub = "BT"+str(i)
    data_order_ix = list(range(n))
    shuffle(data_order_ix) 
    # make Boundary-Tree
    BT, BT_ref = make_BT(n, records, data_order_ix, threshold, maxChild)
    treepicklefile = os.path.join(outputdir,'Forest/pickle/',filestub+'.p')
    pickle.dump(BT, open(treepicklefile, 'wb'))
    # write tree sequences into a fasta file
    tree_seqs = [records[i[0]] for i in BT]
    treefastafile = filestub+'.fasta'
    treefastafile = os.path.join(outputdir,'Forest/fasta/',treefastafile)
    SeqIO.write(tree_seqs, treefastafile, 'fasta')

    # run Diamond
    run_diamond(filestub, outputdir)

    # run MCL
    run_mcl(filestub, outputdir)

    #extend clusters
    mcloutputfile = os.path.join(outputdir, 'Forest/MCL', filestub+'_clusters.tsv')
    clust_assignments = extend_clusters(records, mcloutputfile, BT_ref)

    return(clust_assignments)