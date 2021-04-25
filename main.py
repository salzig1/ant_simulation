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
  
    def run(self):
        pygame.display.set_caption("Ant Simulator")
        # saving cords every ... secs
        pygame.time.set_timer(pygame.USEREVENT, 600)
        # initialize food
        food = Object(100, 500, 50, 50, (0, 255, 0))
        # init nest
        nest = Object(self.width/2, self.height/2, 10, 10, (0, 0, 0))
        ants = []
        
        run = True
        while run:
            self.screen.fill((200, 200, 200))
            self.clock.tick(70)
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
                    ants.append(Ant(self.width/2, self.height/2, 1, random.randrange(25, 30)))
                self.ant_stop = True

            # draw things
            for i in range(len(ants)):
                ants[i].update(self.screen, self.width, self.height)

            food.update(self.screen)
            nest.update(self.screen)

            # food collison
            for ant in ants:
                if ant.x >= food.x and ant.x <= food.x + food.width:
                    if ant.y >= food.y and ant.y <= food.y + food.height:
                        if not self.save_coords:
                            ant.saveCoordinates()
                            self.save_coords = True
                        ant.drawPath(self.screen)
                        ant.moveBack(self.screen)
                        self.foundFood = True

            
            pygame.display.flip()


class Ant:
    def __init__(self, x, y, radius, walk_time):
        self.x = x
        self.y = y
        self.radius = radius
        self.vel = 3
        self.rand = numpy.linspace(-self.vel, +self.vel, 100)
        self.walk_time = walk_time
        self.walk_count = self.walk_time
        self.walk_list = [0, 0]
        self.coordinates = [[350, 350]]
        self.coord_count = 0  # used for going back to nest
        self.back = False
        
    
    def update(self, screen, width, height):
        # stop moving if food has been found
        if not main.foundFood:
            # gets a ranodom value from rand every walk_time ticks and sets x and y
            if self.walk_count == self.walk_time:
                self.walk_list[0] = random.choice(self.rand)
                self.walk_list[1] = random.choice(self.rand)
                self.walk_count = 0
            
            self.x += self.walk_list[0]
            self.y += self.walk_list[1]

            self.walk_count += 1

        # draw updated ant
        pygame.draw.circle(screen, (120, 30, 60), (self.x, self.y), self.radius)

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

        #pygame.draw.line(screen, (120, 30, 60), (350, 350), (self.coordinates[0][0], self.coordinates[0][1]))
        #pygame.draw.line(screen, (120, 30, 60), (self.coordinates[0][0], self.coordinates[0][1]), (self.coordinates[1][0], self.coordinates[1][1]))
        #pygame.draw.line(screen, (120, 30, 60), (self.coordinates[1][0], self.coordinates[1][1]), (self.coordinates[2][0], self.coordinates[2][1]))
        #pygame.draw.line(screen, (120, 30, 60), (self.coordinates[2][0], self.coordinates[2][1]), (self.coordinates[3][0], self.coordinates[3][1]))
        
    def moveBack(self, screen):
        print(self.coordinates[:-1])
        return

    
  



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