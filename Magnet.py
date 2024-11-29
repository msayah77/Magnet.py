import pygame
import random
import sys

pygame.init()

# Initialize screen dimensions and colors
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Coin Catch Game")

# Load and scale images
coin_image = pygame.image.load("Coin.png")
coin_image = pygame.transform.scale(coin_image, (50, 50))

magnet_image = pygame.image.load("Magnet.png")
magnet_image = pygame.transform.scale(magnet_image, (80, 80))

background_image = pygame.image.load("Sky.jpg")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

ribbit_sound = pygame.mixer.Sound("COINN.wav") # Sound effect

pygame.mixer.music.load("triple_bubble_music_-_world_1_forest.wav")  #  Background music
pygame.mixer.music.play(-1, 0.0) # Loop the music indefinitely

# Timer
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()
GAME_TIME = 10  

# Define the Coin class
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = coin_image
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
         # Randomly position and rotate the coin
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)
        self.angle = random.randint(-45, 45)
        self.image = pygame.transform.rotate(coin_image, self.angle)

    def update(self):
        # Move the coin and make it reappear on the opposite side if it goes off-screen
        self.rect.x += 2  
        if self.rect.right > SCREEN_WIDTH:
            self.rect.left = 0
        elif self.rect.left < 0:
            self.rect.right = SCREEN_WIDTH
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.top = 0
        elif self.rect.top < 0:
            self.rect.bottom = SCREEN_HEIGHT

# Define the Magnet 
class Magnet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = magnet_image
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.speed = 8

    def update(self, keys):
         # Move the magnet based on user input
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.image = pygame.transform.rotate(magnet_image, 10)  
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
            self.image = pygame.transform.rotate(magnet_image, -10)  
        if keys[pygame.K_UP] and self.rect.top > 0: 
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:  
            self.rect.y += self.speed


# Create the game objects
magnet = Magnet()
coins = pygame.sprite.Group()

# Add 3 coins to the game
for _ in range(3):
    coins.add(Coin())

# Sprites
all_sprites = pygame.sprite.Group(magnet, *coins)

# Score and start time
score = 0
start_ticks = pygame.time.get_ticks()

# Main game loop
def main():
    global score
    running = True

    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()

        
        keys = pygame.key.get_pressed()
        magnet.update(keys)
        coins.update()

        
        collisions = pygame.sprite.spritecollide(magnet, coins, True)  
        for coin in collisions:
            ribbit_sound.play()
            score += 1
            # Add a new coin after a collision
            new_coin = Coin()
            coins.add(new_coin)
            all_sprites.add(new_coin)

        
        time_left = GAME_TIME - (pygame.time.get_ticks() - start_ticks) / 1000
        if time_left <= 0:
            running = False # End the game if time runs out

        
        screen.blit(background_image, (0, 0))
        all_sprites.draw(screen)

        
        score_text = font.render(f"Score: {score}", True, WHITE)
        timer_text = font.render(f"Time Left: {max(0, int(time_left))}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(timer_text, (SCREEN_WIDTH - 200, 10))

        
        pygame.display.flip()
        clock.tick(60)

    
    game_over()


def game_over():
    global score
    screen.fill(BLACK)
    game_over_text = font.render("Game Over", True, WHITE)
    final_score_text = font.render(f"Your Score: {score}", True, WHITE)
    restart_text = font.render("Press R to Restart or Q to Quit", True, WHITE)

    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 60))
    screen.blit(final_score_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 + 60))

    pygame.display.flip()

    # Wait for user input to restart or quit
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()


def reset_game():
    global score, start_ticks
    score = 0
    start_ticks = pygame.time.get_ticks()
    main()


if __name__ == "__main__":
    main()
