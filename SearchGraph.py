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
    9: [8]
}

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

def isBFSComplete(G, start):
    returnVisit = BFS(G, start)
    if len(returnVisit) == len(G.keys()):
        return True
    return False

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

def isDFSComplete(G, start):
    returnVisit = DFS(G, start)
    if len(returnVisit) == len(G.keys()):
        return True
    return False

print(BFS(graph, 0))
print(DFS(graph, 0))