

import sys
import csv
import collections
from os import path

node_dictionary = {}
shortest_paths = {}
column_names = []

# The following checks to ensure that one argument is given to the program
if len(sys.argv) != 2:
    script_name = (path.basename(__file__))
    exit('Incorrect number of parameters given. Please enter command in following format:\n'
         'python {} [CSV File]'.format(script_name))


# This function creates the dictionary that contains every node as a key and its distance to other nodes
def create_node_mapping():
    node_dictionary.clear()
    node_csv_reader = csv.reader(open(csv_filename))
    first_column = next(node_csv_reader)
    for row in node_csv_reader:
        temp_dictionary = {}
        for idx, item in enumerate(row):
            # Here we are filtering out the non neighbor nodes
            if idx == 0 or item == '9999':
                continue
            temp_dictionary[first_column[idx]] = int(item)
        node_dictionary[row[0]] = temp_dictionary
    return node_dictionary


def dijkstra_algorithm(initial_node, finishing_node):
    shortest_distance = {}
    path_predecessor = {}
    node_mapping = create_node_mapping()
    unvisited_nodes = node_mapping
    infinity = float('inf')
    node_path = []
    for unvisited_node in unvisited_nodes:
        # Here infinity is set as the shortest distance for unvisited nodes because that is minimum at this time
        shortest_distance[unvisited_node] = infinity
    shortest_distance[initial_node] = 0

    while unvisited_nodes:
        minimum_node = None
        for unvisited_node in unvisited_nodes:
            if minimum_node is None:
                minimum_node = unvisited_node
            elif shortest_distance[unvisited_node] < shortest_distance[minimum_node]:
                # If a shorter path is found set the unvisited node to the new found minumum
                minimum_node = unvisited_node

        for child_node, distance in node_mapping[minimum_node].items():
            if distance + shortest_distance[minimum_node] < shortest_distance[child_node]:
                shortest_distance[child_node] = distance + shortest_distance[minimum_node]
                path_predecessor[child_node] = minimum_node
        # Remove the node that was just visited
        unvisited_nodes.pop(minimum_node)

    current_node = finishing_node
    while current_node != initial_node:
        node_path.insert(0, current_node)
        try:
            # Here the program traverses backwards from the destination node to the original to gain a path.
            current_node = path_predecessor[current_node]
        except KeyError:
            exit('Sorry that node was not found in the given CSV file. Please choose from: \n ' + str(column_names))
    node_path.insert(0, initial_node)
    if shortest_distance[finishing_node] != infinity:
        # If a given path is found it is added to the dictionary of paths
        shortest_paths[finishing_node] = (str(shortest_distance[finishing_node]), node_path)


csv_filename = sys.argv[1]

# Here the CSV file is attempted to be opened and read
try:
    node_csv_reader = csv.reader(open(csv_filename))
except FileNotFoundError:
    exit('Sorry the given file {} was not found. Please choose a valid CSV file.'.format(csv_filename))

first_column = next(node_csv_reader)
node_to_calculate = input('Please, provide the node’s name: ')

for i in range(1, len(first_column)):
    column_names.append(first_column[i])

# Here the shortest path from the input node and all other nodes is calculated
for column in column_names:
    dijkstra_algorithm(node_to_calculate, column)

# Below the paths and costs are seperated to make sorting them easier
path_distances = {}
paths = {}
for key in shortest_paths.keys():
    path_distances[key] = shortest_paths[key][0]
    paths[key] = shortest_paths[key][1]

path_distances = sorted(path_distances.items(), key=lambda dist: dist[0])
path_distances = collections.OrderedDict(path_distances)
paths = sorted(paths.items(), key=lambda kv: len(kv[1]))
paths = collections.OrderedDict(paths)

# Below we print the output of the program in the specified format
print('Shortest path tree for node {}:'.format(node_to_calculate))
for idx, key in enumerate(paths.keys()):
    if key == node_to_calculate:
        continue
    if idx < len(paths.keys()) - 1:
        print('{}, '.format(''.join(paths[key])), end='')
    else:
        print('{}'.format(''.join(paths[key])), end='')

print('\nCosts of least-cost paths for node: {}:'.format(node_to_calculate))

for idx, key in enumerate(path_distances.keys()):
    if idx < len(path_distances.keys()) - 1:
        print('{}:{}, '.format(key, path_distances[key]), end='')
    else:
        print('{}:{}'.format(key, path_distances[key]), end='')
