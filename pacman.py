import pygame
import math

from board import boards

pygame.init()


WIDTH = 900
HEIGHT = 950
PI = math.pi
player_images = []
for i in range(1,5):
    player_images.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'), (45,45)))
blinky_image = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/red.png'), (45,45))
pinky_image = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/pink.png'), (45,45))
inky_image = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/blue.png'), (45,45))
clyde_image = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/orange.png'), (45,45))
spooked_image = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/powerup.png'), (45,45))
dead_image = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/dead.png'), (45,45))


player_x = 450
player_y = 663
direction = 0

blinky_x = 56
blinky_y = 58
blinky_direction = 0

inky_x = 440
inky_y = 388
inky_direction = 2

pinky_x = 440
pinky_y = 438
pinky_direction = 2

clyde_x = 440
clyde_y = 438
clyde_direction = 2

counter = 0
flicker = False
valid_turns = [False, False, False, False]
direction_command = 0
player_speed = 2
score = 0
power = False
power_counter = 0
eaten_ghosts = [False, False, False, False]
targets = [(player_x, player_y), (player_x, player_y), (player_x, player_y), (player_x, player_y)]
blinky_dead = False
inky_dead = False
clyde_dead = False
pinky_dead = False
blinky_box = False
inky_box = False
clyde_box = False
pinky_box = False
ghost_speed = 2






startup_counter = 0
moving = False
lives = 3

screen_padding = HEIGHT - WIDTH

screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf',20)
level = boards
color = 'blue'

class Ghost:
    def __init__(self, x_coord, y_coord, target, speed, img, direct, dead, box, id):
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.center_x = self.x_pos + 22
        self.center_y = self.y_pos + 22
        self.target = target
        self.speed = speed
        self.img = img
        self.direction = direct
        self.dead = dead
        self.in_box = box
        self.id = id
        self.turns, self.in_box = self.check_collisions()
        self.rect = self.draw()
    
    def draw(self):
        if (not power and not self.dead) or (eaten_ghosts[self.id] and power and not self.dead):
            screen.blit(self.img, (self.x_pos, self.y_pos))
        elif power and not self.dead and not eaten_ghosts[self.id]:
            screen.blit(spooked_image, (self.x_pos, self.y_pos))
        else:
            screen.blit(dead_image, (self.x_pos, self.y_pos))
        ghost_rect = pygame.rect.Rect((self.center_x - 18, self.center_y - 18), (36, 36))
        return ghost_rect
    
    def move_clyde(self):
        
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed

        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        
        elif self.direction == 2:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed            
        
        elif self.direction == 3:
            
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed                  
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction          
            
    def check_collisions(self):  
        num1 = ((HEIGHT - 50) // 32)
        num2 = WIDTH // 30
        num3 = 15
        self.turns = [False, False, False, False]
        if self.center_x // 30 < 29:
            if level[(self.center_y - num3) // num1][self.center_x // num2] == 9:
                self.turns[2] = True
            if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                    or level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (self.in_box or self.dead):
                self.turns[1] = True
            if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                    or level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (self.in_box or self.dead):
                self.turns[0] = True
            if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                    or level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (self.in_box or self.dead):
                self.turns[3] = True
            if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                    or level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (self.in_box or self.dead):
                self.turns[2] = True
                
            if self.direction == 2 or self.direction == 3:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                        or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                        or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num2) // num2] < 3 \
                        or (level[self.center_y // num1][(self.center_x - num2) // num2] == 9 and (self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num2) // num2] < 3 \
                        or (level[self.center_y // num1][(self.center_x + num2) // num2] == 9 and (self.in_box or self.dead)):
                        self.turns[0] = True
                
                        
            if self.direction == 0 or self.direction == 1:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                        or (level[(self.center_y + num3) // num1][self.center_x// num2] == 9 and (self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                        or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                        or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                        or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (self.in_box or self.dead)):
                        self.turns[0] = True
        else:
            self.turns[0] = True
            self.turns[1] = True
        if 350 < self.x_pos < 550 and 370 < self.y_pos < 490:
            self.in_box = True
        else:
            self.in_box = False
            
                
        return self.turns, self.in_box

def drawboard(level):
    num1 = ((HEIGHT - screen_padding)// 32)
    num2 = (WIDTH // 30)
    for i in range (len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), WIDTH // 225)
            if level[i][j] == 2 and not flicker:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), WIDTH // 90)
            if level[i][j] == 3:
                pygame.draw.line(screen, color, (j * num2 + (0.5 * num2), i * num1), (j * num2 + (0.5 * num2), i * num1 + num1), WIDTH // 300)
            if level[i][j] == 4:
                pygame.draw.line(screen, color, (j * num2, i * num1 + (0.5 * num1)), (j * num2 + num2, i * num1 + (0.5 * num1)), WIDTH // 300)
            if level[i][j] == 5:
                pygame.draw.arc(screen, color, [(j * num2 - (num2 * 0.4)) - 2, (i * num1 + (0.5 * num1)), num2, num1], 0, PI / 2, WIDTH // 300)
            if level[i][j] == 6:
                pygame.draw.arc(screen, color, [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], PI / 2, PI, WIDTH // 300)
            if level[i][j] == 7:
                pygame.draw.arc(screen, color, [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], PI, 3 * PI / 2, WIDTH // 300)
            if level[i][j] == 8:
                pygame.draw.arc(screen, color, [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1], 3 * PI / 2, 2 * PI, WIDTH // 300)
            if level[i][j] == 9:
                pygame.draw.line(screen, 'white', (j * num2, i * num1 + (0.5 * num1)), (j * num2 + num2, i * num1 + (0.5 * num1)), WIDTH // 300)
            if level[i][j] == 9:
                pygame.draw.line(screen, 'white', (j * num2, i * num1 + (0.5 * num1)), (j * num2 + num2, i * num1 + (0.5 * num1)), WIDTH // 300)

def draw_player():
    #0-RIGHT 1-LEFT 2-UP 3-DOWN
    if direction == 0:
        screen.blit(player_images[counter // 5], (player_x, player_y))
    elif direction == 1:
        screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y))
    elif direction == 2:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x, player_y))
    elif direction == 3:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (player_x, player_y))

def check_position(center_x, center_y):
    valid_turns = [False, False, False, False]
    num1 = ((HEIGHT - screen_padding) // 32)
    num2 = (WIDTH // 30)
    num3 = 15
    #check collisions based on center x and y based on +/- num3
    if center_x // 30 < 29:
        if direction == 0:
            if level[center_y // num1][(center_x - num3) // num2] < 3:
                valid_turns[1] = True
        if direction == 1:
            if level[center_y // num1][(center_x + num3) // num2] < 3:
                valid_turns[0] = True
        if direction == 2:
            if level[(center_y + num3) // num1][center_x // num2] < 3:
                valid_turns[3] = True
        if direction == 3:
            if level[(center_y - num3) // num1][center_x // num2] < 3:
                valid_turns[2] = True
    
        if direction == 2 or direction == 3:
            if 12 <= center_x % num2 <= 18:
                if level[(center_y + num3) // num1][center_x // num2] < 3:
                    valid_turns[3] = True
                if level[(center_y - num3) // num1][center_x // num2] < 3:
                    valid_turns[2] = True
            if 12 <= center_y % num1 <= 18:
                if level[(center_y) // num1][(center_x - num2) // num2] < 3:
                    valid_turns[1] = True
                if level[(center_y) // num1][(center_x + num2) // num2] < 3:
                    valid_turns[0] = True

        if direction == 0 or direction == 1:
            if 12 <= center_x % num2 <= 18:
                if level[(center_y + num3) // num1][center_x // num2] < 3:
                    valid_turns[3] = True
                if level[(center_y - num3) // num1][center_x // num2] < 3:
                    valid_turns[2] = True
            if 12 <= center_y % num1 <= 18:
                if level[(center_y) // num1][(center_x - num3) // num2] < 3:
                    valid_turns[1] = True
                if level[(center_y) // num1][(center_x + num3) // num2] < 3:
                    valid_turns[0] = True


    else:
        valid_turns[0] = True
        valid_turns[1] = True

    return valid_turns

def move_player(player_x, player_y):
    if direction == 0 and valid_turns[0]:
        player_x += player_speed
    elif direction == 1 and valid_turns[1]:
        player_x -= player_speed
    elif direction == 2 and valid_turns[2]:
        player_y -= player_speed
    elif direction == 3 and valid_turns[3]:
        player_y += player_speed
    return player_x, player_y

def check_collisions(score, power, power_counter, eaten_ghosts):
    num1 = (HEIGHT - 50) // 32
    num2 = WIDTH // 30
    if 0 < player_x < 870:
        if level[center_y // num1][center_x // num2] == 1:
            level[center_y // num1][center_x // num2] = 0
            score += 10
        if level[center_y // num1][center_x // num2] == 2:
            level[center_y // num1][center_x // num2] = 0
            score += 50
            power = True
            power_counter = 0
            eaten_ghosts = [False, False, False, False]
            
    return score, power, power_counter, eaten_ghosts

def draw_misc():
    score_text = font.render(f'Score: {score}', True, 'white')
    screen.blit(score_text, (10, 920))
    if power:
        pygame.draw.circle(screen, 'blue', (140, 930), 15)
    for i in range(lives):
        screen.blit(pygame.transform.scale(player_images[0], (30, 30)), (650 + i * 40, 915))

def get_targets(blinky_x, blinky_y, inky_x, inky_y, pinky_x, pinky_y, clyde_x, clyde_y):
    if player_x < 450:
        runaway_x = 900
    else:
        runaway_x = 0
    if player_y < 450:
        runaway_y = 900
    else:
        runaway_y = 0
    return_target = (380, 400)
    if power:
        if not blinky.dead:
            blinky_target = (runaway_x, runaway_y)
        else: 
            blinky_target = return_target
        if not inky.dead:
            inky_target = (runaway_x, player_y)
        else: 
            inky_target = return_target
        if not pinky.dead:
            pinky_target = (player_x, runaway_y)
        else: 
            pinky_target = return_target
        if not clyde.dead:
            clyde_target = (450, 450)
        else: 
            clyde_target = return_target
    else:
        if not blinky.dead:
            if 340 < blinky_x < 560 and 340 < blinky_y < 500:
                blinky_target = (400, 100)
            else: 
                blinky_target = (player_x, player_y)
        else: 
            blinky_target = return_target
        if not inky.dead:
            if 340 < inky_x < 560 and 340 < inky_y < 500:
                inky_target = (400, 100)
            else: 
                inky_target = (player_x, player_y) 
        else: 
            inky_target = return_target   
        if not pinky.dead:
            if 340 < pinky_x < 560 and 340 <  pinky_y < 500:
                pinky_target = (400, 100)
            else: 
                pinky_target = (player_x, player_y)
        else: 
            pinky_target = return_target    
        if not clyde.dead:
            if 340 < clyde_x < 560 and 340 <  clyde_y < 500:
                clyde_target = (400, 100)
            else: 
                clyde_target = (player_x, player_y) 
        else: 
            clyde_target = return_target       
        
    return [blinky_target, inky_target, pinky_target, clyde_target]

run = True
while run:
    timer.tick(fps)
    if counter < 19:
        counter += 1
        if counter > 3:
            flicker = False
    else:
        counter = 0
        flicker = True
    if power and power_counter < 600:
        power_counter += 1
    elif power and power_counter >= 600:
        power_counter = 0
        power = False
        eaten_ghosts = [False, False, False, False]
    if startup_counter < 180:
        moving = False
        startup_counter += 1
    else:
        moving = True    
    
    
    screen.fill('black')
    drawboard(level)
    draw_player()
    blinky = Ghost(blinky_x, blinky_y, targets[0], ghost_speed, blinky_image, blinky_direction, blinky_dead, blinky_box, 0)
    inky = Ghost(inky_x, inky_y, targets[1], ghost_speed, inky_image, inky_direction, inky_dead, inky_box, 1)
    pinky = Ghost(pinky_x, pinky_y, targets[2], ghost_speed, pinky_image, pinky_direction, pinky_dead, pinky_box, 2)
    clyde = Ghost(clyde_x, clyde_y, targets[3], ghost_speed, clyde_image, clyde_direction, clyde_dead, clyde_box, 3)
    draw_misc()
    targets = get_targets(blinky_x, blinky_y, inky_x, inky_y, pinky_x, pinky_y, clyde_x, clyde_y)
    
    center_x = player_x + 23
    center_y = player_y + 24
    valid_turns = check_position(center_x, center_y)
    if moving:
        player_x, player_y = move_player(player_x, player_y)
        blinky_x, blinky_y, blinky_direction = blinky.move_clyde()
        pinky_x, pinky_y, pinky_direction = pinky.move_clyde()
        inky_x, inky_y, inky_direction = inky.move_clyde()
        clyde_x, clyde_y, clyde_direction = clyde.move_clyde()
        
    score, power, power_counter, eaten_ghosts = check_collisions(score, power, power_counter, eaten_ghosts)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction_command = 0
            if event.key == pygame.K_LEFT:
                direction_command = 1
            if event.key == pygame.K_UP:
                direction_command = 2
            if event.key == pygame.K_DOWN:
                direction_command = 3
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and direction_command == 0:
                direction_command = direction
            if event.key == pygame.K_LEFT and direction_command == 1:
                direction_command = direction
            if event.key == pygame.K_UP and direction_command == 2:
                direction_command = direction
            if event.key == pygame.K_DOWN and direction_command == 3:
                direction_command = direction
        
    if direction_command == 0 and valid_turns[0]:
        direction = 0
    if direction_command == 1 and valid_turns[1]:
        direction = 1
    if direction_command == 2 and valid_turns[2]:
        direction = 2
    if direction_command == 3 and valid_turns[3]:
        direction = 3

    if player_x > WIDTH:
        player_x = -47
    elif player_x < -50:
        player_x = WIDTH - 3
    


    pygame.display.flip()
pygame.quit()