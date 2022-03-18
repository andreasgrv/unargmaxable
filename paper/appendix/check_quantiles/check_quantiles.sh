#!/bin/bash
trap "exit" INT

NUM_LINES=10000000

python check_quantiles.py --data /mnt/universe/models/mt/opus/bul-eng/data/ --model 'Helsinki-NLP/opus-mt-bg-en' --device cuda:0 --num-lines $NUM_LINES
python check_quantiles.py --data /mnt/universe/models/mt/opus/eng-rus/data/ --model 'Helsinki-NLP/opus-mt-en-ru' --device cuda:0 --num-lines $NUM_LINES


#      Results bg-en
# Min values range [-37.45, -9.39]
# Max values range [12.12, 40.31]
# Minimum overall: -57.473873
# Maximum overall: 58.872795
# Loading model Helsinki-NLP/opus-mt-en-ru...
# Processing 10000000 lines...
# 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 10000000/10000000 [2:36:00<00:00, 1068.27it/s]
#      Results en-ru
# Min values range [-41.62, -9.87]
# Max values range [10.87, 36.45]
# Minimum overall: -95.357574
# Maximum overall: 94.423370
