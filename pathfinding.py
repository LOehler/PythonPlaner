import graph
from queue import PriorityQueue

def default_heuristic(n, edge):
    """
    Default heuristic for A*. Do not change, rename or remove!
    """
    return 0
    
def astar(start, heuristic, goal):
    """
    A* search algorithm. The function is passed a start (graph.Node) object, a heuristic function, and a goal predicate.
    
    The start node can produce neighbors as needed, see graph.py for details.
    
    The heuristic is a function that takes two parameters: a node, and an edge. The algorithm uses the heuristic to determine which node to expand next.
    Note that, unlike in classical A*, the heuristic can also use the edge employed to get to a node to determine the node's heuristic value. This can be beneficial when the 
    edges represent complex actions (as in the planning case), and we want to take into account the differences produced by that action.
    
    The goal is also represented as a function, that is passed a node, and returns True if that node is a goal node, otherwise False. This representation was also chosen to
    simplify implementing the planner later, which can use the functions developed in Task 1 to determine if a state models the goal condition, 
    but is otherwise equivalent to classical A*. 
    
    The function should return a 4-tuple (path,distance,visited,expanded):
        - path is a sequence of (graph.Edge) objects that have to be traversed to reach a goal state from the start.
        - distance is the sum of costs of all edges in the path 
        - visited is the total number of nodes that were added to the frontier during the execution of the algorithm 
        - expanded is the total number of nodes that were expanded (i.e. whose neighbors were added to the frontier)
    """
    
    frontier = PriorityQueue() # decides which nodes gets extendet next by sorting after expected cost (cost + heuristic_cost)
    expa_count = 0 # counts how many nodes have been expanded
    vis_count = 0 # counts how many nodes have been visited (not actually visited but looked at the edges of them)
    cost_so_far = {start.get_id():0} # The cost from the curent node (start node has cost 0)
    came_from = {} # parent relation
    cur_node = start # for better readability

    while True: # Runs until goal is found or frontier is empty
        
        if goal(cur_node):
            cost = 0
            edge_path = []
            while cur_node != start:
                # Getting edges out of node
                for x in came_from[cur_node.get_id()].get_neighbors():
                    if x.target == cur_node:
                        prev_edge = x
                # Adding up cost and a list of edges
                cost += prev_edge.cost
                edge_path.append(prev_edge)
                cur_node = came_from[cur_node.get_id()]
            return edge_path[::-1], cost, vis_count, expa_count
        
        expa_count += 1
        
        # getting all neighbors and adding it to PriorityQueue       
        for neighbor in cur_node.get_neighbors(): # get_neighbors() = list with graph.Edge
        # looking for best heuristic in all neighbors
        # A* adds to the cost for the next neighbor a heuristic to improve search
            new_cost = neighbor.cost + cost_so_far[cur_node.get_id()]
            if neighbor.target.get_id() not in cost_so_far or new_cost < cost_so_far[neighbor.target.get_id()]:
                vis_count += 1 # incrementing visited nodes
                cost_so_far[neighbor.target.get_id()] = new_cost # updating cost_so_far with better neighbor
                # calculate heuristic and put it on sorted stack
                frontier.put((heuristic(cur_node, neighbor) + neighbor.cost, vis_count, neighbor)) # vis_count only in there to avoid neighbor
                                                                                                   # comparison (ask for more detailed explanation!)
                came_from[neighbor.target.get_id()] = cur_node # set parrent (for retracing the path)


        new_edge = frontier.get()[2] # Gets the Edge of the lowest Heuristic
        cur_node = new_edge.target
         
        if frontier.empty():
            return [],0, vis_count, expa_count



def print_path(result):
    (path,cost,visited_cnt,expanded_cnt) = result
    print("visited nodes:", visited_cnt, "expanded nodes:",expanded_cnt)
    if path:
        print("Path found with cost", cost)
        for n in path:
            print(n.name)
    else:
        print("No path found")
    print("\n")

def main():
    """
    You are free (and encouraged) to change this function to add more test cases.
    
    You are provided with three test cases:
        - pathfinding in Austria. This is a relatively small graph, but it comes with an admissible heuristic. Below astar is called using that heuristic, 
          as well as with the default heuristic (which always returns 0). If you implement A* correctly, you should see a small difference in the number of visited/expanded nodes between the two heuristics;
        - pathfinding on an infinite graph, where each node corresponds to a natural number, which is connected to its predecessor, successor and twice its value, as well as half its value, if the number is even.
          e.g. 16 is connected to 15, 17, 32, and 8. The problem given is to find a path from 1 to 2050, for example by doubling the number until 2048 is reached and then adding 1 twice. There is also a heuristic 
          provided for this problem, but it is not admissible (a heuristic is admissible if it never overestimates the cost of reaching the goal), but it should result in a path being found almost instantaneously. On the other hand, if the default heuristic is used, the search process 
          will take a noticeable amount (a couple of seconds);
        - pathfinding on the same infinite graph, but with infinitely many goal nodes. Each node corresponding to a number greater than 1000 that is congruent to 63 mod 123 is a valid goal node. As before, a non-admissible
          heuristic is provided, which greatly accelerates the search process. 
    """
    target = "Bregenz"
    def atheuristic(n, edge):
        return graph.AustriaHeuristic[target][n.get_id()]
    def atgoal(n):
        return n.get_id() == target
    
    result = astar(graph.Austria["Eisenstadt"], atheuristic, atgoal)
    print_path(result)
    
    result = astar(graph.Austria["Eisenstadt"], default_heuristic, atgoal)
    print_path(result)
    
    target = 2050
    def infheuristic(n, edge):
        return abs(n.get_id() - target)
    def infgoal(n):
        return n.get_id() == target
    
    result = astar(graph.InfNode(1), infheuristic, infgoal)
    print_path(result)
    
    result = astar(graph.InfNode(1), default_heuristic, infgoal)
    print_path(result)
    
    def multiheuristic(n, edge):
        return abs(n.get_id()%123 - 63)
    def multigoal(n):
        return n.get_id() > 1000 and n.get_id()%123 == 63
    
    result = astar(graph.InfNode(1), infheuristic, multigoal)
    print_path(result)
    
    result = astar(graph.InfNode(1), default_heuristic, multigoal)
    print_path(result)
    

if __name__ == "__main__":
    main()