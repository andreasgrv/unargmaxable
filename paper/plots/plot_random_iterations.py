import os
import numpy as np
import matplotlib.lines as mlines
import matplotlib.pyplot as plt

from argparse import ArgumentParser

from stollen.server import create_app
from stollen.server.data_model import Experiment, Model, Result, Solution


if __name__ == "__main__":
    
    parser = ArgumentParser(description='Plot iterations needed to prove unbounded.')

    parser.add_argument('--ids-file', type=str, required=True,
                        help='TXT file to find experiment ids.')

    args = parser.parse_args()

    with open(args.ids_file) as f:
        eids = [int(l.strip()) for l in f.readlines()]

    app, db = create_app()
    with app.app_context():
        fig, axs = plt.subplots(2, 5)
        for i, eid in enumerate(eids):
            row = i // 5
            col = i % 5
            print(row, col)

            experiment = Experiment.query.filter(Experiment.id == eid).first()
            results = Result.query.filter(Result.experiment_id == eid).all()
            results = sorted(results, key=lambda x: x.index)
            results_dict = {r.index: r for r in results}

            unbounded = [r.index for r in results if not r.is_bounded and (r.iterations is not None and r.iterations < r.experiment.patience - 1)]
            approx_failed = [r.index for r in results if not r.is_bounded and (r.iterations is None or r.iterations >= r.experiment.patience - 1)]
            bounded = [r.index for r in results if r.is_bounded]

            if len(bounded) or len(approx_failed):
                max_val = experiment.patience
            else:
                max_val = max([r.iterations for r in results])

            print('Argmaxable       : %d' % len(unbounded))
            print('Potentially Unargmaxable: %d' % len(approx_failed))
            print('Unargmaxable         : %d' % len(bounded))

            ax = axs[row, col]
            if len(unbounded):
                ax.scatter(unbounded,
                            [results_dict[i].iterations for i in unbounded],
                            s=.5, alpha=.2, label='Argmaxable=%d' % len(unbounded))
            if len(approx_failed):
                ax.scatter(approx_failed,
                            [results_dict[i].experiment.patience - 1 for i in approx_failed],
                            s=.5, alpha=.5, color='purple', label='Argmaxable but approx failed=%d' % len(approx_failed))
            if len(bounded):
                ax.scatter(bounded,
                            [results_dict[i].experiment.patience*1.01 for i in bounded],
                            s=.5, alpha=.5, color='red', label='Unargmaxable=%d' % len(bounded))
            ax.set_xlabel('Vocabulary Index', fontsize=16)
            ax.set_ylabel('Iterations of Approx Algorithm', fontsize=16)
            top = max(1.1, max_val)
            bottom = -top * 0.1
            top = top * 1.1
            ax.set_ylim([bottom, top])
            ax.yaxis.get_major_locator().set_params(integer=True)
            ax.title.set_text('Softmax W dim=%d' % experiment.model.embed_dim)

        unb_dot = mlines.Line2D([], [], color='blue', marker='o', linestyle='None', markersize=6, label='Argmaxable')
        apx_unb_dot = mlines.Line2D([], [], color='purple', marker='o', linestyle='None', markersize=6, label='Argmaxable but approx alg failed')
        bnd_dot = mlines.Line2D([], [], color='red', marker='o', linestyle='None', markersize=6, label='Unargmaxable')

        handles = [unb_dot, apx_unb_dot, bnd_dot]
        filename = os.path.basename(args.ids_file)
        fig.suptitle('Random %s initialisation with $|C|$=%d' % (filename.split('_')[0], experiment.model.vocab_size), fontsize=20)
        fig.legend(handles=handles, fontsize=12)
        plt.subplots_adjust(left=0.07, right=0.98, top=0.91, bottom=0.07, wspace=0.25, hspace=0.4)
        # plt.tight_layout()
        plt.show()
