# Look for #IMPLEMENT tags in this file. These tags indicate what has
# to be implemented to complete the warehouse domain.
#
# You may add only standard python imports---i.e., ones that are automatically
# available on TEACH.CS
# You may not remove any imports.
# You may not import or otherwise source any of your own files

import os
from search import *  # for search engines
from snowman import SnowmanState, Direction, snowman_goal_state  # for snowball specific classes
from test_problems import PROBLEMS  # 20 test problems


def heur_manhattan_distance(state):
    # IMPLEMENT
    '''admissible sokoban puzzle heuristic: manhattan distance'''
    '''INPUT: a snowman state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    # We want an admissible heuristic, which is an optimistic heuristic.
    # It must never overestimate the cost to get from the current state to the goal.
    # The sum of the Manhattan distances between each snowball that has yet to be stored and the storage point is such a heuristic.
    # When calculating distances, assume there are no obstacles on the grid.
    # You should implement this heuristic function exactly, even if it is tempting to improve it.
    # Your function should return a numeric value; this is the estimate of the distance to the goal.
    result = 0
    for snowball in state.snowballs:
        result += abs(snowball[0] - state.destination[0])
        result += abs(snowball[1] - state.destination[1])

    return result


# HEURISTICS
def trivial_heuristic(state):
    '''trivial admissible snowball heuristic'''
    '''INPUT: a snowball state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state (# of moves required to get) to the goal.'''
    return len(state.snowballs)


def heur_alternate(state):
    # IMPLEMENT
    '''a better heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    # heur_manhattan_distance has flaws.
    # Write a heuristic function that improves upon heur_manhattan_distance to estimate distance between the current state and the goal.
    # Your function should return a numeric value for the estimate of the distance to the goal.

    top = state.height - 1
    right = state.width - 1
    destination = state.destination
    robot = state.robot
    snowballs = state.snowballs
    obstacles = state.obstacles
    result = 0
    small_weight = 1.0
    medium_weight = 1.1
    big_weight = 1.2
    small_path = 0.3
    medium_path = 0.7
    big_path = 1.5

    for snowball, size in snowballs.items():
        if (snowball[0] == 0 or snowball[0] == right) and snowball[0] != destination[0]:
            return float("inf")
        if (snowball[1] == 0 or snowball[1] == top) and snowball[1] != destination[1]:
            return float("inf")

        if snowball != destination:
            if ((snowball[0] - 1, snowball[1]) in obstacles or snowball[0] == 0) \
                    and ((snowball[0], snowball[1] - 1) in obstacles or snowball[1] == 0):
                return float("inf")
            elif ((snowball[0] + 1, snowball[1]) in obstacles or snowball[0] == right) \
                    and ((snowball[0], snowball[1] - 1) in obstacles or snowball[1] == 0):
                return float("inf")
            elif ((snowball[0] - 1, snowball[1]) in obstacles or snowball[0] == 0) \
                    and ((snowball[0], snowball[1] + 1) in obstacles or snowball[1] == top):
                return float("inf")
            elif ((snowball[0] + 1, snowball[1]) in obstacles or snowball[0] == right) \
                    and ((snowball[0], snowball[1] + 1) in obstacles or snowball[1] == top):
                return float("inf")

        if size == 2:
            result += small_weight * abs(snowball[0] - destination[0])
            result += small_weight * abs(snowball[1] - destination[1])
            result += small_path * abs(snowball[0] - robot[0])
            result += small_path * abs(snowball[1] - robot[1])
        elif size == 1:
            result += medium_weight * abs(snowball[0] - destination[0])
            result += medium_weight * abs(snowball[1] - destination[1])
            result += medium_path * abs(snowball[0] - robot[0])
            result += medium_path * abs(snowball[1] - robot[1])
        elif size == 0:
            result += big_weight * abs(snowball[0] - destination[0])
            result += big_weight * abs(snowball[1] - destination[1])
            if snowball != destination:
                result += big_path * abs(snowball[0] - robot[0])
                result += big_path * abs(snowball[1] - robot[1])
        elif size == 4:
            result += (small_weight + medium_weight) * abs(snowball[0] - destination[0])
            result += (small_weight + medium_weight) * abs(snowball[1] - destination[1])
            result += (small_path + medium_path) * abs(snowball[0] - robot[0])
            result += (small_path + medium_path) * abs(snowball[1] - robot[1])
        elif size == 5:
            result += (small_weight + big_weight) * abs(snowball[0] - destination[0])
            result += (small_weight + big_weight) * abs(snowball[1] - destination[1])
            result += (small_path + big_path) * abs(snowball[0] - robot[0])
            result += (small_path + big_path) * abs(snowball[1] - robot[1])
        elif size == 3:
            result += (big_weight + medium_weight) * abs(snowball[0] - destination[0])
            result += (big_weight + medium_weight) * abs(snowball[1] - destination[1])
            if snowball != destination:
                result += (big_path + medium_path) * abs(snowball[0] - robot[0])
                result += (big_path + medium_path) * abs(snowball[1] - robot[1])
        elif size == 6:
            result += (big_weight + medium_weight + small_weight) * abs(snowball[0] - destination[0])
            result += (big_weight + medium_weight + small_weight) * abs(snowball[1] - destination[1])
            if snowball != destination:
                result += (big_path + medium_path + small_path) * abs(snowball[0] - destination[0])
                result += (big_path + medium_path + small_path) * abs(snowball[1] - destination[1])

    return result


def heur_zero(state):
    '''Zero Heuristic can be used to make A* search perform uniform cost search'''
    return 0


def fval_function(sN, weight):
    # IMPLEMENT
    """
    Provide a custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.

    @param sNode sN: A search node (containing a SokobanState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """

    # Many searches will explore nodes (or states) that are ordered by their f-value.
    # For UCS, the fvalue is the same as the gval of the state. For best-first search, the fvalue is the hval of the state.
    # You can use this function to create an alternate f-value for states; this must be a function of the state and the weight.
    # The function must return a numeric f-value.
    # The value will determine your state's position on the Frontier list during a 'custom' search.
    # You must initialize your search engine object as a 'custom' search engine if you supply a custom fval function.
    return sN.gval + weight * sN.hval


def anytime_weighted_astar(initial_state, heur_fn, weight=100, timebound=5):
    # IMPLEMENT
    '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    '''implementation of weighted astar algorithm'''
    current = os.times()[0]
    time_limit = timebound + current
    cost_bound = (float("inf"), float("inf"), float("inf"))
    prime_result = False


    wrapped_fval_function = (lambda sN: fval_function(sN, weight))
    strategy = SearchEngine('custom', 'default')
    strategy.init_search(initial_state, snowman_goal_state, heur_fn, wrapped_fval_function)

    while current < time_limit:
        timebound = time_limit - current
        weight -= 0.1
        result = strategy.search(timebound, cost_bound)
        if result:
            if result.gval < cost_bound[0]:
                cost_bound = (result.gval, float("inf"), result.gval)
                prime_result = result
        current = os.times()[0]

    return prime_result


def anytime_gbfs(initial_state, heur_fn, timebound=5):
    # IMPLEMENT
    '''Provides an implementation of anytime greedy best-first search, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    '''implementation of weighted astar algorithm'''

    current = os.times()[0]
    time_limit = timebound + current
    prime_cost = (float("inf"), float("inf"), float("inf"))
    prime_result = False

    strategy = SearchEngine('best_first', 'default')
    strategy.init_search(initial_state, snowman_goal_state, heur_fn)

    while current < time_limit:
        timebound = time_limit - current
        result = strategy.search(timebound, prime_cost)
        if result:
            if result.gval < prime_cost[0]:
                prime_cost = (result.gval, float("inf"), result.gval)
                prime_result = result
        current = os.times()[0]

    return prime_result

    # cost_bound = (search_result.gval, search_result.gval, search_result.gval)

    return result
