import pandas as pd
import numpy as np
import argparse

def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('raw_prediction_file',   help="file containing raw CanID predictions", type=str)
    parser.add_argument('output_prefix',         help="outprefix", type=str)
    args = parser.parse_args()
    return args

def build_thresh_dict():
    thresh_dict = {}
    thresh_dict['ACC']  = 0.595281
    thresh_dict['ARMS'] = 0.417000
    thresh_dict['ERMS'] = 0.642000
    thresh_dict['EWS']  = 0.841000
    thresh_dict['HB']   = 0.595281
    thresh_dict['MEL']  = 0.841000
    thresh_dict['NBL']  = 0.841000
    thresh_dict['OS']   = 0.841000
    thresh_dict['RBL']  = 0.727000
    thresh_dict['RT']   = 0.595281
    thresh_dict['SYNS'] = 0.595281
    thresh_dict['THPA'] = 0.841000
    thresh_dict['WT']   = 0.841000
    thresh_dict['AMKLGATA1'] = 0.622000
    thresh_dict['AMKLHOX']   = 0.492000
    thresh_dict['AMKLKMT2A'] = 0.565000
    thresh_dict['AMKLNUP98'] = 0.500000
    thresh_dict['AMLCBFA2T3GLIS2'] = 0.705000
    thresh_dict['AMLCBFBMYH11'] = 0.727000
    thresh_dict['AMLCEBPA'] = 0.727000
    thresh_dict['AMLETS']   = 0.483000
    thresh_dict['AMLKMT2A'] = 0.727000
    thresh_dict['AMLNPM1']  = 0.719000
    thresh_dict['AMLNUP98'] = 0.627000
    thresh_dict['AMLRUNX1RUNX1T1'] = 0.727000
    thresh_dict['AMLUBTF'] = 0.518000
    thresh_dict['BALLBCRABL1'] = 0.727000
    thresh_dict['BALLBCRABL1L'] = 0.727000
    thresh_dict['BALLDUX4IGH'] = 0.727000
    thresh_dict['BALLETV6RUNX1'] = 0.727000
    thresh_dict['BALLETV6RUNX1L'] = 0.691000
    thresh_dict['BALLHAPLO'] = 0.405000
    thresh_dict['BALLHYPER'] = 0.727000
    thresh_dict['BALLHYPO'] = 0.598000
    thresh_dict['BALLIAMP21'] = 0.727000
    thresh_dict['BALLKMT2A'] = 0.727000
    thresh_dict['BALLMEF2D'] = 0.727000
    thresh_dict['BALLNUTM1'] = 0.500000
    thresh_dict['BALLPAX5'] = 0.727000
    thresh_dict['BALLPAX5P80R'] = 0.599000
    thresh_dict['BALLTCF3PBX1'] = 0.727000
    thresh_dict['BALLZNF384'] = 0.657000
    thresh_dict['TALLBCL11B'] = 0.500000
    thresh_dict['TALLHOXA'] = 0.669000
    thresh_dict['TALLLMO2'] = 0.500000
    thresh_dict['TALLNKX2'] = 0.372000
    thresh_dict['TALLTAL1'] = 0.378000
    thresh_dict['TALLTAL2'] = 0.500000
    thresh_dict['TALLTLX1'] = 0.727000
    thresh_dict['TALLTLX3'] = 0.446000
    return thresh_dict

def final_prediction(df):
    thresh_dict = build_thresh_dict()
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
    output_prefix   = LineArgs.output_prefix

    df = pd.read_csv(pred_file, header='infer', sep="\t", index_col = 0)
    df = df[['pred_proba', 'pred_label']].copy()
    df.columns = ['Confidence_Score', 'Raw_Prediction']
    final_df = final_prediction(df)
    final_df = final_df[['Raw_Prediction', 'Confidence_Score', 'Threshold', 'Final_Prediction']]
    final_output = output_prefix + ".txt"
    final_df.to_csv(final_output, index=True, header=True, sep="\t")

if __name__ == '__main__':
    LineArgs = parseArguments()
    main(LineArgs)





