import pandas as pd
import numpy as np
import pickle
from sklearn.decomposition import PCA

import argparse

def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('Train_expression_file', help="file containing Training  RNA-Seq expression matrix (Gene x Sample)", type=str)
    parser.add_argument('desired_variance',     help="how many features to keep", type=float)
    parser.add_argument('model_prefix', help="modelprefix", type=str)
    args = parser.parse_args()
    return args

def clean_nans(df):
    # Drop any gene that contains Nans
    # Should not have genes with Nans, but if so, removed them
    sample_df = df.T
    clean_sample_df = sample_df.dropna(how='all', axis='columns')
    clean_df = clean_sample_df.T
    return clean_df

def components_for_variance_explained(explained_variance, desired_percentage):
    n = 1
    total = 0
    for variance in explained_variance:
        total = total + variance
        if total >= desired_percentage:
            break
        else:
            n += 1
    return n

def main(LineArgs):
    train_expression_file = LineArgs.Train_expression_file
    desired_variance      = LineArgs.desired_variance
    modelprefix           = LineArgs.model_prefix

    expression_df = pd.read_csv(train_expression_file, sep="\t", header='infer', index_col = 0)
    clean_expression_df = clean_nans(expression_df)
    clean_expression_df = clean_expression_df.T
    expression_data = clean_expression_df.to_numpy()

    print('data shape:', clean_expression_df.shape)

    # Apply PCA to train dataset
    pca = PCA()
    pca.fit(expression_data)
    explained_variance = pca.explained_variance_ratio_

    print("\nVariance Explained")
    print(explained_variance[0])
    print(explained_variance[1])
    print(explained_variance[2])
    print(explained_variance[3])
    print(explained_variance[4])
    
    print("\nSingular Values")
    print(pca.singular_values_[0])
    print(pca.singular_values_[1])
    print(pca.singular_values_[2])
    print(pca.singular_values_[3])
    print(pca.singular_values_[4])

    desired_components = components_for_variance_explained(explained_variance, desired_variance)
    print('number of components to describe desired variance:', desired_components)

    pca = PCA(n_components=desired_components)
    pca.fit(expression_data)

    pca_model_label = modelprefix + ".pickle"

    with open(pca_model_label, 'wb') as handle:
        pickle.dump(pca, handle, protocol=pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
    LineArgs = parseArguments()
    main(LineArgs)





