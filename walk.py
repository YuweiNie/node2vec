#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-05-17 17:02
# @Author  : nieyuwei

import numpy as np
import logging
import os
from utils import chunks, mkdir
from joblib import Parallel, delayed

logger = logging.getLogger(__name__)


def walker(g, source_node, length, p, q):
    """
    Return a path through the graph by weighted random walking.
    :param g: graph
    :param source_node: starting node
    :param length: walk length
    :param p: controls the likelihood of immediately revisiting a node in the walk
    :param q: allows the search to differentiate between “inward” and “outward” nodes
    :return: a random walk path including a list of nodes
    """
    path = [source_node]
    adj = (p != 1 or q != 1)
    while len(path) < length:
        cur_node = path[-1]
        neighbors, weight = g.weighted_neighbors(cur_node)
        if not neighbors:
            break
        neighbor_size = len(neighbors)
        if neighbor_size == 1:
            path.append(neighbors[0])
            continue
        if len(path) >= 2 and adj:
            pre_node = path[-2]
            for idx, n in enumerate(neighbors):
                if p != 1 and n == pre_node:
                    weight[idx] *= 1. / p
                elif q != 1 and not g.has_edge(pre_node, n):
                    weight[idx] *= 1. / q
        weight = np.array(weight)
        j = int(np.random.choice(neighbor_size, size=1, p=weight / sum(weight)))
        path.append(neighbors[j])
    return path


def batch_walk(g, file_name, batch_no, nodes, length, p, q):
    """
    Walk from a batch of nodes, and write the walks to a file.
    :param g: graph
    :param file_name: file to save the walk
    :param batch_no: batch number
    :param nodes: a batch of nodes which is iterable
    :param length: walk length
    :param p: controls the likelihood of immediately revisiting a node in the walk
    :param q: allows the search to differentiate between “inward” and “outward” nodes
    :return: None
    """
    nodes_num = len(nodes)
    logger.info("Batch %s: random walking in %d nodes...", batch_no, nodes_num)
    with open(file_name, 'a') as wf:
        for i, n in enumerate(nodes):
            if not (i + 1) % 1000:
                print("Batch {}: working on {}kth node, {}% complete".format(batch_no, (i + 1) // 1000,
                                                                             100 * (i + 1) // nodes_num), end='\r')
            path = walker(g, n, length, p, q)
            wf.write(" ".join([str(x) for x in path]) + '\n')


def walk(g, iter, out_dir, walk_length, p, q, workers):
    """
    Walk from all the nodes of the graph and loop for some iterations.
    Nodes will be split into batches and walk can be parallel.
    :param g: graph
    :param iter: iterations
    :param out_dir: output directory
    :param walk_length: walk length
    :param p: controls the likelihood of immediately revisiting a node in the walk
    :param q: allows the search to differentiate between “inward” and “outward” nodes
    :param workers: number of cpu cores work at the same time
    :return: directory saving the walk corpus
    """
    nodes_num = g.order()
    if nodes_num > 100000:
        batch_size = 100000
    else:
        batch_size = (nodes_num + workers - 1) // workers
    batch_num = (nodes_num + batch_size - 1) // batch_size
    corpus_path = os.path.join(out_dir, 'walk_corpus')
    mkdir(corpus_path)
    for walk_iter in range(iter):
        logger.info('Walk iteration: %d / %d', walk_iter + 1, iter)
        file_name = os.path.join(corpus_path, 'walk_corpus_' + str(walk_iter))
        nodes_batch = chunks(g.nodes(), batch_size)
        Parallel(n_jobs=workers, verbose=50)(
            delayed(batch_walk)(g, file_name, '{}/{}'.format(i, batch_num), n, walk_length, p, q) for i, n in enumerate(nodes_batch)
        )
    return corpus_path
