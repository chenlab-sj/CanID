import pandas as pd
import numpy as np
import qnorm

import argparse
import math

def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('raw_counts_file',help="matrix file gene (genes x samples)", type=str)
    parser.add_argument('qn_mean_file',   help="output file from step 1a", type=str)
    parser.add_argument('outputfile', help="outputfile name", type=str)
    args = parser.parse_args()
    return args

def parse_qn_mean_file(infile):
    f = open(infile, 'r')
    data_list = []
    for line in f:
        line = line.strip()
        line_array = line.split()
        data_list.append(float(line_array[1]))
    f.close()
    return data_list

def main(LineArgs):
    raw_counts_file  = LineArgs.raw_counts_file
    qn_mean_file   = LineArgs.qn_mean_file
    outputfile     = LineArgs.outputfile

    raw_df = pd.read_csv(raw_counts_file, header='infer', sep="\t")
    mean_list = parse_qn_mean_file(qn_mean_file)
    qn_df = qnorm.quantile_normalize(raw_df, target=mean_list)
    qn_df.to_csv(outputfile, sep="\t", header=True)

if __name__ == '__main__':
    LineArgs = parseArguments()
    main(LineArgs)





