import pygame
import random
import math
import numpy
import ant as at

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
                if event.type == pygame.USEREVENT and not self.foundFood:
                    for ant in ants:
                        ant.saveCoordinates()
  
            # create ants one time
            while not self.ant_stop:
                for i in range(500):
                    ants.append(at.Ant(self.width/2, self.height/2, 1, random.randrange(3, 12)))
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
                            back_ants.append(ant)
                            self.foundFood = True

            # move ant back to nest
            if self.foundFood:
                for ant in back_ants:
                    ant.moveBack(nest)
                    #ant.drawPath(self.screen)
            
            pygame.display.flip()


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