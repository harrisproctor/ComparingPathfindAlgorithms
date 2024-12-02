import random
import time

class CoOrdinates():
    '''
    class containing all coordinates and functions for calculations todo with them
    '''

    def __init__(self):
        self.remove_all()

    def remove_all(self):
        self.start = None
        self.end = None
        self.obstacle = []
        self.maze = []
        self.open_list = []
        self.closed_list = []
        self.final_path = []
        self.check_points = []

    def remove_last(self):
        self.maze = []
        self.open_list = []
        self.closed_list = []
        self.final_path = []

    # gets the furthest distance of a node from the (0, 0)
    def largest_distance(self):
        largest = 0
        for wall in self.obstacle:
            if wall[0] > largest: largest = wall[0]
            if wall[1] > largest: largest = wall[1]
        for point in self.check_points:
            if point[0] > largest: largest = point[0]
            if point[1] > largest: largest = point[1]
        return largest + 1

    # creates a 2d array of the maze and its walls
    def create_maze(self, gui):
        
        largest_distance = self.largest_distance()
        
        # makes sure the size of the maze if either the size of the gui
        # or the size of the maze made using the obstacle and checkpoints
        if gui.grid_size > largest_distance:
            largest = gui.grid_size
        else:
            largest = largest_distance
            
        self.maze = [[0 for x in range(largest)] for y in range(largest)]
        for wall in self.obstacle:
            try:
                wall_x, wall_y = wall
                self.maze[wall_x][wall_y] = 1
            except:
                pass

    # creates random obstacles in the form of blob clusters
    def generate_blobs(self, gui):
        self.obstacle = []
        grid_size = gui.grid_size
        
        # Define the range of cluster sizes
        min_cluster_size = 1
        max_cluster_size = 5

        for _ in range(grid_size):
            # choosing a random cluster center
            center = (random.randint(0, grid_size), random.randint(0, grid_size))
            
            # randomly selecting a cluster size given our min and max
            cluster_size = random.randint(min_cluster_size, max_cluster_size)

            # generating a cluster around the center
            cluster = [(x, y) for x in range(center[0] - cluster_size // 2, center[0] + cluster_size // 2 + 1)
                            for y in range(center[1] - cluster_size // 2, center[1] + cluster_size // 2 + 1)
                            if 0 <= x < grid_size and 0 <= y < grid_size and (x, y) not in self.obstacle]
            
            # add the clusters to our walls
            self.obstacle.extend(cluster)
            #remove two specific walls for test speed imporvement
            if((5,5) in self.obstacle):
                self.obstacle.remove((5,5))
            if ((25, 25) in self.obstacle):
                self.obstacle.remove((25, 25))


class AnytimeAstar():

    def __init__(self, tim):
        #coeffiecnt for the heurstic
        self.heurcoef = 1000
        #list of possible coeffient states
        self.heurcolist = [1000,4,1,0]
        # index of current coeffiecnt
        self.heurind = 0
        # maxmium number of secends allowed to be taken
        self.timelimit = tim
        #is the current path optimal
        self.opti = False
        #current best path
        self.bestpath = None

    def popbestpath(self):
        p = self.bestpath
        self.bestpath = None
        return p

    def updateHeur(self):
        #updates the coef to one further down the list
        self.heurind += 1
        self.heurcoef = self.heurcolist[self.heurind]

    def chooseNode(self,open_list):
        current_node = open_list[0]


        current_index = 0

        for index, item in enumerate(open_list):

            if item.f < current_node.f:
                current_node = item

                current_index = index

        return [current_node,current_index]

    def calcValue(self,child,current_node,end_node):
        child.g = current_node.g + 1

        # distance to end point

        # the reason the h distance is powered by 0.6 is because

        # it makes it prioritse diagonal paths over straight ones

        # even though they are technically the same g distance, this makes a* look better

        child.h = (((abs(child.position[0] - end_node.position[0]) ** 2) +

                    (abs(child.position[1] - end_node.position[1]) ** 2)) ** 0.6)
        #multiply pure heurstic by coeffeint for speed intially then later for optimal pathing
        child.h = child.h * self.heurcoef
        child.f = child.g + child.h


#create instance of anytime astar class
aastar = AnytimeAstar(0)

# function for pathfinding using dfs, bfs, dijkstra and A*
# Returns a list of tuples as a path from the given start to the given end in the given maze
def pathfind(maze, start, end, gui, coords, key,f = None):
    
    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    count = 0
    starttime = time.monotonic()
    # Loop until you find the end

    # Loop until you find the end
    while len(open_list) > 0:

        # skip pathfinding to create a wait effect. Ajustable speed
        if count >= gui.animation_speed:

            count = 0
            
            if key == "q": # dfs, get the latest node
                current_node = open_list[-1]
                current_index = len(open_list)-1
                
            elif key == "w": # bfs, get the newest node
                current_node = open_list[0]
                current_index = 0               
                
            elif key == "r": # a*, get the node with the lowest f value
                current_node = open_list[0]
                current_index = 0
                for index, item in enumerate(open_list):
                    if item.f < current_node.f:
                        current_node = item
                        current_index = index
            elif key == 't':  # theta*, get the node with the lowest f value but also check line of sight for lineage
                current_node = open_list[0]
                current_index = 0

                # if parent(s) and neighbor have line of sight
                # then ignore s and use path from parent(s) to neighbor
                for index, item in enumerate(open_list):
                    if item.f < current_node.f:
                        current_node = item
                        current_index = index

                if current_node.parent is not None:
                    p = current_node.parent
                    for index, item in enumerate(open_list):
                        if item.position == p.position:
                            continue  # skip over parent
                        if los(maze, p, item):
                            current_node.parent = p
                            current_node.g = p.g + 1


            elif key == "a":  # anytime a* get the node with the lowest f value
                current_node,current_index = aastar.chooseNode(open_list)
                        
            elif key == "e": # dijkstra, get the node with the lowest g value
                current_node = open_list[0]
                current_index = 0
                for index, item in enumerate(open_list):
                    if item.g < current_node.g:
                        current_node = item
                        current_index = index

            # Pop current off open list, add to closed list
            open_list.pop(current_index)
            closed_list.append(current_node)

            # Found the goal
            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                coords.open_list = open_list
                coords.closed_list = closed_list
                endtime = time.monotonic()
                elasped = endtime - starttime
                if key == "a" and aastar.heurcoef == 0:
                    aastar.opti = True


                #print(elasped)
                #print(aastar.timelimit)
                if key == "a" and elasped < aastar.timelimit and aastar.opti == False:
                    aastar.updateHeur()
                    aastar.bestpath = path
                    #print("sav")
                    return pathfind(maze, start, end, gui, coords, key)

                if key == "a":
                    aastar.bestpath = None
                    aastar.heurcoef = 1000
                    aastar.heurind = 0
                    aastar.opti = False
                #print("ret")


                endtime = time.monotonic()
                elasped = endtime - starttime
                #print("time elapsed", elasped)
                if(f is not None):
                    f.write(str(elasped))
                    f.write("\n")
                    f.write("algo " + key + " path length " + str(len(path)))
                    f.write("\n")
                return path  # Return path

            endtime = time.monotonic()
            elasped = endtime - starttime
            if key == "a" and elasped > aastar.timelimit and aastar.bestpath is not None:
                #print("time elapsed", elasped)
                if (f is not None):
                    f.write(str(elasped))
                    f.write("\n")
                    f.write("algo " + key + " path length " + str(len(aastar.popbestpath())))
                    f.write("\n")
                aastar.heurcoef = 1000
                aastar.heurind = 0
                aastar.opti = False
                return aastar.popbestpath()

            # Generate children
            # left, down, right, up. Which makes dfs go in up, right, down, left order
            for new_pos in [(-1, 0), (0, 1), (1, 0), (0, -1)]: # Adjacent squares

                # Get node position
                node_pos = (current_node.position[0] + new_pos[0],
                            current_node.position[1] + new_pos[1])

                # Make sure within range
                if (node_pos[0] > (len(maze) - 1) or node_pos[0] < 0
                        or node_pos[1] > (len(maze[len(maze)-1]) -1)
                        or node_pos[1] < 0):
                    continue

                # Make sure walkable terrain
                if maze[node_pos[0]][node_pos[1]] != 0:
                    continue

                if Node(current_node, node_pos) in closed_list:
                    continue

                # Create new node
                child = Node(current_node, node_pos)

                # Child is on the closed list
                passList = [False for closed_child in closed_list if child == closed_child]
                if False in passList:
                    continue

                # for dfs and bfs we dont add anything to the node values
                
                if key == "e": # dijkstra, add one to g value
                    child.g = current_node.g + 1

                elif key == "a":  # a*, calculate f value
                    aastar.calcValue(child,current_node,end_node)
                    
                elif key == "r": # a*, calculate f value
                    child.g = current_node.g + 1
                    # distance to end point
                    # the reason the h distance is powered by 0.6 is because
                    #it makes it prioritse diagonal paths over straight ones
                    # even though they are technically the same g distance, this makes a* look better
                    child.h = (((abs(child.position[0] - end_node.position[0]) ** 2) +
                                (abs(child.position[1] - end_node.position[1]) ** 2)) ** 0.6)
                    child.f = child.g + child.h


                elif key == "t":  # theta*, calculate f value
                    child.g = current_node.g + 1
                    # distance to end point
                    # the reason the h distance is powered by 0.6 is because
                    # it makes it prioritize diagonal paths over straight ones
                    # even though they are technically the same g distance, this makes theta* look better
                    child.h = (((abs(child.position[0] - end_node.position[0]) ** 2) +
                                (abs(child.position[1] - end_node.position[1]) ** 2)) ** 0.6)
                    child.f = child.g + child.h

                # Child is already in the open list
                
                for open_node in open_list:
                    # check if the new path to children is worst or equal 
                    # than one already in the open_list (by measuring g)
                    if child == open_node and child.g >= open_node.g:
                        break
                    
                else:
                    # Add the child to the open list
                    open_list.append(child)

        # if skipped just update the gui
        else:

            coords.open_list = open_list
            coords.closed_list = closed_list
            gui.main(True)

        count += 1
    #print("no path found")
    if (f is not None):
        f.write("no path found")
        f.write("\n")


# returns whether current_node has a line of sight with its successor
def los(maze, current_node, succ):
    x1 = current_node.position[0]
    y1 = current_node.position[1]

    x2 = succ.position[0]
    y2 = succ.position[1]

    # check for straight line
    if x1 == x2 or y1 == y2:
        # if x2 is greater than x1
        if x1 - x2 < 0:
            dx = 1
        # if x1 is greater than x2
        elif x1 - x2 > 0:
            dx = -1
        # if x1 and x2 are equal
        else:
            dx = 0

        # if x2 is greater than x1
        if y1 - y2 < 0:
            dy = 1
        # if x1 is greater than x2
        elif y1 - y2 > 0:
            dy = -1
        # if y1 and y2 are equal
        else:
            dy = 0

        x = x1 + dx
        y = y1 + dy

        # while we're not at the successor, look for obstacles
        while (x, y) != succ.position:
            if not (0 <= x < len(maze) and 0 <= y < len(maze[0])):
                return False
            if maze[x][y] == 1:
                return False
            # update current position
            x += dx
            y += dy
    # try for a diagonal line
    else:
        if x1 < x2:
            dx = 1
        else:
            dx = -1
        if y1 < y2:
            dy = 1
        else:
            dy = -1

        x = x1
        y = y1

        # while we're not at the successor, look for obstacles
        while (x, y) != succ.position:
            if not (0 <= x < len(maze) and 0 <= y < len(maze[0])):
                return False
            if maze[x][y] == 1:
                return False
            # corner cutting?
            # if maze[x + dx][y] == 1 and maze[x][y + dy] == 1:
            # return False
            # update current position
            x += dx
            y += dy
    # if we haven't tripped a flag at this point, there should be line of sight
    return True

class Node():
    '''
    node class for containing position, parent and costs
    '''
    
    def __init__(self, parent, position):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position