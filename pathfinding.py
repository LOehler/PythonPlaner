import graph, heapq
import queue




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


    # initiating
    # to return
    path = []  # represented as a sequence of Edge objects
    distance_from_start = 0  # total length of the path
    visited = 0 # number of nodes visited, i.e. added to the frontier, during search
    expanded = 0 #  number of nodes expanded, i.e. removed from the frontier, during search

    # other
    #search_space = []
    search_tree = []
    agenda_h = []  #  empty heap -> why heap? to get path by moving backwards (children to parent)
    frontier = queue.PriorityQueue()  # decides which nodes gets extendet next by sorting after expected cost (cost + heuristic_cost)



    cur_node = start

    while(len(cur_node.get_neighbors()) != 0):
    # termination rule (no node can be expanded?)

        # check: is neighbor already in search tree



        # ADD neighbors of cur_node to heap
        for neighbor in cur_node.get_neighbors():  # get_neighbors() = list with graph.Edge

          #   heapq.heappush(agenda_h, ((heuristic(neighbor.target, neighbor) + cost_dist(neighbor, 0)),neighbor)) # distance of prev nodes has np effect
            heapq.heappush(agenda_h, ((heuristic(neighbor.target, neighbor) + cost_dist(neighbor, distance_from_start)),neighbor))  # add ALL to heap (need to be able to use neighbors later)
           # frontier.put(score(neighbor), neighbor)

        #print("agenda_h", agenda_h)
       # show_tree(agenda_h)
        # node is visited iff its neighbors have been added to heap


        # update cur_node
        cur_edge = heapq.heappop(agenda_h)
       # cur_edge =agenda_h[0]

        cur_node = cur_edge[1].target
       # print("cur_node", cur_node)
      #  print("cur_node[1]", cur_node[1])

        # add distance from visited node
        distance_from_start += cur_edge[1].cost
        print("distance_from_start", distance_from_start)

        # calc a* score of neighbors
      #  score(cur_node.get_neighbors())


        # use heapq.heappushpop(heap, item) ?


       # cur_node = heapq.heappop(agenda_h)


        # Found the goal
        if(goal(cur_node)):
            rewind_path = []
            print(agenda_h)
            current = cur_edge
            while (agenda_h != []): # as long as heap is not empty
                print("current", current[1].name)
                rewind_path.append(current[1].name)
                current = heapq.heappop(agenda_h) # get parent bro i will legit make a new obj just so i can use get_parent dont @ me
                

            return rewind_path[::-1]
           # path = rewind_path[::-1]  # Return reversed path














        #  If no path is found, the first two values should be None, but the number of visited and expanded nodes should still be reported.

    print("test")


   # return [],0,0,0
    #return path, distance, visited, expanded


# a* score = cost of path [start, cur_node] + estimated distance to goal (heuristic)
def cost_dist(edge, distance_from_start): # edge obj not node obj

    # get distance

    # need path here
   # + node_cost
    distance = distance_from_start #
    distance += edge.cost # cost of self
    # TODO: add cost of prev edges


    # calc heuristic
    # estimated distance to goal NOTE: DO NOT OVERESTIMATE
    #heuristic = 0
    # default_heuristic()



    # calc score
  #  a_score = distance + heuristic()

    # all costs are bound from below by a positive constant (maybe del)
   # if(a_score > 0):
    #    return a_score

   # else:
   #     return 0
    return distance




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

# test

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

    # print for debug
    print(atgoal(graph.Austria["Bregenz"]))
    #print("graph", graph.Austria)
    
    result = astar(graph.Austria["Eisenstadt"], atheuristic, atgoal)
    print("did i make it here")
    print("result", result)
   # print_path(result)
    #
    # result = astar(graph.Austria["Eisenstadt"], default_heuristic, atgoal)
    # print_path(result)
    #
    # target = 2050
    # def infheuristic(n, edge):
    #     return abs(n.get_id() - target)
    # def infgoal(n):
    #     return n.get_id() == target
    #
    # result = astar(graph.InfNode(1), infheuristic, infgoal)
    # print_path(result)
    #
    # result = astar(graph.InfNode(1), default_heuristic, infgoal)
    # print_path(result)
    #
    # def multiheuristic(n, edge):
    #     return abs(n.get_id()%123 - 63)
    # def multigoal(n):
    #     return n.get_id() > 1000 and n.get_id()%123 == 63
    #
    # result = astar(graph.InfNode(1), infheuristic, multigoal)
    # print_path(result)
    #
    # result = astar(graph.InfNode(1), default_heuristic, multigoal)
    # print_path(result)

if __name__ == "__main__":
    main()