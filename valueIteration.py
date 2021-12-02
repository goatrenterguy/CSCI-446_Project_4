from markovDecisionProcess import MDP


def valueIteration(mdp: MDP, epsilon=.001):
    """
    Function for conducting value iteration on an MDP, based on the pseudo code from the text book
    :param mdp: A markov decision process
    :param epsilon: Tunable value for when to stop iterating
    :return: The potential utility for all states
    """
    U1 = {s: 0 for s in mdp.states}
    R, T, gamma = mdp.R, mdp.T, mdp.discountFactor
    while True:
        U = U1.copy()
        delta = 0
        for s in mdp.states:
            U1[s] = R(s) + gamma * max([sum([p * U[s1] for (p, s1) in T(s, a)]) for a in mdp.A(s)])
            delta = max(delta, abs(U1[s] - U[s]))
        if delta < epsilon * (1 - gamma) / gamma:
            return U

