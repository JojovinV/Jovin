import pygame
import random
import sys

pygame.init()

screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Dino Game")

clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)

# Dino
dino_rect = pygame.Rect(50, 300, 50, 50)
dino_vel = 0
gravity = 1
jump = -20

# Cactus
cactus_list = []
cactus_speed = 5

# Ground
ground_y = 350

def draw_dino():
    pygame.draw.rect(screen, GREEN, dino_rect)

def draw_cactus(cactus):
    pygame.draw.rect(screen, BROWN, cactus)

def create_cactus():
    height = random.randint(30, 70)
    cactus = pygame.Rect(800, ground_y - height, 30, height)
    cactus_list.append(cactus)

running = True
score = 0

while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and dino_rect.bottom >= ground_y:
                dino_vel = jump

    # Update dino
    dino_vel += gravity
    dino_rect.y += dino_vel
    if dino_rect.bottom > ground_y:
        dino_rect.bottom = ground_y
        dino_vel = 0

    # Update cactus
    for cactus in cactus_list[:]:
        cactus.x -= cactus_speed
        if cactus.right < 0:
            cactus_list.remove(cactus)
            score += 1

    # Create new cactus
    if random.randint(1, 100) == 1:
        create_cactus()

    # Check collision
    for cactus in cactus_list:
        if dino_rect.colliderect(cactus):
            running = False

    # Draw
    draw_dino()
    for cactus in cactus_list:
        draw_cactus(cactus)

    # Draw ground
    pygame.draw.line(screen, BLACK, (0, ground_y), (800, ground_y), 5)

    # Draw score
    font = pygame.font.SysFont(None, 36)
    text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
