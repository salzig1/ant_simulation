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
        self.ant_stop = False
        self.fps = 30
        self.nest = Object(self.width/2-5, self.height/2-5, 10, 10, (55, 55, 55))
  
    def run(self):
        pygame.display.set_caption("Ant Simulator")
        # saving cords every ... secs
        pygame.time.set_timer(pygame.USEREVENT, 3000)
        # initialize food
        food = Object(500, 350, 50, 50, (0, 255, 0))
        nest = Object(self.width/2-5, self.height/2-5, 10, 10, (55, 55, 55))

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

  
            # create ants one time
            while not self.ant_stop:
                for i in range(1000):
                    ants.append(Ant(self.width/2, self.height/2, 1, random.randrange(6, 7)))
                self.ant_stop = True
            
            
            # draw things
            for i in range(len(ants)):
                ants[i].update(self.screen, self.width, self.height, self.nest, self.fps)

            food.update(self.screen)
            self.nest.update(self.screen)

            # food collison
            for ant in ants:
                if not ant.foundFood:
                    if ant.x >= food.x and ant.x <= food.x + food.width:
                        if ant.y >= food.y and ant.y <= food.y + food.height:
                            ant.foundFood = True

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
        self.beforeCoords = []
        self.afterCoords = []
        self.coord_count = 0 
        self.foundFood = False
        self.timerRed = 1000
        self.timerBlue = 1000
        self.blue = 255
        self.stepx = 0
        self.stepy = 0
        self.foundWay = False

    def update(self, screen, width, height, nest, fps):
        if not self.foundFood:
            if self.walk_count == self.walk_time:
                self.walk_list[0] = random.choice(self.rand)
                self.walk_list[1] = random.choice(self.rand)
                self.walk_count = 0
        
            self.x += self.walk_list[0]
            self.y += self.walk_list[1]
            self.walk_count += 1
     
        if self.foundFood:
            self.moveBack(screen, nest, fps)

        self.drawPath(screen)
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

    def drawPath(self, screen):
        pass
    
    def moveBack(self, screen, nest, fps):
        if not self.foundWay:
            dx, dy = (nest.x - self.x, nest.y - self.y)
            self.stepx, self.stepy = (dx/fps, dy/fps)
            self.foundWay = True

        self.x += self.stepx
        self.y += self.stepy

        if round(self.x) == nest.x and round(self.y) == nest.y:
            self.foundFood = False
            
        # pheromones
                
            

    
        

class Object:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def update(self, screen):
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.width, self.height], border_radius=20)
        

 
if __name__ == "__main__":
    main = Main()
    main.run()