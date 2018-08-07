from __future__ import print_function
from tulip import tlp
from tulipgui import tlpgui
import numpy as np
import time
import os
import cmath

'''
function:out_to_txt(output_list,filename):
returns:none

output the content in the output_list to the file filename.
always overwrite.
'''
def out_to_txt(output_list, outfilename = 'output.txt'):
        f = open(outfilename,'w')
        counter = 0
        for row in output_list:
                if counter == 0:
                        print(row[0],row[1],file=f)
                else:
                        print(row[0],row[1],row[2],file=f)
                counter = counter + 1

'''
function:get_files(root_path)
returns: list of string
param: root_path, The path of the document

returns the list of files(which store graphs)
'''
def Get_files(root_path):
	files = os.listdir(root_path)
	return files

'''
function:load_graph(filename):
returns: nnode(int), nedge(int), data(list)

returns the graph's number of nodes, edges and
the edge datas.

'''
def Load_graph(filename):
	print("Loading data:",filename)
	nnode = 0
	nedge = 0
	with open(filename) as f:
		header = f.readline()
		nnode,nedge = [int(i) for i in header.split()]
	rawdata = np.loadtxt(filename,dtype=int,skiprows=1)
	data = [(e[0],e[1]) for e in rawdata]
	print("Data Loaded!")
	return nnode,nedge, data


'''
function:execute(root_path, graphname,layoutname)
returns:time(double)

Applying the layout 'layoutname' to the graph 'graphname'.
graph should be placed in the root_path folder.
Automatically computes the time.
'''

def Execute(ith, root_path, graphname,layoutname):
	#Inserting nodes and edges.
	nnode,nedge,data = Load_graph(root_path + graphname)
	graph = tlp.newGraph()
	nodes = graph.addNodes(nnode)
	data2 = [(nodes[n[0]],nodes[n[1]]) for n in data]
	graph.addEdges(data2)

	#Initializing the graph.
	viewLayout = graph.getLayoutProperty("viewLayout")
	LayoutName = 'Random layout'
	LayoutParams = tlp.getDefaultPluginParameters(LayoutName, graph)
	graph.applyLayoutAlgorithm(LayoutName, viewLayout, LayoutParams)
	print("Graph Initalized!")

	#Applying layout.
	LayoutName = layoutname
	LayoutParams = tlp.getDefaultPluginParameters(LayoutName, graph)

	print ('Nodes number:', len(nodes))

	LayoutParams['number of pivots'] = int(len(nodes) ** 0.5)
	# LayoutParams['number of pivots'] = 250

	time_start = time.time()
	print ("Start applying layout: ",LayoutName," Current time is ")
	print (time.asctime(time.localtime(time_start)))

	graph.applyLayoutAlgorithm(LayoutName, viewLayout, LayoutParams)

	print("Layout Finished!")
	time_end = time.time()
	time_cost = time_end-time_start
	print ("Total time cost: ", time_cost)

	#Output to the files.
	outpath = "outputs/"
	mylist = [(nnode,2)]
	coords = [viewLayout.getNodeValue(n) for n in nodes]
	counter = 0
	for c in coords:
		row = (counter,c[0],c[1])
		mylist.append(row)
		counter = counter + 1
	out_to_txt(mylist,outfilename=outpath + os.path.splitext(graphname)[0]+ "/" + LayoutName + "_" + str(ith) + "_vec2D.txt")

	return time_cost


'''
set the graphname
'''
graphname = 'data/dwt_72.txt'

'''
choose one layout algorithm from below:
'3-Connected (Tutte)', 'Balloon (OGDF)', 'Bertault (OGDF)',
'Bubble Pack', 'Bubble Tree', 'Circular', 'Circular (OGDF)',
'Cone Tree', 'Connected Component Packing', 'Connected Component Packing (Polyomino)',
'Davidson Harel (OGDF)', 'Dendrogram', 'Dominance (OGDF)', 'FM^3 (OGDF)',
'Fast Multipole Embedder (OGDF)', 'Fast Multipole Multilevel Embedder (OGDF)',
'Fast Overlap Removal', 'Frutcherman Reingold (OGDF)', 'GEM (Frick)',
'GEM Frick (OGDF)', 'GRIP', 'Hierarchical Graph', 'Hierarchical Tree (R-T Extended)',
'Improved Walker', 'Improved Walker (OGDF)', 'Kamada Kawai (OGDF)', 'LinLog',
'MMM Example Fast Layout (OGDF)', 'MMM Example Nice Layout (OGDF)',
'MMM Example No Twist Layout (OGDF)', 'Mixed Model', 'OrthoTree',
'Perfect aspect ratio', 'Pivot MDS (OGDF)', 'Planarization Grid (OGDF)',
'Planarization Layout (OGDF)', 'Random layout', 'Squarified Tree Map',
'Stress Majorization (OGDF)', 'Sugiyama (OGDF)', 'Tile To Rows Packing (OGDF)',
'Tree Leaf', 'Tree Radial', 'Upward Planarization (OGDF)', 'Visibility (OGDF)'
'''

# layoutAlgorithms = ['Kamada Kawai (OGDF)']
# layoutAlgorithms = ['Frutcherman Reingold (OGDF)']
# layoutAlgorithms = ['Stress Majorization (OGDF)']
layoutAlgorithms = ['Pivot MDS (OGDF)']
# layoutAlgorithms = ['FM^3 (OGDF)']


layoutname = ''

data_root_path = 'data/'
files = Get_files(data_root_path)
print(files)
#files = ['fe_4elt2.txt', 'bcsstk09.txt', 'dwt_1005.txt',
#'Flan_1565.txt', 'fe_ocean.txt', 'bcsstk31.txt', 'fe_body.txt', 'dwt_72.txt']
# files = ['dwt_72.txt','dwt_419.txt','dwt_1005.txt','block_2000.txt','3elt.txt','G65.txt','fe_4elt2.txt','barth5.txt','bcsstk31.txt','fe_ocean.txt','troll.txt','Flan_1565.txt']
# files = ['dwt_419.txt','dwt_1005.txt','block_2000.txt','3elt.txt','G65.txt','fe_4elt2.txt']
# files = ['dwt_419.txt']
# files = ['dwt_1005.txt']
# files = ['block_2000.txt']
# files = ['3elt.txt']
# files = ['G65.txt']
# files = ['fe_4elt2.txt']
# files = ['bcsstk31.txt']
# files = ['fe_ocean.txt']
# files = ['troll.txt']
files = ['Flan_1565.txt']

for graphname in files:
	for layoutname in layoutAlgorithms:
		f = open("summary.txt",'a')
		print(graphname, layoutname, file=f)
		for ith in range(7, 10):
			print("Case" + str(ith))			
			cost = Execute(ith, data_root_path, graphname, layoutname)
			print(cost, file = f)
		f.close()
#Using SSH linux, GUI is not needed.
# nodeLinkView = tlpgui.createNodeLinkDiagramView(graph)
                                      