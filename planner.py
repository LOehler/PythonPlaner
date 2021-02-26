import time
import pddl
import graph
import expressions
import pathfinding
import sys 

class ExpNode(graph.Node):
    def __init__(self, name):
        self.name = name
    def get_neighbors(list_of_actions):
        neighbors = []
        self.name
        # for each action generate the neighbor that would be reached by this action
        # for x in list_of_actions:
            # neighbors.append(ExpNode(change_through_action))
        return []# return generated neighbors (Edges with e.g. cost = 1, name = move(agent-1,sq-1-1,sq-2-1), target = ExpNode)
    def get_id(self):
        return self.name
    
def plan(domain, problem, useheuristic=True):
    """
    Find a solution to a planning problem in the given domain 
    
    The parameters domain and problem are exactly what is returned from pddl.parse_domain and pddl.parse_problem. If useheuristic is true,
    a planning heuristic (as developed in Task 4) should be used, otherwise use pathfinding.default_heuristic. This allows you to compare 
    the effect of your heuristic vs. the default one easily.
    
    The return value of this function should be a 4-tuple, with the exact same elements as returned by pathfinding.astar:
       - A plan, which is a sequence of (graph.Edge) objects that have to be traversed to reach a goal state from the start. Each Edge object represents an action, 
         and the edge's name should be the name of the action, consisting of the name of the operator the action was derived from, followed by the parenthesized 
         and comma-separated parameter values e.g. "move(agent-1,sq-1-1,sq-2-1)"
       - distance is the number of actions in the plan (i.e. each action has cost 1)
       - visited is the total number of nodes that were added to the frontier during the execution of the algorithm 
       - expanded is the total number of nodes that were expanded (i.e. whose neighbors were added to the frontier)
    """

    types = problem[0].update(domain[1]) # doesnt work. Again because lists (either find alternativ dict or merge both manually)
    print(type(types), types)
    # start = startnode created from init (problem[1])
#     if useheuristic:
#         pass
#     #else:
#     define neighborhood for each node as actions from domain that are possible (from each node) = graph
#     run and return A* on the constructed graph (or probably procedural generate neighbors while traversing graph)

#     return pathfinding.astar(start, heuristic(), problem[2])
        
    
    
    def heuristic(state, action):
        return pathfinding.default_heuristic
        
    def isgoal(state):
        return True
    
    start = graph.Node()
    return pathfinding.astar(start, heuristic if useheuristic else pathfinding.default_heuristic, isgoal)

def main(domain, problem, useheuristic):
    t0 = time.time()
    (path,cost,visited_cnt,expanded_cnt) = plan(pddl.parse_domain(domain), pddl.parse_problem(problem), useheuristic)
    print("visited nodes:", visited_cnt, "expanded nodes:",expanded_cnt)
    if path is not None:
        print("Plan found with cost", cost)
        for n in path:
            print(n.name)
    else:
        print("No plan found")
    print("needed %.2f seconds"%(time.time() - t0))
    

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], "-d" not in sys.argv)