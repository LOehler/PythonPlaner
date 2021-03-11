# PythonPlaner
Programming Task Methods of AI Seminar

This is the Project for the Methods of AI Seminar in which we were tasked to program a Planner capable of solving problems in classical PDDL-syntax.

## expressions.py
A file which provides functionality to make worlds and expressions from syntax trees (created in pddl.py)\
The code might be not overly object oriented (for new operators no new class has to be implemented but the behavior of the functions and in ```Expression()``` ```apply_self_on()```. (Slow string comparisons add up when using same expression several times)
 
## graph.py
A file defining a "lazy" representation of an graph (by only representing the neighbors of each node)

This file has already been provided
  
## pathfinding.py
A file that implements A* which traverses the graph provided by Graph.py\
A* seems to could perform better (based on Terminal output of Teacher), meaning less nodes extensions and visits\
Possible explanation: (visited is supposed to only count the first time when node is explored (not when its revisited))\
Unrelated: if a path with lower cost of an existing node is found, this node is added to frontier *again* instead of being replaced This is desired behavior
  
## .pddl
Files expressing a problem domain and the problem itself (wumpus problem) which serves testing purposes

## pddl.py
A file that parses pddl domains and problems to be used in planner
  
## planner.py
A file that uses A* implemented in pathfinding on the expressions created by pddl.py and expressions.py
A very simple subgoal heuristic has been implemented

## runall.py
Given an directory with at least one pddl domain and problem it will run all pddl problems

This file has already been provided

\
\
### Things that could be done
- Representing vis_count right in pathfinding (so that it only increments the first time when it finds a node)
- Getting rid of m_counter and putting everything in pddl.parse_domain in a while loop (asking for example if domain[i][0] == ":requirements"
- The heuristic is bad (cut down to 6000 from 6600 visited nodes in p-07-airport2) and only helps if there are multiple goals. Something like Fast Forward or Fast Downward would be better
- Using inheritance (with subclasses of Expression i.e. AndExpression) in expressions.py to avoid unnecessary string comparisons when expression is asked to model the model multiple times
- (planner.py) Only the prerequesite substitution list could  be given to the ExpNode where it can than create the effect. Meaning that instead of already giving the substituted effects, the combi  (substitutet variables) should be given next to the the substituted prerequesites (to get_neighbor). This would prevent the unnecessary creation of substituted effects (while only costing little in get_neighbor). Our planner struggles a bit with the whole airport-adl problem package because the large amount of preprocessing (10 nodes expanded but 27 sec needed)