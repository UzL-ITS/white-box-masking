#!/bin/sh
echo "########## Verification ##########"
python gadget_trace.py
/home/oseker/SageMath/sage gadget_check.py traces/hybrid


