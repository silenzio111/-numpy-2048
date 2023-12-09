import pygame 
import random as rd

#init
pygame.init()
screen = pygame.display.set_mode((720,720))
clock  = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        print("up")
        pass
    if keys[pygame.K_DOWN]:
        pass
    if keys[pygame.K_LEFT]:
        pass
    if keys[pygame.K_RIGHT]:
        pass   
        
        
        
        
    screen.fill("white")
    
    pygame.display.flip()
    
    clock.tick(60)
    
pygame.quit()