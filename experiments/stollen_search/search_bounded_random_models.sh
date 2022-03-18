#!/bin/bash
trap "exit" INT
shopt -s nullglob


# Adapt below if needed
export MODEL_PATH="../create_random_models/models"


for model in "$MODEL_PATH/"*.npz;
do
	vocabfile="${model/.npz/-vocab.json}"
	stollen_numpy --numpy-file $model --W 'W' --b 'b' --vocab $vocabfile \
	   	--patience 2500 --exact-algorithm lp_chebyshev --save-db
done
