import networkx as nx
import matplotlib.pyplot as plot
import Tkinter as tk

G = nx.Graph()

def mapping(x):
	return ""

with open("nodes.csv", 'r') as file:
	lines = [line.rstrip('\n') for line in file]
	for line in lines:
		words = line.split(',')
		G.add_node(words[0])

with open("links.rn", "r") as file:
	lines = [line.rstrip('\n') for line in file]
	for line in lines:
		words = line.split(',')
		G.add_edge(words[0], words[1])

nx.spring_layout(G, dim=2, k=None, pos=None, fixed=None, iterations=50, weight='weight', scale=1.0)

nx.draw_networkx(G,with_labels=False, node_size = 1)
plot.show()
