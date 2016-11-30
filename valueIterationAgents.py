import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        testing = util.Counter()
        testis = self.values
        states = []
        states = mdp.getStates()
        print states
       # actions = mdp.getPossibleActions(states)
        #print actions

        for i in range(iterations):
            temp1 = 0
            #print "values", self.values
            print i
            testing = self.values
            for state in states:
                if mdp.isTerminal(state):
                    self.values[state] = 0
                else:
                    actions = mdp.getPossibleActions(state)
                    for action in actions:
                        temp2 = self.getQValue(state, action)
                        temp1 = max(temp1, temp2)

                        print self.values

                    self.values[state] = temp1




    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        value = 0
        transition = self.mdp.getTransitionStatesAndProbs(state, action)

        for nextState in transition:
            probability = nextState[1]
            reward = self.mdp.getReward(state, action, nextState)
            gamma = self.discount
            valueNext = self.values[nextState[0]]
            value += probability * (reward + (gamma * valueNext))
            print "value:", value
        return value


    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        posActions = self.mdp.getPossibleActions(state)

        if len(posActions) == 0:
            return None
        value = None
        result = None

        for action in posActions:
            temp = self.getQValue(state, action)
            if value is None or temp > value:
                value = temp
                result = value

        return result

        #util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
