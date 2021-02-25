import sys
import expressions
import re
from queue import LifoQueue as LQ

SUPPORTED_REQUIREMENTS = [":strips",":typing",":disjunctive-preconditions",":equality",":existential-preconditions",":universal-preconditions",":conditional-effects",":adl"]

# Small Exception raised if PDDL-Domain is supported
class NotSupported(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message
        
def parser(fname):
    stack = []
    str_file = ""
    file = open(fname, "r")
    for line in file.readlines():
        if not ";" in line: # Comments are assumed to be on new lines (like it is in all the cases I looked so far)
                            # Now it checks for all charackters in whole file (would be better if it checks just for the first one)
            str_file += line.lower() # PDDL is case sensitive
    file.close()
    tockens = re.findall(r"([:|\?]?[\w+-?]+\w+|[(|)|-])", str_file) # getts all the occurences of the stuff we need
                        # translation of regular expression optionally ":" or "?" with arbitrarily many letters following it (word or number)
                        #                                    optionally followed by other words joined by "-"
                        #                                    or paranthesis or "-"
    for tocken in tockens:
        if tocken == ")": # Backtracing to last opening paranthesis from closing paranthesis and adding it to the stack again (as a sublist)
            l = [stack.pop()]
            while not l[-1] == "(":
                l.append(stack.pop())
            l.pop() # removing "("
            stack.append(l[::-1])
        else:
            stack.append(tocken)
    return stack[0] # stack has only one element

    
def parse_domain(fname):
    """
    Parses a PDDL domain file contained in the file fname
    
    The return value of this function is passed to planner.plan, and does not have to follow any particular format
    """
    domain = parser(fname)
    
    #checking requirements
    requirements = domain[2][1:] # no check needed, requirements is not optional
    for x in requirements:
        if x not in SUPPORTED_REQUIREMENTS:
            raise NotSupported(x, "Planner does not support it")
    
    type_to_constant = {key: None for key in domain[3][1:]} # should I check first if domain[3][0] == ":types"  ?
    for i, constant in enumerate(domain[4][3::3]): # again, should I check first if domain[4][0] == ":constants"  ?
                                                    # for every third element in the constants list of the domain (starting from 3rd)
        type_to_constant[constant] = [domain[4][i*3+1]] # map the type to the constant as list (+1 to ignore "constants")
        # mapping to sets of constants. Lists for the non constants (objects) are later provided by parse problem
        
    # ----------- works - so - far ---------------
            
    type_hierachy = {}
            
    # Translating actions into when expressions (with every variable substitution from variable)?
    act_sch = [] # TODO fill action schemata
    
# it is recommended to return a list of an action schemata representation, a dictionary mapping types to sets of constants for each type, and the type hierarchy information. Take care to include an extra mapping from the type "" to a set of all objects.
    return act_sch, type_to_constant, type_hierachy
    
def parse_problem(fname):
    """
    Parses a PDDL problem file contained in the file fname
    
    The return value of this function is passed to planner.plan, and does not have to follow any particular format
    """
    problem = parser(fname)
    
# it is recommend to return a dictionary mapping types to sets of objects for each type (same as for the domain), a list of atoms representing the initial state, and an expression object (perhaps obtained with expressions.make_expression) representing the goal.
    return None
    
    
if __name__ == "__main__":
    print(parse_domain(sys.argv[1]))
    print(parse_problem(sys.argv[2]))

