# attempted to do some little project with BFS and DFS but ended up not finishing

graph = {
    0: [1, 2],
    1: [0, 2, 3, 4],
    2: [0, 1],
    3: [1, 5],
    4: [1],
    5: [3, 6, 7, 8],
    6: [5],
    7: [5, 8],
    8: [5, 7, 9],
    9: [8], 
    10: [11],
    11: [10],
    12: [13],
    13: [12, 14, 15],
    14: [13, 15],
    15: [13, 14]
}

# function for BFS Search
def BFS(G, start):

    # make sure the starting Node is in the graph
    if start not in set(G.keys()):
        raise Exception("Start node is invalid")

    visited = []
    queue = [start]
    while len(queue) > 0:
        node = queue.pop(0)
        if node not in set(visited):
            visited.append(node)
            for neighbors in set(G[node]):
                if neighbors not in set(visited):
                    queue.append(neighbors)
    return visited

# return if the BFS search went through 
# this will also show if a graph is 'strongly connected' or not
def isBFSComplete(G, start):
    returnVisit = BFS(G, start)
    if len(returnVisit) == len(G.keys()):
        return True
    return False

# function for DFS Search
def DFS(G, start):

    # make sure the starting Node is in the graph
    if start not in set(G.keys()):
        raise Exception("Start node is invalid")

    visited = []

    # inner function to search the graph
    def DFS_algo(G, start):
        stack = [start]
        while len(stack) > 0:
            node = stack.pop()
            if node not in set(visited):
                visited.append(node)
                for neighbors in set(G[node]):
                    if neighbors not in set(visited):
                        stack.append(neighbors)
    DFS_algo(G, start)
    return visited

# return if the DFS search went through 
def isDFSComplete(G, start):
    returnVisit = DFS(G, start)
    if len(returnVisit) == len(G.keys()):
        return True
    return False

# function that returns all the "islands" of the graph
def getIslands(G):

    if len(G.keys()) == 0:
        return 0

    start = list(G.keys())[0]
    islands = []

    def lenLists(listOfLists):
        length = 0
        for listBig in listOfLists:
            for listSmall in listBig:
                length += 1
        return length

    while True:
        islands.append(BFS(G, start))
        totalNodesList = set([y for x in islands for y in x])

        if lenLists(islands) == len(G.keys()):
            break

        start = sorted(set(G.keys()).difference(totalNodesList))[0]

    return islands

def numIslands(G):
    return len(getIslands(G))


print(BFS(graph, 0))
print(DFS(graph, 0))
print(getIslands(graph))
print(numIslands(graph))
