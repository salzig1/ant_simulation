import pygame
import random
import numpy


class Main:
    pygame.init()
    def __init__(self):
        pygame.display.set_caption("ants")
        self.WIDTH = 700
        self.HEIGHT = 700
        self.FPS = 30
        self.ANT_COUNT = 1 # change this for more ants
        self.ants = []
        self.ant_stop = False
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.food = Object(500, 200, 50, 300, (0, 255, 0))
        self.nest = Object(self.WIDTH/2-5, self.HEIGHT/2-5, 10, 10, (55, 55, 55))
        pygame.time.set_timer(pygame.USEREVENT+1, random.randrange(1000))

    def run(self):
        self.createAnts(self.ANT_COUNT)
        run = True
        while run:
            self.screen.fill((0, 0, 0))
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_ESCAPE:
                        run = False
                if event.type == pygame.USEREVENT+1:
                    for ant in self.ants:
                        ant.new_line = True
 
            self.drawWindow()     
            pygame.display.flip()
    
    def createAnts(self, ant_count):
        for i in range(self.ANT_COUNT):
            self.ants.append(Ant(self.WIDTH/2, self.HEIGHT/2, 1))
    
    def drawWindow(self):
        for ant in self.ants:
            ant.update()
        self.food.update()
        self.nest.update()
    
           

class Ant:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.VEL = 2
        self.RAND = numpy.linspace(-self.VEL, +self.VEL, 100)
        self.new_line = False
       
        self.foundFood = False
        self.foundWay = False
  
        self.deltax = 0
        self.deltay = 0
        self.sx = 0
        self.sy = 0
        
    def update(self):
        self.movement()
        self.foodCollision()
        self.nestCollision(main.nest)
        self.wallCollision(main.WIDTH, main.WIDTH)

        pygame.draw.circle(main.screen, (255, 255, 255), (self.x, self.y), self.radius)

    def movement(self):
        if not self.foundFood:
            if self.new_line:
                self.deltax = random.choice(self.RAND)
                self.deltay = random.choice(self.RAND)
                self.new_line = False
            self.move(self.deltax, self.deltay)
        else:
            self.backToNest(main.screen, main.nest)

    def foodCollision(self):
        if self.x >= main.food.x and self.x <= main.food.x + main.food.WIDTH:
            if self.y >= main.food.y and self.y <= main.food.y + main.food.HEIGHT:
                self.foundFood = True
                self.radius = 4  # for visualization

    def wallCollision(self, width, height):
        if self.x > width:
            self.x = width
        if self.x < 0:
            self.x = 0
        if self.y > height:
            self.y = height
        if self.y < 0:
            self.y = 0

    def nestCollision(self ,nest):
        if round(self.x) == nest.x and round(self.y) == nest.y:
            self.foundFood = False
            self.foundWay = False
            self.radius = 1
    
    def backToNest(self, screen, nest):
        if not self.foundWay:
            dx, dy = (nest.x - self.x, nest.y - self.y)
            self.sx, self.sy = (dx/main.FPS, dy/main.FPS)
            self.foundWay = True
        self.move(self.sx, self.sy)
        
    def move(self, deltax, deltay):
        self.x += deltax
        self.y += deltay









class Object:
    def __init__(self, x, y, WIDTH, HEIGHT, color):
        self.x = x
        self.y = y
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.color = color

    def update(self):
        pygame.draw.rect(main.screen, self.color, [self.x, self.y, self.WIDTH, self.HEIGHT], border_radius=10)
        
 
if __name__ == "__main__":
    main = Main()
    main.run()