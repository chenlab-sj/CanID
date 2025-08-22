import pandas as pd
import numpy as np

import argparse
import math

def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('expression_file', help="Matrix of raw count data to run prediction on", type=str)
    parser.add_argument('outputfile', help="outputfile name", type=str)
    args = parser.parse_args()
    return args

def main(LineArgs):
    expression_file    = LineArgs.expression_file
    outfile            = LineArgs.outputfile

    df = pd.read_csv(expression_file, header='infer', sep="\t", index_col=0)
    basis_gene_list = list(df.index)
    
    # Write the list to a file, one item per line
    with open(outfile, "w") as file:
        for item in basis_gene_list:
            file.write(f"{item}\n")

if __name__ == '__main__':
    LineArgs = parseArguments()
    main(LineArgs)
