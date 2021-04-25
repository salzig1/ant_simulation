import pygame
import random
import math
import numpy

class Main:
    pygame.init()
    def __init__(self):
        self.width = 700
        self.height = 700
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.foundFood = False
        self.ant_stop = False
        self.save_coords = False
        self.fps = 30
        self.nest = Object(self.width/2-5, self.height/2-5, 10, 10, (55, 55, 55))
  
    def run(self):
        pygame.display.set_caption("Ant Simulator")
        # saving cords every ... secs
        pygame.time.set_timer(pygame.USEREVENT, 3000)
        # initialize food
        food = Object(500, 350, 50, 50, (0, 255, 0))

        ants = []
        back_ants = []
        
        run = True
        while run:
            self.screen.fill((0, 0, 0))
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False 
                if event.type == pygame.USEREVENT and not self.foundFood:
                    for ant in ants:
                        ant.saveCoordinates()
  
            # create ants one time
            while not self.ant_stop:
                for i in range(500):
                    ants.append(Ant(self.width/2, self.height/2, 1, random.randrange(3, 12)))
                self.ant_stop = True

            # draw things
            for i in range(len(ants)):
                ants[i].update(self.screen, self.width, self.height)

            food.update(self.screen)
            self.nest.update(self.screen)

            # food collison
            for ant in ants:
                if not ant.back:
                    if ant.x >= food.x and ant.x <= food.x + food.width:
                        if ant.y >= food.y and ant.y <= food.y + food.height:
                            # save cords for one last time
                            ant.saveCoordinates()  
                            ant.radius = 3
                            back_ants.append(ant)
                            self.foundFood = True

            # move ant back to nest
            if self.foundFood:
                for ant in back_ants:
                    ant.moveBack()
                    ant.drawPath(self.screen)
            
            pygame.display.flip()


class Ant:
    def __init__(self, x, y, radius, walk_time):
        self.x = x
        self.y = y
        self.radius = radius
        self.vel = 2
        self.rand = numpy.linspace(-self.vel, +self.vel, 100)
        self.walk_time = walk_time
        self.walk_count = self.walk_time
        self.walk_list = [0, 0]
        self.coordinates = [[350, 350]]
        self.coord_count = 0  # used for going back to nest
        self.back = False
        self.line_count = 1 # used for going back to nest
        
    
    def update(self, screen, width, height):
        if not self.back:
            if self.walk_count == self.walk_time:
                self.walk_list[0] = random.choice(self.rand)
                self.walk_list[1] = random.choice(self.rand)
                self.walk_count = 0
        
            self.x += self.walk_list[0]
            self.y += self.walk_list[1]
            self.walk_count += 1
     
        # draw updated ant
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), self.radius)

        # wall collision
        if self.x > width:
            self.x = width-self.radius*2
        if self.x < 0:
            self.x = 0+self.radius*2
        if self.y > height:
            self.y = height-self.radius*2
        if self.y < 0:
            self.y = 0+self.radius*2

    def saveCoordinates(self):
        self.coordinates.append([round(self.x), round(self.y)]) 
    
    def drawPath(self, screen):
        for i in range(len(self.coordinates)-1):
            pygame.draw.line(screen, (120, 30, 60), (self.coordinates[i][0], self.coordinates[i][1]), (self.coordinates[i+1][0], self.coordinates[i+1][1]))
    
    def moveBack(self):
        self.back = True
        len_coords = len(self.coordinates)
        if self.line_count != len_coords:
            a = self.coordinates[-self.line_count]
            e = self.coordinates[-(self.line_count+1)]
            dx, dy = (e[0] - a[0], e[1] - a[1])
            stepx, stepy = (dx/main.fps, dy/main.fps)
            print(stepx, stepy)

            self.x += stepx
            self.y += stepy

            # when reached end
            if round(self.x) == self.coordinates[-1-self.line_count][0] and round(self.y) == self.coordinates[-1-self.line_count][1]:
                self.line_count += 1
                print("true")

            if self.x >= main.nest.x and self.x <= main.nest.x + main.nest.width:
                    if self.y >= main.nest.y and self.y <= main.nest.y + main.nest.height:
                        print("true")


class Object:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def update(self, screen):
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.width, self.height])
        


if __name__ == "__main__":
    main = Main()
    main.run()