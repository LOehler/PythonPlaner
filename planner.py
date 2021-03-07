import time
import pddl
import graph
import expressions
import pathfinding
import sys
from itertools import product

def substitute_all(exp, combi, dic): # substitutes all variables of an expression with values of combi
    subst_exp = exp
    for i, atom in enumerate(combi):
        subst_exp = expressions.Expression(expressions.substitute(subst_exp, list(dic.keys())[i], atom))
    return subst_exp 

class ExpNode(graph.Node):
    def __init__(self, world, list_of_actions):
        self.world = world
        self.list_of_actions = list_of_actions
    def get_neighbors(self):
        neighbors = []
        
        '''current Problems:
        what to do when no type is given for variable in :parameters (why is ?what substituted by agent-1)
        find a better get_id() return
        find a better is_goal definition
        make the creation of joined recursive'''
        
        for action in self.list_of_actions: # e.g. move, take, shoot
              
            # mapping each parameter variable to all possible world ground objects
            variable_atom_mapping = {} # needs to be sorted to run it.products on
            for type in action[1]:
                for variable in action[1][type]:
                    variable_atom_mapping[variable] = self.world.sets[type]  #  get list of ground objects mapped to the variable
           
            sorted_list = sorted(variable_atom_mapping) # needs to be a list for it.product
            # Getting all possible combinations of variabe_atom_mapping entries in an iterator (from itertools)
            combinations = product(*(variable_atom_mapping[variable] for variable in sorted_list))

            # trying out for each combination if precondition holds. If so, it will be applied to the world and a new Edge will be appended to neighbors         
            for combination in combinations:
                subst_exp = substitute_all(action[2], combination, variable_atom_mapping) # substitute the precondition
                if expressions.models(self.world, subst_exp): # if precondition models world
                    grounded_effect = substitute_all(action[3], combination, variable_atom_mapping) # substitue the effect
                    
                    print("applied changes", grounded_effect.string)
                    
                    changed_world = expressions.apply(self.world, grounded_effect) # apply changes to world
                    neighbors.append(graph.Edge(ExpNode(changed_world, self.list_of_actions), 1, f"{action[0]}{tuple(combination)}")) # append new Edge to neighbors target = Nextnode with changed world, cost = 1, name = "action(grounded_variable, grounded_variable ...)"
                    
                    print(f"neighbors in edge {action[0]}{tuple(combination)}")
        
        return neighbors # generated neighbor edges
    
    def get_id(self):
        return self.world#.atoms # No Node has same world atoms since they differ in applied changes
    
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
    joined = {**domain[1], **problem[0]}
    
    for key in list(domain[2].keys()):
        if domain[2][key]: # if key is not empty
            for item in domain[2][key]: # iterate over the subtypes of the type
                if domain[2][item]: # if it is not a subtype of a subtype
                    pass
                    # recurse # not yet implemented but works for now because no subtypes of subtypes in our domain (type hierarchy)
                else:
                    if key in joined:
                        joined[key] += joined[item]
                    else:
                        joined[key] = joined[item]
                    
    # create world from the joined dict (type hierachy, constants, objects) and theinitial atoms and 
    world = expressions.make_world(problem[1], joined)
    
    # create start node for A* from world and the action schemata
    start = ExpNode(world, domain[0])
    
#     procedural generate neighbors with A*
#           define neighborhood each time as actions from domain that are possible (from each node) = graph
 
        
    def heuristic(state, action):
        return pathfinding.default_heuristic(state, action)
        
    def isgoal(state):
#         if not expressions.models(state.world, problem[2]): 
#             return False
        return False#True
    
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