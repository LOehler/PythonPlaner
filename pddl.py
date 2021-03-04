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
    print("parser", stack[0])
    return stack[0] # stack has only one element


# TODO split in multiple functions for readability
def assign_types(list_tokens):

    # create dict
    dict_types = {}
    # make keys
    for sub_list in list_tokens:
        if sub_list[0] == ":types":  # didnt clean list yet so idk where :types is and have to iterate over nested_list -> could be prettier?
            # both of the following work:
            # dict_types = {i: [] for i in sub_list[1:] }#and i != "-"}
            dict_types = dict.fromkeys(sub_list[1:], [])

            # TODO
            # cur problem: "-" is in dict bc it is in types
            # cannot delete dash bc we need it for hierarchy
            # just letting it in for now


  #  dict_types[""] = []  # if no dash

    # fill lists
    # example: sub_list[0] == ":constants" to test if assign types work

    print(list_tokens[2:])
    for sub_list in list_tokens[1:]:  # cut off [['domain', 'test-adl']

        # if sub_list[0] == ":types":
        sub_list = sub_list[1:]
        print("sub_list", sub_list)
        i = 0  # reset for each sublist
        stack = []

        for char in sub_list:
            #  print("sub_list for loop", sub_list)
            if char != '-':
                if sub_list[i - 1] == '-':  # check if char == key and skip
                    i += 1
                    # continue
                else:
                    stack.append(char)
                    i += 1
            # print("stack", stack)
            if char == '-':
                #  print("key", sub_list[i+1])  # = key
                if dict_types[sub_list[i + 1]]:  # list not empty -> key already has entries
                    dict_types[sub_list[i + 1]].append(  # append not overwrite
                        stack[0])  # stack[0] to get rid of nested list
                else:
                    dict_types[sub_list[i + 1]] = stack
                print("stack", stack)
                stack = []  # reset
                i += 1



        # no type assigned
        if "-" not in sub_list and sub_list[0] == ":types":
            dict_types[""] = sub_list

        # TODO fix duplicates in list (entries of keys)
    # idea 1: change lists to sets
    # idea 2: use sets from beginning

    # print("dict_types", dict_types)
    # return(dict_types)

   # print("assign types", dict_types)
    return dict_types

def create_hierarchy(dict_types):
    # check if key is entry of other key
    # = if key is a subtype
    # then copy all entries of subtype to other key
    for key_i in dict_types:
        for key_j in dict_types:
            if key_i in dict_types[key_j]:  # if key_i is a subtype
                print("key_i", key_i)
                print("key_j", key_j)

                # delete subtype in entry
                test = dict_types[key_j]
                print("test", test)
                # test.remove(key_i)
                print("", test.remove(key_i))

                if dict_types[key_i]:  # AND already has entries

                    list_to_copy = dict_types[key_i]  # copy entries of subtype
                    print("list to copy", list_to_copy)

                    # add to key_i
                    for item in list_to_copy:
                        dict_types[key_j].append(item)  # works

                    #  dict_types[key_j].append(list_to_copy)  # would work too but nested lists
                    continue
            else:
                continue

    print("dictype", dict_types)
    return dict_types

def parse_domain(fname):
    """
    Parses a PDDL domain file contained in the file fname
    
    The return value of this function is passed to planner.plan, and does not have to follow any particular format

    Hint: it is recommended to return a list of an action schemata representation, a dictionary mapping types to sets of
    constants for each type, and the type hierarchy information. Take care to include an extra mapping from the type ""
    to a set of all objects.
    """

    tokens = parser(fname)[1:]  # cut off ['define'
    print("tokens", tokens)

    assignment = assign_types(tokens)
    print("assignment", assignment)

    dict_hierarchy = create_hierarchy(assignment)
    print("hierarchy types", dict_hierarchy)

    # -------  action schemata confusion   ------

    #predicates = domain[5 - m_counter]  # what to do with predicates?

    # Translating actions into when expressions (with every variable substitution from variable)?
    # or passing it like this:
    act_sch = []
    for action in tokens[6 - m_counter:]:
        parameter = assign_types(
            action[3])  # This should work in a well formed domain. But should I check if action[2] = ":parameters"
        precondition = expressions.make_expression(action[5])
        effect = expressions.make_expression(action[7])
        #         precondition = action[5]
        #         effect = action[7]
        act_sch.append((parameter, precondition, effect))

    # it is recommended to return a list of an action schemata representation, a dictionary mapping types to sets of constants for each type, and the type hierarchy information. Take care to include an extra mapping from the type "" to a set of all objects.
    return act_sch, type_to_constant, type_hierachy

    return None 
    
def parse_problem(fname):
    """
    Parses a PDDL problem file contained in the file fname
    
    The return value of this function is passed to planner.plan, and does not have to follow any particular format

    Hint: it is recommend to return a dictionary mapping types to sets of objects for each type (same as for the domain),
    a list of atoms representing the initial state, and an expression object (perhaps obtained with expressions.make_expression)
    representing the goal.
    """

    tokens = parser(fname)[1:]  # ignore define
    print("tokens", tokens)

    assignment = assign_types(tokens)
    print("assignment", assignment)

    dict_hierarchy = create_hierarchy(assignment)
    print("hierarchy types", dict_hierarchy)

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
    print("test")
    print(parse_domain("type_hierarchy_test.pddl"))
    #print(parse_domain(sys.argv[1]))
    #print(parse_problem(sys.argv[2]))


