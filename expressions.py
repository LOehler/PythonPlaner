# global variable (list) containing all supported logical operators
OPERATORS = ['and', 'or', 'not', '=', 'imply', 'when', 'exists', 'forall']

# A logical expression with which logical operation can be done
class Expression:
    def __init__(self, string):
        self.string = string # Actually represents the whole expression as tuple. Bad name, I know. Sorry
        self.name = string[0] # Name of expression (either operator or world description literal (at, have, alive, ...))
        self.children = [] # Every object or sub expressions following the name
        for child in string[1:]:
            self.children.append(Expression(child))
            
    # applies changes to the passed world
    def apply_self_on(self, world):
        if self.name == "and": # adds to world
            for child in self.children:
                if child.name in OPERATORS:
                    child.apply_self_on(world)
                else:
                    world.atoms.add(child.string)
        
        elif self.name == "not": # removes from world
            if self.children[0].string in world.atoms:
                world.atoms.remove(self.children[0].string)
        
        elif self.name == "when": # applies changes if when condition is met
            if models(world, self.children[0]):
                self.children[1].apply_self_on(world)

        else: # currently includes all other operators (basically saves everything that is an atom in world)
            world.atoms.add(self.string)
        
            
class World:
    def __init__(self, atoms, sets):
        self.sets = sets # A dictionary mapping all objects to types
        self.atoms = set(atoms) # World atoms that constitute the world
        
            
def make_expression(ast):
    """
    This function receives a sequence (list or tuple) representing the abstract syntax tree of a logical expression and returns an expression object suitable for further processing.
    
    In the Abstract Syntax Tree, the first element of the sequence is the operator (if applicable), with the subsequent items being the arguments to that operator. The possible operators are:
    
       - "and" with *arbitrarily many parameters*
       - "or" with *arbitrarily many parameters*
       - "not" with exactly one parameter 
       - "=" with exactly two parameters which are variables or constants
       - "imply" with exactly two parameters 
       - "when" with exactly two parameters 
       - "exists" with exactly two parameters, where the first one is a variable specification
       - "forall" with exactly two parameters, where the first one is a variable specification
    
    Unless otherwise noted, parameters may be, in turn, arbitrary expressions. Variable specifications are sequences of one or three elements:
       - A variable specification of the form ("?s", "-", "Stories") refers to a variable with name "?s", which is an element of the set "Stories"
       - A variable specification of the form ("?s",) refers to a variable with name "?s" with no type 
       
    If the first element of the passed sequence is not a parameter name, it can be assumed to be the name of a predicate in an atomic expression. In this case, 
    the remaining elements are the parameters, which may be constants or variables.
    
    An example for an abstract syntax tree corresponding to the expression 
          "forall s in stories: (murdermystery(s) imply (at(sherlock, bakerstreet) and not at(watson, bakerstreet) and at(body, crimescene)))" 
    would be (formatted for readability):
    
        ("forall", ("?s", "-", "Stories"), 
                   ("imply", 
                         ("murdermystery", "?s"),
                         ("and", 
                              ("at", "sherlock", "bakerstreet"),
                              ("not", 
                                   ("at", "watson", "bakerstreet")
                              ),
                              ("at", "body", "crimescene")
                         )
                   )
        )
    
    The return value of this function can be an arbitrary python object representing the expression, which will later be passed to the functions listed below. For notes on the "when" operator, 
    please refer to the documentation of the function "apply" below. Hint: A good way to represent logical formulas is to use objects that mirror the abstract syntax tree, e.g. an "And" object with 
    a "children" member, that then performs the operations described below.
    """

    # Eventuelle Fehlerbehandlung von ast

    return Expression(ast)
    
def make_world(atoms, sets):
    """
    This function receives a list of atomic propositions, and a dictionary of sets and returns an object representing a logical world.
    
    The format of atoms passed to this function is identical to the atomic expressions passed to make_expression above, i.e. 
    the first element specifies the name of the predicate and the remaining elements are the parameters. For example 
       ("at", "a", "b") represents the atom "at(a, b)"
       
    The sets are passed as a dictionary, with the keys defining the names of all available sets, each mapping to a sequence of strings. 
    For example: {"people": ["holmes", "watson", "moriarty", "adler"], 
                  "stories": ["signoffour", "scandalinbohemia"], 
                  "": ["holmes", "watson", "moriarty", "adler", "signoffour", "scandalinbohemia"]}
                  
    The entry with the key "" contains all possible constants, and can be used if a variable is not given any particular domain.
    
    The world has to store these sets in order to allow the quantifiers forall and exists to use them. When evaluated, the forall operator from the 
    example above would look up the set "stories" in the world, and use the values found within to expand the formula.
    
    Similar to make_expression, this function returns an arbitrary python object that will only be used to pass to the functions below. Hint: A simple solution would consist in storing the atoms in a set using the same representation as for atomic expressions, and the set dictionary as-is.
    """
    
    # Eventuelle Fehlerbehandlung von atoms und sets
    
    return World(atoms, sets)
    
def models(world, expression):
    """
    This function takes a world and a logical expression, and determines if the expression holds in the given world.
    
    The semantics of the logical operators are the usual ones, e.g. a world models an "and" expression if it models every child of the "and" expression.
    For the quantifiers, when the world is constructed it is passed all possible sets, and the quantifiers will use this dictionary to determine their domain. 
    
    The special "when" operator is only used by the "apply" function (see below), and no world models it.
    
    The return value of this function should be True if the condition holds in the given world, and False otherwise.
    """
    
    if expression.string in world.atoms: # recursion anchor (if atom exists in world)
        return True
    
    elif expression.name == 'and': # when all expressions are True
        for a in expression.children:
            if not models(world, a):
                return False
        return True
    
    elif expression.name == 'or': # when either expression is True
        for a in expression.children:
            if models(world, a):
                return True
        return False
        
    elif expression.name == 'not': # when the expression is not True
        if expression.children[0].string in world.atoms:
            return False
        return True

    elif expression.name == '=': # when previous and following variable is equal
        return expression.children[0].string == expression.children[1].string
        
    elif expression.name == 'imply': # when first expression does not model world or second models the world
        if models(world, expression.children[0]) and not models(world, expression.children[1]):
            return False
        return True

    elif expression.name == 'exists': # when a variable assignment exists that models the world
        # iterating over all values with the specified type
        for value in world.sets[expression.children[0].children[1].string]: # Name of type given on the last position of the first part after exists
            # checking if world models substituted 
            if models(world, Expression(substitute(expression.children[1], expression.children[0].string[0], value))):
                return True
        return False
        
    elif expression.name == 'forall': # when all possible variable assignments model the world
        for value in world.sets[expression.children[0].children[1].string]:
            if not models(world, Expression(substitute(expression.children[1], expression.children[0].string[0], value))):
                return False
        return True

    return False
    
def substitute(expression, variable, value):
    """
    This function takes an expression, the name of a variable (usually starting with a question mark), and a constant value, and returns a *new* expression with all occurences of the variable 
    replaced with the value
    
    Do *not* replace the variable in-place, always return a new expression object. When you implement the quantifiers, you should use this same functionality to expand the formula to all possible 
    replacements for the variable that is quantified over.
    """

    # return deep copy with all variables replaced

    # feels dirty but "=" is the only operator that does not subdivide the tree further
    if not expression.name in OPERATORS or expression.name == '=':
        new_list = []
        for exp in expression.string:
            if exp == variable:
                new_list.append(value)
            else:
                new_list.append(exp)
    else: # nested case
        new_list = [expression.name]
        # substitutes all nested expression in one list (recursively)
        for exp in expression.children:
            new_list.append(substitute(exp, variable, value))
    return tuple(new_list)
    
def apply(world, effect):
    """
    This function takes a world, and an expression, and returns a new world, with the expression used to change the world. 
    
    For the effect you can assume the following restrictions:
       - The basic structure of the effect is a conjunction ("and") of modifications.
       - Each modification may be a literal (atom, or negation of an atom), a forall expression, or a when expression 
       - In the world produced by the application, positive literals should be added to the atoms of the world, and negative literals should be removed 
       - Forall expressions should be expanded by substituting the variable and processed recursively in the same way (the inner expression will only contain a conjunction of 
             literals, forall expressions, and when expressions as well)
       - "when" expressions have two parameters: A condition (which may be an arbitrary expression), and an effect, which follows the same restrictions (conjunction of literals, forall expressions and when expressions)
             The way "when" expressions are applied to a world depends on the condition: If the world models the condition (i.e. models(world, condition) is true, the effect is applied to the world. Otherwise, nothing happens.
             "when" expressions provide a nice, succinct way to define conditional effects, e.g. if someone is trying to open a door, the door will only open if it is unlocked.
             
    If an effect would cause the same atom to be set to true and to false, it should be set to false, i.e. removed from the set.
             
    The result of this function should be a *new* world, with the changes defined by the effect applied to the atoms, but with the same definition of sets as the original world. 
    
    Hint: If your world stores the atoms in a set, you can determine the change caused by the effect as two sets: an add set and a delete set, and get the atoms for the new world using basic set operations.
    """
    
    # deep copy here too
    new_world = World(world.atoms, world.sets)
    effect.apply_self_on(new_world)
    return new_world



if __name__ == "__main__":
    exp = make_expression(("or", ("on", "a", "b"), ("on", "a", "d")))
    world = make_world([("on", "a", "b"), ("on", "b", "c"), ("on", "c", "d")], {})
    
    
    print("Should be True: ", end="")
    print(models(world, exp))
    change = make_expression(["and", ("not", ("on", "a", "b")), ("on", "a", "c")])
    
    print("Should be False: ", end="")
    print(models(apply(world, change), exp))
    
    
    # _____Mickey_Example____________
    
    print("mickey/minny example")
    world = make_world([("at", "store", "mickey"), ("at", "airport", "minny")], {"Locations": ["home", "park", "store", "airport", "theater"], "": ["home", "park", "store", "airport", "theater", "mickey", "minny"]})
    exp = make_expression(("and", 
        ("not", ("at", "park", "mickey")), 
        ("or", 
              ("at", "home", "mickey"), 
              ("at", "store", "mickey"), 
              ("at", "theater", "mickey"), 
              ("at", "airport", "mickey")), 
        ("imply", 
                  ("friends", "mickey", "minny"), 
                  ("forall", 
                            ("?l", "-", "Locations"),
                            ("imply",
                                    ("at", "?l", "mickey"),
                                    ("at", "?l", "minny"))))))

    print("Should be True: ", end="")
    print(models(world, exp))
    become_friends = make_expression(("friends", "mickey", "minny"))
    friendsworld = apply(world, become_friends)
    
    print("Should be False: ", end="")
    print(models(friendsworld, exp))
    move_minny = make_expression(("and", ("at", "store", "minny"), ("not", ("at", "airport", "minny"))))

    movedworld = apply(friendsworld, move_minny)
    print("Should be True: ", end="")
    

    print(models(movedworld, exp))
    
    
    move_both_cond = make_expression(("and",
                                      ("at", "home", "mickey"),
                                      ("not", ("at", "store", "mickey")),
                                      ("when",
                                       ("at", "store", "minny"),
                                       ("and",
                                        ("at", "home", "minny"),
                                        ("not", ("at", "store", "minny"))))))

    # print("mickey with minny at home")
    print("Should be True: ", end="")
    print(models(apply(movedworld, move_both_cond), exp))


    # print('minny still at airport (mickey is a bad friend)')
    print("Should be False: ", end="")
    another_world = apply(friendsworld, move_both_cond)
    print(models(another_world, exp))


    exp1 = make_expression(("forall",
                            ("?l", "-", "Locations"),
                            ("forall",
                             ("?l1", "-", "Locations"),
                             ("imply",
                              ("and", ("at", "?l", "mickey"),
                               ("at", "?l1", "minny")),
                              ("=", "?l", "?l1")))))
    
    print("Should be True: ", end="")
    print(models(apply(movedworld, move_both_cond), exp1))

    print("Should be False: ", end="")
    print(models(apply(friendsworld, move_both_cond), exp1))

    move_both_cond = make_expression(("and",
                                           ("at", "home", "mickey"),
                                           ("not", ("at", "store", "mickey")),
                                           ("when",
                                                 ("at", "store", "minny"),
                                                 ("and",
                                                      ("at", "home", "minny"),
                                                      ("not", ("at", "store", "minny"))))))

    print("Should be True: ", end="")
    print(models(apply(movedworld, move_both_cond), exp))

    print("Should be False: ", end="")
    print(models(apply(friendsworld, move_both_cond), exp))

    exp1 = make_expression(("forall",
                            ("?l", "-", "Locations"),
                            ("forall",
                                  ("?l1", "-", "Locations"),
                                  ("imply",
                                       ("and", ("at", "?l", "mickey"),
                                               ("at", "?l1", "minny")),
                                       ("=", "?l", "?l1")))))

    print("Should be True: ", end="")
    print(models(apply(movedworld, move_both_cond), exp1))

    print("Should be False: ", end="")
    print(models(apply(friendsworld, move_both_cond), exp1))
