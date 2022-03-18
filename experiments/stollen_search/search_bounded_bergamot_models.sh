#!/bin/bash
trap "exit" INT

# Download the language pair models following instructions from https://github.com/browsermt/students
# place the folders at a path of your choice.
# then point the MODEL_PATH below to that folder.
export MODEL_PATH=''

if [[ ! $MODEL_PATH ]]
then
	echo "MODEL_PATH not set, please read instruction in this script"
	exit
fi

########################################################################
############################ MT MODEL TESTING ##########################
########################################################################
teachers=(
"$MODEL_PATH/esen/esen.teacher.bigx2/model1.npz"
"$MODEL_PATH/esen/esen.teacher.bigx2/model2.npz"
"$MODEL_PATH/esen/enes.teacher.bigx2/model1.npz"
"$MODEL_PATH/esen/enes.teacher.bigx2/model2.npz"
"$MODEL_PATH/eten/eten.teacher.bigx2/model1.npz"
"$MODEL_PATH/eten/eten.teacher.bigx2/model2.npz"
"$MODEL_PATH/eten/enet.teacher.bigx2/model1.npz"
"$MODEL_PATH/eten/enet.teacher.bigx2/model2.npz"
"$MODEL_PATH/nben/nben.teacher.base/model.npz"
"$MODEL_PATH/nnen/nnen.teacher.base/model.npz"
"$MODEL_PATH/isen/isen.teacher.base/model.npz"
)

for model in ${teachers[@]};
do
	langpair="$(echo "$model" | awk -F/ '{print $(NF-2)}')"
	modeldir="$(dirname "$model")"
	vocabfile="$modeldir/vocab.$langpair.spm"
	echo -e "Running model $model ...\n"
	stollen_numpy --numpy-file $model --W 'Wemb' --b 'decoder_ff_logit_out_b' --vocab $vocabfile \
	   	--patience 2500 --exact-algorithm lp_chebyshev --save-db
done

students=(
"$MODEL_PATH/csen/csen.student.base/model.npz"
"$MODEL_PATH/csen/csen.student.tiny11/model.npz"
"$MODEL_PATH/csen/encs.student.base/model.npz"
"$MODEL_PATH/csen/encs.student.tiny11/model.npz"
"$MODEL_PATH/deen/ende.student.base/model.npz"
"$MODEL_PATH/deen/ende.student.tiny11/model.npz"
"$MODEL_PATH/esen/esen.student.tiny11/model.npz"
"$MODEL_PATH/esen/enes.student.tiny11/model.npz"
"$MODEL_PATH/eten/eten.student.tiny11/model.npz"
"$MODEL_PATH/eten/enet.student.tiny11/model.npz"
"$MODEL_PATH/isen/isen.student.tiny11/model.npz"
"$MODEL_PATH/nben/nben.student.tiny11/model.npz"
"$MODEL_PATH/nnen/nnen.student.tiny11/model.npz"
)

for model in ${students[@]};
do
	langpair="$(echo "$model" | awk -F/ '{print $(NF-2)}')"
	modeldir="$(dirname "$model")"
	vocabfile="$modeldir/vocab.$langpair.spm"
	echo -e "Running model $model ...\n"
	stollen_numpy --numpy-file $model --W 'Wemb' --b 'decoder_ff_logit_out_b' --vocab $vocabfile \
	   	--patience 2500 --exact-algorithm lp_chebyshev --save-db
done
