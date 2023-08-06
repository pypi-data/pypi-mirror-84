#!/usr/bin/env python3

from BFClust import BoundaryForest
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
	
def make_tree_fasta(BT, records, filename):
	tree_ixs_dict = BT.traverse()
	BT_size = BT.treeSize
	tree_seqs = [records[tree_ixs_dict[i]] for i in  range(BT_size)]
	SeqIO.write(tree_seqs, filename, 'fasta')
	

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



		
def BT_function(i, n, records, threshold, maxChild, outputdir):
    filestub = "BT"+str(i)
    data_order_ix = list(range(n))
    shuffle(data_order_ix) 
    # make Boundary-Tree
    BT, BT_ref = BoundaryForest.make_BT(n, records, data_order_ix, threshold, maxChild)
    treepicklefile = os.path.join(outputdir,'Forest/pickle/',filestub+'.p')
    pickle.dump(BT, open(treepicklefile, 'wb'))

    # write tree sequences into a fasta file
    treefastafile = filestub+'.fasta'
    treefastafile = os.path.join(outputdir,'Forest/fasta/',treefastafile)
    make_tree_fasta(BT, records, treefastafile)

    # run Diamond
    run_diamond(filestub, outputdir)
    # run MCL
    run_mcl(filestub, outputdir)
    #extend clusters
    mcloutputfile = os.path.join(outputdir, 'Forest/MCL', filestub+'_clusters.tsv')
    clust_assignments = extend_clusters(records, mcloutputfile, BT_ref)

    return(clust_assignments)