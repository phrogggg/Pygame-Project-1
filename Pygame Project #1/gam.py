import pygame
import os
pygame.font.init()
pygame.mixer.init()

#defining the window size
width, height = 900,700
window = pygame.display.set_mode((width, height))

#creating color pressets
WHITE = (255,255,255)
CYAN = (197,245,234)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

#delcaring font type and size
HEALTH_FONT = pygame.font.Font("Doom2016Right-VGz0z.ttf", 40)
WINNER_FONT = pygame.font.Font("Doom2016Right-VGz0z.ttf", 100)

#Naming and creating the game window
pygame.display.set_caption("Doom Eternal")
border = pygame.Rect(0, height//2 , width, 10)

#all sound effects for the marine
marine_damage = pygame.mixer.Sound(os.path.join("sound effects","marine_hit.wav"))
marine_fire = pygame.mixer.Sound(os.path.join("sound effects","marine_fire.wav"))
marine_death = pygame.mixer.Sound(os.path.join("sound effects","marine_death.wav"))

#all sound effects for the icon of sin
icon_of_sin_damage = pygame.mixer.Sound(os.path.join("sound effects","icon_of_sin_hit.wav"))
icon_of_sin_fire = pygame.mixer.Sound(os.path.join("sound effects","icon_of_sin_fire.wav"))
icon_of_sin_death = pygame.mixer.Sound(os.path.join("sound effects","icon_of_sin_death.wav"))
soundtrack = pygame.mixer.Sound(os.path.join("sound effects","soundtrack.mp3"))


#declaring the constant variables
FPS = 60
model_width, model_height = 75, 75
velocity = 10
bullet_vel = 8
max_bullets = 100

#calculating the marine and icon of sin health
marine_hit = pygame.USEREVENT + 1
icon_of_sin_hit = pygame.USEREVENT + 2

#dead marine and icon of sin sprites
dead_sin = pygame.image.load(os.path.join("background assets", "icon of sin gib.png"))
dead_sin = pygame.transform.rotate(pygame.transform.scale(dead_sin,(model_width, model_height)), 360)
dead_marine = pygame.image.load(os.path.join("background assets","icon of sin gib.png"))
dead_marine = pygame.transform.rotate(pygame.transform.scale(dead_marine,(model_width, model_height)), 360)

#marine and icon of sin sprites
marine = pygame.image.load(
    os.path.join("Assets","marine.png"))
marine = pygame.transform.rotate(pygame.transform.scale(marine,(model_width, model_height)), 360)
icon_of_sin = pygame.image.load(
    os.path.join("Assets","icon_of_sin.png"))
icon_of_sin = pygame.transform.rotate(pygame.transform.scale(icon_of_sin,(model_width, model_height)),360)

#background design
level = pygame.image.load(os.path.join("Assets","game_background.png"))

#movement of the marine
def marine_movement(pressed, mar):
    #LEFT
    if pressed[pygame.K_a] and mar.x - velocity > 0: 
        mar.x -= velocity
    #RIGHT
    if pressed[pygame.K_d] and mar.x + velocity + mar.width < border.width: 
        mar.x += velocity
    #UP
    if pressed[pygame.K_w] and mar.y - velocity > 0:
        mar.y -= velocity
    #DOWN
    if pressed[pygame.K_s] and mar.y + velocity + mar.height < height//2: 
        mar.y += velocity

#movement of the icon of sin
def icon_of_sin_movement(pressed, sin):
    #LEFT
    if pressed[pygame.K_LEFT] and sin.x - velocity > border.x + border.height: 
        sin.x -= velocity
    #RIGHT
    if pressed[pygame.K_RIGHT] and sin.x + velocity + sin.width < width: 
        sin.x += velocity
    #UP
    if pressed[pygame.K_UP] and sin.y - velocity > height//2: 
        sin.y -= velocity
    #DOWN
    if pressed[pygame.K_DOWN] and sin.y + velocity + sin.height < height - 15: 
        sin.y += velocity

#creating the bullet travel paths
def handle_bullets(marine_bullets, sin_bullets, mar, sin):
    for bullet in marine_bullets:
        bullet.y -= bullet_vel
        if sin.colliderect(bullet):
            pygame.event.post(pygame.event.Event(marine_hit))
            marine_bullets.remove(bullet)
        elif bullet.x > width:
            marine_bullets.remove(bullet)

    for bullet in sin_bullets:
        bullet.y += bullet_vel
        if mar.colliderect(bullet):
            pygame.event.post(pygame.event.Event(icon_of_sin_hit))
            sin_bullets.remove(bullet)
        elif bullet.x < 0:
            sin_bullets.remove(bullet)

#drawing the bullets, characters and level
def draw(mar, sin, mar_bullets, sin_bullets, icon_of_sin_health, marine_health):
    window.blit(level,(0,0))
    pygame.draw.rect(window, BLACK ,border)
    
    icon_of_sin_health_text = HEALTH_FONT.render("Health: " +str(icon_of_sin_health), 1, WHITE)
    marine_health_text = HEALTH_FONT.render("Health: " +str(marine_health), 1, WHITE)
    
    window.blit(icon_of_sin_health_text, (width - icon_of_sin_health_text.get_width()-10,370))
    window.blit(marine_health_text, (10,10))
    
    window.blit(marine, (mar.x, mar.y))
    window.blit(icon_of_sin, (sin.x, sin.y))
    
    for bullet in mar_bullets:
        pygame.draw.rect(window, YELLOW, bullet)
    for bullet in sin_bullets:
        pygame.draw.rect(window, RED, bullet)
    pygame.display.update()

#draws winner text
def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    window.blit(draw_text, (width/2-draw_text.get_width()/2, height/2-draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

#main function
def main():
    #plays soundtrack and spawns in character
    soundtrack.play()
    mar = pygame.Rect(400, 100, model_width, model_height)
    sin = pygame.Rect(400, 500, model_width, model_height)
    
    mar_bullets = []
    sin_bullets = []
    marine_health = 10
    icon_of_sin_health = 10
    
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run == False
                pygame.quit()
            
            #handling the bullet firing and creates a sound effect per shot
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(mar_bullets) < max_bullets:
                    bullet = pygame.Rect(mar.x + 25, mar.y + mar.height//2 - 2, 5, 10)
                    mar_bullets.append(bullet)
                    marine_fire.play()
                if event.key == pygame.K_RCTRL and len(sin_bullets) < max_bullets:
                    bullet = pygame.Rect(sin.x + 30, sin.y + sin.height//2 - 2, 5, 10)
                    sin_bullets.append(bullet)
                    icon_of_sin_fire.play()
            
            #executes if the icon of sit is hit and plays a damage sound
            if event.type == icon_of_sin_hit:
                icon_of_sin_health -= 1
                icon_of_sin_damage.play()

            #executes if the marine is hit and plays a damage sound
            if event.type == marine_hit:
                marine_health -= 1
                marine_damage.play()
            
            #empty string that executes if the value is changed
            victory = ""
            #executes if the marine wins
            if icon_of_sin_health <= 0:
                victory = "Marine wins!"
                icon_of_sin_death.play()
                window.blit(icon_of_sin,(-700,-700))
                window.blit(dead_sin,(sin.x,sin.y))
                
            #draws if the icon of sin wins
            if marine_health <= 0:
                victory = "The Icon of Sin wins!"
                marine_death.play() 
                window.blit(marine,(-700,-700))    
                window.blit(dead_marine,(mar.x,mar.y))
           
            #executes when someone wins
            if victory != "":
                draw_winner(victory)
                break

        pressed = pygame.key.get_pressed()
        #calling the functions
        icon_of_sin_movement(pressed, sin)
        marine_movement(pressed, mar)
        handle_bullets(sin_bullets, mar_bullets, sin, mar)
        draw(mar, sin, mar_bullets, sin_bullets, icon_of_sin_health, marine_health)
    
    main()

if __name__ == "__main__":
    main()