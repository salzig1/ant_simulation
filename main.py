import pygame
import random
import numpy
import math


class Main:
    pygame.init()

    def __init__(self):
        pygame.display.set_caption("ants")
        self.WIDTH = 700
        self.HEIGHT = 700
        self.FPS = 60
        self.ANT_COUNT = 50
        self.GRID_SIZE = 10
        self.ants = []
        self.ant_stop = False
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.food = Object(500, 50, 50, 50, (0, 255, 0))
        self.nest = Object(int(self.WIDTH/2-5),
                           int(self.HEIGHT/2-5), 10, 10, (55, 55, 55))
        self.grid_list_1 = []
        self.grid_list_2 = []
        self.grid_list_3 = []
        self.grid_list_4 = []

    def run(self):
        self.create_ants(self.ANT_COUNT)
        self.create_grid(self.GRID_SIZE)
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
                    if event.key == pygame.K_i:
                        self.start = True

            self.draw_window()
            pygame.display.flip()

    def create_ants(self, ant_count):
        for i in range(self.ANT_COUNT):
            self.ants.append(Ant(self.WIDTH/2, self.HEIGHT /
                             2, 1, random.randint(10, 13)))

    def create_grid(self, size):
        for i in range(-size, self.WIDTH//2-size, size):
            for j in range(-size, self.HEIGHT//2-size, size):
                self.grid_list_1.append(Grid(size, i, j, (255, 255, 255)))

        for i in range(self.WIDTH//2-size, self.WIDTH, size):
            for j in range(self.HEIGHT//2-size, self.HEIGHT, size):
                self.grid_list_2.append(Grid(size, i, j, (255, 255, 255)))

        for i in range(self.WIDTH//2-size, self.WIDTH, size):
            for j in range(-size, self.HEIGHT//2-size, size):
                self.grid_list_3.append(Grid(size, i, j, (255, 255, 255)))

        for i in range(-size, self.WIDTH//2-size, size):
            for j in range(self.HEIGHT//2-size, self.HEIGHT, size):
                self.grid_list_4.append(Grid(size, i, j, (255, 255, 255)))

    def draw_shortest_path(self):
        for rect in mother_ant.best_path:
            rect.draw(main.screen)

    def draw_window(self):
        for ant in self.ants:
            ant.update()
        self.food.update()
        self.nest.update()
        # self.draw_shortest_path()


class Ant:
    path_count = 100000
    best_path = []

    def __init__(self, x, y, radius, time):
        self.x = x
        self.y = y
        self.radius = radius
        self.VEL = 5
        self.new_line = True
        self.foundFood = False
        self.foundWay = False
        self.deltax = 0
        self.deltay = 0
        self.anglecount = 0
        self.time = time
        self.count = self.time
        self.coords = []
        self.line_count = 0
        self.back = False
        self.addition = 2
       

    def update(self):
        pygame.draw.circle(main.screen, (255, 255, 255),(self.x, self.y), self.radius)
        
        self.foodCollision()
        self.movement()
        
        self.nest_collision(main.nest)
        self.wallCollision(main.WIDTH, main.WIDTH)
        self.grid_collision(main.WIDTH, main.HEIGHT)

    def grid_collision(self, width, height):
        if not self.foundFood:
            if self.x < width/2 and self.y < height/2:
                for rect in main.grid_list_1:
                    self.draw_rect(rect, main.grid_list_1)
            if self.x > width/2 and self.y < height/2:
                for rect in main.grid_list_3:
                    self.draw_rect(rect, main.grid_list_3)
            if self.x < width/2 and self.y > height/2:
                for rect in main.grid_list_4:
                    self.draw_rect(rect, main.grid_list_4)
            if self.x > width/2 and self.y > height/2:
                for rect in main.grid_list_2:
                    self.draw_rect(rect, main.grid_list_2)

    def draw_rect(self, rect, list):
        if rect.rect.collidepoint(self.x, self.y):
            self.coords.append(rect)

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
            
            self.follow_path(main.screen, main.nest, )
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
                if len(self.coords) < mother_ant.path_count:
                    mother_ant.best_path = self.coords.copy()
                    mother_ant.path_count = len(self.coords)
                self.radius = 3
                return True

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

    def nest_collision(self, nest):
        if self.foundFood:
            if round(self.x) in range(nest.x-10, nest.x+10) and round(self.y) in range(nest.y-10, nest.y+10):
                self.foundWay = False
                self.new_line = True
                self.deltax = 0
                self.deltay = 0
                return True
        return False

    def follow_path(self, screen, nest):

        
        index = len(mother_ant.best_path)-1 - self.line_count
        
        coords_x = round(mother_ant.best_path[index].x)
        coords_y = round(mother_ant.best_path[index].y)
        
        dx = coords_x - self.x
        dy = coords_y - self.y
        rads = math.atan2(-dx, dy)
        vector = pygame.math.Vector2(0, self.VEL).rotate_rad(rads)
        self.move(vector.x, vector.y)
        
        print("true", index, self.line_count, "len coords: " + str(len(self.coords)))

        if round(self.x) in range(coords_x-3, coords_x+3) and round(self.y) in range(coords_y-3, coords_y+3):
            self.line_count += self.addition
            if self.nest_collision(main.nest) and self.back:
                print(self.line_count)
                self.addition = -1*self.addition
                self.back = False
            if (self.foodCollision()) and not self.back:
                self.addition = -1*self.addition
                self.back = True
                
            
                
                
        
   

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
        pygame.draw.rect(main.screen, self.color, [
                         self.x, self.y, self.WIDTH, self.HEIGHT], border_radius=10)


class Grid:

    def __init__(self, size, i, j, color):
        self.size = size
        self.i = i
        self.j = j
        self.color = color
        self.visibility = False
        self.back_pheromone = 0
        self.forward_pheromone = 0
        self.rect = pygame.Rect(
            self.i+self.size, self.j+self.size, self.size, self.size)
        self.x = self.i+self.size
        self.y = self.j+self.size
        self.grid_list = []

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


if __name__ == "__main__":
    main = Main()
    rect = Grid(0, 0, 0, (0, 0, 0))
    mother_ant = Ant(0, 0, 0, 0)
    main.run()
