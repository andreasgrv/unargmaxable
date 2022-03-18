import numpy as np

from collections import defaultdict

from stollen.server import create_app
from stollen.server.data_model import Experiment, Model, Result, Solution


HEADER = """
\\begin{table}[h!]
\scalebox{0.85}{
\\begin{tabular}{c c | c c}
\\toprule
group & model & \# approx bounded & \# bounded\\
\midrule
"""

FOOTER = """
\\bottomrule
\end{tabular}
}
\end{table}
"""


if __name__ == "__main__":
    
    with open('experiment_ids.txt') as f:
        eids = [int(l.strip()) for l in f.readlines()]
    app, db = create_app()
    with app.app_context():


        rows = defaultdict(dict)
        for eid in eids:
            # results = Result.query.filter(Result.is_bounded == True).join(Experiment).join(Model).filter(Model.name.contains(query))
            experiment = Experiment.query.filter(Experiment.id == eid).first()
            results = Result.query.filter(Result.experiment_id == eid).all()
            results = sorted(results, key=lambda x: x.index)
            results_dict = {r.index: r for r in results}

            unbounded = [r.index for r in results if not r.is_bounded and (r.iterations is not None and r.iterations < r.experiment.patience - 1)]
            approx_failed = [r.index for r in results if not r.is_bounded and (r.iterations is None or r.iterations >= r.experiment.patience - 1)]
            bounded = [r.index for r in results if r.is_bounded]

            print()
            print('Model           : %s' % experiment.model.name)
            print('Softmax         : %d x %d' % (experiment.model.vocab_size, experiment.model.embed_dim))
            print('Has bias        : %r' % (experiment.model.has_bias))
            print('Unbounded       : %d' % len(unbounded))
            print('Unbounded approx: %d' % len(approx_failed))
            print('Bounded         : %d' % len(bounded))
            rows[eid]['model'] = experiment.model.name
            rows[eid]['unbounded_approx'] = str(len(approx_failed))
            rows[eid]['bounded'] = str(len(bounded))

    print(HEADER)
    for eid in eids:
        row = rows[eid]
        print('\t & ', ' & '.join([row['model'], row['unbounded_approx'], row['bounded']]), '\\\\')
    print(FOOTER)
