import time

import numpy

from node import Node


class VectorField():

    def __init__(self, end, start, maze):
        self.end = end
        self.start = start
        # map is heatmap
        self.map = [[-1 for i in range(len(maze))] for j in range(len(maze))]
        self.maze = maze
        self.vectormap

    # change the map to make it a heat map
    def makehm(self):
        queue = []
        visited = []

        current_node = self.end
        queue.append(current_node)

        self.map[self.end[0]][self.end[1]] = 0

        while len(queue) > 0:

            current_node = queue.pop(0)
            # check to see if vistied, if visited = pass
            # if not visited, add to visited list
            # then get neighboring positions
            if current_node not in visited:
                visited.append(current_node)

                for new_pos in [(-1, 0), (0, 1), (1, 0), (0, -1)]:  # Adjacent squares
                    # Get node position
                    node_pos = (current_node[0] + new_pos[0],
                                current_node[1] + new_pos[1])

                    # Make sure within range
                    if (node_pos[0] > (len(self.maze) - 1) or node_pos[0] < 0
                            or node_pos[1] > (len(self.maze[len(self.maze) - 1]) - 1)
                            or node_pos[1] < 0):
                        continue

                    # Make sure walkable terrain
                    if self.maze[node_pos[0]][node_pos[1]] != 0:
                        continue

                    # add new node back into queue
                    queue.append(node_pos)

                    # if it is smaller than dont change it
                    if self.map[node_pos[0]][node_pos[1]] != -1 and self.map[node_pos[0]][node_pos[1]] < \
                            self.map[current_node[0]][current_node[1]] + 1:
                        continue
                    else:
                        hmnum = self.map[current_node[0]][current_node[1]] + 1
                        self.map[node_pos[0]][node_pos[1]] = hmnum

        for i in range(len(self.map)):
            for j in range(len(self.map)):
                if self.map[i][j] == -1:
                    self.map[i][j] = numpy.inf

    def vectormap(self):
        vector_map = [[0 for i in range(len(self.map))] for j in range(len(self.map))]

        for i in range(len(self.map)):
            for j in range(len(self.map)):

                # get position of right tile, if it is at the end so make it the left tile + 2
                if i == len(self.map) - 1:
                    right = self.map[i - 1][j] + 2
                else:
                    if self.map[i + 1][j] == numpy.inf:
                        right = self.map[i][j]
                    else:
                        right = self.map[i + 1][j]
                # get position of left tile, if i is zero, cannot go to the left so make it the right tile + 2
                if i == 0:
                    left = self.map[i + 1][j] + 2
                else:
                    if self.map[i - 1][j] == numpy.inf:
                        left = self.map[i][j]
                    else:
                        left = self.map[i - 1][j]
                # get position of down tile, if the last thing in the list, cannot go down more so make it the up tile + 2
                if j == len(self.map) - 1:
                    down = (self.map[i][j - 1]) + 2
                else:
                    if self.map[i][j + 1] == numpy.inf:
                        down = self.map[i][j]
                    else:
                        down = self.map[i][j + 1]

                # get position of up tile, if the first thing in the list, cannot go up more make it the down tile + 2
                if j == 0:
                    up = (self.map[i][j + 1]) + 2
                else:
                    if self.map[i][j - 1] == numpy.inf:
                        up = self.map[i][j]
                    else:
                        up = self.map[i][j - 1]

                # divide vector by 2 and flooring it so that it doesnt go in an infinite loop
                vector_map[i][j] = [(left - right) // 2, (up - down) // 2]
                # if there is an obstacle up, then set it to down tile distance
                # if i != 0 and hm_map[i-1][j] == -1 or i != len(hm_map) - 1 and hm_map[i+1][j]:
                #    vector_map[i][j][0] = 0
                # if j != len(hm_map) - 1 and hm_map[i][j+1] == -1 or j == 0 and hm_map[i][j-1]:
                #    vector_map[i][j][1] = 0

        # makes obstacle clear in vector map so there isnt a chance of two (0,0)s
        for i in range(len(self.map)):
            for j in range(len(self.map)):
                if self.map[i][j] == numpy.inf:
                    vector_map[i][j] = "(x, x)"
        # just in case the end point is at the edge
        vector_map[self.end[0]][self.end[1]] = [0, 0]

        self.vectormap = vector_map

    def pathmaker(self):
        # get position of start node
        curr_pos = self.start
        # find the vector of start node position
        vector = self.vectormap[curr_pos[0]][curr_pos[1]]

        # to be returned
        path = []
        vector_moves = []
        # adding start position
        path.append(curr_pos)
        # keep going until the vector equals (0, 0)
        while vector != [0, 0]:
            # if the vector has infinity on the left value, dont change the left value
            if vector[0] == numpy.inf:
                continue
            else:
                if vector[0] < 0:
                    for i in range(abs(vector[0])):
                        # put new position into path
                        if self.vectormap[curr_pos[0] - 1][curr_pos[1]] == ('(x,x)'):
                            break
                        else:
                            curr_pos = (curr_pos[0] - 1, curr_pos[1])
                            path.append(curr_pos)

                elif vector[0] > 0:
                    for i in range(abs(vector[0])):
                        # put new position into path
                        if self.vectormap[curr_pos[0] + 1][curr_pos[1]] == ('(x,x)'):
                            break
                        else:
                            curr_pos = (curr_pos[0] + 1, curr_pos[1])
                            path.append(curr_pos)

            # if the vector has infinity on the right value, dont change the right value
            if vector[1] == numpy.inf:
                continue
            else:
                if vector[1] < 0:
                    for i in range(abs(vector[1])):
                        # put new position into path
                        if self.vectormap[curr_pos[0]][curr_pos[1] - 1] == ('(x,x)'):
                            break
                        else:
                            curr_pos = (curr_pos[0], curr_pos[1] - 1)
                            path.append(curr_pos)


                elif vector[1] > 0:
                    for i in range(abs(vector[1])):
                        if self.vectormap[curr_pos[0]][curr_pos[1] + 1] == ('(x,x)'):
                            break
                    else:
                        curr_pos = (curr_pos[0], curr_pos[1] + 1)
                        # put new position into path
                        path.append(curr_pos)

            # new_pos = (curr_pos[0] + vector[0], curr_pos[1] + vector[1])

            # get vector of next position
            # while loop stops here if it is (0,0)
            vector = self.vectormap[curr_pos[0]][curr_pos[1]]

            # i need to find a way to make sure the vector doesnt get set to the string

            # update curr poss to new poss

        return path

class AnytimeAstar():
    #the anytime a* algorithm

    def __init__(self, tim):
        # coeffiecnt for the heurstic
        self.heurcoef = 1000
        # list of possible coeffient states
        self.heurcolist = [1000,4, 1, 0]
        # index of current coeffiecnt
        self.heurind = 0
        # maxmium number of secends allowed to be taken
        self.timelimit = tim
        # is the current path optimal
        self.opti = False
        # current best path
        self.bestpath = None

    def popbestpath(self):
        # returns most optimal path computed
        p = self.bestpath
        self.bestpath = None
        return p

    def updateHeur(self):
        # updates the coef to one further down the list
        self.heurind += 1
        self.heurcoef = self.heurcolist[self.heurind]

    def chooseNode(self, open_list):
        #chooses the node with the lowest f value as current
        current_node = open_list[0]

        current_index = 0

        for index, item in enumerate(open_list):

            if item.f < current_node.f:
                current_node = item

                current_index = index

        return [current_node, current_index]

    def calcValue(self, child, current_node, end_node):
        child.g = current_node.g + 1

        # distance to end point

        # the reason the h distance is powered by 0.6 is because

        # it makes it prioritze diagonal paths over straight ones

        # even though they are technically the same g distance, this makes a* look better

        child.h = (((abs(child.position[0] - end_node.position[0]) ** 2) +

                    (abs(child.position[1] - end_node.position[1]) ** 2)) ** 0.6)
        # multiply pure heurstic by coeffeint for speed intially then later for optimal pathing
        child.h = child.h * self.heurcoef
        child.f = child.g + child.h


class ThetaStar():
    @staticmethod
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
                # update current position
                x += dx
                y += dy
        # if we haven't tripped a flag at this point, there should be line of sight
        return True


# change this for Harris' presentation
# create instance of anytime astar class
aastar = AnytimeAstar(0)
tstar = ThetaStar()


# function for pathfinding using dfs, bfs, dijkstra and A*
# Returns a list of tuples as a path from the given start to the given end in the given maze
def pathfind(maze, start, end, gui, coords, key, f=None):
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

    # looping until the end is found
    while len(open_list) > 0:

        # creating a wait affect so the results are not instant
        # adjustable through animation_speed in main_game.py
        if count >= gui.animation_speed:

            count = 0

            if key == "q":  # dfs, get the latest node
                current_node = open_list[-1]
                current_index = len(open_list) - 1

            elif key == "w":  # bfs, get the newest node
                current_node = open_list[0]
                current_index = 0

            elif key == "r":  # a*, get the node with the lowest f value
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
                        if tstar.los(maze, p, item):
                            current_node.parent = p
                            current_node.g = p.g + 1

            elif key == "v":  # vector field function
                vector = VectorField(end_node.position, start_node.position, maze)
                vector.makehm()
                #for i in range(len(vector.map)):
                #    print(vector.map[i])
                vector.vectormap()
                #for i in range(len(vector.map)):
                #    print(vector.vectormap[i])
                return (vector.pathmaker())


            elif key == "a":  # anytime a* get the node with the lowest f value
                current_node, current_index = aastar.chooseNode(open_list)

            elif key == "e":  # dijkstra, get the node with the lowest g value
                current_node = open_list[0]
                current_index = 0
                for index, item in enumerate(open_list):
                    if item.g < current_node.g:
                        current_node = item
                        current_index = index


            elif key == "y":  # theta*, get the node with the lowest f value but also check line of sight for lineage
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
                        if tstar.los(maze, p, current_node):
                            current_node.parent = p
                            current_node.g = p.g + 1

            # Pop current off open list, add to closed list
            open_list.pop(current_index)
            closed_list.append(current_node)

            # Found the goal
            if current_node == end_node:
                path = []
                current = current_node
                #construct path
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                coords.open_list = open_list
                coords.closed_list = closed_list
                #if its running anytime a* check time and potenttially recompute path
                endtime = time.monotonic()
                elasped = endtime - starttime
                if key == "a" and aastar.heurcoef == 0:
                    aastar.opti = True
                if key == "a" and elasped < aastar.timelimit and aastar.opti == False:
                    aastar.updateHeur()
                    aastar.bestpath = path
                    return pathfind(maze, start, end, gui, coords, key)

                if key == "a":
                    aastar.bestpath = None
                    aastar.heurcoef = 1000
                    aastar.heurind = 0
                    aastar.opti = False

                #if were recording data, then do that
                if (f is not None):
                    endtime = time.monotonic()
                    elasped = endtime - starttime
                    f.write(str(elasped))
                    f.write("\n")
                    f.write("algo " + key + " path length " + str(len(path)))
                    f.write("\n")
                return path  # Return path

            endtime = time.monotonic()
            elasped = endtime - starttime
            if key == "a" and elasped > aastar.timelimit and aastar.bestpath is not None:
                #if were recording data, then do that
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
            for new_pos in [(-1, 0), (0, 1), (1, 0), (0, -1)]:  # Adjacent squares

                # Get node position
                node_pos = (current_node.position[0] + new_pos[0],
                            current_node.position[1] + new_pos[1])

                # Make sure within range
                if (node_pos[0] > (len(maze) - 1) or node_pos[0] < 0
                        or node_pos[1] > (len(maze[len(maze) - 1]) - 1)
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

                if key == "e":  # dijkstra, add one to g value
                    child.g = current_node.g + 1


                elif key == "a":  # a*, calculate f value
                    aastar.calcValue(child, current_node, end_node)

                elif key == "r":  # a*, calculate f value
                    child.g = current_node.g + 1
                    # distance to end point
                    # the reason the h distance is powered by 0.6 is because
                    # it makes it prioritse diagonal paths over straight ones
                    # even though they are technically the same g distance, this makes a* look better
                    child.h = (((abs(child.position[0] - end_node.position[0]) ** 2) +
                                (abs(child.position[1] - end_node.position[1]) ** 2)) ** 0.6)
                    child.f = child.g + child.h


                elif key == "y":  # theta*, calculate f value
                    child.g = current_node.g + 1
                    # distance to end point
                    # the reason the h distance is powered by 0.6 is because
                    # it makes it prioritize diagonal paths over straight ones
                    # even though they are technically the same g distance, this makes a* look better
                    child.h = (((abs(child.position[0] - end_node.position[0]) ** 2) +
                                (abs(child.position[1] - end_node.position[1]) ** 2)) ** 0.6)
                    child.f = child.g + child.h

                # child is already in the open list
                for open_node in open_list:
                    # checking if the new path to children is worst or equal
                    # than one already in the open_list (by measuring g)
                    if child == open_node and child.g >= open_node.g:
                        break

                else:
                    # adding the child to the open list
                    open_list.append(child)


        # if skipped then update the gui
        else:
            coords.open_list = open_list
            coords.closed_list = closed_list
            gui.main(True)

        count += 1

    # print("no path found")
    if (f is not None):
        f.write("no path found")
        f.write("\n")
