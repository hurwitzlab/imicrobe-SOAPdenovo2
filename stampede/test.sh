#!/bin/bash

#SBATCH -A iPlant-Collabs
#SBATCH -N 1
#SBATCH -n 16
#SBATCH -t 00:30:00
#SBATCH -p development
#SBATCH -J test-imicrobe-soapdenovo2
#SBATCH --mail-type BEGIN,END,FAIL
#SBATCH --mail-user jklynch@email.arizona.edu

module load irods

INPUT_DIR="$SCRATCH/imicrobe-soapdenovo2/test/input"
if [[ -d $INPUT_DIR ]]; then
  rm -rf $INPUT_DIR
fi

mkdir -p $INPUT_DIR
iget /iplant/home/shared/iplant_training/genome_assembly_soapdenovo/A_Assemble_Reads/fragScSi_1.fq $INPUT_DIR
iget /iplant/home/shared/iplant_training/genome_assembly_soapdenovo/A_Assemble_Reads/fragScSi_2.fq $INPUT_DIR
iget /iplant/home/jklynch/test/imicrobe-soapdenovo2/test.config $INPUT_DIR
INPUT_FILE_1=$INPUT_DIR/fragScSi_1.fq
INPUT_FILE_2=$INPUT_DIR/fragScSi_2.fq
CONFIG_FILE=$INPUT_DIR/test.config

OUT_DIR="$SCRATCH/imicrobe-soapdenovo2/test/output"

if [[ -d $OUT_DIR ]]; then
  rm -rf $OUT_DIR
fi

mkdir -p $OUT_DIR

./run.sh $CONFIG_FILE -o $OUT_DIR -q1 $INPUT_FILE_1 -q2 $INPUT_FILE_2
