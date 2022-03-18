#!/bin/bash
trap "exit" INT
shopt -s nullglob

# Download the language pair folders following instructions from http://data.statmt.org/wmt17_systems/
# place the folders at a path of your choice.
# then adapt the MODEL_PATH below to point to that folder.
export MODEL_PATH=''

if [[ ! $MODEL_PATH ]]
then
	echo "MODEL_PATH not set, please read instruction in this script"
	exit
fi

########################################################################
############################ MT MODEL TESTING ##########################
########################################################################
models=(
en-cs
cs-en
en-de
de-en
en-ru
ru-en
en-tr
tr-en
en-zh
zh-en
lv-en
)

for model in ${models[@]};
do
	vocab="$MODEL_PATH/$model/vocab.${model:3:2}.json"
	for path in "$MODEL_PATH/$model/"*".npz"
	do
		echo -e "Running model $path ...\n"
		stollen_numpy --numpy-file $path --W 'Wemb_dec' --b 'ff_logit_b' --vocab $vocab --patience 2500 --exact-algorithm lp_chebyshev --save-db
	done
done
