import pandas as pd
import numpy as np
import argparse

def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('qn_matrixfile',         help="Matrix of Quantile normalized training data", type=str)
    parser.add_argument('master_labelfile',      help="file of all ID and tumor assignments", type=str)
    parser.add_argument('class_file',            help="file containing class code assignments", type=str)
    parser.add_argument('output_prefix',         help="outprefix", type=str)
    args = parser.parse_args()
    return args

def read_data(datafile):
    df = pd.read_csv(datafile, header='infer', sep="\t", index_col = 0)
    # Randomize the samples
    df = df.T
    df = df.sample(frac=1)
    df = df.T
    return df

def main(LineArgs):
    qn_matrixfile          = LineArgs.qn_matrixfile
    master_labelfile       = LineArgs.master_labelfile
    class_file             = LineArgs.class_file
    outprefix              = LineArgs.output_prefix

    # output files
    phenotype_output = outprefix + "_train_pheno.txt"
    train_expression_output = outprefix + "_train_expression.txt"
    test_expression_output = outprefix + "_dummy_test.txt"

    # Create train_df
    train_df = read_data(qn_matrixfile)

    # Set up Phenotype data based on training set
    label_df = pd.read_csv(master_labelfile, header='infer', sep="\t", index_col = 0)
    
    pheno_df = train_df.T

    sample_num = [x for x in range(1, pheno_df.shape[0] + 1)]
    pheno_df['sample'] = sample_num
    pheno_df = pheno_df['sample'].copy()

    pheno_df = pd.merge(pheno_df, label_df[['class_label']], left_index=True, right_index=True, how='left')
    pheno_df.columns = ['sample', 'outcome']

    encode_df = pd.read_csv(class_file, header='infer', sep="\t")

    # Add 1 to removed 0-based indexing, fSVA requires 1-based indexing
    encode_df['tumor_code'] = encode_df['tumor_code'] + 1
    
    encode_dict = pd.Series(encode_df.tumor_code.values, index=encode_df.tumor_class).to_dict()
    batch = [encode_dict[x] for x in list(pheno_df['outcome'].values)]
    pheno_df['batch'] = batch
    pheno_df['cancer'] = pheno_df['outcome']

    test_df = train_df.iloc[:, [0]].copy()
    test_df.columns = ['test1']
    
    # Write Files
    pheno_df.to_csv(phenotype_output, sep="\t", header=True)
    train_df.to_csv(train_expression_output, sep="\t", header=True)
    test_df.to_csv(test_expression_output, sep="\t", header=True)

if __name__ == '__main__':
    LineArgs = parseArguments()
    main(LineArgs)
