"""Classes giving the felt core data model"""

import math
from collections import defaultdict
from typing import Hashable, Mapping
from dataclasses import dataclass
from .routing import shortest_path



__all__ = ['Network', 'Node', 'Way']



@dataclass
class Node:
    """Represents a node.

    Nodes have a position in 2-dimensional space given by the
    ``x`` and ``y`` attributes. Nodes also have a ``name``
    that serves as a unique identifier, and an ``attr`` map.

    An ordered sequence of nodes can be used to construct
    :class:`felt.network.Path`, :class:`felt.network.Way`, and
    :class:`felt.network.Link` instances.

    Users will typically initialize node instances directly as part of creating
    a :class:`felt.network.Network` instance.

    Args:
        name: a unique identifier for the node
        x: the x position of the node
        y: the y position of the node
        **attr: extra key word arguments to give attributes of the node
    """
    name: Hashable  #: a unique identifier for the node
    x: float  #: node x location
    y: float  #: node y location
    attr: Mapping  #: node attributes

    def __init__(self, name, x, y, **attr):
        """Initialize a Node instance"""
        self.name = name
        self.x = x
        self.y = y
        self.attr = attr
        self.network = None


class Way:
    """An ordered sequence of nodes with attributes

    Used to represent a way in a :class:`felt.network.Network`.

    Users will typically initialize way instances directly as part of creating
    a :class:`felt.network.Network` instance.

    The way may allow flow with or against the order of the nodes,
    or both. This is specified with the ``oneway`` argument.
    A positive value indicates with the node ordering. A negative
    value indicates against the node ordering. A zero value
    indicates both. The default is zero.

    Args:
        node_names: a sequence of node names
        oneway: Used to specify the direction of flow along the way
    """
    def __init__(self, node_names, oneway=None):
        self.node_names = node_names  #: names of nodes making the path
        if oneway is None:
            oneway = 0
        self._oneway = oneway
        self.network = None

    def __repr__(self):
        return f'Way({self.node_names})'

    def __iter__(self):
        return iter(self.nodes)

    def __eq__(self, other):
        if not isinstance(other, Path):
            return False
        return list(self) == list(other)

    @property
    def oneway(self):
        """The orientation of the way."""
        return self._oneway

    @property
    def nodes(self):
        """The sequence of nodes making the path"""
        return [self.network.nodes[name] for name in self.node_names]

    @property
    def links(self):
        """The links of the path"""
        oneway = self.oneway
        if oneway > 0:
            oriented_seqs = [self.node_names]
        elif oneway < 0:
            oriented_seqs = [self.node_names[::-1]]
        else:
            oriented_seqs = [self.node_names, self.node_names[::-1]]
        links = []
        for seq in oriented_seqs:
            for name0, name1 in zip(seq[:-1], seq[1:]):
                link = Link(name0, name1)
                link.network = self
                links.append(link)
        return links

    @property
    def length(self):
        """The length of the path, as defined by the positions of the path
        nodes."""
        return sum(link.length for link in self.links)



class Path(Way):
    """An ordered sequence of nodes.

    Used to represent a path on a :class:`felt.network.Network`. A path is
    a sequence of nodes from a source node to a sink node that may have a path
    flow associated with it.

    Users will often initialize path instances in one of two ways:

    - use :meth:`felt.network.Nework.path`
    - use :meth:`felt.network.Network.shortest_path`

    Paths are always oneway with the direction of the nodes.

    A sequence of path instances is used by the :func:`felt.estimate.estimate`
    function to specify the paths to generate estimates for.

    Args:
        node_names: a sequence of node names
    """
    def __init__(self, node_names):
        super().__init__(node_names, oneway=1)

    def __repr__(self):
        return f'Path({self.node_names})'


class Link(Path):
    """An ordered pair of nodes with attributes.

    A collection of links is used to initialize a :class:`Graph` instance.

    Users should not instantiate link instances directly. Links are used
    under-the-hood to support :meth:`Network.shortest_path`.

    Args:
        node_name0: the name of the first node
        node_name1: the name of the second node
    """

    def __init__(self, node_name0, node_name1):
        super().__init__([node_name0, node_name1])
        self.node_name0 = node_name0  #: the name of the first node
        self.node_name1 = node_name1  #: the name of the second node

    def __repr__(self):
        return f'Link({self.node_name0}, {self.node_name1})'

    @property
    def node0(self):
        """The first node"""
        return self.network.nodes[self.node_name0]

    @property
    def node1(self):
        """The second node"""
        return self.network.nodes[self.node_name1]

    @property
    def length(self):
        """The length of the link, based on the node locations"""
        return math.hypot(
            self.node1.x - self.node0.x,
            self.node1.y - self.node0.y
        )


class Network:
    """A network of ways and nodes.

    A collection of ways and nodes. Ways may share nodes to form intersections.

    Users will typically initialize a network instance directly, and then
    use it's :meth:`shortest_path` method to create :class:`Path` instances.

    Args:
        nodes: a collection of node instances
        ways: a collection of way instances
    """
    def __init__(self, nodes, ways):

        node_names = [node.name for node in nodes]
        for way in ways:
            for node_name in way.node_names:
                if node_name not in node_names:
                    raise ValueError(
                        f'Node {node_name} in way but not in nodes')

        self.node_names = node_names  #: the names of the nodes in the network
        self.nodes = {}  #: the network nodes; a dictionary with node name keys
        for node in nodes:
            node.network = self
            self.nodes[node.name] = node

        self.ways = []  #: the ways in the network
        for way in ways:
            way.network = self
            self.ways.append(way)

    @property
    def links(self):
        """The links in the network"""
        return [link for way in self.ways for link in way.links]

    @property
    def graph(self):
        """The graph defined by the network"""
        return Graph(self.nodes.values(), self.links)

    def shortest_path(self, source, sink):
        """Get the shortest path between two nodes in the network.

        Args:
            source: the name of the source node
            sink: the name of the sink node

        Returns:
            The shortest path between the two nodes

        Raises:
            NoPath: If there is no path between the source and sink.
        """
        path = Path(shortest_path(self.graph, source, sink))
        path.network = self
        return path

    def path(self, node_names):
        """Create a path on a network

        Args:
            node_names: the names of the nodes in the path

        Raises:
            ValueError: if the path is not valid
        """
        path = Path(node_names)
        for link in path.links:
            try:
                self.graph.link_map[link.node_name0][link.node_name1]
            except KeyError:
                raise ValueError(f'link {link} not in network')
        path.network = self
        return path


class Graph(Network):
    """Represents a mathematical graph.

    Users typically won't need to initialize this class directly.
    Graphs are used under-the-hood to support :meth:`Network.shortest_path`.

    Args:
        nodes: the nodes in the graph
        links: the links in the graph
    """

    def __init__(self, nodes, links):
        super().__init__(nodes, links)

        link_map = defaultdict(dict)
        for link in links:
            link_map[link.node_name0][link.node_name1] = link
        #: dict with first node and second node as keys, links as values
        self.link_map = dict(link_map)

    def neighbors(self, node_name):
        """Get the neighbors (successors) of a node.

        Args:
            node_name: the name of the node to get neighbors for

        Returns:
            the neighbor nodes
        """
        if node_name not in self.node_names:
            raise ValueError(f"Node {node_name} not in graph")
        if node_name not in self.link_map:
            return []
        return [
            self.nodes[node_name]
            for node_name in self.link_map[node_name].keys()
        ]
