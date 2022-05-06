# does not work yet
def BFS(graph, start):
    visited = [False for i in range(len(graph))]
    visitedOrder = []
    queueVisited = []

    visited[start - 1] = True
    queueVisited.append(start)
    visitedOrder.append(start)
    while queueVisited:
        node = queueVisited.pop(0)
        if not visited[node - 1]:
            visited[node - 1] = True
            visitedOrder.append(node)
            for neighbors in graph[node]:
                queueVisited.append(neighbors)
    return visitedOrder

graph = {
    1: [2, 3],
    2: [3, 1],
    3: [2, 1]
}

a = BFS(graph, 1)
print(a)
