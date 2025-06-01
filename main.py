import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Shooter")

# Clock for controlling game speed
clock = pygame.time.Clock()

# Stars for background
stars = []
for _ in range(100):
    stars.append([
        random.randint(0, SCREEN_WIDTH),
        random.randint(0, SCREEN_HEIGHT),
        random.randint(1, 3)  # Star size
    ])

def draw_stars():
    for star in stars:
        pygame.draw.circle(screen, WHITE, (star[0], star[1]), star[2])
        # Move stars down to create scrolling effect
        star[1] += star[2] // 2
        if star[1] > SCREEN_HEIGHT:
            star[1] = 0
            star[0] = random.randint(0, SCREEN_WIDTH)

def draw_menu():
    # Draw title
    font = pygame.font.SysFont(None, 80)
    title_text = font.render("SPACE SHOOTER", True, YELLOW)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - 240, 100))
    
    # Draw buttons
    font = pygame.font.SysFont(None, 50)
    classic_text = font.render("Classic Mode", True, WHITE)
    unlimited_text = font.render("Unlimited Mode", True, WHITE)
    
    # Button backgrounds
    pygame.draw.rect(screen, BLUE, (SCREEN_WIDTH // 2 - 150, 250, 300, 60))
    pygame.draw.rect(screen, RED, (SCREEN_WIDTH // 2 - 150, 350, 300, 60))
    
    # Button text
    screen.blit(classic_text, (SCREEN_WIDTH // 2 - 120, 260))
    screen.blit(unlimited_text, (SCREEN_WIDTH // 2 - 130, 360))

# Main game loop
running = True

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if classic mode button is clicked
            if SCREEN_WIDTH // 2 - 150 <= event.pos[0] <= SCREEN_WIDTH // 2 + 150 and 250 <= event.pos[1] <= 310:
                # Run classic mode directly
                import classic_mode
                classic_mode.run_classic_mode(screen, clock)
            
            # Check if unlimited mode button is clicked
            if SCREEN_WIDTH // 2 - 150 <= event.pos[0] <= SCREEN_WIDTH // 2 + 150 and 350 <= event.pos[1] <= 410:
                # Run unlimited mode directly
                import unlimited_mode
                unlimited_mode.run_unlimited_mode(screen, clock)
    
    # Drawing
    screen.fill(BLACK)
    
    # Draw stars
    draw_stars()
    
    # Draw menu
    draw_menu()
    
    # Update the display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()