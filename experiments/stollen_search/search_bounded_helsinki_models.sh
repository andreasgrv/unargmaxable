#!/bin/bash
trap "exit" INT
mkdir -p ignored

########################################################################
############################ MT MODEL TESTING ##########################
########################################################################
en_urls=(
https://huggingface.co/Helsinki-NLP/opus-mt-ja-en
https://huggingface.co/Helsinki-NLP/opus-mt-ru-en
https://huggingface.co/Helsinki-NLP/opus-mt-bg-en
https://huggingface.co/Helsinki-NLP/opus-mt-jap-en
https://huggingface.co/Helsinki-NLP/opus-mt-ar-en
)

for url in ${en_urls[@]};
do
	echo -e "Running model $url ...\n"
	stollen_hugging --url $url --patience 2500 --filter-lang en --exact-algorithm lp_chebyshev --save-db
done

el_urls=(
https://huggingface.co/Helsinki-NLP/opus-mt-en-el
https://huggingface.co/Helsinki-NLP/opus-mt-de-el
https://huggingface.co/Helsinki-NLP/opus-mt-ar-el
https://huggingface.co/Helsinki-NLP/opus-mt-es-el
https://huggingface.co/Helsinki-NLP/opus-mt-fi-el
)

for url in ${el_urls[@]};
do
	echo -e "Running model $url ...\n"
	stollen_hugging --url $url --patience 2500 --filter-lang el --exact-algorithm lp_chebyshev --save-db
done

he_urls=(
https://huggingface.co/Helsinki-NLP/opus-mt-ar-he
https://huggingface.co/Helsinki-NLP/opus-mt-de-he
https://huggingface.co/Helsinki-NLP/opus-mt-es-he
https://huggingface.co/Helsinki-NLP/opus-mt-fr-he
https://huggingface.co/Helsinki-NLP/opus-mt-fi-he
https://huggingface.co/Helsinki-NLP/opus-mt-ja-he
)

for url in ${he_urls[@]};
do
	echo -e "Running model $url ...\n"
	stollen_hugging --url $url --patience 2500 --filter-lang he --exact-algorithm lp_chebyshev --save-db
done

ar_urls=(
https://huggingface.co/Helsinki-NLP/opus-mt-en-ar
https://huggingface.co/Helsinki-NLP/opus-mt-el-ar
https://huggingface.co/Helsinki-NLP/opus-mt-es-ar
https://huggingface.co/Helsinki-NLP/opus-mt-fr-ar
https://huggingface.co/Helsinki-NLP/opus-mt-he-ar
https://huggingface.co/Helsinki-NLP/opus-mt-it-ar
https://huggingface.co/Helsinki-NLP/opus-mt-ja-ar
https://huggingface.co/Helsinki-NLP/opus-mt-pl-ar
https://huggingface.co/Helsinki-NLP/opus-mt-ru-ar
)

for url in ${ar_urls[@]};
do
	echo -e "Running model $url ...\n"
	stollen_hugging --url $url --patience 2500 --filter-lang ar --exact-algorithm lp_chebyshev --save-db
done

ru_urls=(
https://huggingface.co/Helsinki-NLP/opus-mt-en-ru
https://huggingface.co/Helsinki-NLP/opus-mt-es-ru
https://huggingface.co/Helsinki-NLP/opus-mt-fi-ru
https://huggingface.co/Helsinki-NLP/opus-mt-fr-ru
https://huggingface.co/Helsinki-NLP/opus-mt-he-ru
https://huggingface.co/Helsinki-NLP/opus-mt-ja-ru
https://huggingface.co/Helsinki-NLP/opus-mt-ko-ru
)

for url in ${ru_urls[@]};
do
	echo -e "Running model $url ...\n"
	stollen_hugging --url $url --patience 2500 --filter-lang ru --exact-algorithm lp_chebyshev --save-db
done
