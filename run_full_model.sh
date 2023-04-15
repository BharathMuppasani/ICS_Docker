#!/bin/bash
cd /home/src/Agent-Factory
# Run script.sh from Agent-Factory directory
bash script.sh

cd /home/netlogo
# Run netlogo-headw.sh with NLModel.nlogo from netlogo directory
bash netlogo-headw.sh /home/src/Netlogo-Model/NLModel.nlogo
