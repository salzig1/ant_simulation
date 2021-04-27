import numpy
import random
import pygame



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
    
    def moveBack(self, nest):
        import main

        self.back = True
        len_coords = len(self.coordinates)
        if self.line_count != len_coords:
            a = self.coordinates[-self.line_count]
            e = self.coordinates[-(self.line_count+1)]
            dx, dy = (e[0] - a[0], e[1] - a[1])
            stepx, stepy = (dx/60, dy/60)
            
        
            self.x += stepx
            self.y += stepy

            # when reached end
            if round(self.x) == self.coordinates[-1-self.line_count][0] and round(self.y) == self.coordinates[-1-self.line_count][1]:
                self.line_count += 1
                
            
            if self.x >= nest.x and self.x <= nest.x + nest.width:
                    if self.y >= nest.y and self.y <= nest.y + nest.height:
                        pass
            
            