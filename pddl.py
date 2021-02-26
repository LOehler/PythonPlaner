import sys
import expressions
import re

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

def type_to_object(list):
    dict = {"" : []}
    # c1 c2 ... cN - type  has to become type_to_constant[type] = [c1, c2, ... cN]
    l = [] # list supposed to be returned with key in Type_to_constant
    for i, x in enumerate(list):
        if x == "-":
            dict[list[i+1]] = l
            dict[""] += l
            l = []
        elif list[i-1] == "-": # not elegant but efficient. The key itself was already written in previous iteration
            continue
        else:
            l.append(x)
    return dict
     
            
    
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
            
    m_counter = 0 # keeps track of how many sections in the domain are missing
    
    type_hierachy = {} # will be returned empty if :types is missing
    if domain[3][0] == ":types":
        # TYPE_NAME - SUBTYPE_NAME  has to become type_hierachy[TYPENAME_NAME] = SUBTYPE_NAME
        for i, x in enumerate(domain[3][1:]):
            if x == "-":
                if domain[3][i+2] in type_hierachy:
                    l = [] # need to be a new list or dict would return none (for some reason)          
                    for x in type_hierachy[domain[3][i+2]]:
                        l.append(x)
                    l.append(s)
                    type_hierachy[domain[3][i+2]] = l
                else:
                    type_hierachy[domain[3][i+2]] = [s]
            elif domain[3][i] == "-": # not elegant but efficient. The key itself was already written in previous iteration
                continue
            else:
                type_hierachy[x] = []
                s = x
    else:
        m_counter += 1
    
    type_to_constant = {}
    if domain[4 - m_counter][0] == ":constants":
        type_to_constant = type_to_object(domain[4 - m_counter][1:]) # getting constants without ":constants"
    else:
        m_counter += 1
        
        
    # ----------- works - so - far ---------------

            
    # Translating actions into when expressions (with every variable substitution from variable)?
    act_sch = domain[5 - m_counter:] # for now just all the rest from the domain
    # TODO fill action schemata more sensible
    
    # Leftover I might need here
#             # PREDICATE_1_NAME ?A1 ?A2 ... ?AN  has to become type_hierachy[PREDICTE_1_NAME] = [?A1 ?A2 ... ?AN]
#         l = [] # list supposed to be returned with key in type_hierachy
#         s = domain[3][1] # the previous key
#         for x in domain[3][1:]:
#             if x[0] == "?":
#                 l.append(x)
#             else:
#                 type_hierachy[s] = l
#                 s = x
#                 l = []
#         type_hierachy[""] = l # rest of list
    
# it is recommended to return a list of an action schemata representation, a dictionary mapping types to sets of constants for each type, and the type hierarchy information. Take care to include an extra mapping from the type "" to a set of all objects.
    return act_sch, type_to_constant, type_hierachy
    
def parse_problem(fname):
    """
    Parses a PDDL problem file contained in the file fname
    
    The return value of this function is passed to planner.plan, and does not have to follow any particular format
    """
    problem = parser(fname)
    
# it is recommend to return a dictionary mapping types to sets of objects for each type (same as for the domain), a list of atoms representing the initial state, and an expression object (perhaps obtained with expressions.make_expression) representing the goal.
    return type_to_object(problem[3][1:]), problem[4][1:], expressions.make_expression(problem[5][1:]) # objects, init, goal
    
    
if __name__ == "__main__":
    print(parse_domain(sys.argv[1]))
    print(parse_problem(sys.argv[2]))

