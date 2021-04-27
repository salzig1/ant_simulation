import pygame
import random
import math
import numpy
import ant as ant_file

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
        self.fps = 70
        self.nest = Object(self.width/2-5, self.height/2-5, 10, 10, (55, 55, 55))
  
    def run(self):
        pygame.display.set_caption("Ant Simulator")
        # saving cords every ... secs
        pygame.time.set_timer(pygame.USEREVENT, 3000)
        # initialize food
        nest = Object(self.width/2-5, self.height/2-5, 10, 10, (55, 55, 55))
        foods = []
        ants = []


        foods.append(Object(500, 200, 50, 50, (0, 255, 0)))
        foods.append(Object(100, 350, 50, 100, (0, 255, 0)))
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
                for i in range(1500):
                    ants.append(ant_file.Ant(self.width/2, self.height/2, 1, random.randrange(3, 12)))
                self.ant_stop = True
            
            
            # draw things
            for ant in ants:
                ant.update(self.screen, self.width, self.height)

            for food in foods:
                food.update(self.screen)
            self.nest.update(self.screen)

            # food collison
            for ant in ants:
                if not ant.back:
                    for food in foods:
                        if ant.x >= food.x and ant.x <= food.x + food.width:
                            if ant.y >= food.y and ant.y <= food.y + food.height:
                                # save cords for one last time
                                ant.saveCoordinates()  
                                back_ants.append(ant)
                                self.foundFood = True

            # move ant back to nest
            if self.foundFood:
                for ant in back_ants:
                    #}ant.color = (127, 30, 212)
                    ant.moveBack(nest, self.fps)
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
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.width, self.height], border_radius=0)
        


if __name__ == "__main__":
    main = Main()
    main.run()