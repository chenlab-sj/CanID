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
    parser.add_argument('test_expression_file',  help="file containing test RNA-Seq expression matrix", type=str)
    parser.add_argument('f_format',              help="(id_by_gene, vs. gene_by_id)", type=str)
    parser.add_argument('model_file',            help="trained model saved to pickle object", type=str)
    parser.add_argument('scaler_file',           help="trained scaler saved to pickle object", type=str)
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
    model = StackingClassifier(estimators=level0, final_estimator=level1, cv=5)
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


def generate_class_dict(encode_dict):
    return {v:k for k,v in encode_dict.items()}

def main(LineArgs):
    input_file      = LineArgs.test_expression_file
    f_format        = LineArgs.f_format
    model_file      = LineArgs.model_file
    scaler_file     = LineArgs.scaler_file
    class_file      = LineArgs.class_file
    output_prefix   = LineArgs.output_prefix

    test_df  = pd.read_csv(input_file, header="infer", sep="\t", index_col = 0)
    test_df = test_df.astype('float')
    encode_df = pd.read_csv(class_file, header="infer", sep="\t")
    encode_dict = pd.Series(encode_df.tumor_code.values, index=encode_df.tumor_class).to_dict()

    if f_format == 'gene_by_id':
        test_df = test_df.T

    # Prepare test data
    X_test = np.array(test_df)
    X_test = X_test.astype('float64')
    S_test = list(test_df.index)

    # Scale Test data using same scaler from Training data
    scaler = pickle.load(open(scaler_file, 'rb'))
    X_test_std = scaler.transform(X_test)

    # Load the Classifier
    clf = pickle.load(open(model_file, 'rb'))
    
    y_test_pred = np.zeros(X_test_std.shape[0])
    y_test_proba = np.zeros(X_test_std.shape[0])

    for i in range(X_test_std.shape[0]):
        print(i)
        X_single = X_test_std[[i]]
        y_test_pred[i] = clf.predict(X_single)
        y_proba = clf.predict_proba(X_single)
        y_test_proba[i] = y_proba.max()

    class_dict = generate_class_dict(encode_dict)
    test_df['pred_class'] = y_test_pred
    test_df['pred_proba'] = y_test_proba

    # convert predictions to int
    test_df['pred_class'] = test_df['pred_class'].astype('int')

    pred_class = list(test_df['pred_class'].values)
    pred_labels = [class_dict[x] for x in pred_class]
    test_df['pred_label'] = pred_labels
    
    final_output = output_prefix + ".txt"
    test_df.to_csv(final_output, sep="\t", header=True, index=True)

if __name__ == '__main__':
    LineArgs = parseArguments()
    main(LineArgs)





