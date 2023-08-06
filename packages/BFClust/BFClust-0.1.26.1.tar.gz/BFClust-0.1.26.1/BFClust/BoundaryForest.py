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
	

class Node: 
	def __init__(self, dataval = None):
		self.dataval = dataval
		self.children = []
		self.numChildren = 0
		self.index = 0
	def traverse(self):
		mydict = {self.index:self.dataval}
		for child in self.children:
			mydict.update(child.traverse())
		return(mydict)

class BoundaryTree:
	def __init__(self, rootval = None, children = [], maxChild = 10): 
		self.root = Node(rootval)
		self.maxChild = maxChild
		self.root.children = children
		self.treeSize = 1
	def add_child(self, parentNode, newNode):
		newindex = self.treeSize 
		newNode.index = newindex
		parentNode.children.append(newNode)
		parentNode.numChildren += 1 
		self.treeSize += 1
	def traverse(self):
		return(self.root.traverse())
		
def make_BT(n, records, data_order_ix, threshold, maxChild):
	tree_node_ref = [0 for i in range(n)]
	tree = BoundaryTree(rootval = data_order_ix[0])
	tree.add_child(tree.root, Node(data_order_ix[1]))
	tree_node_ref[data_order_ix[0]] = data_order_ix[0]
	tree_node_ref[data_order_ix[1]] = data_order_ix[1]
	
	for i in range(2,n):
		ele_being_proc_data_ix = data_order_ix[i]
		curr_tree_node = tree.root
		while True: 
			curr_node_data_ix = curr_tree_node.dataval
			curr_node_all_children = curr_tree_node.children

			if curr_tree_node.numChildren == 0:
				score = aligner.score(records[ele_being_proc_data_ix].seq, records[curr_node_data_ix].seq)
				if score > threshold:
					new_node = Node(ele_being_proc_data_ix)
					tree.add_child(curr_tree_node, new_node)
				else: 
					tree_node_ref[ele_being_proc_data_ix] = curr_tree_node.dataval
				break
			else:
				#find the child closest to the ele_being_proc
				highest_score = -10000000
				best_child_node = np.nan
				for child_node in curr_node_all_children:
					child_node_data_ix = child_node.dataval
					score1 = aligner.score(records[ele_being_proc_data_ix].seq, records[child_node_data_ix].seq)
					if score1 > highest_score: 
						highest_score = score1
						best_child_node = child_node
				score2 = aligner.score(records[ele_being_proc_data_ix].seq, records[curr_node_data_ix].seq)
				#if the current node is more similar to element being processed than 
				# any of its children
				if score2 > highest_score and curr_tree_node.numChildren < maxChild:
					#if the element being processed is sufficiently similar to the current node, 
					#mark element being processed to be represented by current node
					pdist = jc_distance(records[ele_being_proc_data_ix].seq, records[curr_node_data_ix].seq)
					if pdist < threshold:
						tree_node_ref[ele_being_proc_data_ix] = curr_tree_node.dataval

					# otherwise add element being processed as a child
					else: 
						new_node = Node(ele_being_proc_data_ix)
						tree.add_child(curr_tree_node, new_node)
						
						tree_node_ref[ele_being_proc_data_ix] = ele_being_proc_data_ix
						#treesize+=1
					break
				# otherwise move onto the best child node
				else: 
					curr_tree_node = best_child_node
                
	print("Boundary Tree size: ", tree.treeSize)
	return(tree, tree_node_ref)
	
def find_rep(incoming_seq, tree, treeseqs):
	curr_tree_node = tree.root
	curr_node_all_children = curr_tree_node.children
	curr_node_score = aligner.score(incoming_seq.seq, treeseqs[curr_tree_node.index].seq)
	path = [curr_tree_node]
	path_scores = [curr_node_score]
	
	while curr_tree_node.numChildren>0:
		max_score = -10000000
		for child in curr_node_all_children:
			child_score = aligner.score(incoming_seq.seq, treeseqs[child.index].seq)
			if child_score > max_score:
				max_score = child_score
				best_child_node = child
		path = path + [best_child_node]
		path_scores = path_scores + [max_score]
		curr_tree_node = best_child_node
		curr_node_all_children = curr_tree_node.children
		
	best_match_index = np.argmax(path_scores)
	# index in the input sequence order - should match all_clusters
	representative = path[best_match_index].dataval
	return(representative)
	 