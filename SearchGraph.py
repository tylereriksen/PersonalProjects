graph = {
    0: [1, 2, 3],
    1: [0, 3],
    2: [0, 3],
    3: [0, 1, 2, 4],
    4: [3]
}

def BFS(G, start):
    if start not in G.keys():
        raise Exception("Start node is invalid")

    visited = []
    queue = [start]
    while len(queue) > 0:
        node = queue.pop(0)
        if node not in visited:
            visited.append(node)
            for neighbors in G[node]:
                if neighbors not in visited:
                    queue.append(neighbors)
    return visited

def isBFSComplete(G, start):
    returnVisit = BFS(G, start)
    if len(returnVisit) == len(G.keys()):
        return True
    return False

print(BFS(graph, 0))
print(isBFSComplete(graph, 0))