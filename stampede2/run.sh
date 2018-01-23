#!/bin/bash

module load tacc-singularity

echo "$@"

SOAPDENOVO2_CMD_LINE_ARGS=`singularity exec imicrobe-soapdenovo2.img python3 /scripts/agave_to_soapdenovo2_cmd_line_args.py $@`

echo "SOAPdenovo2 command line args: \"${SOAPDENOVO2_CMD_LINE_ARGS}\""
echo "SOAPdenovo2 configuration file:"
cat $2

singularity run imicrobe-soapdenovo2.img ${SOAPDENOVO2_CMD_LINE_ARGS}
