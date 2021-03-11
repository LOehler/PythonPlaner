import sys
import expressions
import re

SUPPORTED_REQUIREMENTS = [":strips",":typing",":disjunctive-preconditions",":equality",":existential-preconditions",":universal-preconditions",":conditional-effects",":adl"]

# Small Exception raised if PDDL-Domain is supported
class NotSupported(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

# takes a file and tokenizes the input (ignoring comment lines starting with ";")
# the resulting list is then nested depending on the placement of "(" and ")"
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
                
    # nesting into sublists depending on placement of "(" and ")"
    for tocken in tockens:
        if tocken == ")": # Backtracing to last opening paranthesis from closing paranthesis and adding it to the stack again (as a sublist)
            l = [stack.pop()]
            while not l[-1] == "(":
                l.append(stack.pop())
            l.pop() # removing "("
            stack.append(tuple(l[::-1]))
        else:
            stack.append(tocken)
    return stack[0] # stack has only one element

# creates a dictionary that maps types to world objects
# c1 c2 ... cN - type  has to become type_to_constant[type] = [c1, c2, ... cN]
def type_to_object(list):
    dict = {"" : []}
    l = [] # list supposed to be returned with key in Type_to_constant
    for i, x in enumerate(list): # For each element after "-" put previous elements as list in dict 
        if x == "-":
            dict[list[i+1]] = l
            dict[""] += l
            l = []
        elif list[i-1] == "-": # not elegant but efficient. The key itself was already written in previous iteration
            continue
        else:
            l.append(x)
    return dict

# creates a dictionary that maps variables to predicates and also a list containing the variable order
#  ?A1 ?A2 ... ?AN - PREDICATE_1_NAME  has to become dic[PREDICTE_1_NAME] = [?A1 ?A2 ... ?AN]
def make_pred_dic(list):
    dic = {} # dic mapping types to variables
    variables = [] # list containing variables
    var_struc = [] # saves the structure of the variables
    for x in list:
        if x[0] == "?":
            variables.append(x)
            var_struc.append(x)
        elif x == "-":
            continue
        else:
            if x in dic:
                dic[x] += variables
            else:
                dic[x] = variables
            variables = []
    dic[""] = variables # rest of list
    return dic, var_struc

          
    
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
    
    # creating the type hierarchy
    type_hierarchy = {} # will be returned empty if :types is missing
    if domain[3][0] == ":types":
        # TYPE_NAME - SUBTYPE_NAME  has to become type_hierachy[TYPENAME_NAME] = SUBTYPE_NAME
        for i, x in enumerate(domain[3][1:]): # Iterates through types and adds to the sub types to the type (key of type_hierachy)
            if x == "-":
                if domain[3][i+2] in type_hierarchy:
                    type_hierarchy[domain[3][i+2]] += list([from_before])
                else:
                    type_hierarchy[domain[3][i+2]] = list([from_before])
            elif domain[3][i] == "-":
                continue
            elif x in type_hierarchy:
                from_before = x
            else:
                type_hierarchy[x] = []
                from_before = x
    else:
        m_counter += 1
    
    # mapping constants to types
    type_to_constant = {}
    if domain[4 - m_counter][0] == ":constants":
        type_to_constant = type_to_object(domain[4 - m_counter][1:]) # getting constants without ":constants"
    else:
        m_counter += 1
        
    # Predicates not needed since they are already contained in the structure of precondition/effect
    
    # Action schemat contains a list of tuples for each action with precondition (Expression)
    #                                                               effect (Expression)
    #                                                               param_structure (list) - list containing the order of the variables
    #                                                               pred_dic (dict) - dictionary mapping variables to predicates
    act_sch = []
    for action in domain[6 - m_counter:]:
        precondition = expressions.make_expression(action[5])
        effect = expressions.make_expression(action[7])
        pred_dic, param_structure = make_pred_dic(action[3]) # dictionary of the predicates
        act_sch.append([action[1], precondition, effect, param_structure, pred_dic])

    return act_sch, type_to_constant, type_hierarchy
    
def parse_problem(fname):
    """
    Parses a PDDL problem file contained in the file fname
    
    The return value of this function is passed to planner.plan, and does not have to follow any particular format
    """
    problem = parser(fname)
    
    # Getting initial world atoms to be tuples (instead of lists)
    tmp = problem[4][1:]
    init = []
    for x in tmp:
        init.append(tuple(x))

    return type_to_object(problem[3][1:]), init, expressions.make_expression(problem[5][1:][0]) # objects, init, goal
    
    
if __name__ == "__main__":
    print(parse_domain(sys.argv[1]))
    print(parse_problem(sys.argv[2]))

