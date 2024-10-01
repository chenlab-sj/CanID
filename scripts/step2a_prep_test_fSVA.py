import pandas as pd
import numpy as np
import argparse

def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('qn_outputfile',     help="file containing quantile normalized expression data", type=str)
    parser.add_argument('test_ids',          help="file containing test ids", type=str)
    parser.add_argument('output_prefix',     help="outprefix", type=str)
    args = parser.parse_args()
    return args

def get_list(infile):
    f = open(infile, 'r')
    data_list = []
    for line in f:
        line = line.strip()
        data_list.append(line)
    f.close()
    return data_list

def main(LineArgs):
    expression_file  = LineArgs.qn_outputfile
    test_ids         = LineArgs.test_ids
    outprefix        = LineArgs.output_prefix

    # output files
    test_expression_output = outprefix + "_test_expression.txt"

    # Retrive lists of samples for training/test sets
    test_list      = get_list(test_ids)

    # Read in SJ Data
    expression_df = pd.read_csv(expression_file, header='infer', sep="\t", index_col = 0)
    test_df = expression_df[test_list].copy()

    # Write Files
    test_df.to_csv(test_expression_output, sep="\t", header=True)

if __name__ == '__main__':
    LineArgs = parseArguments()
    main(LineArgs)





