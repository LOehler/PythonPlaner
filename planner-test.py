import time
import pddl
import graph
import expressions
import pathfinding
import sys
import re

"""
other approach:
    idea: assign and check if assignment is valid at the same time 
    (only have to loop through the expression once) (instead of substituting and checking) 
    
    how? 
        > break down expression (to atom-lvl like in models()) -> return atom not boolean 
        > go through atom_expression (e.g. ['at', '?who', '?from']) and 
            check in world/state if type can be matched -> is valid 
                > if so, new assignment
"""

def make_new_assignment(obj_dict, action_para_dict, action_precond,state):  # use action -> remember action.name
    """
    return list of diff assignment_dicts
    """
    assignment_dict = {}

  #  action_precond_list = action_precond.string
    action_precond_list = re.findall(r"([:|\?]?[\w+-?]+\w)",  action_precond.string)
    print(action_precond_list)
    print("TYPE", type(action_precond_list))

    while action_precond_list:  # use list.pop(index) ?
        for sublist in state:
            if sublist[0] == action_precond_list[0]:  # at   alternative -> make at, adj, ... to types and check with others in others in 2nd for loop
                # at = [at]
                print(sublist[0])
                sublist = sublist[1:]  # cut off "at"
                action_precond_list = action_precond_list[1:]  # cut off "at"

                assign_possible = True  # init
                print(sublist)

                # while assign_possible:

                # recursion here ?
                for i, sub_atom in enumerate(action_precond_list):

                    print("sublist[i]", sublist[i])
                    print("sub_atom", sub_atom)
                    # if type of expr == type of state ->check if key is the same -> rewrite -> check if entry (now type) is the same
                    #             agent-1                         ?who
                    if obj_dict[sublist[i]] == action_para_dict[sub_atom]:

                        #                   ?who  = [agent-1]
                        assignment_dict[sub_atom] = sublist[i]
                        action_precond_list.remove(sub_atom)
                        print("assignment_dict", assignment_dict)

                    else:  # continue to other sublist! -> TODO: HOW DO I DO THAT
                        pass
                    # assign_possible = False
                    # continue  # to other sublist!
            else:
                continue



            """
            for sub_atom in action_precond_list[1:]:

                print("sub_atom", sub_atom)
                for item in sublist:
                    print("item", item)

                    #             agent-1                         ?who
                    if obj_dict[item] == action_para_dict[sub_atom]:
                        assignment_dict[sub_atom] = item
                        print("assignment_dict", assignment_dict)
            """




    return assignment_dict#, action_name

# TODO handle action_that_was_taken str

def apply_changes(state_before, assignment_dict, action):
    """
    plug assignments in effects
    + copy what hasnt changed
    ? + permutate unbound var if exist ?

    """



    return [] # list of new states + action.name that was used


"""
how to use edge:

edge.target = succ_state
edge.cost = 1
edge.name = str action_that_was_taken
"""


class PlanningState(graph.Node):   # similar to your ExpNode
    def __init__(self, state, list_of_actions):
        self.state = state
        self.list_of_actions = list_of_actions

    def get_id(self):
        return self.state  # .atoms # No Node has same world atoms since they differ in applied changes

    def get_neighbors(self):
        """
        returns list of edge obj
        """


        for action in self.list_of_actions:
            assignment_dict = make_new_assignment(self.state, action)
            # apply_changes(state_before, assignment_dict, action)
            # plus cost
        return neighbors






def main():
    action_para_dict = {"at": ["at"], 'agent': ['?who'], 'wumpus': ['?victim'], 'gold': ['the-gold'], 'arrow': ['?with-arrow'],
                      'square': ['?where-victim'], '': []}

    # act_sch ['move', {'agent': ['?who'], 'wumpus': [], 'gold': ['the-gold'], 'arrow': ['the-arrow'], 'square': ['?to'], '': []}
    action_para_dict = {"at": ["at"], '?who': ['agent'], 'the-gold': ['gold'], '?with-arrow': ['arrow'],
                        '?from': ['square'], '': []}

    print("action_para_dict", action_para_dict)

   # action_precond = expressions.make_expression(("and (alive ?who) (at ?who ?from) (adj ?from ?to)"))
    action_precond = expressions.make_expression(("(at ?who ?from)"))

    print(action_precond)


    #state = pddl.parse_problem(sys.argv[2])
  #  print(state)
    parsed = (pddl.parse_domain("domain.pddl", sys.argv[2]))

    (all_actions, dict_hierarchy, obj_dict, state) = parsed

    # obj_dict {'agent': ['agent-1'], 'wumpus': ['wumpus-1'], 'gold': ['the-gold'], 'arrow': ['?with-arrow'], 'square': ['sq-1-1'], '': []}
    obj_dict = {"at": ["at"], 'agent-1': ['agent'], 'wumpus-1': ['wumpus'], 'the-gold': ['gold'], '?with-arrow': ['arrow'], 'sq-1-1': ['square'], 'sq-1-3': ['square'], '': []}
    print("obj_dict", obj_dict)
    print("state", state)


    print(make_new_assignment(obj_dict, action_para_dict, action_precond,state))





if __name__ == "__main__":
    main()














