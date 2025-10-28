import math
inf = math.inf
x = -inf # no path from ... to ... in adjacency matrix

# predecessor of discovered node
pred = []
# costs to starting node s
cost = []
# set of finished nodes
f = []
# length of the graph
n = None
# graph
g = None

pq = []
def extract_min(pq):
   min_index = 0
   for i in range(1, len(pq)):
      if cost[pq[i]] < cost[pq[min_index]]:
         min_index = i
   min_index = pq.pop(min_index)
   return min_index

def initialization(s, graph):
   global pred, cost, f, pq, n, g
   g = graph 
   n = len(g) 
   pred = [-1]*n
   cost = [inf]*n
   cost[s] = 0
   f = []
   pq = [i for i in range(n)]

def relax(u, v):
   if cost[v] > cost[u] + g[u][v]:
      cost[v] = cost[u] + g[u][v]
      pred[v] = u

def dijkstra():
   while len(pq) > 0:
      u = extract_min(pq)
      f.append(u)
      for v in range(n):
         if g[u][v] > 0:
            relax(u,v)

def get_path(u, v):
   if pred[v] == -1:
      return []
   # start from last node
   path = [v]
   while u != v:
      v = pred[v]
      path.insert(0,v)
   return path
