#!/bin/bash

echo "Started $(date)"

echo "CONFIG_FILE             \"${CONFIG_FILE}\""
echo "OUTPUT_GRAPH_PREFIX     \"${OUTPUT_GRAPH_PREFIX}\""
echo "SINGLE_END_FA           \"${SINGLE_END_FA}\""
echo "SINGLE_END_FQ           \"${SINGLE_END_FQ}\""
echo "PAIRED_END_COMBINED_FA  \"${PAIRED_END_COMBINED_FA}\""
echo "PAIRED_END_COMBINED_BAM \"${PAIRED_END_COMBINED_BAM}\""
echo "FORWARD_FA              \"${FORWARD_FA}\""
echo "REVERSE_FA              \"${REVERSE_FA}\""
echo "FORWARD_FQ              \"${FORWARD_FQ}\""
echo "REVERSE_FQ              \"${REVERSE_FQ}\""

sh run.sh \
    ${CONFIG_FP} \
    --output-dir `pwd` \
    ${OUTPUT_GRAPH_PREFIX} \
    ${SINGLE_END_FA} \
    ${SINGLE_END_FQ} \
    ${PAIRED_END_COMBINED_FA} \
    ${PAIRED_END_COMBINED_BAM} \
    ${FORWARD_FA} \
    ${REVERSE_FA} \
    ${FORWARD_FQ} \
    ${REVERSE_FQ}

echo "Ended $(date)"
exit 0
