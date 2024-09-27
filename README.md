# CanID
A pan-cancer classifer for pediatric solid tumors and hematologic malignancy samples using RNA-Seq Counts.

## Description

Cancer identification (CanID) is designed a a lightweight classsification scheme without the need for GPU acceleration.  It can be run as a stand-alone classifer or integrated with classifiers using other data modalities to further imporve subtyping accuracy.  As addtional tumor subtypes become available, it can be easily extended.

CanID utilizes RNAseq feature count data from protein coding genes.  The training data feature count matrix was used as the raw input that is processed sequentially through multiple steps: 1) quantile normalization, 2) batch correction using frozen surrogate variable analysis (fSVA), and 3) Principal Component Analysis (PCA) feature reduction.  The information dense PCA features are used to train a stacked ensemble model.  The output includes the predicted class along with a confidence score for the prediction.    

## Getting Started

### Dependencies

* python: v3.10.4,  pandas: v2.0.1, numpy: v1.22.3, qnorm: v0.8.1, pickle: v4.0, sklearn: v1.1.1, scipy: v1.8.0, matplotlib: v3.7.1
* R: v4.3.1, packages: sva, limma

### Installing

* How/where to download your program
* Any modifications needed to be made to files/folders

### Executing program

* How to run the program
* Step-by-step bullets
```
code blocks for commands
```

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
