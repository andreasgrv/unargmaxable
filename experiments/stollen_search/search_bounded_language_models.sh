#!/bin/bash
trap "exit" INT

########################################################################
########################### CORE MODEL TESTING #########################
########################################################################
contextual_urls=(
https://huggingface.co/bert-base-cased
https://huggingface.co/bert-base-uncased
https://huggingface.co/roberta-base
https://huggingface.co/roberta-large
https://huggingface.co/xlm-roberta-base
https://huggingface.co/xlm-roberta-large
https://huggingface.co/gpt2
# https://huggingface.co/google/bert_uncased_L-2_H-128_A-2
# https://huggingface.co/google/bert_uncased_L-4_H-128_A-2
# https://huggingface.co/google/bert_uncased_L-6_H-128_A-2
# https://huggingface.co/google/bert_uncased_L-8_H-128_A-2
# https://huggingface.co/google/bert_uncased_L-10_H-128_A-2
# https://huggingface.co/google/bert_uncased_L-12_H-128_A-2
# https://huggingface.co/google/bert_uncased_L-2_H-768_A-12
# https://huggingface.co/google/bert_uncased_L-4_H-768_A-12
# https://huggingface.co/google/bert_uncased_L-6_H-768_A-12
# https://huggingface.co/google/bert_uncased_L-8_H-768_A-12
# https://huggingface.co/google/bert_uncased_L-10_H-768_A-12
# https://huggingface.co/google/bert_uncased_L-12_H-768_A-12
)

for url in ${contextual_urls[@]};
do
	echo -e "Running model $url ...\n"
	stollen_hugging --url $url --patience 2500 --exact-algorithm lp_chebyshev --save-db
done
