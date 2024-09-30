# CanID
A pan-cancer classifer for pediatric solid tumors and hematologic malignancy samples using RNA-Seq Counts.

## Description

Cancer identification (CanID) is designed a a lightweight classsification scheme without the need for GPU acceleration.  It can be run as a stand-alone classifer or integrated with classifiers using other data modalities to further improve subtyping accuracy.  As addtional tumor subtypes become available, it can be easily extended.

CanID utilizes RNAseq feature count data from protein coding genes.  The training data RNAseq counts matrix is processed sequentially through multiple steps: 1) quantile normalization, 2) batch correction using frozen surrogate variable analysis (fSVA), and 3) Principal Component Analysis (PCA) feature reduction.  The information dense PCA features inputs to train a stacked ensemble model.  CanID's output includes the predicted class along with a confidence score for the prediction.

This workflow will show how to run each step to build a classifier for your own data

## Getting Started

### Dependencies

* python: v3.10.4,  pandas: v2.0.1, numpy: v1.22.3, qnorm: v0.8.1, pickle: v4.0, sklearn: v1.1.1, scipy: v1.8.0, matplotlib: v3.7.1
* R: v4.3.1, packages: sva, limma

### Installing

* clone this github respository onto your computer

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

## Model Generation
### 1) Quantile Normalization

* list the formatted RNA-seq count files (one per line) in a .txt file, norm_list.txt
* list the training id files (one per line) for each file in the norm_list.txt



## Help

Any advise for common problems or issues.
```
command to run if program contains helper info
```

## Authors

Contributors names and contact info

ex. Dominique Pizzie  
ex. [@DomPizzie](https://twitter.com/dompizzie)

## Version History

* 0.2
    * Various bug fixes and optimizations
    * See [commit change]() or See [release history]()
* 0.1
    * Initial Release

## License

This project is licensed under the [NAME HERE] License - see the LICENSE.md file for details

## Acknowledgments

Inspiration, code snippets, etc.
* [awesome-readme](https://github.com/matiassingers/awesome-readme)
* [PurpleBooth](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)
* [dbader](https://github.com/dbader/readme-template)
* [zenorocha](https://gist.github.com/zenorocha/4526327)
* [fvcproductions](https://gist.github.com/fvcproductions/1bfc2d4aecb01a834b46)
