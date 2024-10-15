"""An implementation of Dijkstra's shortest path algorithm"""

__all__ = ['shortest_path']

class NoPath(Exception):
    """Raised by the algorithm if there is no path."""


def shortest_path(graph, source, sink):
    """Find the shortest path between two nodes.

    Args:
        graph: The graph to perform routing on
        source: the name of the source node
        sink: the name of the sink node

    Returns:
        A list of node names for the shortest path

    Raises:
        NoPath: if there is no path
    """

    unvisited = set(graph.node_names)
    prev = {n: None for n in unvisited}
    dist = {n: float('inf') for n in unvisited}
    dist[source] = 0

    while unvisited:
        current_node = min([(dist[n], n) for n in unvisited])[1]
        unvisited.remove(current_node)
        if current_node == sink:
            break

        for neighbor in unvisited.intersection(
                node.name for node in graph.neighbors(current_node)):

            new_dist = dist[current_node] + \
                graph.link_map[current_node][neighbor].length
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                prev[neighbor] = current_node

    nodes = []
    current_node = sink
    while current_node is not None:
        nodes.append(current_node)
        current_node = prev[current_node]
    nodes = nodes[::-1]

    if any([not nodes, nodes[0] != source, nodes[-1] != sink]):
        raise NoPath(source, sink)

    return nodes
