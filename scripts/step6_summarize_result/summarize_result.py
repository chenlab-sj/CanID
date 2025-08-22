import pandas as pd
import numpy as np
import argparse

def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('raw_prediction_file',   help="file containing raw CanID predictions", type=str)
    parser.add_argument('threshold_file',        help="file containing thresholds for each class", type=str)
    parser.add_argument('output_prefix',         help="outprefix", type=str)
    args = parser.parse_args()
    return args

def build_thresh_dict(threshold_file):
    thresh_df = pd.read_csv(threshold_file, header='infer', sep="\t", index_col = 0)
    thresh_dict = thresh_df['final_threshold'].to_dict()
    return thresh_dict

def final_prediction(df, threshold_file):
    thresh_dict = build_thresh_dict(threshold_file)
    scores = list(df.Confidence_Score)
    raws   = list(df.Raw_Prediction)
    final_pred = []
    thresh_list = []
    for score, raw in zip(scores, raws):
        thresh = thresh_dict[raw]
        thresh_list.append(thresh)
        if score > thresh:
            final_pred.append(raw)
        else:
            final_pred.append('Unknown')
    new_df = df.copy()
    new_df['Final_Prediction'] = final_pred
    new_df['Threshold'] = thresh_list
    return new_df

def main(LineArgs):
    pred_file       = LineArgs.raw_prediction_file
    threshold_file  = LineArgs.threshold_file
    output_prefix   = LineArgs.output_prefix

    df = pd.read_csv(pred_file, header='infer', sep="\t", index_col = 0)
    df = df[['pred_proba', 'pred_label']].copy()
    df.columns = ['Confidence_Score', 'Raw_Prediction']
    final_df = final_prediction(df, threshold_file)
    final_df = final_df[['Raw_Prediction', 'Confidence_Score', 'Threshold', 'Final_Prediction']]
    final_output = output_prefix + ".txt"
    final_df.to_csv(final_output, index=True, header=True, sep="\t")

if __name__ == '__main__':
    LineArgs = parseArguments()
    main(LineArgs)





