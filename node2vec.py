#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-05-17 17:54
# @Author  : nieyuwei

import logging
import argparse
import gensim
import os
from walk import walk
from graph import Graph
from utils import MyReader, mkdir


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def parse_args():
    '''
    Parse the node2vec arguments.
    '''
    parser = argparse.ArgumentParser(description="Run node2vec.")

    parser.add_argument('--edge_path', nargs='?', default=None,
                        help='Input edge path')

    parser.add_argument('--sep', type=str, default=' ', help='Separator of the edge data.')

    parser.add_argument('--out_dir', nargs='?', default='.',
                        help='Embeddings path')

    parser.add_argument('--unweighted', dest='weighted', action='store_false', default=True)

    parser.add_argument('--directed', dest='directed', action='store_true', default=False,
                        help='Graph is (un)directed. Default is undirected.')

    parser.add_argument('--walk_length', type=int, default=80,
                        help='Length of walk per source. Default is 80.')

    parser.add_argument('--walk_num', type=int, default=10,
                        help='Number of walks per source. Default is 10.')

    parser.add_argument('--p', type=float, default=1,
                        help='Return hyperparameter. Default is 1.')

    parser.add_argument('--q', type=float, default=1,
                        help='Inout hyperparameter. Default is 1.')

    parser.add_argument('--size', type=int, default=128,
                        help='Number of dimensions. Default is 128.')

    parser.add_argument('--window', type=int, default=5,
                        help='Context size for optimization. Default is 5.')

    parser.add_argument('--min_count', type=int, default=5,
                        help='Ignores all words with total frequency lower than this. Default is 5.')

    parser.add_argument('--iter', type=int, default=5,
                        help='Number of epochs in SGD')

    parser.add_argument('--workers', type=int, default=3,
                        help='Number of parallel workers. Default is 3.')

    return parser.parse_args()


def word2vec(corpus_dir, out_dir, size, window, min_count, iter, workers):
    """
    Training word2vec model on walk corpus.
    :param corpus_dir: directory saving the walk corpus
    :param out_dir: output directory
    :param size: embedding size (vector dimensions)
    :param window: skip-gram window size
    :param min_count: ignores all words with total frequency lower than this
    :param iter: number of iterations (epochs) over the corpus
    :param workers: use these many worker threads to train the model (=faster training with multicore machines).
    :return:
    """
    sentences = MyReader(corpus_dir)
    model = gensim.models.Word2Vec(sentences, size=size, window=window, min_count=min_count, iter=iter, workers=workers, sg=1)
    mkdir(out_dir)
    model.wv.save_word2vec_format(os.path.join(out_dir, 'node2vec.vector'), os.path.join(out_dir, 'node2vec.vocab'))


if __name__ == "__main__":
    args = parse_args()
    G = Graph(args.directed)
    G.read_edgelist(args.edge_path, args.weighted, args.sep)
    corpus_dir = walk(G, args.walk_num, args.out_dir, args.walk_length, args.p, args.q, args.workers)
    word2vec(corpus_dir, args.out_dir, args.size, args.window, args.min_count, args.iter, args.workers)

