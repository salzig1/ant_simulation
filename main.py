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
        self.ANT_COUNT = 50 # change this for more ants
        self.ants = []
        self.ant_stop = False
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.food = Object(500, 200, 50, 50, (0, 255, 0))
        self.nest = Object(self.WIDTH/2-5, self.HEIGHT/2-5, 10, 10, (55, 55, 55))


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
              
 
            self.drawWindow()     
            pygame.display.flip()
    
    def createAnts(self, ant_count):
        for i in range(self.ANT_COUNT):
            self.ants.append(Ant(self.WIDTH/2, self.HEIGHT/2, 1, 10))
    
    def drawWindow(self):
        for ant in self.ants:
            ant.update()
        self.food.update()
        self.nest.update()
    
           

class Ant:
    def __init__(self, x, y, radius, time):
        self.x = x
        self.y = y
        self.radius = radius
        self.VEL = 2
        self.new_line = True
        self.foundFood = False
        self.foundWay = False
        self.deltax = 0
        self.deltay = 0
        self.sx = 0
        self.sy = 0
        self.anglecount = 0
        self.time = time
        self.count = self.time  
        
    def update(self):
        
        self.movement()
        self.foodCollision()
        self.nestCollision(main.nest)
        self.wallCollision(main.WIDTH, main.WIDTH)

        pygame.draw.circle(main.screen, (255, 255, 255), (self.x, self.y), self.radius)
        

    def movement(self):
        if not self.foundFood:
            if self.new_line or self.count == self.time:
                angle = self.getNewAngle(self.deltax, self.deltay)
                vector = pygame.math.Vector2(0, self.VEL).rotate(angle)
                self.deltax = vector.x
                self.deltay = vector.y
                self.new_line = False
                self.count = 0
            self.move(self.deltax, self.deltay)
        else:
            self.backToNest(main.screen, main.nest)
        self.count += 1 
    
    def getNewAngle(self, x, y):
        if x > 0 and y > 0:
            return random.randint(-110, 20)
        if x > 0 and y < 0:
            return random.randint(160, 290)
        if x < 0 and y > 0:
            return random.randint(-20, 110)
        if x < 0 and y < 0:
            return random.randint(70, 200)
        if x == 0 and y == 0:
            return random.randint(0, 360)
        else:
            return random.randint(-65, 65)
     
    def foodCollision(self):
        if self.x >= main.food.x and self.x <= main.food.x + main.food.WIDTH:
            if self.y >= main.food.y and self.y <= main.food.y + main.food.HEIGHT:
                self.foundFood = True

    def wallCollision(self, width, height):
        collision = False
        if self.x < 0:
            angle = random.randint(-135, -45)
            collision = True
        if self.y < 0:
            angle = random.randint(-45, 45)
            collision = True
        if self.x > width:
            angle = random.randint(45, 135)
            collision = True
        if self.y > height:
            angle = random.randint(135, 225)
            collision = True
    
        if collision:
            self.new_line = False
            vector = pygame.math.Vector2(0, self.VEL).rotate(angle)
            self.deltax = vector.x
            self.deltay = vector.y

    def nestCollision(self ,nest):
        if round(self.x) == nest.x and round(self.y) == nest.y:
            self.foundFood = False
            self.foundWay = False
            self.new_line = True
            self.deltax = 0
            self.deltay = 0
    
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