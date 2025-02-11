import pandas as pd
import numpy as np
import argparse
import os
import pickle
from sklearn.calibration import CalibratedClassifierCV
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import StackingClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC
from sklearn.utils import resample
from sklearn.utils import shuffle

def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('train_expression_file', help="file containing Training RNA-Seq expression matrix (Gene x Sample)", type=str)
    parser.add_argument('label_file',            help="file containing sj_id and class assignment", type=str)
    parser.add_argument('f_format',              help="(id_by_gene, vs. gene_by_id)", type=str)
    parser.add_argument('model_type',            help="(svm, rnf, lda, lgr, mlp, stack)", type=str)
    parser.add_argument('class_file',            help="file containing class code assignments", type=str)
    parser.add_argument('output_prefix',         help="outprefix", type=str)
    args = parser.parse_args()
    return args

def get_stacking():
    svm_clf = CalibratedClassifierCV(LinearSVC(dual=False, multi_class="ovr", verbose=False, max_iter=10000))
    mlp_clf = MLPClassifier(max_iter=1000, early_stopping=True)
    lgr_clf = LogisticRegression(multi_class="multinomial", max_iter=100000)
    rnf_clf = RandomForestClassifier(n_estimators=1000)
    lda_clf = LinearDiscriminantAnalysis()
    # define base models
    level0 = list()
    level0.append(('svm', svm_clf))
    level0.append(('rnf', rnf_clf))
    level0.append(('lda', lda_clf))
    level0.append(('lgr', lgr_clf))
    level0.append(('mlp', mlp_clf))
    # define meta learner model
    level1 = LogisticRegression()
    # For the low sample counts in the solid cohort, I had to reduce the cv to 3, othewise the mlp solver crashed
    # There are too few data points
    model = StackingClassifier(estimators=level0, final_estimator=level1, cv=3)
    return model

def get_model_dict():
    svm_clf = CalibratedClassifierCV(LinearSVC(dual=False, multi_class="ovr", verbose=False, max_iter=10000))
    mlp_clf = MLPClassifier(max_iter=1000, early_stopping=True)
    lgr_clf = LogisticRegression(multi_class="multinomial", max_iter=100000)
    rnf_clf = RandomForestClassifier(n_estimators=1000)
    lda_clf = LinearDiscriminantAnalysis()
    models = dict()
    models['svm'] = svm_clf
    models['rnf'] = rnf_clf
    models['lda'] = lda_clf
    models['lgr'] = lgr_clf
    models['mlp'] = mlp_clf
    models['stack'] = get_stacking()
    return models

def main(LineArgs):
    input_file      = LineArgs.train_expression_file
    label_file      = LineArgs.label_file
    f_format        = LineArgs.f_format
    model_type      = LineArgs.model_type
    class_file      = LineArgs.class_file
    output_prefix   = LineArgs.output_prefix

    # Use the post fSVA formatting for sample ID's, set index_col = 1
    label_df = pd.read_csv(label_file, header="infer", sep="\t", index_col = 1)
    train_df = pd.read_csv(input_file, header="infer", sep="\t", index_col = 0)
    encode_df = pd.read_csv(class_file, header="infer", sep="\t")
    encode_dict = pd.Series(encode_df.tumor_code.values, index=encode_df.tumor_class).to_dict()

    if f_format == 'gene_by_id':
        train_df = train_df.T

    df = pd.merge(train_df, label_df[['class_label']], left_index=True, right_index=True, how='left')
    train_data = np.array(df)
    X_train = train_data[:, :-1]
    y = train_data[:, -1]
    y_train = [encode_dict[x] for x in y]
    S_train = list(df.index)
    
    # Transform Input Data
    scaler = StandardScaler()
    scaler.fit(X_train)

    scaler_filename = output_prefix + '_scaler.sav'
    pickle.dump(scaler, open(scaler_filename, 'wb'))

    X_train_std = scaler.transform(X_train)

    # Get Ensemble Classifier and Train it
    model_dict = get_model_dict()
    clf = model_dict[model_type]
    clf.fit(X_train_std, y_train)

    model_filename = output_prefix + '_model.sav'
    pickle.dump(clf, open(model_filename, 'wb'))

if __name__ == '__main__':
    LineArgs = parseArguments()
    main(LineArgs)





