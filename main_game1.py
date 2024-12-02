import pygame
import logic

class Gui():
    '''
    Class for the gui of the application
    '''
    
    # gui constants
    FPS = 60
    WIDTH = 590 
    HEIGHT = 590 

    # actual grid size
    g_restrict_size = 575
    
    def __init__(self, coords):

        # gui variables
        self.grid_size = 30
        self.box_width = self.g_restrict_size/self.grid_size
        self.coords = coords
        self.placing_walls = False
        self.removing_walls = False
        self.animation_speed = 2

        # start pygame application
        pygame.init()
        self.win = pygame.display.set_mode((self.WIDTH, self.HEIGHT))  # Updated window size
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Visualizing Pathfinding Algorithms")

    # main function for gui
    def main(self, running=False):
        
        self.clock.tick(self.FPS)

        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
                
        # if the mouse button was pressed down continue placing obstacle
        if not running:
            if self.placing_walls == True:
                self.place_wall()
            elif self.removing_walls == True:
                self.remove()

        # get mouse and key presses
        self.event_handle(running)

        # redraw and update the display
        self.redraw()
        pygame.display.update()
        
    # handles key and mouse presses
    def event_handle(self, running):

        run_keys = {"q", "w", "e", "r","a","t"}
        checkpoint_keys = {"1", "2"}

        # gets key presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # key presses
            elif event.type == pygame.KEYDOWN:
                
                key = chr(event.key)

                if running == False:

                    # spacebar to generate blobs                    
                    if key == " ":
                        self.coords.generate_blobs(gui)

                    # run algorithm 
                    if key in run_keys: # q, w, e and r
                        self.run_algorithm(key)              
                    
                    # clear the whole board
                    elif key == "x":
                        self.coords.remove_all()

                    elif key == "l":
                        loop = dataLoop(10,"a","t")
                        loop.theblobloop()


                        
                    # place checkpoints with number keys
                    elif key in checkpoint_keys: # 1 and 2
                        self.place_check_point(key)
                    
                    else:
                        # case to avoid our program crashing
                        print(key)

                # increase speed of the pathfinding
                elif (key == "+" or key == "=") and self.animation_speed > 0:
                    if self.animation_speed <= 2:
                        self.animation_speed = 1
                    else:
                        self.animation_speed = int(self.animation_speed * 0.5) + 1

                # decrease speed of pathfinding
                elif key == "-":
                    self.animation_speed = int(self.animation_speed * 2) + 1

                else:
                    print(key)

            # mouse button down
            elif event.type == pygame.MOUSEBUTTONDOWN:

                if running == False:
                
                    # place walls
                    if event.button == 1: # left down
                        self.placing_walls = True
                        # debugging: print("This works.")

                    # remove walls
                    elif event.button == 3: # right down
                        self.removing_walls = True

            # cases for when the mouse button is lifted up
            # otherwise it would keep it held down

            elif event.type == pygame.MOUSEBUTTONUP:

                # stop placing walls
                if event.button == 1: # left up
                    self.placing_walls = False

                # stop removing walls
                elif event.button == 3: # right up
                    self.removing_walls = False

    # redrawing the gui
    # contains (and hides) most of our interface

    def redraw(self):

        # background color
        self.win.fill((0, 40, 50))
        self.draw_points()

        # redrawing grids
        self.draw_grid()

        """
        # screen borders
        pygame.draw.rect(self.win,(10,80,80),(-2,0,22,self.HEIGHT)) # left
        pygame.draw.rect(self.win,(10,80,80),(572,0,19,self.HEIGHT)) # right
        pygame.draw.rect(self.win,(10,80,80),(0,0,self.HEIGHT,18)) # top
        pygame.draw.rect(self.win,(10,80,80),(0,573,self.HEIGHT,20)) # bottom
        # pygame.draw.rect(self.win,(0, 40, 50),(591,0,330, self.HEIGHT))
        """


    # draw the grid lines
    def draw_grid(self):
        for i in range(self.grid_size-1):

            # vertical grids
            pygame.draw.rect(self.win, (10,80,80),
                             (((i+1)*self.box_width-2), 18, 2.8, self.g_restrict_size))
            # horizontal
            pygame.draw.rect(self.win, (10,80,80),
                             (20,((i+1)*self.box_width-2), self.g_restrict_size, 2.8))

    # draws all the squares for the walls, checkpoints ect
    def draw_points(self):

        # currently searching this box
        for node in self.coords.open_list:
            self.draw_box(node.position, (0, 255, 0))

        for node in self.coords.closed_list:
            self.draw_box(node.position, (0, 0, 255))

        for wall in self.coords.final_path:
            self.draw_box(wall, (255, 0, 255))

        for wall in self.coords.obstacle:
            self.draw_box(wall, (0, 0, 0))

        for i,point in enumerate(self.coords.check_points):
            if point != "None":
                self.draw_box(point, (255, 30, 30))
                self.display_text(str(i+1), (255, 255, 255),
                                  self.box_center(point), int(self.box_width))
        
        if self.coords.start != None:
            self.draw_box(self.coords.start, (255, 0, 0))
            self.display_text("S", (255, 255, 255),
                              self.box_center(self.coords.start), int(self.box_width))

        if self.coords.end != None:
            self.draw_box(self.coords.end, (255, 0, 0))
            self.display_text("E", (255, 255, 255),
                              self.box_center(self.coords.end), int(self.box_width))

    # gets the center point of a node
    def box_center(self, box):
        boxX, boxY = box
        center = ((boxX*self.box_width+(self.box_width/2)),
                  (boxY*self.box_width+(self.box_width/2)))
        return center

    # used to draw the boxed given colours and position
    def draw_box(self, box, colour):
        boxX, boxY = box
        pygame.draw.rect(self.win, colour,
                        (boxX*self.box_width, boxY*self.box_width,
                         self.box_width, self.box_width))

    # getting the coordinates of clicked cells
    # restricts the user and algorithm from accessing cells outside of the area 
      
    def get_box_coords(self):
        adjusted_mouse_x = min(max(self.mouse_x - 1, 0), self.g_restrict_size - 1)
        adjusted_mouse_y = min(max(self.mouse_y - 1, 0), self.g_restrict_size - 1)
        
        # checking if the adjusted mouse position is within the leftmost column
        if adjusted_mouse_x < self.box_width:
            adjusted_mouse_x = self.box_width
        
        # checking if the adjusted mouse position is within the top row
        if adjusted_mouse_y < self.box_width:
            adjusted_mouse_y = self.box_width
        
        boxX = int(adjusted_mouse_x / self.box_width)
        boxY = int(adjusted_mouse_y / self.box_width)
        
        # returning the grid cell coordinates
        return (boxX, boxY)

    # placing checkpoints
    def place_check_point(self, index):
        coords = self.get_box_coords()
        if (coords != self.coords.start and coords != self.coords.end
                and coords not in self.coords.obstacle and coords
                not in self.coords.check_points):
            
            while len(self.coords.check_points) <= int(index)-1:
                self.coords.check_points.append("None")
            self.coords.check_points[int(index)-1] = coords

    # placing obstacle
    def place_wall(self):
        coords = self.get_box_coords()
        if (coords != self.coords.start and coords != self.coords.end
                and coords not in self.coords.obstacle and coords
                not in self.coords.check_points):
            self.coords.obstacle.append(coords)

    # removing nodes such as obstacle checkpoints ect
    def remove(self):
        coords = self.get_box_coords()
        if coords in self.coords.waobstaclells:
            self.coords.obstacle.remove(coords)
        elif coords in self.coords.check_points:
            self.coords.check_points.remove(coords)
        elif coords == self.coords.start:
            self.coords.start = None
        elif coords == self.coords.end:
            self.coords.end = None

    # function that prepares for a pathfind and runs pathfind function
    def run_algorithm(self, key, f = None):
        self.placing_walls == False
        self.removing_walls == False
        self.coords.remove_last()

        # for now we'll only have 1 checkpoint
        # if we have 2 or more checkpoints
        if len(self.coords.check_points) > 1:

            # create the maze array and remove missed checkpoint numbers
            self.coords.create_maze(gui)
            check_points = self.coords.check_points[:]
            check_points = [point for point in check_points if point != "None"]

            # iterate through every checkpoint and pathfind to it
            for i,point in enumerate(check_points):
                if i != len(check_points)-1:
                    
                    start = point
                    end = check_points[i+1]

                    new_path = logic.pathfind(self.coords.maze, start, end,
                                        self, self.coords, key,f=f)
                    if new_path == None:
                        new_path = []
                        
                    self.coords.final_path.extend(new_path)

    
    # to show numbers (1 and 2)
    def display_text(self, txt, colour, center, size):
        font = pygame.font.Font(None, size)
        text_surf = font.render(txt, True, colour)
        text_rect = text_surf.get_rect()
        text_rect.center = (center)
        self.win.blit(text_surf, text_rect)


class dataLoop():
    def __init__(self,l,k,k2):
        self.loopfor = l
        self.key = k
        self.key2 = k2


    def theblobloop(self):
        f = open("resultsoutput.txt", "w")
        f.write("Now comparing "+self.key+" and "+self.key2+" for "+str(self.loopfor))
        f.write("\n")
        ind = 1
        for x in range(self.loopfor):
            #print("trial: ",ind)
            f.write("trial: "+ str(ind))
            f.write("\n")

            gui.coords.generate_blobs(gui)

            f.write("alg " + self.key+ " ")
            #f.write("\n")
            gui.run_algorithm(self.key,f=f)
            f.write("alg " + self.key2 + " ")
            #f.write("\n")
            gui.run_algorithm(self.key2, f=f)
            ind += 1


        f.close()
        k1, k2, kd1, kd2,lt1,lt2,ld1,ld2 = self.computeavg()
        f = open("resultsoutput.txt", "a")

        f.write("\n")
        f.write("average for " + self.key + ": " + str(k1))
        f.write("\n")
        f.write(str(lt1))
        f.write("\n")
        f.write("average for " + self.key2 + ": " + str(k2))
        f.write("\n")
        f.write(str(lt2))
        f.write("\n")
        f.write("average for path length for " + self.key + ": " + str(kd1))
        f.write("\n")
        f.write(str(ld1))
        f.write("\n")
        f.write("average path length for " + self.key2 + ": " + str(kd2))
        f.write("\n")
        f.write(str(ld2))

        f.close()


    def thecurveloop(self):
        pass

    def has_numbers(self,inputString):
        return any(char.isdigit() for char in inputString)

    def computeavg(self):
        f = open("resultsoutput.txt")
        key1distvals = []
        key2distvals = []
        key1vals = []
        key2vals = []
        key1loc = "alg "+self.key+" "
        key2loc = "alg " + self.key2 + " "
        key1distloc = "algo "+self.key+" "
        key2distloc = "algo " + self.key2 + " "
        for line in f.readlines():
            if key1loc in line and self.has_numbers(line) == True:
                trash,trahs2,val =line.split(" ")
                val = float(val.replace("\n",""))
                key1vals.append(val)
            if key1distloc in line and self.has_numbers(line) == True:
                trash,trahs2,tra3,tra4,val =line.split(" ")
                val = float(val.replace("\n",""))
                key1distvals.append(val)
            if key2loc in line and self.has_numbers(line) == True:
                trash,trahs2,val =line.split(" ")
                val = float(val.replace("\n",""))
                key2vals.append(val)
            if key2distloc in line and self.has_numbers(line) == True:
                trash,trahs2,tra3,tra4,val =line.split(" ")
                val = float(val.replace("\n",""))
                key2distvals.append(val)
        key1avg = None
        key2avg = None
        key1distavg = None
        key2distavg = None

        listtime1 = key1vals

        listtime2 = key2vals

        listdist1 = key1distvals

        listdist2 = key2distvals

        if(len(key1vals) > 0):
            k1l = len(key1vals)
            key1avg = sum(key1vals) / k1l
        if (len(key2vals) > 0):
            k2l = len(key2vals)
            key2avg = sum(key2vals) / k2l
        if (len(key1distvals) > 0):
            k1dl = len(key1distvals)
            key1distavg = sum(key1distvals) / k1dl
        if (len(key2distvals) > 0):
            k2dl = len(key2distvals)
            key2distavg = sum(key2distvals) / k2dl

        return key1avg,key2avg,key1distavg,key2distavg,listtime1,listtime2,listdist1,listdist2


        f.close()




        # main loop
if __name__ == "__main__":
    gui = Gui(logic.CoOrdinates())
    while True:
        gui.main()