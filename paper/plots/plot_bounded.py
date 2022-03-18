import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

from sqlalchemy import and_
from argparse import ArgumentParser
from stollen.server import create_app
from collections import defaultdict
from stollen.server.data_model import Experiment, Model, Result, Solution


mpl.rcParams['xtick.labelsize'] = 14


if __name__ == "__main__":
    
    parser = ArgumentParser(description='Plot number of unargmaxable tokens.')

    parser.add_argument('--ids-file', type=str, required=True,
                        help='TXT file to find experiment ids.')
    parser.add_argument('--title', type=str, required=True,
                        help='Title for plot')
    args = parser.parse_args()

    with open(args.ids_file) as f:
        eids = [int(l.strip()) for l in f.readlines()]

    app, db = create_app()
    with app.app_context():

        print('%d experiments' % len(eids))
        num_bounded = []
        model_names = []
        bounded_vocab = defaultdict(list)
        for eid in eids:
            exp = Experiment.query.filter(Experiment.id == eid).first()
            model = Model.query.filter(Model.experiment_id == eid).first()
            print(exp.num_bounded, model.name)
            num_bounded.append(exp.num_bounded)
            if 'jap' in model.name:
                model_names.append(model.name[-6:])
            else:
                model_names.append(model.name[-5:])
            results = Result.query.filter(and_(Result.experiment_id == exp.id, Result.is_bounded == True))

            for r in results:
                bounded_vocab[r.token].append(model.name)
            #     print(r.is_bounded, r.iterations, r.token, r.index, r.misc)
        num_bounded, model_names = zip(*sorted(zip(num_bounded, model_names), key=lambda x: (x[0],x[1][-2:])))
        fig, ax = plt.subplots()
        ax.barh(np.arange(len(num_bounded)), num_bounded)
        for i, nb in enumerate(num_bounded):
            ax.text(nb + .05, i -.05, str(nb), ha='left', va='center', fontsize=16)
        ax.set_yticks(np.arange(len(num_bounded)))
        ax.set_yticklabels(model_names, rotation=0, fontname='FantasqueSansMono Nerd Font', fontsize=16)
        ax.set_ylabel('Model language pairs', fontsize=20)
        ax.set_xlabel('Number of unargmaxable vocabulary tokens', fontsize=20)
        # plt.title('Stolen probability for HelsinkiNLP models', fontsize=22)
        plt.tight_layout()
        plt.show()

        wordlevel_tokens = 0
        single_token = 0
        for token, models in sorted(bounded_vocab.items(), key=lambda x: len(x[0])):
            if token.startswith('▁'):
                wordlevel_tokens += 1
            if len(token) == 1:
                single_token += 1
            print(token.ljust(25), models)
        print('%d tokens' % len(bounded_vocab))
        print('Out of which %d/%d are word level tokens' % (wordlevel_tokens, len(bounded_vocab)))
        print('Out of which %d/%d are single tokens' % (single_token, len(bounded_vocab)))
