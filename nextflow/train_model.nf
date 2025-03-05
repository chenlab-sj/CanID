#!/usr/bin/env nextflow

/*
 * Pipeline Parameters
 */

// Version History
// v1: Initial pipepline

params.fsva_method = params.fsva_method ?: 'exact'
println "FSVA Method (after initialization): ${params.fsva_method}"

globalFSVAscript   = 'run_exact_fsva.R'

process step0_generateBasis {

   publishDir "${params.basedir}/custom/${params.prefix}/intermediate_files", mode: 'copy'

   input:
      path inputfile
      val prefix
      val basedir

   output:
      path "${prefix}_genelist.txt"


   script:
   """
   python ${basedir}/scripts/step0_raw_count_prep/step0_generate_basis.py ${inputfile} ${prefix}_genelist.txt
   """
}

process step1a_trainQN {

   publishDir "${params.basedir}/custom/${params.prefix}/models", mode: 'copy'

   input:
      val prefix
      val basedir
     path inputfile

   output:
      path "${prefix}_qn_model.txt"

   script:
   """
   python ${basedir}/scripts/step1_quantile_norm/train_QN.py ${inputfile} ${prefix}_qn_model.txt
   """
}
  
process step1b_applyQN {

   publishDir "${params.basedir}/custom/${params.prefix}/intermediate_files", mode: 'copy'

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

process step2a_prepBN {

   publishDir "${params.basedir}/custom/${params.prefix}/intermediate_files", mode: 'copy'

   input:
      val prefix
      val basedir
      path inputfile
      path labelfile
      path classfile

   output:
      path "${prefix}_train_pheno.txt", emit: pheno
      path "${prefix}_train_expression.txt", emit: expression
      path "${prefix}_dummy_test.txt", emit: test

   script:
   """
   python ${basedir}/scripts/step2_batch_correction/prep_fSVA.py ${inputfile} ${labelfile} ${classfile} ${prefix}
   """
   
}

process step2b_trainBN {

   publishDir "${params.basedir}/custom/${params.prefix}/models", mode: 'copy'

   input:
      val prefix
      val basedir
      path phenofile
      path expressionfile

   output:
      path "${prefix}_sva_model.Rdata"

   script:
   """
   # Call R script with named arguments
   R CMD BATCH --no-save --no-restore \\
      '--args trainPhenoFile="${phenofile}" trainDataFile="${expressionfile}"  outprefix="${prefix}"' \\
      ${basedir}/scripts/step2_batch_correction/compute_train_sva.R ${prefix}_sva_model.out
   """
   
}

process step2c_applyBN {

   publishDir "${params.basedir}/custom/${params.prefix}/intermediate_files", mode: 'copy'

   input:
      val prefix
      val basedir
      path phenofile
      path expressionfile
      path modelfile
      path testfile
      val fsvascript

   output:
      path "${prefix}_bn_train.txt"

   script:
   """
   # Call R script with named arguments
   R CMD BATCH --no-save --no-restore \\
      '--args trainPhenoFile="${phenofile}" trainDataFile="${expressionfile}" model_file="${modelfile}" testDataFile="${testfile}" testprefix="dummy" trainprefix="${prefix}"' \\
      ${basedir}/scripts/step2_batch_correction/${fsvascript} ${prefix}_fsva.out
   rm dummy_bn_test.txt
   """
  
}

process step3a_trainPCA {

   publishDir "${params.basedir}/custom/${params.prefix}/models", mode: 'copy'

   input:
      val prefix
      val basedir
     path inputfile
      val variance

   output:
      path "${prefix}_${variance.toString()}_pca_model.pickle"

   script:
   """
   python ${basedir}/scripts/step3_feature_selection/pca_train.py ${inputfile} ${variance} ${prefix}_${variance.toString()}_pca_model
   """
}

process step3b_applyPCA {

   publishDir "${params.basedir}/custom/${params.prefix}/intermediate_files", mode: 'copy'

   input:
      val prefix
      val basedir
     path inputfile
     path pcamodel
      val variance

   output:
      path "${prefix}_${variance.toString()}_pca_features.txt"

   script:
   """
   python ${basedir}/scripts/step3_feature_selection/pca_transform.py ${inputfile} ${pcamodel} ${prefix}_${variance.toString()}_pca_features
   """
}

process step4_trainCanID {

   publishDir "${params.basedir}/custom/${params.prefix}/models", mode: 'copy'

   input:
      val prefix
      val basedir
     path inputfile
     path labelfile
     path classfile
      val variance

   output:
      path "${prefix}_${variance.toString()}_CanID_scaler.sav"
      path "${prefix}_${variance.toString()}_CanID_model.sav"
  

   script:
   """
   python ${basedir}/scripts/step4_ensemble_training/train_all_stacking_cv3.py ${inputfile} ${labelfile} id_by_gene stack ${classfile} ${prefix}_${variance.toString()}_CanID
   """
}

workflow {
    // create a channels for inputs
    inputfile_ch      = Channel.of(params.inputfile)
    prefix_ch         = Channel.of(params.prefix)
    basedir_ch        = Channel.of(params.basedir)
    variance_ch       = Channel.of(params.variance)
    labels_ch         = Channel.of(params.labels)
    classcode_ch      = Channel.of(params.classcode)
    fsvascript_ch     = Channel.of(globalFSVAscript)

    // run step0
    step0_generateBasis(inputfile_ch, prefix_ch, basedir_ch)

    // run step1a train QN
    step1a_trainQN(prefix_ch, basedir_ch, inputfile_ch)
    
    // run step1b apply QN
    step1b_applyQN(prefix_ch, basedir_ch, inputfile_ch, step1a_trainQN.out)

    // run step2a prep BN
    step2a_prepBN(prefix_ch, basedir_ch, step1b_applyQN.out, labels_ch, classcode_ch)

    // run step2b train BN
    step2b_trainBN(prefix_ch, basedir_ch, step2a_prepBN.out.pheno, step2a_prepBN.out.expression)
    
    // run step2c apply BN
    step2c_applyBN(prefix_ch, basedir_ch, step2a_prepBN.out.pheno, step2a_prepBN.out.expression, step2b_trainBN.out, step2a_prepBN.out.test, fsvascript_ch)

    // run step3a train PCA
    step3a_trainPCA(prefix_ch, basedir_ch, step2c_applyBN.out, variance_ch)
    
    // run step3b apply PCA
    step3b_applyPCA(prefix_ch, basedir_ch, step2c_applyBN.out, step3a_trainPCA.out, variance_ch)

    // run step4 train CanID
    step4_trainCanID(prefix_ch, basedir_ch, step3b_applyPCA.out, labels_ch, classcode_ch, variance_ch)
}
