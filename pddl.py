import sys
import expressions
import re

SUPPORTED_REQUIREMENTS = [":strips",":typing",":disjunctive-preconditions",":equality",":existential-preconditions",":universal-preconditions",":conditional-effects",":adl"]

# Small Exception raised if PDDL-Domain is supported
class NotSupported(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


def test(domain):
    m_counter = 0  # keeps track of how many sections in the domain are missing

    type_hierarchy = {}  # will be returned empty if :types is missing
    if domain[2][0] == ":types": # hardcoded here
        # TYPE_NAME - SUBTYPE_NAME  has to become type_hierachy[TYPENAME_NAME] = SUBTYPE_NAME
        for i, x in enumerate(
                domain[3][1:]):  # Iterates through types and adds to the sub types to the type (key of type_hierachy)
            if x == "-":
                if domain[2][i + 2] in type_hierarchy:
                    type_hierarchy[domain[2][i + 2]] += [from_before]
                else:
                    type_hierarchy[domain[2][i + 2]] = [from_before]
            elif domain[2][
                i] == "-":  # not elegant but efficient. The key itself was already written in previous iteration
                continue
            else:
                type_hierarchy[x] = []
                from_before = x
    else:
        m_counter += 1

    return m_counter



def parser(fname):
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
        if token == ")": # Backtracing to last opening paranthesis from closing paranthesis and adding it to the stack again (as a sublist)
            l = [stack.pop()]
            while not l[-1] == "(":
                l.append(stack.pop())
            l.pop() # removing "("
            stack.append(l[::-1])
        else:
            stack.append(token)
    print("parser", stack[0])
    return stack[0] # stack has only one element


# TODO split in multiple functions for readability
def assign_types(sub_list):

    # create dict
    dict_types = {}

    dict_types[""] = []  # if no dash


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
            print("key", sub_list[i+1])  # = key

            dict_types[ sub_list[i+1]] = []
            print("dict_types", dict_types)
            if dict_types[sub_list[i + 1]]:  # list not empty -> key already has entries
                dict_types[sub_list[i + 1]].append(  # append not overwrite
                    stack[0])  # stack[0] to get rid of nested list
            else:
                dict_types[sub_list[i + 1]] = stack
            print("stack", stack)
            stack = []  # reset
            i += 1





        # no type assigned TODO ERROR HERE?
      #  if "-" not in sub_list and sub_list[0] == ":types":
       #     dict_types[""] = sub_list

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


def make_act_sch(domain):
    # -------  action schemata confusion   ------

    # predicates = domain[5 - m_counter]  # what to do with predicates?

    # Translating actions into when expressions (with every variable substitution from variable)?
    # or passing it like this:
    act_sch = []
    for sublist in domain:
        if sublist[0] == ":action":
            print("sub_list[3]", sublist[3])
            name = sublist[1]
            parameter = assign_types(
                sublist[3])  # This should work in a well formed domain. But should I check if action[2] = ":parameters"
            precondition = expressions.make_expression(sublist[5]) # i + 2
            effect = expressions.make_expression(sublist[7])
            #         precondition = action[5]
            #         effect = action[7]
            act_sch.append((name, parameter, precondition, effect))



    # testing
    print("parameter", parameter)

    return act_sch


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

    print("list_tokens", tokens)
    for sub_list in tokens:  # cut off [['domain', 'test-adl']
        # if sub_list[0] == ":types":
        sub_list = sub_list[1:]
        print("sub_list", sub_list)

        assignment = assign_types(tokens[2:])
        print("assignment", assignment)


   # m_counter = test(tokens)  # cut off ['define'
    #print("m_counter", m_counter)



    dict_hierarchy = create_hierarchy(assignment)
    print("hierarchy types", dict_hierarchy)

    act_sch = make_act_sch(tokens)
    print("act_sch", act_sch)


    # it is recommended to return a list of an action schemata representation, a dictionary mapping types to sets of constants for each type, and the type hierarchy information. Take care to include an extra mapping from the type "" to a set of all objects.
    return act_sch, dict_hierarchy



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

    #print(parse_domain("type_hierarchy_test.pddl"))
   # print(parse_domain(sys.argv[1]))
    print(parse_domain("domain.pddl"))
    #print(parse_problem(sys.argv[2]))


