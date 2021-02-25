# PythonPlaner
Programming Task Methods of AI Seminar

This is the Project for the Methods of AI Seminar in which we were tasked to program a Planner capable of solving problems in classical PDDL-syntax.

## expressions.py
A file which provides functionality to make worlds and expressions from syntax trees (created in pddl.py) \n
  While the code might be not overly object oriented (for new operators no new class has to be implemented but the behavior of the functions and in ```Expression()``` ```apply_self_on()```, one can still consider it elegant code. ;)
 
## graph.py
A file defining a "lazy" representation of an graph (by only representing the neighbors of each node)
  \n\tThis file has already been provided
  
## pathfinding.py
A file that implements A* which traverses the graph provided by Graph.py
  \n\tA* seems to could perform better (based on Terminal output of Teacher), meaning less nodes extensions and visits
	\n\tPossible explanation: (visited is supposed to only count the first time when node is explored (not when its reevaluated))
  \n\tUnrelated: if a path with lower cost of an existing node is found, this node is added to frontier *again* instead of being replaced
  
## .pddl
Files expressing a problem domain and the problem itself (wumpus problem) which serves testing purposes

## pddl.py
A file that parses pddl domains and problems to be used in planner
  \n\tIN DEVELOPEMENT
  
## planner.py
A file that uses A* implemented in pathfinding on the expressions created by pddl.py and expressions.py
  \n\tIN DEVELOPEMENT

## runall.py
Given an directory with at least pddl domain and problem it will run all pddl problems (with heuristic on)
  \n\tThis file has already been provided