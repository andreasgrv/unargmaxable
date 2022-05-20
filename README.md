# Unargmaxable


## Definition
### un·argmax·able Adjective

* An item that cannot be assigned the largest score by a function assigning scores to items.


## Contents

This repository contains algorithms for detecting **unargmaxable** classes in low-rank softmax layers.
A softmax layer is by construction low-rank if we have C > d + 1, where C is the number of classes
and d is the dimensionality of the input feature vector.

### [Low-Rank Softmax Can Have Unargmaxable Classes in Theory but Rarely in Practice](https://arxiv.org/abs/2203.06462)
The repository also contains code to reproduce our results, tables and figures from our paper that was accepted to ACL 2022.

# Installation

## Install python dependencies
```bash
python3.7 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
pip install -e .
```


## Set environment variables

```bash
export OMP_NUM_THREADS=1
export STOLLEN_NUM_PROCESSES=4

# Adapt below as needed
export FLASK_APP="$PWD/stollen/server"
# Adapt below if you would rather install models elsewhere
mkdir models
export TRANSFORMERS_CACHE="$PWD/models"
```


### Details on environment variables
* `export OMP_NUM_THREADS=1` is needed as otherwise we don't benefit from multithreading (numpy hogs all threads).
* You can set `STOLLEN_NUM_PROCESSES` if you want to run the search on multiple CPUs/threads. Each thread processes a single vocabulary item in parallel. We used `export STOLLEN_NUM_PROCESSES=10` on an AMD 3900X CPU with 64 Gb of RAM.


## Install [Gurobi](https://www.gurobi.com/academia/academic-program-and-licenses/)

The linear programming algorithm depends on Gurobi.
It requires a license, see link above.


# Example Usage

## Verify a randomly initialised softmax layer

This script exists as a sanity check for our algorithms.
We assert that we can detect which points are internal to the convex hull.
To make this assertion we compare results to [QHull](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.ConvexHull.html).


Are any of the 20 class weight vectors randomly initialised in 2 and 3 dimensions unargmaxable?

```bash
stollen_random --num-classes 20 --dim 2
stollen_random --num-classes 20 --dim 3
stollen_random --help   # For more details / options
```

If the dimension is 2 or 3 we also plot the resulting convex hull for visualisation purposes.
The result of the algorithm is also compared to the exact Qhull result if `dim < 10`.
The approximate algorithm will have 100% recall but may have lower precision.
```bash
stollen_random --num-classes 300 --dim 8 --seed 3  --patience 50
```

Below we run the exact algorithm, this should always return 100% for both precision and recall unless the input range is too large.
```bash
stollen_random --num-classes 300 --dim 8 --seed 3  --patience 50 --exact-algorithm lp_chebyshev
```


## Verify that unargmaxable tokens can be avoided by using weight normalisation

As a sanity check we verify that all classes are argmaxable when we normalise the weights or set the bias term as mentioned in Appendix D of the paper.

```bash
stollen_prevention --num-classes 500 --dim 10
stollen_prevention --num-classes 500 --dim 10 --use-bias
```

We can also see that the script would raise an assertion error if we did not follow the normalisation step.

```bash
stollen_prevention --num-classes 500 --dim 10 --do-not-prevent
stollen_prevention --num-classes 500 --dim 10 --use-bias --do-not-prevent
```

Note that in high dimensions unargmaxable tokens are not expected to exist if we randomly initialise the weight vectors.


## Verify a model stored in numpy.npz format

Expects the weight matrix to be in **decoder_Wemb** attribute.
Takes transpose, since expects the matrix in [dim, num_classes] format.

```bash
stollen_numpy --numpy-file path-to-numpy-model.npz
```


## Verify a model from HuggingFace

```bash
stollen_hugging --url https://huggingface.co/bert-base-cased --patience 2500 --exact-algorithm lp_chebyshev
```

NB: The script does not work with any arbitrary model: It needs to be adapted if the Softmax weights and bias are stored in an unforeseen variable.


# Reproducing the Paper Results


## Run experiments

Scripts to reproduce experiments can be found [here](experiments/stollen_search), see the README.md file for details.
The scripts generally write to a postgres database, but the ``save-db`` parameter can be toggled within the script to change that.

## Recreate tables and figures from the original experiments

### More Installation Steps needed

#### OS dependencies

* wget
* gunzip
* psql


#### Install database
```bash
export FLASK_APP="$PWD/stollen/server"
cd db

export DB_FOLDER="$PWD/stollen_data"
export DB_PORT=5436
export DB_USER=`whoami`
export DB_NAME=stollenprob
# fun times
export DB_PASSWD="cov1d"
export PGPASSWORD=$DB_PASSWD
export DB_HOST="localhost"
export DB_SSL="prefer"

# Creates the database, tables etc.
./install.sh

# Will download the tables in CSV format from aws s3
# and populate the psql database
# (the csv files are saved in the data folder - e.g. if you want to use pandas)
./download_and_populate_db.sh
```

#### Deleting the database after done

From the `db` folder, run:

```bash
# IMPORTANT: Run stop before deleting any files
./stop.sh
rm -r stollen_data
rm -r migrations
```

The following scripts generally accept a file with experiment ids to plot/aggregate.
For example:

```
cd ../paper/plots
python plot_bounded.py  --ids-file datafiles/bounded.txt --title "bounded models"
```

```
paper/
├── appendix
│   ├── braid-slice-regions
│   └── check_quantiles
├── plots
│   ├── plot_bounded.py
│   ├── plot_random_iterations.py
│   ├── plot_row_iterations.py
│   ├── plot.sh
│   ├── stolen_probability.py
│   └── stolen_probability_with_convex.py
└── tables
    ├── plot_iterations.py
    └── print_bounded_table.py
```

You can use the above with the experiment ids generated from your own experiments, assuming you save them to the database.

### Generating plots from the paper

From the `paper/plots` folder run:
```bash
./plot.sh
```
This assumes you have installed and populated the database mentioned above.

# Related Work

* [Demeter(2020)](https://arxiv.org/abs/2005.02433) identified that unargmaxable classes can arise in classification layers and coined the more general phenomenon Stolen Probability.
* Warren D. Smith comprehensively summarises [the history of the problem](https://rangevoting.org/WilsonOrder.html).


# Citation

Please cite our work as:


```
@inproceedings{grivas2022,
  title={Low-Rank Softmax Can Have Unargmaxable Classes in Theory but Rarely in Practice},
  author={Andreas Grivas and Nikolay Bogoychev and Adam Lopez},
  journal={ArXiv},
  year={2022}
  volume={abs/2203.06462}
}
```

# Trivia
As we get closer to Christmas, [stollen](https://en.wikipedia.org/wiki/Stollen) probability increases.
