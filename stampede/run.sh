#!/bin/bash

module load singularity

INPUT_DIR=$1
OUTPUT_DIR=$2

echo "starting directory : `pwd`"
echo "`ls -l`"
echo "input directory    : ${INPUT_DIR}"
echo "output directory   : ${OUTPUT_DIR}"

export LAUNCHER_DIR="$HOME/src/launcher"
export LAUNCHER_PLUGIN_DIR=$LAUNCHER_DIR/plugins
export LAUNCHER_WORKDIR=${OUTPUT_DIR}
export LAUNCHER_RMI=SLURM

export LAUNCHER_JOB_FILE=`pwd`/launcher_jobfile_${SLURM_JOB_ID}
echo ${LAUNCHER_JOB_FILE}
singularity exec imicrobe-SOAPdenovo2.img /SOAPdenovo2-r241/SOAPdenovo-63mer \
   -s ${CONFIG_FILE} \
   -K ${kmer} \
   -o ${OUTPUT_DIR}

sleep 10
export LAUNCHER_PPN=2

$LAUNCHER_DIR/paramrun
echo "Ended launcher"
