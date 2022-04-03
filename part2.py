from collections import deque
from state import State
from heapq import heappush, heappop, heapify # liberies used for ques, list etc. 

goalState = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11, 12, 13, 14, 15, 0]
goalNode = State
orginalPuzzleBoard = list()
nodesLookedAt = 0
puzzleLen = 0
puzzleside = 0
depthOfPath = 0
maxQueSize = 0
moves = list()

def main():
   #Example puzzle
   #'2,4,8,0,1,6,3,12,5,7,10,11,9,13,14,15' 
   #'2,6,3,4,1,0,7,8,5,10,11,12,9,13,14,15' 
    puzzleBoard = '2,4,8,0,1,6,3,12,5,7,10,11,9,13,14,15' # change here to test another puzzle. This is multiple steps 17 or so
    global puzzleLen, puzzleside
    data = puzzleBoard.split(",")
    for element in data:
        orginalPuzzleBoard.append(int(element))
    puzzleLen = len(orginalPuzzleBoard)
    puzzleside = int(puzzleLen / 4 ) 
    function = methodTypeForSearch[1]
    function(orginalPuzzleBoard)
    printResultToFile(searchTypeTitle[1])
    resetData()
    puzzleLen = len(orginalPuzzleBoard)
    puzzleside = int(puzzleLen / 4)
    function = methodTypeForSearch[2]
    function(orginalPuzzleBoard)
    printResultToFile(searchTypeTitle[2])

def breadthFirstSearch(startState):
    global maxQueSize, goalNode, depthOfPath
    explored, queue = set(), deque([State(startState, None, None, 0, 0, 0)])
    while queue:
        node = queue.popleft()
        explored.add(node.map)
        if node.state == goalState:
            goalNode = node
            return queue
        neighbors = expandBoard(node)
        for neighbor in neighbors:
            if neighbor.map not in explored:
                queue.append(neighbor)
                explored.add(neighbor.map)
                if neighbor.depth > depthOfPath:
                    depthOfPath += 1
        if len(queue) > maxQueSize:
            maxQueSize = len(queue)

def aStarSearch(startState):
    global maxQueSize, goalNode, depthOfPath
    explored, priorityNode, enteredQue = set(), list(), {}
    key = distanceFromCurrentToChild(startState)
    root = State(startState, None, None, 0, 0, key)
    entry = (key, 0, root)
    heappush(priorityNode, entry)
    enteredQue[root.map] = entry
    while priorityNode:
        node = heappop(priorityNode)
        explored.add(node[2].map)
        if node[2].state == goalState:
            goalNode = node[2]
            return priorityNode
        neighbors = expandBoard(node[2])
        for neighbor in neighbors:
            neighbor.key = neighbor.cost + distanceFromCurrentToChild(neighbor.state)
            entry = (neighbor.key, neighbor.move, neighbor)
            if neighbor.map not in explored:
                heappush(priorityNode, entry)
                explored.add(neighbor.map)
                enteredQue[neighbor.map] = entry
                if neighbor.depth > depthOfPath:
                    depthOfPath += 1
            elif neighbor.map in enteredQue and neighbor.key < enteredQue[neighbor.map][2].key:
                hindex = priorityNode.index((enteredQue[neighbor.map][2].key,
                                     enteredQue[neighbor.map][2].move,
                                     enteredQue[neighbor.map][2]))
                priorityNode[int(hindex)] = entry
                enteredQue[neighbor.map] = entry
                heapify(priorityNode)
        if len(priorityNode) > maxQueSize:
            maxQueSize = len(priorityNode)

def expandBoard(node):
    neighbors = list()
    neighbors.append(State(movePuzzleAround(node.state, 1), node, 1, node.depth + 1, node.cost + 1, 0))
    neighbors.append(State(movePuzzleAround(node.state, 2), node, 2, node.depth + 1, node.cost + 1, 0))
    neighbors.append(State(movePuzzleAround(node.state, 3), node, 3, node.depth + 1, node.cost + 1, 0))
    neighbors.append(State(movePuzzleAround(node.state, 4), node, 4, node.depth + 1, node.cost + 1, 0))
    nodes = [neighbor for neighbor in neighbors if neighbor.state]
    return nodes

def movePuzzleAround(state, position):
    global nodesLookedAt
    nodesLookedAt+=1
    newState = state[:]
    index = newState.index(0)
    if position == 1: 
        if index not in range(0, puzzleside):
            temp = newState[index - puzzleside]
            newState[index - puzzleside] = newState[index]
            newState[index] = temp
            return newState
        else:
            return None
    if position == 2: 
        if index not in range(puzzleLen - puzzleside, puzzleLen):
            temp = newState[index + puzzleside]
            newState[index + puzzleside] = newState[index]
            newState[index] = temp
            return newState
        else:
            return None
    if position == 3: 
        if index not in range(0, puzzleLen, puzzleside):
            temp = newState[index - 1]
            newState[index - 1] = newState[index]
            newState[index] = temp
            return newState
        else:
            return None
    if position == 4: 
        if index not in range(puzzleside - 1, puzzleLen, puzzleside):
            temp = newState[index + 1]
            newState[index + 1] = newState[index]
            newState[index] = temp
            return newState
        else:
            return None

def distanceFromCurrentToChild(startState):
    return sum(abs(current % puzzleside - child % puzzleside) + abs(current//puzzleside - child//puzzleside)
               for current, child in ((startState.index(i), goalState.index(i)) for i in range(1, puzzleLen)))

def trackMovements():
    current_node = goalNode
    while orginalPuzzleBoard != current_node.state:
        if current_node.move == 1:
            movement = 'N'
        elif current_node.move == 2:
            movement = 'S'
        elif current_node.move == 3:
            movement = 'W'
        else:
            movement = 'E'
        moves.insert(0, movement)
        current_node = current_node.parent
    return moves

def printResultToFile(searchType):
    global moves
    moves = trackMovements()
    file = open('result.txt', 'a')
    file.write("Search Type: "+searchType)
    file.write("\norginal puzzle: " + str(orginalPuzzleBoard))
    file.write("\npath taken to solve puzzle: " + str(moves).replace("'", "").replace("[","").replace("]",""))
    file.write("\nnodes looked at: "+str(nodesLookedAt))
    file.write("\n")   
    file.write("\n")   
    file.close()
 
def resetData(): # resert varible to run second search method
    global goalNode, nodesLookedAt
    global puzzleLen, puzzleside, depthOfPath, maxQueSize, moves, goalState
    goalState = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11, 12, 13, 14, 15, 0]
    goalNode = State
    nodesLookedAt = 0
    puzzleLen = 0
    puzzleside = 0
    depthOfPath = 0
    maxQueSize = 0
    moves = list()
  
methodTypeForSearch = {
    1: breadthFirstSearch,
    2: aStarSearch,
}

searchTypeTitle = {
    1: 'Breadth First Search',
    2: 'A* Search'
}

main()

