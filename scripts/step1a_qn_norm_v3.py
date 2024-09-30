import pandas as pd
import numpy as np

import argparse
import math

def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('normalization_list', help="list of files to use to perform Quantile Normalization with", type=str)
    parser.add_argument('id_list', help="list of files containing sample ids for each file in the normlization list", type=str)
    parser.add_argument('outputfile', help="outputfile name", type=str)
    args = parser.parse_args()
    return args

def read_list(inputfile):
    with open(inputfile) as file:
        lines = [line.rstrip() for line in file]
    return lines

def prep_data(datafile, train_id_file):
    my_list = read_list(train_id_file)
    df = pd.read_csv(datafile, header='infer', sep="\t")
    df = df.T
    # Select only desired samples
    sub_df = df.loc[my_list].copy()
    # Add 1 to avoid division by zero
    sub_df += 1
    # Convert to Log scale
    sub_df = np.log2(sub_df)
    sub_df = sub_df.T
    return sub_df

def create_master_df(norm_list, train_id_list):
    df_list = []
    for cohort, cohort_id_file in zip(norm_list, train_id_list):
        df = prep_data(cohort, cohort_id_file)
        df_list.append(df)
    all_df = pd.concat(df_list, axis=1)
    return all_df

def compute_means(df):
    # sort each column (sample) independently
    df_sorted = pd.DataFrame(np.sort(df.values, axis=0), index=df.index, columns = df.columns)
    # compute mean across columns
    df_mean = df_sorted.mean(axis=1)
    # change gene to rank value
    df_mean.index = np.arange(1, len(df_mean) + 1)
    return df_mean

def main(LineArgs):
    norm_listfile  = LineArgs.normalization_list
    id_listfile    = LineArgs.id_list
    outputfile     = LineArgs.outputfile

    norm_list = read_list(norm_listfile)
    train_id_list = read_list(id_listfile)

    all_df = create_master_df(norm_list, train_id_list)
    quantile_means = compute_means(all_df)
    quantile_means.to_csv(outputfile, sep="\t", header=False)

if __name__ == '__main__':
    LineArgs = parseArguments()
    main(LineArgs)





