#!/bin/bash
  
##########################################
# unpack the intermediate files
##########################################

# HM Expression File
cat ./intermediate_files/HM_store/HM_train.tar.gz.part-* | tar -xzf - -C ./intermediate_files 

# ST Expression File
cat ./intermediate_files/ST_store/ST_train.tar.gz.part-* | tar -xzf - -C ./intermediate_files 

# HM PCA Model
cat ./models/HM_store/pca_model/HM_train_pca85.pickle.tar.gz.part-* | tar -xzf - -C ./models

# HM CanID Model
cat ./models/HM_store/CanID_model/HM_train_CanID_pca85_model.tar.gz.part-* | tar -xzf - -C ./models

