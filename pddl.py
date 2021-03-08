import sys
import expressions
import re

SUPPORTED_REQUIREMENTS = [":strips",":typing",":disjunctive-preconditions",":equality",":existential-preconditions",":universal-preconditions",":conditional-effects",":adl"]


class NotSupported(Exception):
    """Small Exception raised if PDDL-Domain is supported"""
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


def tokenize(fname):
    """takes filename and returns tokenized nested list of relevant input"""
    stack = []
    str_file = ""
    file = open(fname, "r")
    for line in file.readlines():
        if not ";" in line: # Comments are assumed to be on new lines (like it is in all the cases I looked so far)
                            # Now it checks for all charackters in whole file (would be better if it checks just for the first one)
            str_file += line.lower() # PDDL is case sensitive
    file.close()
    tokens = re.findall(r"([:|\?]?[\w+-?]+\w+|[(|)|-])", str_file) # getts all the occurences of the stuff we need
                        # translation of regular expression optionally ":" or "?" with arbitrarily many letters following it (word or number)
                        #                                    optionally followed by other words joined by "-"
                        #                                    or paranthesis or "-"
    for token in tokens:
        if token == ")":  # Backtracing to last opening paranthesis from closing paranthesis and adding it to the stack again (as a sublist)
            l = [stack.pop()]
            while not l[-1] == "(":
                l.append(stack.pop())
            l.pop()  # removing "("
            stack.append(l[::-1])
        else:
            stack.append(token)
    return stack[0]  # stack has only one element


def create_dict(types_list):
    """creates dictionary (keys = content of :types)"""
    dict_types = {}
    # make keys
    if types_list[0] == ":types":  # just checking, can be del

        # both of the following work:
        # dict_types = {i: [] for i in sub_list[1:] }#and i != "-"}
        dict_types = dict.fromkeys(types_list[1:], [])

        # TODO
        # cur problem: "-" is in dict bc it is in types
        # cannot delete dash bc we need it for hierarchy
        # just letting it in for now

    dict_types[""] = []  # if no dash
    return dict_types


def assign_to_types(sub_list, dict_types):
    """filling dict_types with everything that belongs to certain type"""

    i = 0  # reset for each sublist
    stack = []

    # TODO steal the enumerate thing from lukas

    for char in sub_list:
        if char != '-':
            if sub_list[i - 1] == '-':  # check if char == key and skip
                i += 1
            else:
                stack.append(char)
                i += 1
        if char == '-':
            key = sub_list[i + 1]
            dict_types[key] = []  # DO NOT DEL THIS LINE!!!
            dict_types[key].append(  # append not overwrite
                    stack[0])  # stack[0] to get rid of nested list
            stack = []  # reset
            i += 1

        # no type assigned
        if "-" not in sub_list and sub_list[0] == ":types":
            dict_types[""] = sub_list

    return dict_types


def create_hierarchy(dict_types):
    """
    >check if key is entry of other key
    >if key is a subtype
    >then copy all entries of subtype to entry of type
    >and delete subtype from entry of type
    """

    for key_i in dict_types:
        for key_j in dict_types:
            if key_i in dict_types[key_j]:  # if key_i is a subtype

                dict_types[key_j].remove(key_i)  # delete subtype in entry of type

                if dict_types[key_i]:  # if subtype already has entries
                    list_to_copy = dict_types[key_i]  # copy entries of subtype
                    # add to key_i
                    for item in list_to_copy:
                        dict_types[key_j].append(item)  # works
                    #  dict_types[key_j].append(list_to_copy)  # would work too but nested lists
            else:
                continue

    return dict_types


def make_act_sch(sublist, dict_types):

    act_sch = {}


    print("sub_list[3]", sublist[3])
    name = sublist[1]  # works
    parameter = assign_to_types(sublist[3], dict_types)  # works
    precondition = expressions.make_expression(sublist[5])  # works
    effect = expressions.make_expression(sublist[7])  # works
    #         precondition = action[5]
    #         effect = action[7]

    # TODO check if wumpus alive

    print("name", name)
    print("parameter", parameter)
   # act_sch.append((name, parameter, precondition, effect))  # TODO issue with parameter (is overwritten each time)

    act_sch = [name, parameter, precondition, effect]
    #nested_dict = dict.fromkeys()
  #  act_sch = dict.fromkeys(name, [])
    print("act_sch", act_sch)

    return act_sch


def parse_domain(fname_domain, fname_prob):
    """
    Parses a PDDL domain file contained in the file fname
    
    The return value of this function is passed to planner.plan, and does not have to follow any particular format

    Hint: it is recommended to return a list of an action schemata representation, a dictionary mapping types to sets of
    constants for each type, and the type hierarchy information. Take care to include an extra mapping from the type ""
    to a set of all objects.
    """

    tokens = tokenize(fname_domain)[1:]  # cut off ['define'
    print("tokens", tokens)

    # checking requirements
    requirements = tokens[1][1:]  # no check needed, requirements is not optional
    for x in requirements:
        if x not in SUPPORTED_REQUIREMENTS:
            raise NotSupported(x, "Planner does not support it")

    tokens = tokens[2:]  # cut off ['domain', 'wumpus-adl'], [':requirements', ':adl', ':typing']

    dict_types = create_dict(tokens[0])  # only accessing :types
    print("dict_types", dict_types)

    for sub_list in tokens:  # iterating to find stuff like constants # TODO skip and access constants directly
        assignment_dict = assign_to_types(sub_list[1:], dict_types)
    print("assignment", assignment_dict)


    dict_hierarchy = create_hierarchy(assignment_dict)
    print("hierarchy types", dict_hierarchy)

    all_actions = []
    for sub_list in tokens:
        if sub_list[0] == ":action":
            act_sch = make_act_sch(sub_list, dict_hierarchy)
            print("acr", act_sch)
            all_actions.append(act_sch)
            print("all_actions", all_actions)

        # TODO what do we do with :predicates



    #-------------PARSING PROBLEM---------------------------------------------------------------------------------------

    tokens_prob = tokenize(fname_prob)[1:]  # cut off ['define'
  #  print("tokens_prob", tokens_prob)

    for sub_list in tokens_prob:
        if sub_list[0] == ":objects":
            obj_dict = assign_to_types(sub_list[1:], dict_types)

   # print("obj-dict", obj_dict)

    for sub_list in tokens_prob:
        if sub_list[0] == ":init":
            state = sub_list[1:]  # cut off init


    # it is recommended to return a list of an action schemata representation, a dictionary mapping types to sets of constants for each type, and the type hierarchy information. Take care to include an extra mapping from the type "" to a set of all objects.
    return all_actions, dict_hierarchy, obj_dict, state
# (all_actions, dict_hierarchy, obj_dict, state) = parsed


    
def parse_problem(fname):
    """
    Parses a PDDL problem file contained in the file fname
    
    The return value of this function is passed to planner.plan, and does not have to follow any particular format

    Hint: it is recommend to return a dictionary mapping types to sets of objects for each type (same as for the domain),
    a list of atoms representing the initial state, and an expression object (perhaps obtained with expressions.make_expression)
    representing the goal.
    """

    state = []
    tokens = tokenize(fname)[1:]  # ignore define
    print("tokens", tokens)
    
    for sub_list in tokens:
        if sub_list[0] == ":init":
            state = sub_list[1:]  # cut off init



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





    return state
    
    
if __name__ == "__main__":
    print("test")

    #print(parse_domain("type_hierarchy_test.pddl"))
   # print(parse_domain(sys.argv[1]))
    parsed = (parse_domain("domain.pddl", sys.argv[2]))

    (all_actions, dict_hierarchy, obj_dict, state) = parsed
    print("obj_dict", obj_dict)

  #  print(parse_problem(sys.argv[2]))


