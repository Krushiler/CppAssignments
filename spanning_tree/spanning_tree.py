import json
import math

import matplotlib.pyplot as plt
import networkx as nx
import shapely


def get_spanning_trees(graph):
    edges = []
    nodes = []
    buffer = []

    first_node = list(graph.nodes)[0]
    tree_nodes = list(graph.nodes)
    nodes.append(first_node)
    connected_edges = filter(lambda edge: edge not in nodes,
                             graph.edges(first_node))

    min_edge = min(connected_edges,
                   key=lambda e: graph.get_edge_data(*e)['weight'])

    buffer.append(min_edge[0])
    buffer.append(min_edge[1])
    edges.append(min_edge +
                 (graph.get_edge_data(*min_edge)['weight'],))
    nodes.append(min_edge[1])

    node_index = 0
    iteration_counter = 0
    while len(tree_nodes) > len(nodes):

        iteration_counter += 1
        print(f'Iteration: {iteration_counter}')

        if node_index >= len(tree_nodes):
            node_index = 0
        node = tree_nodes[node_index]
        if node in buffer:
            node_index += 1
            continue

        connected_edges = filter(
            lambda edge:
            edge not in nodes and edge[1] in buffer,
            graph.edges(node)
        )

        edges_to_connect = filter(
            lambda edge:
            edge not in nodes and edge[1] in buffer,
            graph.edges(node)
        )

        if len(list(edges_to_connect)) < 1:
            node_index += 1
            continue

        min_edge = min(
            connected_edges,
            key=lambda e: graph.get_edge_data(*e)['weight']
        )

        buffer.append(min_edge[0])
        buffer.append(min_edge[1])
        edges.append(min_edge +
                     (graph.get_edge_data(*min_edge)['weight'],))
        nodes.append(node)
        node_index += 1

    result = nx.Graph()
    result.add_weighted_edges_from(edges)
    result.add_nodes_from(nodes)
    return result


def split_to_forests(graph, n=3):
    print('start_split_to_forests')
    G2 = get_spanning_trees(graph)

    for i in range(n - 1):
        max_edge = max(G2.edges, key=lambda x: G2.get_edge_data(*x)['weight'])
        G2.remove_edge(*max_edge)

    return [G2.subgraph(c) for c in nx.connected_components(G2)]


def get_clusters(spanning_tree: nx.Graph, n_clusters: int):
    '''Splits the tree into n_clusters clusters'''
    # Sort edges of the spanning_tree
    sorted_edges = sorted(spanning_tree.edges(data=True),
                          key=lambda x: x[2]['weight'], reverse=True)
    copy_tree = spanning_tree.copy()
    for i in range(n_clusters - 1):
        if len(sorted_edges) > i:
            copy_tree.remove_edge(*sorted_edges[i][:2])
    return list(nx.connected_components(copy_tree))


def draw_graph(graph):
    pos = nx.spring_layout(graph)
    plt.figure(figsize=(7, 6))
    nx.draw_networkx_nodes(graph, pos)
    nx.draw_networkx_labels(graph, pos, font_size=20)
    plt.show()


def distance(site1, site2):
    loc1 = site1['location']
    loc2 = site2['location']
    r = 6371
    phi1 = math.radians(loc1['lat'])
    phi2 = math.radians(loc2['lat'])
    dphi = math.radians(loc2['lat'] - loc1['lat'])
    dlambda = math.radians(loc2['lon'] - loc1['lon'])
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(a ** 0.5, (1 - a) ** 0.5)
    return r * c


def make_graph(sites, max_distance=400):
    edges = []
    nodes = []
    for i, site in enumerate(sites[:-1]):
        print(f'{i + 1}/{len(sites) - 1}')
        nodes.append(site['code'])
        min_distance = 10 ** 16
        min_dest = None
        min_dest_flag = True
        for dest in sites[i + 1:]:
            d = distance(site, dest)
            if d <= max_distance:
                edges.append((site['code'], dest['code'], d))
                min_dest_flag = False
            if d < min_distance:
                min_dest = dest
                min_distance = d
        if min_dest_flag:
            edges.append((site['code'], dest['code'], min_distance))
    return edges, nodes


with open('base.json', 'r') as f:
    sites = json.load(f)
    lons = []
    lats = []
    for site in sites:
        lons.append(site['location']['lon'])
        lats.append(site['location']['lat'])

with open('file.json', 'r') as f:
    continents = json.load(f)
    north_america_polygon = continents['features'][1]['geometry']['coordinates']

max_polygon = []
max_area = 0

for i in range(len(north_america_polygon)):
    points = north_america_polygon[i][0]
    area = shapely.Polygon(points).area
    if area > max_area:
        max_polygon = points
        max_area = area

xs, ys = zip(*max_polygon)

north_america = shapely.Polygon(max_polygon)
north_america_sites = []
for site in sites:
    p = shapely.Point((site['location']['lon']), (site['location']['lat']))
    if north_america.contains(p):
        north_america_sites.append(site)

flons = []
flats = []
for site in north_america_sites:
    flons.append(site['location']['lon'])
    flats.append(site['location']['lat'])

edges, nodes = make_graph(north_america_sites)
graph = nx.Graph()
graph.add_nodes_from(nodes)
graph.add_weighted_edges_from(edges)

answer = split_to_forests(graph, 40)
print(len(answer))
print(answer)
