#!/bin/bash
  
##########################################
# unpack the intermediate files
##########################################
mkdir -p ./intermediate_files/build

# HM Expression File
for file in ./intermediate_files/HM_store/HM*.tar.gz; do
    tar -xvzf "$file" -C ./intermediate_files/HM_store/build
done

cat ./intermediate_files/HM_store/build/HM_part_{00..17} > ./intermediate_files/HM_train_expression.txt
rm ./intermediate_files/HM_store/build/HM_part_??
rmdir ./intermediate_files/HM_store/build

# ST Expression File
for file in ./intermediate_files/ST_store/ST*.tar.gz; do
    tar -xvzf "$file" -C ./intermediate_files/ST_store/build
done

cat ./intermediate_files/ST_store/build/ST_part_{00..17} > ./intermediate_files/ST_train_expression.txt
rm ./intermediate_files/ST_store/build/ST_part_??
rmdir ./intermediate_files/ST_store/build

##########################################
# unpack the HM pca model
##########################################

cat ./models/HM_pca85_part_{00..04} > ./models/HM_train_pca85.pickle
