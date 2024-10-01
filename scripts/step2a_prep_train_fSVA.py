import pandas as pd
import numpy as np
import argparse

def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('qn_listfile',           help="list of QN files", type=str)
    parser.add_argument('trainID_listfile',      help="list of train IDs to select corresponding to qn_listfile", type=str)
    parser.add_argument('master_labelfile',      help="file of all ID and tumor assignments", type=str)
    parser.add_argument('class_file',            help="file containing class code assignments", type=str)
    parser.add_argument('output_prefix',         help="outprefix", type=str)
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

def create_master_df(qn_list, trainID_list):
    df_list = []
    for cohort, ID_list in zip(qn_list, trainID_list):
        df = pd.read_csv(cohort, header='infer', sep="\t", index_col = 0)
        cohort_ids = get_list(ID_list)
        df = df[cohort_ids].copy()
        df_list.append(df)
    all_df = pd.concat(df_list, axis=1)
    # randomize the sample order
    all_df = all_df.T
    all_df = all_df.sample(frac=1)
    all_df = all_df.T
    return all_df

def main(LineArgs):
    qn_listfile            = LineArgs.qn_listfile
    trainID_listfile       = LineArgs.trainID_listfile
    master_labelfile       = LineArgs.master_labelfile
    class_file             = LineArgs.class_file
    outprefix              = LineArgs.output_prefix

    # output files
    phenotype_output = outprefix + "_train_pheno.txt"
    train_expression_output = outprefix + "_train_expression.txt"

    # Create train_df
    qn_list = get_list(qn_listfile)
    trainID_list = get_list(trainID_listfile)
    train_df = create_master_df(qn_list, trainID_list)

    # Set up Phenotype data based on training set
    label_df = pd.read_csv(master_labelfile, header='infer', sep="\t", index_col = 0)
    
    pheno_df = train_df.T
    sample_num = [x for x in range(1, pheno_df.shape[0] + 1)]
    pheno_df['sample'] = sample_num
    pheno_df = pheno_df['sample'].copy()

    pheno_df = pd.merge(pheno_df, label_df[['class_label']], left_index=True, right_index=True, how='left')
    pheno_df.columns = ['sample', 'outcome']

    encode_df = pd.read_csv(class_file, header='infer', sep="\t")
    encode_dict = pd.Series(encode_df.tumor_code.values, index=encode_df.tumor_class).to_dict()
    batch = [encode_dict[x] for x in list(pheno_df['outcome'].values)]
    pheno_df['batch'] = batch
    pheno_df['cancer'] = pheno_df['outcome']

    # Write Files
    pheno_df.to_csv(phenotype_output, sep="\t", header=True)
    train_df.to_csv(train_expression_output, sep="\t", header=True)

if __name__ == '__main__':
    LineArgs = parseArguments()
    main(LineArgs)





