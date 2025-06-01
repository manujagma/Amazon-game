import pygame
import sys
import random

def run_unlimited_mode(screen, clock):
    # Constants
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    PLAYER_SIZE = 50
    ENEMY_SIZE = 40
    MOTHER_SHIP_SIZE = 100
    ADVANCED_SHIP_SIZE = 70
    BULLET_SIZE = 5
    GAME_SPEED = 5

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    PURPLE = (128, 0, 128)
    ORANGE = (255, 165, 0)

    # Player properties
    player_x = SCREEN_WIDTH // 2 - PLAYER_SIZE // 2
    player_y = SCREEN_HEIGHT - PLAYER_SIZE - 20
    player_speed = 8
    player_bullets = []
    bullet_speed = 10
    shoot_cooldown = 0
    shoot_delay = 15  # Frames between shots

    # Enemy properties
    enemies = []
    enemy_spawn_rate = 60  # Frames between enemy spawns
    enemy_spawn_counter = 0
    enemy_speed = 3

    # Mother ship properties
    mother_ship = None
    mother_ship_health = 10
    mother_ship_speed = 2
    mother_ship_bullets = []
    mother_ship_shoot_cooldown = 0
    mother_ship_shoot_delay = 60  # Frames between shots

    # Advanced ship properties
    advanced_ship = None
    advanced_ship_health = 5
    advanced_ship_speed = 3
    advanced_ship_bullets = []
    advanced_ship_shoot_cooldown = 0
    advanced_ship_shoot_delay = 45  # Frames between shots

    # Game state
    score = 0
    game_over = False
    return_to_menu = False

    # Stars for background
    stars = []
    for _ in range(100):
        stars.append([
            random.randint(0, SCREEN_WIDTH),
            random.randint(0, SCREEN_HEIGHT),
            random.randint(1, 3)  # Star size
        ])

    def draw_player(x, y):
        # Draw player spaceship (triangle shape)
        pygame.draw.polygon(screen, BLUE, [
            (x + PLAYER_SIZE // 2, y),  # Top
            (x, y + PLAYER_SIZE),  # Bottom left
            (x + PLAYER_SIZE, y + PLAYER_SIZE)  # Bottom right
        ])
        # Draw cockpit
        pygame.draw.rect(screen, YELLOW, (x + PLAYER_SIZE // 3, y + PLAYER_SIZE // 2, PLAYER_SIZE // 3, PLAYER_SIZE // 3))
        # Draw engines
        pygame.draw.rect(screen, RED, (x + PLAYER_SIZE // 4, y + PLAYER_SIZE, PLAYER_SIZE // 5, PLAYER_SIZE // 4))
        pygame.draw.rect(screen, RED, (x + PLAYER_SIZE - PLAYER_SIZE // 4 - PLAYER_SIZE // 5, y + PLAYER_SIZE, PLAYER_SIZE // 5, PLAYER_SIZE // 4))

    def draw_enemy(x, y):
        # Draw enemy spaceship (circular with details)
        pygame.draw.circle(screen, RED, (x + ENEMY_SIZE // 2, y + ENEMY_SIZE // 2), ENEMY_SIZE // 2)
        pygame.draw.circle(screen, YELLOW, (x + ENEMY_SIZE // 2, y + ENEMY_SIZE // 2), ENEMY_SIZE // 4)
        # Draw wings
        pygame.draw.rect(screen, RED, (x - ENEMY_SIZE // 4, y + ENEMY_SIZE // 3, ENEMY_SIZE // 4, ENEMY_SIZE // 3))
        pygame.draw.rect(screen, RED, (x + ENEMY_SIZE, y + ENEMY_SIZE // 3, ENEMY_SIZE // 4, ENEMY_SIZE // 3))

    def draw_mother_ship(x, y, health):
        # Draw mother ship body (larger oval shape)
        pygame.draw.ellipse(screen, PURPLE, (x, y, MOTHER_SHIP_SIZE, MOTHER_SHIP_SIZE // 2))
        # Draw dome
        pygame.draw.circle(screen, PURPLE, (x + MOTHER_SHIP_SIZE // 2, y + MOTHER_SHIP_SIZE // 4), MOTHER_SHIP_SIZE // 3)
        # Draw lights
        for i in range(5):
            light_color = YELLOW if i % 2 == 0 else RED
            pygame.draw.circle(screen, light_color, 
                            (x + 20 + i * 15, y + MOTHER_SHIP_SIZE // 2 - 5), 3)
        # Draw health bar
        health_width = (MOTHER_SHIP_SIZE * health) // 10
        pygame.draw.rect(screen, RED, (x, y - 10, MOTHER_SHIP_SIZE, 5))
        pygame.draw.rect(screen, GREEN, (x, y - 10, health_width, 5))

    def draw_advanced_ship(x, y, health):
        # Draw advanced ship body (diamond shape)
        pygame.draw.polygon(screen, ORANGE, [
            (x + ADVANCED_SHIP_SIZE // 2, y),  # Top
            (x + ADVANCED_SHIP_SIZE, y + ADVANCED_SHIP_SIZE // 2),  # Right
            (x + ADVANCED_SHIP_SIZE // 2, y + ADVANCED_SHIP_SIZE),  # Bottom
            (x, y + ADVANCED_SHIP_SIZE // 2)  # Left
        ])
        # Draw center
        pygame.draw.circle(screen, RED, (x + ADVANCED_SHIP_SIZE // 2, y + ADVANCED_SHIP_SIZE // 2), ADVANCED_SHIP_SIZE // 4)
        # Draw weapon ports
        pygame.draw.circle(screen, BLACK, (x + ADVANCED_SHIP_SIZE // 4, y + ADVANCED_SHIP_SIZE // 2), 5)
        pygame.draw.circle(screen, BLACK, (x + ADVANCED_SHIP_SIZE // 2, y + ADVANCED_SHIP_SIZE * 3 // 4), 5)
        pygame.draw.circle(screen, BLACK, (x + ADVANCED_SHIP_SIZE * 3 // 4, y + ADVANCED_SHIP_SIZE // 2), 5)
        # Draw health bar
        health_width = (ADVANCED_SHIP_SIZE * health) // 5
        pygame.draw.rect(screen, RED, (x, y - 10, ADVANCED_SHIP_SIZE, 5))
        pygame.draw.rect(screen, GREEN, (x, y - 10, health_width, 5))

    def draw_bullet(x, y, enemy=False):
        if enemy:
            pygame.draw.rect(screen, RED, (x, y, BULLET_SIZE, BULLET_SIZE * 2))
        else:
            pygame.draw.rect(screen, GREEN, (x, y, BULLET_SIZE, BULLET_SIZE * 2))

    def draw_stars():
        for star in stars:
            pygame.draw.circle(screen, WHITE, (star[0], star[1]), star[2])
            # Move stars down to create scrolling effect
            star[1] += star[2] // 2
            if star[1] > SCREEN_HEIGHT:
                star[1] = 0
                star[0] = random.randint(0, SCREEN_WIDTH)

    def show_score():
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

    def show_game_over():
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Black with alpha
        screen.blit(overlay, (0, 0))
        
        font = pygame.font.SysFont(None, 72)
        game_over_text = font.render("GAME OVER", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 - 86))
        
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Final Score: {score}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
        
        restart_text = font.render("Press R to Try Again", True, WHITE)
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 + 50))
        
        menu_text = font.render("Press M for Main Menu", True, WHITE)
        screen.blit(menu_text, (SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 + 90))

    def reset_game():
        nonlocal player_x, player_y, player_bullets, enemies, score, game_over
        nonlocal mother_ship, mother_ship_bullets, mother_ship_health
        nonlocal advanced_ship, advanced_ship_bullets, advanced_ship_health
        
        player_x = SCREEN_WIDTH // 2 - PLAYER_SIZE // 2
        player_y = SCREEN_HEIGHT - PLAYER_SIZE - 20
        player_bullets = []
        enemies = []
        mother_ship = None
        mother_ship_bullets = []
        mother_ship_health = 10
        advanced_ship = None
        advanced_ship_bullets = []
        advanced_ship_health = 5
        score = 0
        game_over = False

    # Game loop
    while not return_to_menu:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game_over:
                    reset_game()
                if event.key == pygame.K_m and game_over:
                    return_to_menu = True
        
        if not game_over:
            # Player movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_x > 0:
                player_x -= player_speed
            if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - PLAYER_SIZE:
                player_x += player_speed
            if keys[pygame.K_UP] and player_y > 0:
                player_y -= player_speed
            if keys[pygame.K_DOWN] and player_y < SCREEN_HEIGHT - PLAYER_SIZE:
                player_y += player_speed
            
            # Shooting
            if keys[pygame.K_SPACE] and shoot_cooldown <= 0:
                # Create a bullet at the top center of the player's ship
                bullet_x = player_x + PLAYER_SIZE // 2 - BULLET_SIZE // 2
                bullet_y = player_y
                player_bullets.append([bullet_x, bullet_y])
                shoot_cooldown = shoot_delay
            
            if shoot_cooldown > 0:
                shoot_cooldown -= 1
            
            # Move bullets
            for bullet in player_bullets[:]:
                bullet[1] -= bullet_speed
                if bullet[1] < 0:
                    player_bullets.remove(bullet)
            
            # Spawn enemies
            enemy_spawn_counter += 1
            if enemy_spawn_counter >= enemy_spawn_rate:
                enemy_x = random.randint(0, SCREEN_WIDTH - ENEMY_SIZE)
                enemy_y = -ENEMY_SIZE
                enemies.append([enemy_x, enemy_y])
                enemy_spawn_counter = 0
            
            # Move enemies
            for enemy in enemies[:]:
                enemy[1] += enemy_speed
                
                # Remove enemies that go off screen
                if enemy[1] > SCREEN_HEIGHT:
                    enemies.remove(enemy)
            
            # Check if mother ship should appear (score >= 50)
            if score >= 50 and mother_ship is None:
                mother_ship = [SCREEN_WIDTH // 2 - MOTHER_SHIP_SIZE // 2, 50]
            
            # Check if advanced ship should appear (score >= 100)
            if score >= 100 and advanced_ship is None:
                advanced_ship = [SCREEN_WIDTH // 2 - ADVANCED_SHIP_SIZE // 2, 100]
            
            # Mother ship movement and shooting
            if mother_ship:
                # Move mother ship side to side
                mother_ship[0] += mother_ship_speed
                if mother_ship[0] <= 0 or mother_ship[0] + MOTHER_SHIP_SIZE >= SCREEN_WIDTH:
                    mother_ship_speed = -mother_ship_speed
                
                # Mother ship shooting
                mother_ship_shoot_cooldown -= 1
                if mother_ship_shoot_cooldown <= 0:
                    # Create a bullet at the bottom of the mother ship
                    bullet_x = mother_ship[0] + random.randint(0, MOTHER_SHIP_SIZE)
                    bullet_y = mother_ship[1] + MOTHER_SHIP_SIZE // 2
                    mother_ship_bullets.append([bullet_x, bullet_y])
                    mother_ship_shoot_cooldown = mother_ship_shoot_delay
            
            # Advanced ship movement and shooting
            if advanced_ship:
                # Move advanced ship in a pattern (side to side with vertical movement)
                advanced_ship[0] += advanced_ship_speed
                if advanced_ship[0] <= 0 or advanced_ship[0] + ADVANCED_SHIP_SIZE >= SCREEN_WIDTH:
                    advanced_ship_speed = -advanced_ship_speed
                
                # Advanced ship shooting (3 bullets at once)
                advanced_ship_shoot_cooldown -= 1
                if advanced_ship_shoot_cooldown <= 0:
                    # Create 3 bullets from different positions
                    bullet_y = advanced_ship[1] + ADVANCED_SHIP_SIZE
                    # Left bullet
                    advanced_ship_bullets.append([advanced_ship[0] + ADVANCED_SHIP_SIZE // 4, bullet_y])
                    # Center bullet
                    advanced_ship_bullets.append([advanced_ship[0] + ADVANCED_SHIP_SIZE // 2, bullet_y])
                    # Right bullet
                    advanced_ship_bullets.append([advanced_ship[0] + ADVANCED_SHIP_SIZE * 3 // 4, bullet_y])
                    advanced_ship_shoot_cooldown = advanced_ship_shoot_delay
            
            # Move mother ship bullets
            for bullet in mother_ship_bullets[:]:
                bullet[1] += bullet_speed // 2
                if bullet[1] > SCREEN_HEIGHT:
                    mother_ship_bullets.remove(bullet)
            
            # Move advanced ship bullets
            for bullet in advanced_ship_bullets[:]:
                bullet[1] += bullet_speed // 2
                if bullet[1] > SCREEN_HEIGHT:
                    advanced_ship_bullets.remove(bullet)
            
            # Collision detection: bullets hitting enemies
            for bullet in player_bullets[:]:
                for enemy in enemies[:]:
                    if (bullet[0] < enemy[0] + ENEMY_SIZE and
                        bullet[0] + BULLET_SIZE > enemy[0] and
                        bullet[1] < enemy[1] + ENEMY_SIZE and
                        bullet[1] + BULLET_SIZE * 2 > enemy[1]):
                        
                        # Remove both bullet and enemy
                        if bullet in player_bullets:
                            player_bullets.remove(bullet)
                        if enemy in enemies:
                            enemies.remove(enemy)
                        score += 10
                
                # Collision detection: bullets hitting mother ship
                if mother_ship and (bullet[0] < mother_ship[0] + MOTHER_SHIP_SIZE and
                    bullet[0] + BULLET_SIZE > mother_ship[0] and
                    bullet[1] < mother_ship[1] + MOTHER_SHIP_SIZE // 2 and
                    bullet[1] + BULLET_SIZE * 2 > mother_ship[1]):
                    
                    if bullet in player_bullets:
                        player_bullets.remove(bullet)
                    mother_ship_health -= 1
                    
                    # Mother ship destroyed
                    if mother_ship_health <= 0:
                        score += 100
                        mother_ship = None
                        mother_ship_health = 10
                        mother_ship_bullets = []
                
                # Collision detection: bullets hitting advanced ship
                if advanced_ship and (bullet[0] < advanced_ship[0] + ADVANCED_SHIP_SIZE and
                    bullet[0] + BULLET_SIZE > advanced_ship[0] and
                    bullet[1] < advanced_ship[1] + ADVANCED_SHIP_SIZE and
                    bullet[1] + BULLET_SIZE * 2 > advanced_ship[1]):
                    
                    if bullet in player_bullets:
                        player_bullets.remove(bullet)
                    advanced_ship_health -= 1
                    
                    # Advanced ship destroyed
                    if advanced_ship_health <= 0:
                        score += 150
                        advanced_ship = None
                        advanced_ship_health = 5
                        advanced_ship_bullets = []
            
            # Collision detection: player hitting enemies
            for enemy in enemies[:]:
                if (player_x < enemy[0] + ENEMY_SIZE and
                    player_x + PLAYER_SIZE > enemy[0] and
                    player_y < enemy[1] + ENEMY_SIZE and
                    player_y + PLAYER_SIZE > enemy[1]):
                    game_over = True
            
            # Collision detection: player hitting mother ship bullets
            for bullet in mother_ship_bullets[:]:
                if (player_x < bullet[0] + BULLET_SIZE and
                    player_x + PLAYER_SIZE > bullet[0] and
                    player_y < bullet[1] + BULLET_SIZE * 2 and
                    player_y + PLAYER_SIZE > bullet[1]):
                    game_over = True
            
            # Collision detection: player hitting advanced ship bullets
            for bullet in advanced_ship_bullets[:]:
                if (player_x < bullet[0] + BULLET_SIZE and
                    player_x + PLAYER_SIZE > bullet[0] and
                    player_y < bullet[1] + BULLET_SIZE * 2 and
                    player_y + PLAYER_SIZE > bullet[1]):
                    game_over = True
        
        # Drawing
        screen.fill(BLACK)
        
        # Draw stars
        draw_stars()
        
        # Draw bullets
        for bullet in player_bullets:
            draw_bullet(bullet[0], bullet[1])
        
        # Draw mother ship bullets
        for bullet in mother_ship_bullets:
            draw_bullet(bullet[0], bullet[1], enemy=True)
        
        # Draw advanced ship bullets
        for bullet in advanced_ship_bullets:
            draw_bullet(bullet[0], bullet[1], enemy=True)
        
        # Draw enemies
        for enemy in enemies:
            draw_enemy(enemy[0], enemy[1])
        
        # Draw mother ship if it exists
        if mother_ship:
            draw_mother_ship(mother_ship[0], mother_ship[1], mother_ship_health)
        
        # Draw advanced ship if it exists
        if advanced_ship:
            draw_advanced_ship(advanced_ship[0], advanced_ship[1], advanced_ship_health)
        
        # Draw player
        draw_player(player_x, player_y)
        
        # Show score
        show_score()
        
        if game_over:
            show_game_over()
        
        # Update the display
        pygame.display.flip()
        
        # Cap the frame rate
        clock.tick(60)
    
    return score