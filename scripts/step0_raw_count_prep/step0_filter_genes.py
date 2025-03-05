import pandas as pd
import numpy as np

import argparse
import math

def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('expression_file', help="Matrix of raw count data to run prediction on", type=str)
    parser.add_argument('geneset_file', help="List of genes model was trained on", type=str)
    parser.add_argument('outputfile', help="outputfile name", type=str)
    args = parser.parse_args()
    return args

def read_list(inputfile):
    with open(inputfile) as file:
        lines = [line.rstrip() for line in file]
    return lines

def get_missing_genes(df, basis_list):
    current_set = set(list(df.index))
    basis_set = set(basis_list)
    intersection = current_set.intersection(basis_set)
    missing_genes = basis_set - intersection
    return list(missing_genes)

def main(LineArgs):
    expression_file    = LineArgs.expression_file
    basis_geneset_file = LineArgs.geneset_file
    outfile            = LineArgs.outputfile

    basis_gene_list = read_list(basis_geneset_file)
    df = pd.read_csv(expression_file, header='infer', sep="\t", index_col=0)

    genes_missing = get_missing_genes(df, basis_gene_list)
    if len(genes_missing) > 0:
        print('CanID has detected missing genes from your training data.')
        print('You must provide count values for the following missing genes:\n')
        print('missing genes:', genes_missing)
    else:
        final_df = df.loc[basis_gene_list].copy()
        final_df.to_csv(outfile, header=True, index=True, sep="\t")

if __name__ == '__main__':
    LineArgs = parseArguments()
    main(LineArgs)
