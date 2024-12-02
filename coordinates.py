
import random
import math
from node import Node


# class containing all coordinates and functions for calculations todo with them
class Coordinates():

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

    # generating obstacles
    # creates random obstacles in the form of blob clusters
    def generate_blobs(self, gui):
        self.obstacle = []
        grid_size = gui.grid_size

        # defining the range of cluster sizes
        min_cluster_size = 1
        max_cluster_size = 5

        # function that calculates the Euclidean distance between two points
        def distance(p1, p2):
            return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

        for _ in range(grid_size):
            cluster_added = False
            while not cluster_added:
                # choosing a random cluster center
                center = (random.randint(0, grid_size), random.randint(0, grid_size))

                # randomly selecting a cluster size within the defined range
                cluster_size = random.randint(min_cluster_size, max_cluster_size)

                # generating a cluster around the center
                cluster = [(x, y) for x in range(center[0] - cluster_size // 2, center[0] + cluster_size // 2 + 1)
                           for y in range(center[1] - cluster_size // 2, center[1] + cluster_size // 2 + 1)
                           if 0 <= x < grid_size and 0 <= y < grid_size]

                # checking if each cluster is at least 2 cells apart
                if all(distance(cell, obstacle) >= 3 for cell in cluster for obstacle in self.obstacle):
                    # Add the cluster to the list of obstacles
                    self.obstacle.extend(cluster)
                    cluster_added = True

            # removing two specific walls for test speed imporvement
            if ((5, 5) in self.obstacle):
                self.obstacle.remove((5, 5))
            if ((25, 25) in self.obstacle):
                self.obstacle.remove((25, 25))

            # remove two specific walls for test speed imporvement
            if ((5, 5) in self.obstacle):
                self.obstacle.remove((5, 5))
            if ((25, 25) in self.obstacle):
                self.obstacle.remove((25, 25))

    """
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
        """

    """
    # hard-coded crescent-shaped obstacles
    def generate_crescent_obstacles(self, gui):
        self.obstacle = []

        grid_size = gui.grid_size

        # Define hard-coded crescent-shaped obstacles
        crescent1 = [
            (2, 5), (2, 6),
            (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7),
            (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7),
            (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7),
            (6, 3), (6, 4), (6, 5)
        ]

        crescent2 = [
            (9, 5), (9, 6),
            (10, 2), (10, 3), (10, 4), (10, 5), (10, 6), (10, 7),
            (11, 2), (11, 3), (11, 4), (11, 5), (11, 6), (11, 7),
            (12, 2), (12, 3), (12, 4), (12, 5), (12, 6), (12, 7),
            (13, 4), (13, 5)
        ]

        self.obstacle.extend(crescent1)
        self.obstacle.extend(crescent2)
        """