import sys
import expressions
import re # prob not allowed?



# tokenize the input, i.e., converting the sequence of characters in input into a sequence of tokens


def parse_domain(fname):
    """
    Parses a PDDL domain file contained in the file fname
    
    The return value of this function is passed to planner.plan, and does not have to follow any particular format

    Hint: it is recommended to return a list of an action schemata representation, a dictionary mapping types to sets of
    constants for each type, and the type hierarchy information. Take care to include an extra mapping from the type ""
    to a set of all objects.
    """
    return None 
    
def parse_problem(fname):
    """
    Parses a PDDL problem file contained in the file fname
    
    The return value of this function is passed to planner.plan, and does not have to follow any particular format

    Hint: it is recommend to return a dictionary mapping types to sets of objects for each type (same as for the domain),
    a list of atoms representing the initial state, and an expression object (perhaps obtained with expressions.make_expression)
    representing the goal.
    """

    domain = parser(fname)[0]  # ignore define
    print("domain", domain)

    # checking requirements
    requirements = []  # TODO: get requirements from domain
    for x in requirements:
        if x not in SUPPORTED_REQUIREMENTS:
            raise NotSupported(x, "Planner does not support it")

    # Translating actions into when expressions (with every variable substitution from variable)?
    # Creating and filling dom_dic NECESSARY?
    domain_name = ""  # TODO: get domain_name
    dom_dic = {"domain": domain_name, "types": [], "constants": [], "predicates": [],
               "actions": []}  # WARNING predicates is optional

    # it is recommended to return a list of an action schemata representation, a dictionary mapping types to sets of constants
    # for each type, and the type hierarchy information.
    # Take care to include an extra mapping from the type "" to a set of all objects.



    return None
    
    
if __name__ == "__main__":




    #print("sys.argv", sys.argv)
   # print(parse_domain(sys.argv[1]))
   # print(parse_problem(sys.argv[2]))

