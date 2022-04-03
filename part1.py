from collections import deque
from state import State

goalState = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]
goalNode = State
orginalPuzzleBoard = list()
puzzleLen = 0
puzzleside = 0
depthOfPath = 0
maxQueSize = 0
moves = list()

def main():
    bfsPuzzle = '2,6,3,4,1,0,7,8,5,10,11,12,9,13,14,15' #multiple steps
    dfsPuzzle = '1,2,3,0,5,6,7,4,9,10,11,8,13,14,15,12' # 3 steps
    idsPuzzle = '1,2,3,0,5,6,7,4,9,10,11,8,13,14,15,12' # 3 steps 
    #bfs implemention
    global puzzleLen, puzzleside,orginalPuzzleBoard
    orginalPuzzleBoard = createPuzzle(bfsPuzzle)
    puzzleLen = len(orginalPuzzleBoard)
    puzzleside = int(puzzleLen / 4)
    function = methodTypeForSearch[1]
    function(orginalPuzzleBoard)
    printResultToFile(searchTypeTitle[1])
    resetData() # reset state and inputs
    orginalPuzzleBoard = createPuzzle(dfsPuzzle)
    #dfs implemention
    puzzleLen = len(orginalPuzzleBoard)
    puzzleside = int(puzzleLen / 4)
    function = methodTypeForSearch[2]
    function(orginalPuzzleBoard)
    printResultToFile(searchTypeTitle[2])
    resetData() # reset state and inputs
    orginalPuzzleBoard = createPuzzle(idsPuzzle)
    #ids implemention
    puzzleLen = len(orginalPuzzleBoard)
    puzzleside = int(puzzleLen / 4)
    function = methodTypeForSearch[3]
    function(orginalPuzzleBoard)
    printResultToFile(searchTypeTitle[3])



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

def depthFirstSearch(startState):
    global maxQueSize, goalNode, depthOfPath
    explored, stack = set(), list([State(startState, None, None, 0, 0, 0)])
    while stack:
        node = stack.pop()
        explored.add(node.map)
        if node.state == goalState:
            goalNode = node
            return stack
        neighbors = reversed(expandBoard(node))
        for neighbor in neighbors:
            if neighbor.map not in explored:
                stack.append(neighbor)
                explored.add(neighbor.map)
                if neighbor.depth > depthOfPath:
                    depthOfPath += 1
        if len(stack) > maxQueSize:
            maxQueSize = len(stack)

def depthLimitedSearch(startState, depth):
     global maxQueSize, goalNode, depthOfPath
     explored, stack = set(), list([State(startState, None, None, 0, 0, 0)])
     while stack:
        node = stack.pop()
        explored.add(node.map)
        if node.state == goalState:
            goalNode = node
            print("solution found")
            return stack, True
        if depthOfPath > depth:
            return None, False
        neighbors = reversed(expandBoard(node))
        for neighbor in neighbors:
            if neighbor.map not in explored:
                stack.append(neighbor)
                explored.add(neighbor.map)
                if neighbor.depth > depthOfPath:
                    depthOfPath += 1
        if len(stack) > maxQueSize:
            maxQueSize = len(stack)

def iterativeDeepeningSearch(startState):
    depth = 1
    bottomReached = False  
    while not bottomReached:
        foundSolvedPuzzleYet, bottomReached = depthLimitedSearch(startState, depth)
        if foundSolvedPuzzleYet is not None:
            print("for ids: found puzzle at the depth of ", depth)
        depth*=5 # increasing depth by 5

def expandBoard(node):
    neighbors = list()
    neighbors.append(State(movePuzzleAround(node.state, 1), node, 1, node.depth + 1, node.cost + 1, 0))
    neighbors.append(State(movePuzzleAround(node.state, 2), node, 2, node.depth + 1, node.cost + 1, 0))
    neighbors.append(State(movePuzzleAround(node.state, 3), node, 3, node.depth + 1, node.cost + 1, 0))
    neighbors.append(State(movePuzzleAround(node.state, 4), node, 4, node.depth + 1, node.cost + 1, 0))
    nodes = [neighbor for neighbor in neighbors if neighbor.state]
    return nodes

def movePuzzleAround(state, position):
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

def trackMovements():
    currentNode = goalNode
    while orginalPuzzleBoard != currentNode.state:
        if currentNode.move == 1:
            movement = 'N'
        elif currentNode.move == 2:
            movement = 'S'
        elif currentNode.move == 3:
            movement = 'W'
        else:
            movement = 'E'
        moves.insert(0, movement)
        currentNode = currentNode.parent
    return moves

def printResultToFile(searchType):
    global moves
    moves = trackMovements()
    file = open('result.txt', 'a')
    file.write("Search Type: "+searchType)
    file.write("\norginal puzzle: " + str(orginalPuzzleBoard))
    file.write("\npath taken to solve puzzle: " + str(moves).replace("'", "").replace("[","").replace("]",""))
    file.write("\n")   
    file.write("\n")   
    file.close()

def resetData(): # resert varible to run second search method
    global goalNode, depthOfPath, maxQueSize, moves, goalState
    global puzzleLen, puzzleside
    goalState = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11, 12, 13, 14, 15, 0]
    goalNode = State
    puzzleLen = 0
    puzzleside = 0
    depthOfPath = 0
    maxQueSize = 0
    moves = list()

def createPuzzle(puzzleInput):
    data = puzzleInput.split(",")
    orginalPuzzleBoard = list()
    for element in data:
        orginalPuzzleBoard.append(int(element))
    return orginalPuzzleBoard


methodTypeForSearch = {
    1: breadthFirstSearch,
    2: depthFirstSearch,
    3: iterativeDeepeningSearch
}

searchTypeTitle = {
    1: 'Breadth First Search',
    2: 'Depth First Search',
    3: 'Iterative Deepening Search'
}

main()
