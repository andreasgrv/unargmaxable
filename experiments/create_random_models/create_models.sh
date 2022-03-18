#!/bin/bash
mkdir -p models

dims=(
2
4
6
8
10
15
20
30
40
50
)

for dim in ${dims[@]};
do
	python create_model.py --embed-dim $dim --vocab-dim 10000 --init uniform
	python create_model.py --embed-dim $dim --vocab-dim 10000 --init normal
done
