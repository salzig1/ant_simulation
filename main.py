import pygame
import random
import math
import numpy

class Main:
    pygame.init()
    def __init__(self):
        self.width = 400
        self.height = 400
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        
  
    def run(self):
        # userevent for saving coords
        pygame.time.set_timer(pygame.USEREVENT, 5000)
        # userevent for coming back to nest
        pygame.time.set_timer(pygame.USEREVENT + 1, 20000)

        ants = []
        # initialize food
        food = Food(100, 500, 50, 50, (0, 255, 0))
        # dead ants count
        pop = 0
        run = True
        ant_stop = False
        drawline = False
        
        while run:
            self.screen.fill((200, 200, 200))
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False 
                if event.type == pygame.USEREVENT:
                    for ant in ants:
                        ant.saveCoordinates()
                if event.type == pygame.USEREVENT + 1:  # when it is time to come back
                    for ant in ants:
                        ant.back = True

                    
            # create ants one time
            while not ant_stop:
                for i in range(1):
                    ants.append(Ant(self.width/2, self.height/2, 1, random.randrange(15, 25)))
                ant_stop = True

            # ant nest
            pygame.draw.circle(self.screen, (0, 0, 0), (self.width/2, self.height/2), 10)

            # draw ants
            for i in range(len(ants)):
                ants[i].update(self.screen, self.width, self.height)

            #draw food
            food.update(self.screen)

            # food collison
            for ant in ants:
                if ant.x >= food.x and ant.x <= food.x + food.width:
                    if ant.y >= food.y and ant.y <= food.y + food.height:
                        ants.pop(ants.index(ant))
                        pop += 1
                        print(pop)

            pygame.display.flip()


class Ant:
    def __init__(self, x, y, radius, walk_time):
        self.x = x
        self.y = y
        self.radius = radius
        self.vel = 1
        self.rand = numpy.linspace(-self.vel, +self.vel, 100)
        self.walk_time = walk_time
        self.walk_count = self.walk_time
        self.walk_list = [0, 0]
        self.coordinates = []
        self.back = False
        
    
    def update(self, screen, width, height):
        if not self.back:
            # gets a ranodom value from rand every walk_time ticks and sets x and y
            if self.walk_count == self.walk_time:
                self.walk_list[0] = random.choice(self.rand)
                self.walk_list[1] = random.choice(self.rand)
                self.walk_count = 0
            
            self.x += self.walk_list[0]
            self.y += self.walk_list[1]

            self.walk_count += 1

        # called if it is time to come back
        if self.back:
            print(self.coordinates)
            pygame.draw.line(screen, (120, 30, 60) )
            pygame.draw.circle(screen, (120, 30, 60), (self.coordinates[0][0], self.coordinates[0][1]), self.radius)
            pygame.draw.circle(screen, (120, 30, 60), (self.coordinates[1][0], self.coordinates[1][1]), self.radius)
            pygame.draw.circle(screen, (120, 30, 60), (self.coordinates[2][0], self.coordinates[2][1]), self.radius)
            pygame.draw.circle(screen, (120, 30, 60), (self.coordinates[3][0], self.coordinates[3][1]), self.radius)

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
    

    
  
       


        
   


class Food:
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