graph = {
    0: [1, 2, 3],
    1: [0, 3],
    2: [0, 3],
    3: [0, 1, 2, 4],
    4: [3]
}

def BFS(G, start):
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

print(BFS(graph, 1))
# print(isBFSComplete(graph, 0))