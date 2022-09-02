import pandas
from numpy import nan


# Function to create the heuristic graph and main graph
def createGraphs(fileName):
    # Create two graphs and assign their indices
    file = pandas.read_excel(fr'{fileName}')
    cityNames = (pandas.DataFrame(file))["City"].values.tolist()
    citiesGraph = {}
    heuristic = {}
    counter = cityNames.count(nan)
    for i in range(counter):
        cityNames.remove(nan)
    for city in cityNames:
        if city not in citiesGraph:
            citiesGraph[city] = []
        if city not in heuristic:
            heuristic[city] = []
    # Add the edges to the graphs
    for city in citiesGraph:
        distancesTemp = (pandas.DataFrame(file))[city].values.tolist()[:len(cityNames)]
        distances = []
        for num in distancesTemp:
            if num != 0:
                num = num.replace("km", "")
                num = num.replace(" ", "")
                dis = list(map(int, num.split(",")))
                distances.append(dis)
        counter = 0
        for city2 in cityNames:
            if city != city2:
                if len(distances[counter]) == 3:
                    costBetween1and2 = [city2, distances[counter][1]]
                    citiesGraph[city].append(costBetween1and2)
                    heuristicBetween1and2 = [city2, distances[counter][0], distances[counter][2]]
                    heuristic[city].append(heuristicBetween1and2)
                elif len(distances[counter]) == 2:
                    heuristicBetween1and2 = [city2, distances[counter][0], distances[counter][1]]
                    heuristic[city].append(heuristicBetween1and2)
                counter += 1
    return citiesGraph, heuristic


# heuristic function 1 (the aerial (straight line distance) between node and goal)
def h1(heuristicG, node, goal):
    if node == goal:
        return 0
    for i in heuristicG[goal]:
        if i[0] == node:
            return i[1]


# heuristic function 1 (Walking distance between node and goal)
def h2(heuristicG, node, goal):
    if node == goal:
        return 0
    for i in heuristicG[goal]:
        if i[0] == node:
            return i[2]


# Function to get the path, each child city has a parent city.
# Child is the key and the Parent is the value,
# so we can reach all the parent of one child (path)
def getPath(path, start, goal):
    pathList = []
    n = goal
    while path[n] != 0:
        pathList.append(n)
        n = path[n]
    pathList.append(start)
    pathList.reverse()
    return pathList


# Same as previous function but used for Uniform cost and A*
def getPath1(path, start, goal):
    pathList = []
    n = goal
    while path[n][0] != 0:
        pathList.append(n)
        n = path[n][0]
    pathList.append(start)
    pathList.reverse()
    return pathList


def greedyBestFirstSearchH1(graph, heuristic, start, goal):
    if start == goal:
        return "The start node is the goal node!"
    visitedNodes = [start]
    node = start
    while node != goal:
        # sort the nodes by their heuristic values then choose the minimum value and continue.
        nextNode = sorted(graph[node], key=lambda x: h1(heuristic, x[0], goal))[0][0]
        if nextNode in visitedNodes:
            break
        visitedNodes.append(nextNode)
        node = nextNode
    return visitedNodes


def greedyBestFirstSearchH2(graph, heuristic, start, goal):
    if start == goal:
        return "The start node is the goal node!"
    visitedNodes = [start]
    node = start
    while node != goal:
        nextNode = sorted(graph[node], key=lambda x: h2(heuristic, x[0], goal))[0][0]
        if nextNode in visitedNodes:
            break
        visitedNodes.append(nextNode)
        node = nextNode
    return visitedNodes


def breadthFirstSearchBFS(graph, start, goal):
    if start == goal:
        return "The start node is the goal node!"
    node = start
    visitedNodes = [node]
    path = {start: 0}
    counter = 0
    find = False
    while True:
        # sort the nodes alphabetically and choose the first one
        breadthLevel = sorted(graph[node], key=lambda x: x[0])
        for cityDistance in breadthLevel:
            # if the node is not visited, then add it to visited node
            # and to the path graph (used to find the path) with its parent
            if cityDistance[0] not in visitedNodes:
                visitedNodes.append(cityDistance[0])
                path[cityDistance[0]] = node
                if cityDistance[0] == goal:
                    find = True
                    break
        if find:
            return getPath(path, start, goal)
        # if the node is not find then go to the next level for each node and continue
        node = visitedNodes[counter]
        counter += 1


def depthFirstSearchDFS(graph, start, goal):
    if start == goal:
        return "The start node is the goal node!"
    node = start
    visitedNodes = []
    path = {node: 0}
    stack = [node]
    while len(stack) != 0:
        node = stack.pop()
        if node == goal:
            return getPath(path, start, goal)
        if node in visitedNodes:
            continue
        # if the node is not the goal nor in visited nodes then add it to visited nodes
        visitedNodes.append(node)
        # add the children of the node alphabetically to the stack (from z to a)
        for i in sorted(graph[node], key=lambda x: x[0], reverse=True):
            if i[0] in visitedNodes:
                continue
            stack.append(i[0])
            path[i[0]] = node


def uniformCost(graph, start, goal):
    if start == goal:
        return "The start node is the goal node!"
    path = {start: (0, 0)}
    queue = [(start, 0)]
    while len(queue) != 0:
        # sort the nodes by their costs
        queue.sort(key=lambda element: element[1])
        node = queue.pop(0)
        for x in graph[node[0]]:
            # if the node is not visited or the previous cost greater than the newest cost then update
            if x[0] not in path.keys() or path[x[0]][1] > path[node[0]][1] + x[1]:
                path[x[0]] = (node[0], path[node[0]][1] + x[1])
                queue.append((x[0], path[x[0]][1]))
    return "Path: " + str(getPath1(path, start, goal)) + "\nCost: " + str(path[goal][1])


def AStar1(graph, heuristic, start, goal):
    if start == goal:
        return "The start node is the goal node!"
    path = {start: (0, 0)}
    queue = [(start, 0)]
    while len(queue) != 0:
        # sort the nodes by their costs + heuristic
        queue.sort(key=lambda element: element[1] + h1(heuristic, element[0], goal))
        node = queue.pop(0)
        for x in graph[node[0]]:
            # if the node is not visited or the previous cost greater than the newest cost then update
            if x[0] not in path.keys() or path[x[0]][1] > path[node[0]][1] + x[1]:
                path[x[0]] = (node[0], path[node[0]][1] + x[1])
                queue.append((x[0], path[x[0]][1]))
    return "Path: " + str(getPath1(path, start, goal)) + "\nCost: " + str(path[goal][1])


def AStar2(graph, heuristic, start, goal):
    if start == goal:
        return "The start node is the goal node!"
    path = {start: (0, 0)}
    queue = [(start, 0)]
    while len(queue) != 0:
        queue.sort(key=lambda element: element[1] + h2(heuristic, element[0], goal))
        node = queue.pop(0)
        for x in graph[node[0]]:
            if x[0] not in path.keys() or path[x[0]][1] > path[node[0]][1] + x[1]:
                path[x[0]] = (node[0], path[node[0]][1] + x[1])
                queue.append((x[0], path[x[0]][1]))
    return "Path: " + str(getPath1(path, start, goal)) + "\nCost: " + str(path[goal][1])


Data = 'C:/Users/HP/Downloads/DB_Cities.xlsx'
graphOfCities, heuristicGraph = createGraphs(Data)
while True:
    # Print the menu and get the choice
    choice = int(input("Please Choose a number from the following algorithms set:\n"
                       "0- ALL Search Algorithms\n"
                       "1- Uninformed Search\n"
                       "2- Informed Search\n"
                       "3- Greedy Best First Search\n"
                       "4- Greedy Best First Search with air heuristic\n"
                       "5- Greedy Best First Search with walk heuristic\n"
                       "6- Breadth First Search\n"
                       "7- Depth First Search\n"
                       "8- Uniform Cost Search\n"
                       "9- A* Search\n"
                       "10- A* Search with car cost and air heuristic\n"
                       "11- A* Search with car cost and walk heuristic\n"
                       "12- Exit program\n"
                       "Your Choice: "))
    if choice == 12:
        print("Good Bye, 100% is what we deserve, But we will settle for 99%.")
        break
    print("Set of available cities: ", list(graphOfCities.keys()))
    startNode = input("Please Enter The Start city: ")
    while startNode not in graphOfCities.keys():
        print("Please Enter an available city")
        startNode = input()
    number_of_Goals = int(input("Please Enter how many goals you want: "))
    for number in range(number_of_Goals):
        goalNode = input("Please Enter The End city: ")
        while goalNode not in graphOfCities.keys():
            print("Please Enter an available city")
            goalNode = input()
        if choice == 0 or choice == 2 or choice == 3 or choice == 4:
            print("GreedyH1:", greedyBestFirstSearchH1(graphOfCities, heuristicGraph, startNode, goalNode))
        if choice == 0 or choice == 2 or choice == 3 or choice == 4:
            print("GreedyH2:", greedyBestFirstSearchH2(graphOfCities, heuristicGraph, startNode, goalNode))
        if choice == 0 or choice == 1 or choice == 6:
            print("BFS:", breadthFirstSearchBFS(graphOfCities, startNode, goalNode))
        if choice == 0 or choice == 1 or choice == 7:
            print("DFS:", depthFirstSearchDFS(graphOfCities, startNode, goalNode))
        if choice == 0 or choice == 2 or choice == 8:
            print("UC:", uniformCost(graphOfCities, startNode, goalNode))
        if choice == 0 or choice == 2 or choice == 9 or choice == 10:
            print("A*H1:", AStar1(graphOfCities, heuristicGraph, startNode, goalNode))
        if choice == 0 or choice == 2 or choice == 9 or choice == 11:
            print("A*H2:", AStar2(graphOfCities, heuristicGraph, startNode, goalNode))
