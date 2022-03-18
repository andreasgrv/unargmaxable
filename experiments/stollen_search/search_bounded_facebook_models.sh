#!/bin/bash
trap "exit" INT
mkdir -p ignored

########################################################################
############################ MT MODEL TESTING ##########################
########################################################################

urls=(
https://huggingface.co/facebook/wmt19-ru-en
https://huggingface.co/facebook/wmt19-en-ru
https://huggingface.co/facebook/wmt19-de-en
https://huggingface.co/facebook/wmt19-en-de
)

for url in ${urls[@]};
do
	echo -e "Running model $url ...\n"
	trglang="${url: -2}"
	stollen_hugging --url $url --patience 2500 --filter-lang $trglang --exact-algorithm lp_chebyshev --save-db
done
