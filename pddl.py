import sys
import expressions
import tokenize

SUPPORTED_REQUIREMENTS = [":strips",":typing",":disjunctive-preconditions",":equality",":existential-preconditions",":universal-preconditions",":conditional-effects",":adl"]

# Small Exception raised if PDDL-Domain is supported
class NotSupported(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message
        
def parser(fname):
    stack = []
    file = open(fname, "r")
    tockens = tokenize(file) # TODO: Ignore PDDL Comments starting with ";"
    for tocken in tockens:
        stack.push(tocken)
        if tocken == ")":
            l = []
            while not tocken == "(":
                l.append(stack.pop)
            stack.append(l)
    file.close()
    return stack
    
def parse_domain(fname):
    """
    Parses a PDDL domain file contained in the file fname
    
    The return value of this function is passed to planner.plan, and does not have to follow any particular format
    """
    domain = parser(fname)[0] # ignore define
    
    #checking requirements
    requirements = [] # TODO: get requirements from domain
    for x in requirements:
        if x not in SUPPORTED_REQUIREMENTS:
            raise NotSupported(x, "Planner does not support it")
    
    # Translating actions into when expressions (with every variable substitution from variable)?
    # Creating and filling dom_dic NECESSARY?
    domain_name = "" # TODO: get domain_name
    dom_dic = {"domain":domain_name, "types":[], "constants":[], "predicates":[], "actions":[]} # WARNING predicates is optional
    
# it is recommended to return a list of an action schemata representation, a dictionary mapping types to sets of constants for each type, and the type hierarchy information. Take care to include an extra mapping from the type "" to a set of all objects.
    return None
    
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

