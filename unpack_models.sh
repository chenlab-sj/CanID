#!/bin/bash
  
##########################################
# unpack the intermediate files
##########################################
mkdir -p ./intermediate_files/build

# HM Expression File
for file in ./intermediate_files/HM*.tar.gz; do
    tar -xvzf "$file" -C ./intermediate_files/build
done

cat ./intermediate_files/build/HM_part_{00..17} > ./intermediate_files/build/HM_train_expression.txt
rm ./intermediate_files/build/HM_part_??

# ST Expression File
for file in ./intermediate_files/ST*.tar.gz; do
    tar -xvzf "$file" -C ./intermediate_files/build
done

cat ./intermediate_files/build/ST_part_{00..17} > ./intermediate_files/build/ST_train_expression.txt
rm ./intermediate_files/build/ST_part_??

# Place Final file in intermediate files directory
mv ./intermediate_files/build/*.txt ./intermediate_files
rmdir ./intermediate_files/build

##########################################
# unpack the HM pca model
##########################################

cat ./models/HM_pca85_part_{00..04} > ./models/HM_train_pca85.pickle
