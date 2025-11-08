from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    def getAction(self, gameState):
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
    
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    def getAction(self, gameState):
        # Calls the minimax function to choose the best action
        return self.minimax(gameState, self.depth, 0)  # Start with depth 0, Pacman is agent 0

    def minimax(self, gameState, depth, agentIndex):
        # If the depth limit is reached or the game state is a terminal state (win/loss)
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        
        # If it is Pacman's turn (Maximizing agent)
        if agentIndex == 0:
            return self.maxValue(gameState, depth, agentIndex)
        # If it is a ghost's turn (Minimizing agent)
        else:
            return self.minValue(gameState, depth, agentIndex)

    def maxValue(self, gameState, depth, agentIndex):
        # Pacman's move (maximize the evaluation function)
        v = float('-inf')  # start with negative infinity
        legalMoves = gameState.getLegalActions(agentIndex)
        bestAction = None
        
        # Try each legal move and recursively find the best move
        for action in legalMoves:
            successor = gameState.generateSuccessor(agentIndex, action)
            value = self.minimax(successor, depth - 1, 1)  # Next agent is the first ghost (index 1)
            
            if value > v:
                v = value
                bestAction = action
        
        if depth == self.depth:
            return bestAction
        else:
            return v

    def minValue(self, gameState, depth, agentIndex):
        # Ghost's move (minimize the evaluation function)
        v = float('inf')  # start with positive infinity
        legalMoves = gameState.getLegalActions(agentIndex)
        
        # Try each legal move and recursively find the worst value for ghosts
        for action in legalMoves:
            successor = gameState.generateSuccessor(agentIndex, action)
            if agentIndex == gameState.getNumAgents() - 1:
                # After the last ghost, switch to Pacman's turn (index 0)
                value = self.minimax(successor, depth - 1, 0)
            else:
                # Keep going to the next ghost
                value = self.minimax(successor, depth, agentIndex + 1)
            
            v = min(v, value)
        
        return v
