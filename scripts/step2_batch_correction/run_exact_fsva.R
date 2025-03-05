library(sva)
library(limma)

##########################################################i#############################################################################
#  module load R/4.3.1-shlib                                                                                                           #
#                                                                                                                                      #
#  Commandline Example to run fSVA estimate:                                                                                           #
#  R CMD BATCH --no-save --no-restore '--args trainPhenoFile="pheno_file"  trainDataFile="QN_normalized_train_file"                    #
#    model_file="SVA_model" testDataFile="QN_normalized_test_file" testprefix="solid_sjInternal" trainprefix="ST"  run_fSVA.R fSVA.out #
#                                                                                                                                      #
########################################################################################################################################

args=(commandArgs(TRUE))

if(length(args)==0){
   print("No arguments supplied. Try again")
   quit(save = "no", status = 1, runLast = TRUE)
} else {
    for(i in 1:length(args)){
        eval(parse(text=args[[i]]))
    }
}

trainPheno = read.table(trainPhenoFile, header=T)
trainData  = read.table(trainDataFile, header=T)
trainMatrix = data.matrix(trainData)

testData = read.table(testDataFile, header=T)
testMatrix = data.matrix(testData)

trainMod  = model.matrix(~cancer, data=trainPheno)
trainMod0 = model.matrix(~1,data=trainPheno)

load(model_file)

fsvaobj = fsva(trainMatrix, trainMod, trainSv, testMatrix, method = "exact")

train_output = paste(trainprefix, "_bn_train.txt", sep="")
test_output  = paste(testprefix, "_bn_test.txt", sep="")

write.table(fsvaobj$db, train_output, sep="\t", row.names=TRUE, quote=FALSE)
write.table(fsvaobj$new, test_output, sep="\t", row.names=TRUE, quote=FALSE)

# fsvaobj contains:
# 1) db:  An adjusted version of the training database where the effect of batch/expression heterogeneity has been removed
# 2) new: An adjusted version of the new samples, adjusted one at a time using the fsva methodology
# 3) newsv: Surrogate variables for the new samples
quit(save = "no", status = 0, runLast = TRUE)
