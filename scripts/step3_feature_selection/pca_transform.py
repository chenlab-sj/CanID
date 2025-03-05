import pandas as pd
import numpy as np
import pickle
from scipy.linalg import svd

import argparse

def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('test_expression_file', help="file containing Training  RNA-Seq expression matrix (Gene x Sample)", type=str)
    parser.add_argument('pca_model_file',       help="pickled training pca model", type=str)
    parser.add_argument('output_prefix',        help="outprefix", type=str)
    args = parser.parse_args()
    return args

def clean_nans(df):
    # Drop any gene that contains Nans
    # Should not have genes with Nans, but if so, removed them
    sample_df = df.T
    clean_sample_df = sample_df.dropna(how='all', axis='columns')
    clean_df = clean_sample_df.T
    return clean_df

def main(LineArgs):
    test_expression_file  = LineArgs.test_expression_file
    pca_model_file        = LineArgs.pca_model_file
    outprefix             = LineArgs.output_prefix

    expression_df = pd.read_csv(test_expression_file, sep="\t", header='infer', index_col = 0)
    clean_expression_df = clean_nans(expression_df)
    clean_expression_df = clean_expression_df.T
    expression_data = clean_expression_df.to_numpy()

    print('data shape:', clean_expression_df.shape)

    # apply trining pca model
    with open(pca_model_file, 'rb') as handle:
        pca_model = pickle.load(handle)

    reduced_test_features = pca_model.transform(expression_data)
    print('transformed data', reduced_test_features.shape)
    feature_df   = pd.DataFrame(reduced_test_features)
    feature_df['sj_id'] = list(clean_expression_df.index)
    feature_df.set_index('sj_id', inplace=True, drop=True)
    feature_filename = outprefix + ".txt"
    feature_df.to_csv(feature_filename, sep="\t", index=True)

if __name__ == '__main__':
    LineArgs = parseArguments()
    main(LineArgs)





