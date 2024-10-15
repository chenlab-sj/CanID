#!/bin/bash
  
BASE_DIR=$PWD
cd models
tar -xvzf heme_pca85_CanID_model.tar.gz
tar -xvzf heme_pca85_model.tar.gz
rm heme_pca85_CanID_model.tar.gz
rm heme_pca85_model.tar.gz
