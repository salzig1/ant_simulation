import pygame
pygame.init()

def main():
    screen = pygame.display.set_mode((400, 400))
    count = 1

    x = 10
    y = 10
    clock = pygame.time.Clock()
    
    run = True
    while run:
        clock.tick(30)
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # coords from start to finish
        coordinates = [[5, 5], [80, 230], [230, 230], [380, 50]]
    

        for i in range(len(coordinates)-1):
            pygame.draw.line(screen, (120, 30, 60), (coordinates[i][0], coordinates[i][1]), (coordinates[i+1][0], coordinates[i+1][1]))

        pygame.draw.circle(screen, (0, 0, 0), (x, y), 3)

        value_x = 1
        value_y = 2
        if y != 200:
            x += value_x
            y += value_y
            

        if y > 200:
            x += 1 * value_y
            y += 5 * value_x


        
        pygame.display.flip()



if __name__ == "__main__":
    main()