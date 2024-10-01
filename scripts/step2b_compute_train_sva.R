library(sva)
library(limma)

##########################################################i##########################################################
#                                                                                                                   #
#                                                                                                                   #
#  Commandline Example to run fSVA estimate:                                                                        #
#  R CMD BATCH --no-save --no-restore '--args trainPhenoFile="pheno_file"  trainDataFile="QN_normalized_train_file" #
#     outprefix="solid_sjInternal"' compute_train_sva.R train_SVA.out                                               #
#                                                                                                                   #
#####################################################################################################################

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

trainMod  = model.matrix(~cancer, data=trainPheno)
trainMod0 = model.matrix(~1,data=trainPheno)
trainSv   = sva(trainMatrix,trainMod,trainMod0)

sva_output = paste(outprefix, "_sva_model.Rdata", sep="")
save(trainSv, file=sva_output)

quit(save = "no", status = 0, runLast = TRUE)
