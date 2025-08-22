#!/usr/bin/env nextflow

/*
 * Pipeline Parameters
 */

// Version History
// v1: Initial pipepline

params.fsva_method = params.fsva_method ?: 'exact'
println "FSVA Method (after initialization): ${params.fsva_method}"

if (params.modeltype == 'ST'){
    globalGeneList     = "${params.basedir}/input_files/CanID_geneList.txt"
    globalQNModel      = "${params.basedir}/models/ST_QN_trained_model.txt"
    globalBNExpression = "${params.basedir}/intermediate_files/ST_train_expression.txt"
    globalBNPheno      = "${params.basedir}/intermediate_files/ST_train_masked_pheno.txt"
    globalBNModel      = "${params.basedir}/models/ST_SVA_Model_sva_model.Rdata"
    globalPCAModel     = "${params.basedir}/models/ST_train_pca80.pickle"
    globalCanIDScalar  = "${params.basedir}/models/ST_train_CanID_pca80_scaler.sav"
    globalCanIDModel   = "${params.basedir}/models/ST_train_CanID_pca80_model.sav"
    globalClassCode    = "${params.basedir}/input_files/CanID_ST_class_code.txt"
} else if (params.modeltype == 'HM'){
    globalGeneList     = "${params.basedir}/input_files/CanID_geneList.txt"
    globalQNModel      = "${params.basedir}/models/HM_QN_trained_model.txt"
    globalBNExpression = "${params.basedir}/intermediate_files/HM_train_expression.txt"
    globalBNPheno      = "${params.basedir}/intermediate_files/HM_train_masked_pheno.txt"
    globalBNModel      = "${params.basedir}/models/HM_SVA_Model_sva_model.Rdata"
    globalPCAModel     = "${params.basedir}/models/HM_train_pca85.pickle"
    globalCanIDScalar  = "${params.basedir}/models/HM_train_CanID_pca85_scaler.sav"
    globalCanIDModel   = "${params.basedir}/models/HM_train_CanID_pca85_model.sav"
    globalClassCode    = "${params.basedir}/input_files/CanID_HM_class_code.txt"
} else {
    globalGeneList     = params.genelist ?: 'missing'
    globalQNModel      = params.qnmodel ?: 'missing'
    globalBNExpression = params.bnexpression ?: 'missing'
    globalBNPheno      = params.bnpheno ?: 'missing'
    globalBNModel      = params.bnmodel ?: 'missing'
    globalPCAModel     = params.pcamodel ?: 'missing'
    globalCanIDScalar  = params.canidscalar ?: 'missing'
    globalCanIDModel   = params.canidmodel ?: 'missing'
    globalClassCode    = params.classcode ?: 'missing'
}

if (params.fsva_method == 'fast'){
    globalFSVAscript   = 'run_fsva.R' 
} else {
    globalFSVAscript   = 'run_exact_fsva.R'
}

process step0_genefilter {

   publishDir "${params.basedir}/output_files/${params.prefix}/intermediate_files", mode: 'copy'

   input:
      path inputfile
      val prefix
      val basedir
      path genelist

   output:
      path "${prefix}_filtered.txt"

   script:
   """
   python ${basedir}/scripts/step0_raw_count_prep/step0_filter_genes.py ${inputfile} ${genelist} ${prefix}_filtered.txt
   """
}

process step1_applyQN {

   publishDir "${params.basedir}/output_files/${params.prefix}/intermediate_files", mode: 'copy'

   input:
      val prefix
      val basedir
     path inputfile
     path qnmodel

   output:
      path "${prefix}_qn.txt"

   script:
   """
   python ${basedir}/scripts/step1_quantile_norm/apply_QN.py ${inputfile} ${qnmodel} ${prefix}_qn.txt
   """
}

process step2_applyBN {

   publishDir "${params.basedir}/output_files/${params.prefix}/intermediate_files", mode: 'copy'

   input:
      val prefix
      val basedir
      path inputfile
      path phenofile
      path expressionfile
      path modelfile
      val fsvascript

   output:
      path "${prefix}_bn_test.txt", emit: canid_test

   script:
   """
   # Call R script with named arguments
   R CMD BATCH --no-save --no-restore \\
      '--args trainPhenoFile="${phenofile}" trainDataFile="${expressionfile}" model_file="${modelfile}" testDataFile="${inputfile}" testprefix="${prefix}" trainprefix="CANID"' \\
      ${basedir}/scripts/step2_batch_correction/${fsvascript} ${prefix}_CANID_exact_fsva.out
   """
   
}

process step3_applyPCA {

   publishDir "${params.basedir}/output_files/${params.prefix}/intermediate_files", mode: 'copy'

   input:
      val prefix
      val basedir
     path inputfile
     path pcamodel

   output:
      path "${prefix}_pca.txt"

   script:
   """
   python ${basedir}/scripts/step3_feature_selection/pca_transform.py ${inputfile} ${pcamodel} ${prefix}_pca
   """
}

process step4_applyCanID {

   publishDir "${params.basedir}/output_files/${params.prefix}/intermediate_files", mode: 'copy'

   input:
      val prefix
      val basedir
     path inputfile
     path model
     path scalar
     path classcode

   output:
      path "${prefix}_CanID_prediction.txt"

   script:
   """
   python ${basedir}/scripts/step5_class_prediction/run_model.py ${inputfile} id_by_gene ${model} ${scalar} ${classcode}  ${prefix}_CanID_prediction
   """
}

process step5_filterCanID {

   publishDir "${params.basedir}/output_files/${params.prefix}/results", mode: 'copy'

   input:
      val prefix
      val basedir
     path inputfile

   output:
      path "${prefix}_CanID_Final_prediction.txt"

   script:
   """
   python ${basedir}/scripts/step6_summarize_result/summarize_result.py ${inputfile} ${prefix}_CanID_Final_prediction
   """
}

workflow {
    // create a channels for inputs
    inputfile_ch      = Channel.of(params.inputfile)
    prefix_ch         = Channel.of(params.prefix)
    basedir_ch        = Channel.of(params.basedir)
    genelistfile_ch   = Channel.of(globalGeneList)
    qnmodel_ch        = Channel.of(globalQNModel)
    bnexpression_ch   = Channel.of(globalBNExpression)
    bnpheno_ch        = Channel.of(globalBNPheno)
    bnmodel_ch        = Channel.of(globalBNModel)
    pcamodel_ch       = Channel.of(globalPCAModel)
    canidscalar_ch    = Channel.of(globalCanIDScalar)
    canidmodel_ch     = Channel.of(globalCanIDModel)
    classcode_ch      = Channel.of(globalClassCode)
    fsvascript_ch     = Channel.of(globalFSVAscript)

    // run step0
    step0_genefilter(inputfile_ch, prefix_ch, basedir_ch, genelistfile_ch)

    // run step1 apply QN
    step1_applyQN(prefix_ch, basedir_ch, step0_genefilter.out, qnmodel_ch)
    
    // run step2 apply BN
    step2_applyBN(prefix_ch, basedir_ch, step1_applyQN.out, bnpheno_ch, bnexpression_ch, bnmodel_ch, fsvascript_ch)

    // run step3 apply PCA
    step3_applyPCA(prefix_ch, basedir_ch, step2_applyBN.out.canid_test, pcamodel_ch)

    // run step4 apply CanID
    step4_applyCanID(prefix_ch, basedir_ch, step3_applyPCA.out, canidmodel_ch, canidscalar_ch, classcode_ch)

    // run step5 filter CanID
    step5_filterCanID(prefix_ch, basedir_ch, step4_applyCanID.out)

}
