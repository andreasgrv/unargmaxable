import os
import json
import numpy as np
from argparse import ArgumentParser


if __name__ == "__main__":
    parser = ArgumentParser(description='Create randomly initialised models.')
    parser.add_argument('--embed-dim', type=int,
                        help='The dimensionality of softmax embeddings')
    parser.add_argument('--vocab-dim', type=int,
                        help='The vocabulary size')
    parser.add_argument('--init', type=str, choices=('uniform', 'normal'),
                        help='The vocabulary size')

    args = parser.parse_args()
    np.random.seed(13)
    if args.init == 'uniform':
        W = np.random.uniform(-1, 1, (args.vocab_dim, args.embed_dim))
        b = np.random.uniform(-1, 1, (1, args.vocab_dim))
    elif args.init =='normal':
        W = np.random.normal(0, 1, (args.vocab_dim, args.embed_dim))
        b = np.random.normal(0, 1, (1, args.vocab_dim))
    else:
        raise ValueError('Unexpected init type %s' % args.init)

    name = 'random-%s-model-%d-%d' % (args.init, args.vocab_dim, args.embed_dim)
    outfile = '%s.npz' % name
    outpath = os.path.join('models', outfile)
    print('Saving %s...' % outpath)
    np.savez(outpath, W=W, b=b)

    vocab = {i:i for i in range(args.vocab_dim)}
    vocabfile = '%s-vocab.json' % name
    outpath = os.path.join('models', vocabfile)
    with open(outpath, 'w') as f:
        f.write(json.dumps(vocab))
