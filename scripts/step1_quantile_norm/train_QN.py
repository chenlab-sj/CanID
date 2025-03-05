import pandas as pd
import numpy as np

import argparse
import math

def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('expression_file', help="Raw Count matrix of training data", type=str)
    parser.add_argument('outputfile', help="outputfile name", type=str)
    args = parser.parse_args()
    return args

def prep_data(expression_file):
    df = pd.read_csv(expression_file, header='infer', sep="\t", index_col=0)
    df = df.T
    # Add 1 to avoid division by zero
    df += 1
    # Convert to log scale
    df = np.log2(df)
    df = df.T
    return df

def compute_means(df):
    # sort each column (sample) independently
    df_sorted = pd.DataFrame(np.sort(df.values, axis=0), index=df.index, columns = df.columns)
    # compute mean across columns
    df_mean = df_sorted.mean(axis=1)
    # change gene to rank value
    df_mean.index = np.arange(1, len(df_mean) + 1)
    return df_mean

def main(LineArgs):
    expression_file  = LineArgs.expression_file
    outputfile     = LineArgs.outputfile

    all_df = prep_data(expression_file)
    quantile_means = compute_means(all_df)
    quantile_means.to_csv(outputfile, sep="\t", header=False)

if __name__ == '__main__':
    LineArgs = parseArguments()
    main(LineArgs)
