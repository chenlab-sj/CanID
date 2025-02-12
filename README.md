# CanID
A pan-cancer classifer for pediatric solid tumors and hematologic malignancy samples using RNA-Seq Counts.

## Description

Cancer identification (CanID) is designed a a lightweight classsification scheme without the need for GPU acceleration.  It can be run as a stand-alone classifer or integrated with classifiers using other data modalities to further improve subtyping accuracy.  As addtional tumor subtypes become available, it can be easily extended.

CanID utilizes RNAseq feature count data from protein coding genes.  The training data RNAseq counts matrix is processed sequentially through multiple steps: 1) quantile normalization, 2) batch correction using frozen surrogate variable analysis (fSVA), and 3) Principal Component Analysis (PCA) feature reduction.  The information dense PCA features inputs to train a stacked ensemble model.  CanID's output includes the predicted class along with a confidence score for the prediction.

This workflow will show how to run each step to build a classifier for your own data.
Seperate classifiers were built for solid tumor and hematalogic malignacy disease types.

## Getting Started

### Installing on Linux or Mac

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
   sh unpack_models.sh
```
* Warning: The python models are stored as pickle files
* The tutorial below will show how to build your own models

* CanID is setup to run using a nextflow pipeline
* Make sure to have nextflow version: 23.04.1 or greater

## RNAseq Count Data Format

* CanID uses a set of 17975 protein coding genes from Gencode v31
* Format the RNAseq Count Data to a tab-delimited gene by sample matrix
* Filter the formatted matrix to use the 17975 genes included in input_files/CanID_geneList.txt

```
        sample1     sample2     sample3 ... sampleN
A1BG         49         107          29          59
ALCF          3           7           8           8
A2M       26860        6917       15878        3375
...                                             ...
ZZEF1      3508        8394        5132        2387
```

## Train Custom model
The Input RNASeq Matrix must be transformed through a series of data transformations using pretraining models before being passed to the Ensemble Classifier
```
# Train Model (from the nextflow folder)
set -e
nextflow train_model.nf --inputfile ['raw_counts_file'] --prefix ['file_prefix'] --basedir ['path_to_repository'] --classcode ['class_code_file'] --labels ['label_file'] --variance ['variance_explained'] -resume
```

## Make a Prediction using SJ Model
```
set -e
nextflow make_prediction.nf --inputfile ['raw_counts_file'] --fsva_method ['exact' or 'fast'] --prefix ['file_prefix'] --basedir ['path_to_repository'] --modeltype ['ST' or 'HM'] -resume
```
## Make a Prediction using Custom Model
```
set -e
nextflow make_prediction.nf --inputfile ['raw_counts_file'] --fsva_method ['exact' or 'fast'] --prefix ['file_prefix'] --basedir ['path_to_repository'] --modeltype ['CUSTOM'] --genelist ['genelist'] --qnmodel ['qn_model'] --bnexpression ['bn_expression_file'] --bnpheno ['bn_pheno_file'] --bnmodel ['bn_model_file'] --pcamodel ['pca_model_file'] --canidscaler ['canid_scalar_file'] -- canidmodel ['canid_model_file'] classcode ['class_code_file'] -resume
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
