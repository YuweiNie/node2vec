#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Graph utilities."""

import logging
from time import time
from utils import MyReader
from collections import defaultdict

logger = logging.getLogger("deepwalk")

__author__ = "Yuwei Nie"
__email__ = "yuweinie@163.com"

LOGFORMAT = "%(asctime).19s %(levelname)s %(filename)s: %(lineno)s %(message)s"


class Graph(defaultdict):
    """Efficient basic implementation of Graph """

    def __init__(self, ts, directed=False):
        super(Graph, self).__init__(defaultdict)
        self.directed = directed
        self.ts = ts

    def nodes(self):
        return list(self.keys())

    def neighbors(self, node):
        return list(self[node].keys())

    def weighted_neighbors(self, node):
        nodes = self.neighbors(node)
        attr = self[node]
        weight = [attr[n] for n in nodes]
        return nodes, weight

    def has_edge(self, v1, v2):
        return v2 in self[v1]

    def add_edge(self, v1, v2, weight):
        self[v1][v2] = weight
        if not self.directed:
            self[v2][v1] = weight

    def read_edgelist(self, edge_path):
        print("building graph...")
        edgelist = MyReader(edge_path)
        step = 0
        for i, e in enumerate(edgelist):
            step += 1
            if not step % 1000:
                print("working on {}kth edge".format(step // 1000), end='\r')
            self.add_edge(int(e[0]), int(e[1]), int(e[2]))
        self.remove_self_loops()
        print("\nthe graph has {} nodes and {} edges".format(self.order(), self.number_of_edges()))

    def adjacency_iter(self):
        return self.items()

    def subgraph(self, nodes={}):
        subgraph = Graph()

        for n in nodes:
            if n in self:
                subgraph[n] = [x for x in self[n] if x in nodes]

        return subgraph

    def make_undirected(self):

        t0 = time()

        for v in self.keys():
            for other in self[v]:
                if v != other:
                    self[other].append(v)

        t1 = time()
        logger.info('make_directed: added missing edges {}s'.format(t1 - t0))

        self.make_consistent()
        return self

    # def make_consistent(self):
    #     t0 = time()
    #     for k in iterkeys(self):
    #         self[k] = list(sorted(set(self[k])))
    #
    #     t1 = time()
    #     logger.info('make_consistent: made consistent in {}s'.format(t1 - t0))
    #
    #     self.remove_self_loops()
    #
    #     return self

    def remove_self_loops(self):

        removed = 0
        t0 = time()

        for x in self:
            if x in self[x]:
                self[x].pop(x)
                removed += 1

        t1 = time()

        logger.info('remove_self_loops: removed {} loops in {}s'.format(removed, (t1 - t0)))
        return self

    def check_self_loops(self):
        for x in self:
            for y in self[x]:
                if x == y:
                    return True

        return False

    def degree(self, node):
        return len(self[node])

    def order(self):
        "Returns the number of nodes in the graph"
        return len(self)

    def number_of_edges(self):
        "Returns the number of nodes in the graph"
        return sum([self.degree(x) for x in self.keys()]) / 2

    def number_of_nodes(self):
        "Returns the number of nodes in the graph"
        return self.order()




