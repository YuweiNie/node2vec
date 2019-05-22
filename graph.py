#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from time import time
from utils import MyReader
from collections import defaultdict

logger = logging.getLogger(__name__)


class Graph(defaultdict):
    """
    Efficient basic implementation of graph
    """

    def __init__(self, directed=False):
        """
        Initialize a graph.
        :param directed: whether the constructed graph will be directed
        """
        super(Graph, self).__init__(defaultdict)
        self.directed = directed

    def nodes(self):
        """
        Nodes which can be a starting point of the walking path.
        May be less than all the nodes of the graph when the graph is directed.
        :return: a list of nodes
        """
        return list(self.keys())

    def neighbors(self, node):
        """
        Nodes adjacent to a specific node.
        :param node: a node
        :return: a list of nodes
        """
        return list(self[node].keys())

    def weighted_neighbors(self, node):
        """
        Nodes adjacent to a specific node and their weights.
        :param node: a node
        :return: a list of nodes, a list of corresponding weights
        """
        nodes = self.neighbors(node)
        attr = self[node]
        weight = [attr[n] for n in nodes]
        return nodes, weight

    def has_edge(self, v1, v2):
        """
        Whether an edge exists between v1 and v2.
        The edge must be v1->v2 if the graph is directed.
        :param v1: node 1
        :param v2: node 2
        :return: bool
        """
        return v2 in self[v1]

    def add_edge(self, v1, v2, weight=1.):
        """
        Add an edge to the graph
        :param v1: node 1
        :param v2: node 2
        :param weight: weight of the edge
        :return: None
        """
        self[v1][v2] = weight
        if not self.directed:
            self[v2][v1] = weight

    def read_edgelist(self, edge_path, weighted=True, sep=" "):
        """
        Load edges from files.
        The file should contain lines like '111 222 3.0'.
        First two integers(must be int) represent the nodes, and the last number for weight.
        :param edge_path: a file path or a directory
        :param weighted: whether the edge weighted
        :param sep: separator of your edge data.
        :return: None
        """
        logger.info("Building graph...")
        edgelist = MyReader(edge_path, sep)
        step = 0
        for i, e in enumerate(edgelist):
            step += 1
            if not step % 1000:
                print("Working on {}kth edge".format(step // 1000), end='\r')
            if weighted:
                self.add_edge(int(e[0]), int(e[1]), float(e[2]))
            else:
                self.add_edge(int(e[0]), int(e[1]))
        self.remove_self_loops()
        logger.info("The graph has %s nodes and %s edges", self.order(), self.number_of_edges())

    def to_undirected(self):
        """
        Make directed graph undirected.
        Weights of the directed edges will be added up.
        :return: undirected graph
        """
        if not self.directed:
            logger.info("The graph is already undirected, can't be transformed!")
            return self
        edge_weight = {}
        for v in self:
            for nb in self[v]:
                edge = tuple(sorted([v, nb]))
                if edge in edge_weight:
                    self[nb][v] = edge_weight[edge]
                    edge_weight.pop(edge)
                else:
                    if v in self[nb]:
                        weight = self[v][nb] + self[nb][v]
                    else:
                        weight = self[v][nb]
                    self[nb][v] = weight
                    edge_weight[edge] = weight
        self.directed = False
        return self

    def remove_self_loops(self):
        """
        Remove self loops.
        :return: graph
        """
        removed = 0
        t0 = time()
        for x in self:
            if x in self[x]:
                self[x].pop(x)
                removed += 1
        t1 = time()
        logger.info('remove_self_loops: removed {} loops in {}s'.format(removed, (t1 - t0)))
        return self

    def degree(self, node):
        """
        Number of nodes adjacent to a specific node.
        :param node: a node
        :return: degree of the node
        """
        return len(self[node])

    def order(self):
        """
        Number of nodes in the graph
        :return:
        """
        return len(self)

    def number_of_edges(self):
        """
        Number of edges in the graph
        :return:
        """
        num = sum([self.degree(x) for x in self.keys()])
        return num if self.directed else num / 2

    def number_of_nodes(self):
        """
        Number of nodes in the graph
        :return:
        """
        return self.order()




