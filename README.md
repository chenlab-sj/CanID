# CanID
A pan-cancer classifer for pediatric solid tumors and hematologic malignancy samples using RNA-Seq Counts.

## Description

Cancer identification (CanID) is designed a a lightweight classsification scheme without the need for GPU acceleration.  It can be run as a stand-alone classifer or integrated with classifiers using other data modalities to further improve subtyping accuracy.  As addtional tumor subtypes become available, it can be easily extended.

CanID utilizes RNAseq feature count data from protein coding genes.  The training data RNAseq counts matrix is processed sequentially through multiple steps: 1) quantile normalization, 2) batch correction using frozen surrogate variable analysis (fSVA), and 3) Principal Component Analysis (PCA) feature reduction.  The information dense PCA features inputs to train a stacked ensemble model.  CanID's output includes the predicted class along with a confidence score for the prediction.

This workflow will show how to run each step to build a classifier for your own data

## Getting Started

### Installing

* Clone this github respository onto your computer
```
  git clone https://github.com/chenlab-sj/CanID.git
```
* Navigate into the CanID folder
* Build and activate the Conda environment
```
  conda env create -n CanID --file requirements.yaml
  conda activate CanID
```
* CanID primarily uses Python3, but also includes an application in R
* Make sure you run the python and R applications from the CanID conda environment
* Unpack the trained CanID models
```
   python unpack_models.sh
```

## Data Preparation
### 1) RNAseq Count Data format

* CanID uses a set of 17975 protein coding genes from Gencode v31
* Format the RNAseq Count Data to a tab-delimited gene by sample matrix
* Filter the formatted matrix to use the 17975 genes included in input_files/CanID_geneList.txt

```
sample1     sample2     sample3 ... sampleN
A1BG       49         107          29          59
ALCF        3           7           8           8
A2M     26860        6917       15878        3375
...                                           ...
ZZEF1    3508        8394        5132        2387
```

### 2) MetaData format

* Create a tab delimited text file with the following columns: sample_id, class_label, group
* Recommend 70% training and 30% testing sample split
```
sample_id     class_label     group
sample1       NBL             train
sample2       OS              train
sample3       NBL             test
...                           ...
sampleN       OS              test
```

### 3) Training ID files

* Create list of training ID's for each RNA-Seq Count Matrix used

### 4) Class Code file
* Create tab delimited file of tumor_class and tumor_code where tumor_class is the specific cancer and tumor_code is an integer value
```
tumor_class     tumor_code
ACC             0
ARMS            1
...             ...
``` 

## Model Generation: Quantile Normalization Model
### 1a) Quantile Normalization Train

* list the formatted RNA-seq count files (one per line), norm_list.txt
* list the training id files (one per line) for each file from norm_list.txt
* Execute step1a_qn_norm_v3.py
```
python step1a_qn_norm_v3.py norm_list.txt id_list.txt qn_norm_matrix_samples.txt
``` 

### 1b) Quantile Normalization Transform

* get path to formatted RNA-seq count file
* get path to qn_norm_matrix_samples.txt
* provide output file name, i.e. dataset_QN_NormMatrix_17975.txt
```
python step1b_apply_qn.py RNAseq_count_matrix.txt qn_norm_matrix_samples.txt dataset_QN_NormMatrix_17975.txt
```
## Model Generation: Frozen Surrogate Variable Batch Correction Model
### 2a) Prep Inputs
#### Train)
* Create list file of quantile normalized count matrices for training data
* Create list file of training samples for each quantile normalized count matrix
* The output of this script is a formatted phenotype file and count matrix for input into SVA algorihtm
```
python step2a_prep_train_fSVA.py qn_list.txt trainID_list.txt master_labels.txt class_code.txt train_fSVA_g17975
```
#### Test)
* create list of test sample IDs
```
python step2a_prep_test_fSVA.py quantile_normalized_count_matrix.txt testIDs.txt test_fSVA_g17975
```
### 2b) Generate SVA Model from Training Data
* The output of this script is an RData object of the leared SVA model from the training data 
```
R CMD BATCH --no-save --no-restore '--args trainPhenoFile="train_fSVA_g17975_train_pheno.txt" trainDataFile="train_fSVA_g17975_train_expression.txt" outprefix="train_fSVA_g17975"' step2b_compute_train_sva.R train_fSVA_g17975.out
```

### 2c) Transform Data using fSVA
* The output of this script is the batch corrected training matrix and
* The batch corrected test matrix
```
R CMD BATCH --no-save --no-restore '--args trainPhenoFile="train_fSVA_g17975_train_pheno.txt" trainDataFile="train_fSVA_g17975_train_expression.txt" model_file="train_fSVA_g17975_sva_model.Rdata, testDataFile="test_fSVA_g17975_test_expression.txt outprefix="test_fSVA_g17975"' step2c_run_fsva.R test_fSVA_g17975.out
```

## Model Generation: Principal Component Feature Reduction Model
### 3a) PCA Reduction Fit
Output of this step:
* PCA model file (.pickle) used to transform unseen test data to the same feature space as the training data
* Transformed training data (.txt) - sample_name by PCA_Features
```
python step3a_pca_train.py output_step2c.txt fraction_variance_explained output_prefix
python step3a_pca_train.py train_fSVA_g17975.txt 0.70 train_pca70_g17975
```
### 3b) PCA Reduction Transform
```
python step3b_pca_transform.py test_matrix_step2c.txt pca_model.pickle output_prefix
python step3b_pca_transform.py test_fSVA_g17975.txt train_pca70_g17975.pickle test_pca70_g17975
```
## Model Generation: Stacked Ensemble Classification Model
### 4a) Model Fit
```
python step4a_stacked_model_train.py pca_transformed_train_matrix.txt metadata.txt id_by_gene stack class_code.txt output_prefix
```
### 4a) Model Predict
```
python step4b_stacked_model_predict.py pca_transformed_test_matrix.txt trained_model.sav scaling.sav class_code.txt output_prefix
```
## Authors

* Daniel Putnam    Daniel.Putnam@stjude.org
* Xiang Chen       Xiang.Chen@stjude.org

## Version History

* 0.1
    * Initial Release

## License
Copyright 2024 St. Jude Children's Research Hospital

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
