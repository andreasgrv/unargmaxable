import numpy as np
import matplotlib.pyplot as plt

from argparse import ArgumentParser

from stollen.server import create_app
from stollen.server.data_model import Experiment, Model, Result, Solution


if __name__ == "__main__":
    
    parser = ArgumentParser(description='Plot iterations needed to prove unbounded.')

    parser.add_argument('--experiment-id', type=int, required=False,
                        help='Experiment id to plot iterations for')

    args = parser.parse_args()

    assert (args.experiment_id is not None) or (args.model is not None)
    app, db = create_app()
    with app.app_context():
        # results = Result.query.filter(Result.is_bounded == True).join(Experiment).join(Model).filter(Model.name.contains(query))
        experiment = Experiment.query.filter(Experiment.id == args.experiment_id)
        results = Result.query.join(Experiment).join(Model)
        results = results.filter(Experiment.algorithm.contains('braid'))
        if args.model:
            results = results.filter(Model.name.contains(args.model))
        else:
            results = results.filter(Result.experiment_id == args.experiment_id)
        results = sorted(results, key=lambda x: x.index)
        results_dict = {r.index: r for r in results}

        unbounded = [r.index for r in results if not r.is_bounded and (r.iterations is not None and r.iterations < r.experiment.patience - 1)]
        approx_failed = [r.index for r in results if not r.is_bounded and (r.iterations is None or r.iterations >= r.experiment.patience - 1)]
        bounded = [r.index for r in results if r.is_bounded]

        print('Unbounded       : %d' % len(unbounded))
        print('Unbounded approx: %d' % len(approx_failed))
        print('Bounded         : %d' % len(bounded))

        fig, ax1 = plt.subplots()
        if len(unbounded):
            ax1.scatter(unbounded,
                        [results_dict[i].iterations for i in unbounded],
                        s=.5, alpha=.2, label='Unbounded')
        if len(approx_failed):
            ax1.scatter(approx_failed,
                        [results_dict[i].experiment.patience - 1 for i in approx_failed],
                        s=.5, alpha=.5, color='purple', label='Unbounded but approx failed')
        if len(bounded):
            ax1.scatter(bounded,
                        [results_dict[i].experiment.patience*1.01 for i in bounded],
                        s=.5, alpha=.5, color='red', label='Bounded')
        ax1.set_xlabel('Vocabulary Index')
        ax1.set_ylabel('Iterations of Approx Algorithm')
        plt.tight_layout()
        plt.legend()
        plt.show()
