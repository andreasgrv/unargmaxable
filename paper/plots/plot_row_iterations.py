import numpy as np
import matplotlib.lines as mlines
import matplotlib.pyplot as plt

from argparse import ArgumentParser

from stollen.server import create_app
from stollen.server.data_model import Experiment, Model, Result, Solution


def filter_modelname(name):
    name = name.replace('bigx2', 'big')
    name = name.replace(':model.npz', '')
    name = name.replace('.npz', '')
    name = name.replace(':model', '')
    return name


if __name__ == "__main__":
    
    parser = ArgumentParser(description='Plot iterations needed to prove argmaxable.')

    parser.add_argument('--ids-file', type=str, required=True,
                        help='TXT file to find experiment ids.')
    parser.add_argument('--title', type=str, required=True,
                        help='Title for plot')
    args = parser.parse_args()

    with open(args.ids_file) as f:
        eids = [int(l.strip()) for l in f.readlines()]

    has_approx_fail = False
    has_bounded = False

    app, db = create_app()
    with app.app_context():
        fig, axs = plt.subplots(1, len(eids))
        for i, eid in enumerate(eids):
            col = i

            experiment = Experiment.query.filter(Experiment.id == eid).first()
            results = Result.query.filter(Result.experiment_id == eid).all()
            results = sorted(results, key=lambda x: x.index)
            results_dict = {r.index: r for r in results}

            unbounded = [r.index for r in results if not r.is_bounded and (r.iterations is not None and r.iterations < r.experiment.patience - 1)]
            approx_failed = [r.index for r in results if not r.is_bounded and (r.iterations is None or r.iterations >= r.experiment.patience - 1)]
            bounded = [r.index for r in results if r.is_bounded]

            iters_needed = [results_dict[i].iterations for i in results_dict]
            print('Iterations needed: mean %.3f, max %d' % (sum(iters_needed)/len(iters_needed), max(iters_needed)))

            if len(approx_failed) > 0:
                has_approx_fail = True

            if len(bounded) > 0:
                has_bounded = True

            if len(bounded) or len(approx_failed):
                max_val = experiment.patience
            else:
                max_val = max([r.iterations for r in results])

            print('Argmaxable       : %d' % len(unbounded))
            print('Argmaxable approx: %d' % len(approx_failed))
            print('Unargmaxable         : %d' % len(bounded))

            ax = axs[col]
            if len(unbounded):
                ax.scatter(unbounded,
                            [results_dict[i].iterations for i in unbounded],
                            s=.5, alpha=.2, label='%d' % len(unbounded))
            if len(approx_failed):
                ax.scatter(approx_failed,
                            [results_dict[i].experiment.patience - 1 for i in approx_failed],
                            s=.5, alpha=.5, color='purple', label='%d' % len(approx_failed))
            if len(bounded):
                ax.scatter(bounded,
                            [results_dict[i].experiment.patience*1.01 for i in bounded],
                            s=.5, alpha=.5, color='red', label='%d' % len(bounded))
            ax.set_xlabel('Vocabulary Index', fontsize=12)
            ax.set_ylabel('Iterations of Approx Algorithm', fontsize=12)
            subplot_hs = []
            subplot_hs.append(mlines.Line2D([], [], color='blue', marker='o', linestyle='None', markersize=6, label='num=%d' % len(unbounded)))
            if len(approx_failed) > 0:
                subplot_hs.append(mlines.Line2D([], [], color='purple', marker='o', linestyle='None', markersize=6, label='num=%d' % len(approx_failed)))
            if len(bounded) > 0:
                subplot_hs.append(mlines.Line2D([], [], color='red', marker='o', linestyle='None', markersize=6, label='num=%d' % len(bounded)))
            ax.legend(handles=subplot_hs)
            top = max(1.1, max_val)
            bottom = -top * 0.1
            top = top * 1.1
            ax.set_ylim([bottom, top])
            ax.yaxis.get_major_locator().set_params(integer=True)
            model_name = filter_modelname(experiment.model.name)
            ax.title.set_text(model_name)

        unb_dot = mlines.Line2D([], [], color='blue', marker='o', linestyle='None', markersize=6, label='Argmaxable')
        apx_unb_dot = mlines.Line2D([], [], color='purple', marker='o', linestyle='None', markersize=6, label='Argmaxable but approx alg failed')
        bnd_dot = mlines.Line2D([], [], color='red', marker='o', linestyle='None', markersize=6, label='Unargmaxable')

        handles = [unb_dot]
        if has_approx_fail:
            handles.append(apx_unb_dot)
        if has_bounded:
            handles.append(bnd_dot)
        fig.suptitle('%s' % args.title, fontsize=20)
        fig.legend(handles=handles)
        plt.subplots_adjust(left=0.07, right=0.98, top=0.91, bottom=0.07, wspace=0.25, hspace=0.4)
        # plt.tight_layout()
        plt.show()
