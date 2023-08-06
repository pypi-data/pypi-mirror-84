#!/usr/bin/env python3


from BFClust.cluster_de_novo import *
from BFClust.consensus import *
from BFClust.gbk_parsing import *

#from BFClust import *

import os
from optparse import OptionParser
import time

options = OptionParser(usage='%prog -i inputdir -o outputdir -n 10 -t 0.1 -m 10 -l 30 -s True',
		description = "Specify the input directory, output directory, number of trees in the forest, sequence similarity threshold, maxChild, and the minimum sequence length.")
		
options.add_option("-i", "--input", dest="inputdir", help="input directory with GBK files")
options.add_option("-o", "--outputdir", dest="outputdir", help="output directory")
options.add_option("-n", "--ntrees", dest="ntrees", help="number of trees in the forest", default = 10)
options.add_option("-t", "--threshold", dest="threshold", help="sequence distance threhold (Jukes Cantor distance) to be used when picking representatives", default=0.1)
options.add_option("-m", "--maxChild", dest="maxChild", help="max number of children a node is allowed to have in the Boundary-Tree", default=10)
options.add_option("-l", "--length", dest="minseqlen", help="amino acid sequences of smaller length will be excluded", default=30)
options.add_option("-s", "--stop", dest="ignore", help="whether or not to ignore internal stop codons", default = True)


def main():
	#read input args
	opts, args = options.parse_args()
	inputdir = opts.inputdir
	outdir = opts.outputdir
	ntrees = int(opts.ntrees)
	t = float(opts.threshold)
	maxChild = int(opts.maxChild)
	minseqlen = int(opts.minseqlen)
	ignoreinternalstop = opts.ignore == 'True'

	tic = time.perf_counter()
	
	records = get_records_from_contigGBKs(inputdir, minseqlen,ignoreinternalstop)
	print('All files successfully parsed')
	
	run_BFC(records, outdir, ntrees, t, maxChild)
	toc = time.perf_counter()
	print("Time elapsed (s):",toc-tic)

if __name__ == '__main__':
	main()