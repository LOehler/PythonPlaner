import time
import pddl
import graph
import expressions
import pathfinding
import sys 

class ExpNode(graph.Node):
    def __init__(self, world, list_of_actions):
        self.world = world
        self.list_of_actions = list_of_actions
    def get_neighbors():
        
        neighbors = []
        # naive approach
#         for action in self.list_of_actions: # move, take, shoot
            
#             for parameters in action[0]: # for parameter in the action parameters
#                 for variable in action[0][parameters]: # for each variable of the paramters (types)
#                     for types in self.world:  # agent, person, wumpus, gold, arrow, square, ""
#                         for atom in self.world[types]: # e.g. sq-1-1, sq-1-2 ...
#                             expressions.substitute(action[1], variable, atom)
                    
            
        # for each action generate the neighbor that would be reached by this action in an edge list
        # for action in self.list_of_actions:
            # for each parameter assignment x that does not violate precondition of self.world
            
                # changed_world = expressions.apply(self.world, x)
                # neighbors.append(Edge(cost = 1, name = "grounded_move(agent-1,sq-1-1,sq-2-1)", target = ExpNode(changed_world, list_of_actions))) #e.g
        return neighbors # generated neighbor edges
    def get_id(self):
        return self.world # or something
    
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
    
    # print("action schemata ", domain[0])
    # print("world ", {**domain[2], **domain[1], **problem[0]})
    
    # create world from the initial atoms and the joined dict (type hierachy, constants, objects)
    world = expressions.make_world(problem[1], {**domain[2], **domain[1], **problem[0]})
    
    # create start node for A* from world and the action schemata
    start = ExpNode(world, domain[0])
    
#     procedural generate neighbors with A*
#           define neighborhood each time as actions from domain that are possible (from each node) = graph
 
        
    def heuristic(state, action):
        return pathfinding.default_heuristic
        
    def isgoal(state):
#         if not expressions.models(state.get_id(), problem[2]): 
#             return False
        return True
    
    # start = graph.Node() # was here before
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