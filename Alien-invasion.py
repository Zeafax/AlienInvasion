import pygame
import sys
import random
import pickle  

def display_player():
    screen.blit(player_surface,player_rect)

def powerup(enemy):
    a = random.randint(1,10)
    b = random.randint(1,5)
    if a ==10 and gun_delay_value > 10:
        return firing_speed(enemy)
    elif b == 5:
        firing_power(enemy)

def firing_speed(enemy):
    speed_rect = speed_surface.get_rect(center = (enemy.centerx,enemy.centery))
    new_speed = [speed_surface,speed_rect]
    powerup_list.append(new_speed)

def firing_power(enemy):
    power_rect = power_surface.get_rect(center = (enemy.centerx,enemy.centery))
    new_power = [power_surface,power_rect]
    powerup_list.append(new_power)

def display_powerups():
    for powerup in powerup_list:
        screen.blit(powerup[0],powerup[1])

def powerups_movement():
    for power in powerup_list:
        power[1].centery +=1

def gun_sound():
    gun_sound = pygame.mixer.Sound("assets/sounds/laser.wav")
    gun_sound.set_volume(0.5)
    gun_sound.play()

def explosion_sound():
    explosion_sound = pygame.mixer.Sound("assets/sounds/explosion-distant.wav")
    explosion_sound.set_volume(1)
    explosion_sound.play()

def spawn_bullet():
    bullet_x1 = player_rect.centerx + 20
    bullet_x2 = player_rect.centerx - 20
    new_bullet1 = bullet_surface.get_rect(center=(bullet_x1,player_rect.centery-40))
    new_bullet2 = bullet_surface.get_rect(center=(bullet_x2,player_rect.centery-40))
    bullet1 = [new_bullet1,bullet_health]
    bullet2 = [new_bullet2,bullet_health]
    return bullet1, bullet2

def spawn_enemy_bullet(enemy): 
    bullet_x = enemy.centerx
    bullet_y = enemy.centery + 40
    enemy_bullet_rect = enemy_bullet_surface1.get_rect(center=(bullet_x, bullet_y))
    new_enemy_bullet = [enemy_bullet_rect, 0]
    enemy_bullet_list.append(new_enemy_bullet)


def enemy_bullet_explosion(enemy_bullet):
    bullet_explosion_x = enemy_bullet.centerx
    bullet_explosion_y = enemy_bullet.centery
    enemy_bullet_explosion_rect = enemy_bullet__explosion_surface1.get_rect(center=(bullet_explosion_x, bullet_explosion_y))
    new_bullet_explosion = [enemy_bullet_explosion_rect, 0]
    enemy_bullet_explosion_list.append(new_bullet_explosion)

def easter_egg():
    global player_surface
    x = player_rect.centerx
    y = player_rect.centery
    if x < 60 and y > 845 : 
        player_surface = pygame.transform.scale(pygame.image.load("assets/img/N/O/T/H/I/N/G/HERE.png").convert_alpha(), (96, 108))

def bullet_movement(bullets, enemy_bullets):
    for bullet in bullets:
        if bullet[0].centery < 0:
            bullet_list.remove(bullet)
        bullet[0].centery  -= 8
    for enemy_bullet in enemy_bullets:
        if enemy_bullet[0].centery > 1080:
            enemy_bullet_list.remove(enemy_bullet)
        enemy_bullet[0].centery  += 4

def display_bullets(bullets,enemy_bullets):
    for bullet in bullets:
        screen.blit(bullet_surface,bullet[0])

    for enemy_bullet in enemy_bullets:
        screen.blit(enemy_bullet_frames[enemy_bullet[1]],enemy_bullet[0])

def enemy_bullet_animation():
    for enemy_bullet in enemy_bullet_list:
        enemy_bullet[1] +=1
        if enemy_bullet[1] <=4:
            new_enemy_bullet = enemy_bullet_frames[enemy_bullet[1]]    
            new_enemy_bullet_rect = new_enemy_bullet.get_rect(center=(enemy_bullet[0].centerx, enemy_bullet[0].centery))
            enemy_bullet[0] = new_enemy_bullet_rect 
        else:
            enemy_bullet_list.remove(enemy_bullet)

def check_collision(enemies,bullets,enemy_bullets):
    global score, game_active, player_lives, gun_delay_value, bullet_health
    dead = False
    for enemy in enemies:
        if enemy[0].centery > 1000:
            enemy_list.remove(enemy)
            player_lives -=1

        if enemy[0].centery == 100 and enemy[2]:
            enemy[2] = False
            spawn_enemy_bullet(enemy[0])

        if player_rect.colliderect(enemy[0]):
            player_lives =0
            game_active = False

        for bullet in bullets:
            if bullet[0].colliderect(enemy[0]):
                for i in range(bullet[1]):
                    enemy[1] -=1
                    bullet[1] -=1
                    if enemy[1] == 0:
                        powerup(enemy[0])
                        enemy_list.remove(enemy)
                        spawn_explosion(enemy[0])
                        dead = True
                        score +=1
                        break
                if bullet[1] == 0:
                    bullet_list.remove(bullet)
                if dead:
                    break

    for enemy_bullet in enemy_bullets:     
        if enemy_bullet[0].colliderect(player_rect):
            player_lives -=1
            explosion_sound()
            enemy_bullet_explosion(enemy_bullet[0])
            enemy_bullet_list.remove(enemy_bullet)
            break

        for bullet in bullets:
            if enemy_bullet[0].colliderect(bullet[0]):
                enemy_bullet_explosion(enemy_bullet[0])
                enemy_bullet_list.remove(enemy_bullet)
                bullet_list.remove(bullet)
                explosion_sound()  
                break  
    for powerUp in powerup_list:
        if powerUp[1].centery > 1000:
            powerup_list.remove(powerUp)
        if player_rect.colliderect(powerUp[1]):
            if powerUp[0] == speed_surface:
                if gun_delay_value > 10:
                    gun_delay_value -=5
                powerup_list.remove(powerUp)

            elif powerUp[0] == power_surface:
                bullet_health +=1
                powerup_list.remove(powerUp)

def spawn_enemy():# [rect, health, ammo-avalible]
    global enemy_x_spawn
    if len(enemy_x_spawn) == 0:
        enemy_x_spawn = [225,375,525,655,805,960,1095,1245,1395,1545,1695]
    random_enemy_spawn = random.choice(enemy_x_spawn)
    enemy_x_spawn.remove(random_enemy_spawn)
    new_enemy = enemy_surface.get_rect(midbottom=(random_enemy_spawn, 0))
    enemy = [new_enemy,enemy_health, True]
    return enemy

def enemy_movement(enemies):
    global enemy_move
    if enemy_move == True:
        for enemy in enemies:
            enemy[0].centery += 1
        enemy_move = False
    else:
        enemy_move = True
    return enemies

def display_enemies(enemies):
    for enemy in enemies:
        screen.blit(enemy_surface,enemy[0])

def spawn_explosion(enemy): #[surface, rect, animation-index]
    explosion_rect = explosion_surface1.get_rect(center = (enemy.centerx,enemy.centery))
    new_explosion = [explosion_surface1,explosion_rect,0]
    enemy_explosion_list.append(new_explosion)
    explosion_sound()

def enemy_explosion_animation():# [surface,rect,index]
    for explosion in enemy_explosion_list:
        if explosion[2] <6:
            explosion[2] += 1
            new_explosion = explosion_frames[explosion[2]]    
            new_explosion_rect = new_explosion.get_rect(center=(explosion[1].centerx, explosion[1].centery))
            explosion[0] = new_explosion 
            explosion[1] = new_explosion_rect
        else:
            enemy_explosion_list.remove(explosion)

def enemy_bullet_explosion_animation(): #[rect, animation-index]
    for bullet_explosion in enemy_bullet_explosion_list:
        if bullet_explosion[1] < 9:
            bullet_explosion[1] += 1
            new_bullet_explosion = enemy_bullet_explosion_frames[bullet_explosion[1]]    
            new_bullet_explosion_rect = new_bullet_explosion.get_rect(center=(bullet_explosion[0].centerx, bullet_explosion[0].centery))
            bullet_explosion[0] = new_bullet_explosion_rect 
        else:
            enemy_bullet_explosion_list.remove(bullet_explosion)

def display_explsions():
    for explosion in enemy_explosion_list:
        screen.blit(explosion[0],explosion[1])
    for bullet_explosion in enemy_bullet_explosion_list:
        screen.blit(enemy_bullet_explosion_frames[bullet_explosion[1]],bullet_explosion[0])

def display_score():
    score_surface = game_font.render(f"Score: {int(score)}",True,(0,255,220))
    score_rect = score_surface.get_rect(center = (960,100))
    screen.blit(score_surface,score_rect)

    level_surface = small_game_font.render(f"Level: {int(game_level)}",True,(0,255,220))
    level_rect = level_surface.get_rect(center = (95,40))
    screen.blit(level_surface,level_rect)

def display_player_stats():
    lives_surface = small_game_font.render(f"Lives: {int(player_lives)}",True,(0,255,220))
    lives_rect = lives_surface.get_rect(center = (1780,40))
    screen.blit(lives_surface,lives_rect)

    power_surface = small_game_font.render(f"power: {int(bullet_health)}",True,(0,255,220))
    power_rect = power_surface.get_rect(center = (1780,100))
    screen.blit(power_surface,power_rect)

    fire_rate = 12-gun_delay_value/5
    if fire_rate <10:
        firing_speed_surface = small_game_font.render(f"Fire rate: {int(fire_rate)}",True,(0,255,220))
        firing_speed_rect = firing_speed_surface.get_rect(center = (1780,160))
        screen.blit(firing_speed_surface,firing_speed_rect)
    else:
        firing_speed_surface = small_game_font.render("Fire rate: MAX",True,(0,255,220))
        firing_speed_rect = firing_speed_surface.get_rect(center = (1780,160))
        screen.blit(firing_speed_surface,firing_speed_rect)

def display_warning():
    Warning_BG = pygame.transform.scale(pygame.image.load("assets/img/WarningBG.png").convert_alpha(), (400,400))
    Warning_BG_rect = Warning_BG.get_rect(center = (960,540))
    screen.blit(Warning_BG,Warning_BG_rect)

    warning_surface= small_game_font.render("Are you sure?",True,(255,0,0))
    warning_rect = warning_surface.get_rect(center = (960,400))
    screen.blit(warning_surface,warning_rect)
    #warning selection
    
    screen.blit(choice_text_surface_YES,choice_text_rect_YES)

    screen.blit(choice_text_surface_NO,choice_text_rect_NO)

    screen.blit(choice_selection_surface_YES,choice_rect_YES)

    screen.blit(choice_selection_surface_NO,choice_rect_NO)

def display_pause():
    if player_lives > 0:
        pause_surface= game_font.render("<Alien Invasion>",True,(0,255,220))
        pause_rect = pause_surface.get_rect(center = (960,250))
        screen.blit(pause_surface,pause_rect)
    else:
        pause_surface= game_font.render("Game over",True,(0,255,220))
        pause_rect = pause_surface.get_rect(center = (960,400))
        screen.blit(pause_surface,pause_rect)

    if player_lives > 0:
        screen.blit(continue_surface,continue_rect)

    screen.blit(restart_surface,restart_rect)

    screen.blit(ESC_surface,ESC_rect)
    high_score_text = f"High score: {high_score[0]},   lvl {high_score[1]}"
    score_surface = game_font.render(high_score_text,True,(0,255,220))
    score_rect = score_surface.get_rect(center = (960,900))
    screen.blit(score_surface,score_rect)

    #controls
    screen.blit(Controls_Surface,(10,500))
    
def save_high_score():
    with open ("assets/high_score_save.dat", "wb") as myFile:
        pickle.dump(high_score, myFile)   

pygame.init()
pygame.display.set_caption('Alien Invasion')
flags = pygame.SCALED | pygame.FULLSCREEN
screen = pygame.display.set_mode((1920, 1080))

clock = pygame.time.Clock()
game_font = pygame.font.Font("assets/Edge.otf",120)
small_game_font = pygame.font.Font("assets/Edge.otf",50)
pygame.mixer.music.load("assets/sounds/BG_Music.mp3")
pygame.mixer.music.play(-1, 0.0)
pygame.mouse.set_visible(True)
# Game Variables
exit = False
restart = False
player_lives = 3
game_level = 1
gun = False
gun_delay_value = 55
gun_delay = gun_delay_value 

enemy_move = True
spawn_rate = 2500
player_movement = 0

player_strafe_left = 0
player_strafe_right = 0
player_strafe_up = 0
player_strafe_down = 0
player_shift = 1
bullet_health = 1
enemy_health = 1
enemy_health_increase = 2
game_active = False
score = 0
popup = False
try:
    with open('assets/high_score_save.dat', 'rb') as myFile:
        high_score = pickle.load(myFile)
except:
    high_score = [0,1]
#Background
bgSurface = pygame.image.load("assets/img/BG2.png").convert()  # .convert() gör att bilden tar mindre belasting för pygame

#Pause Screen
PauseSurface = pygame.image.load("assets/img/PauseBG.png").convert_alpha()

#Controls
Controls_Surface = pygame.transform.scale(pygame.image.load("assets/img/controls.png").convert_alpha(), (512, 512))

#Player
player_surface = pygame.transform.scale(pygame.image.load("assets/img/frame-0.png").convert_alpha(), (96, 108))

player_rect = player_surface.get_rect(midbottom=(960, 900))
speed_surface = pygame.transform.scale(pygame.image.load("assets/img/Faster-gun.png").convert_alpha(), (64, 60))
power_surface =pygame.transform.scale(pygame.image.load("assets/img/Energy_Ammo.png").convert_alpha(), (64, 60))

powerup_list = []

bullet_surface = pygame.image.load("assets/img/bullet.png").convert_alpha()
bullet_list = []

EXPLOSIONANIMATION = pygame.USEREVENT
pygame.time.set_timer(EXPLOSIONANIMATION, 100)

ENEMYBULLETANIMATION = pygame.USEREVENT +3
pygame.time.set_timer(ENEMYBULLETANIMATION, 400)

# enemy
enemy_x_spawn = [225,375,525,655,805,960,1095,1245,1395,1545,1695]
enemy_surface = pygame.transform.scale(pygame.image.load("assets/img/Ship2.1.png").convert_alpha(), (102, 231))
enemy_list = []

explosion_surface1 = pygame.transform.scale(pygame.image.load("assets/explosion/shot4_exp2.png").convert_alpha(), (int(150*1.5), int(172*1.5)))
explosion_surface2 = pygame.transform.scale(pygame.image.load("assets/explosion/shot4_exp3.png").convert_alpha(), (int(150*1.5), int(172*1.5)))
explosion_surface3 = pygame.transform.scale(pygame.image.load("assets/explosion/shot4_exp4.png").convert_alpha(), (int(150*1.5), int(172*1.5)))
explosion_surface4 = pygame.transform.scale(pygame.image.load("assets/explosion/shot4_exp5.png").convert_alpha(), (int(150*1.5), int(172*1.5)))
explosion_surface5 = pygame.transform.scale(pygame.image.load("assets/explosion/shot4_exp6.png").convert_alpha(), (int(150*1.5), int(172*1.5)))
explosion_surface6 = pygame.transform.scale(pygame.image.load("assets/explosion/shot4_exp7.png").convert_alpha(), (int(150*1.5), int(172*1.5)))
explosion_surface7 = pygame.transform.scale(pygame.image.load("assets/explosion/shot4_exp8.png").convert_alpha(), (int(150*1.5), int(172*1.5)))
explosion_frames = [explosion_surface1, explosion_surface2, explosion_surface3, explosion_surface4, explosion_surface5, explosion_surface6, explosion_surface7]
enemy_explosion_list = []
ENEMYSPAWN = pygame.USEREVENT +1
pygame.time.set_timer(ENEMYSPAWN,spawn_rate)
HEALTHINCREASE = pygame.USEREVENT +2
pygame.time.set_timer(HEALTHINCREASE,15000)

#enemy bullets
enemy_bullet_surface1 = pygame.transform.scale2x(pygame.image.load("assets/enemy_bullet/shot_1.png").convert_alpha())
enemy_bullet_surface2 = pygame.transform.scale2x(pygame.image.load("assets/enemy_bullet/shot_2.png").convert_alpha())
enemy_bullet_surface3 = pygame.transform.scale2x(pygame.image.load("assets/enemy_bullet/shot_3.png").convert_alpha())
enemy_bullet_surface4 = pygame.transform.scale2x(pygame.image.load("assets/enemy_bullet/shot_4.png").convert_alpha())
enemy_bullet_surface5 = pygame.transform.scale2x(pygame.image.load("assets/enemy_bullet/shot_5.png").convert_alpha())

enemy_bullet_frames = [enemy_bullet_surface1, enemy_bullet_surface2, enemy_bullet_surface3, enemy_bullet_surface4, enemy_bullet_surface5]
enemy_bullet_list = []

#enemy bullet explosion
enemy_bullet__explosion_surface1 = pygame.transform.scale2x(pygame.image.load("assets/enemy_bullet/shot6_exp1.png").convert_alpha())
enemy_bullet__explosion_surface2 = pygame.transform.scale2x(pygame.image.load("assets/enemy_bullet/shot6_exp2.png").convert_alpha())
enemy_bullet__explosion_surface3 = pygame.transform.scale2x(pygame.image.load("assets/enemy_bullet/shot6_exp3.png").convert_alpha())
enemy_bullet__explosion_surface4 = pygame.transform.scale2x(pygame.image.load("assets/enemy_bullet/shot6_exp4.png").convert_alpha())
enemy_bullet__explosion_surface5 = pygame.transform.scale2x(pygame.image.load("assets/enemy_bullet/shot6_exp5.png").convert_alpha())
enemy_bullet__explosion_surface6 = pygame.transform.scale2x(pygame.image.load("assets/enemy_bullet/shot6_exp6.png").convert_alpha())
enemy_bullet__explosion_surface7 = pygame.transform.scale2x(pygame.image.load("assets/enemy_bullet/shot6_exp7.png").convert_alpha())
enemy_bullet__explosion_surface8 = pygame.transform.scale2x(pygame.image.load("assets/enemy_bullet/shot6_exp8.png").convert_alpha())
enemy_bullet__explosion_surface9 = pygame.transform.scale2x(pygame.image.load("assets/enemy_bullet/shot6_exp9.png").convert_alpha())
enemy_bullet__explosion_surface10 = pygame.transform.scale2x(pygame.image.load("assets/enemy_bullet/shot6_exp10.png").convert_alpha())

enemy_bullet_explosion_frames = [enemy_bullet__explosion_surface1, enemy_bullet__explosion_surface2, enemy_bullet__explosion_surface3, 
enemy_bullet__explosion_surface4, enemy_bullet__explosion_surface5, enemy_bullet__explosion_surface6, enemy_bullet__explosion_surface7,
enemy_bullet__explosion_surface8, enemy_bullet__explosion_surface9, enemy_bullet__explosion_surface10]
enemy_bullet_explosion_list=[]

#pause surfaces are loaded here with rectangles
continue_surface= game_font.render("<Press P to continue>",True,(0,255,220))
continue_rect = continue_surface.get_rect(center = (960,400))

choice_text_surface_YES = small_game_font.render("YES",True,(255,0,0))
choice_text_rect_YES = choice_text_surface_YES.get_rect(center = (890,500))

choice_text_surface_NO = small_game_font.render("NO",True,(255,0,0))
choice_text_rect_NO = choice_text_surface_NO.get_rect(center = (1045,500))

choice_selection_surface_YES = small_game_font.render("<Enter>",True,(255,0,0))
choice_rect_YES = choice_selection_surface_YES.get_rect(center = (890,550))

choice_selection_surface_NO = small_game_font.render("<ESC>",True,(255,0,0))
choice_rect_NO = choice_selection_surface_NO.get_rect(center = (1045,550))

restart_surface= small_game_font.render("<Press R to restart>",True,(0,255,220))
restart_rect = restart_surface.get_rect(center = (960,500))

ESC_surface= small_game_font.render("<Press ESC to quit>",True,(0,255,220))
ESC_rect = ESC_surface.get_rect(center = (960,560))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_high_score()
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN: 
            if event.button == 1 and game_active:
                gun = True
            if not game_active:
                if choice_text_rect_YES.collidepoint(event.pos) and popup or choice_rect_YES.collidepoint(event.pos) and popup: 
                    if exit:
                        save_high_score()
                        pygame.quit()
                        sys.exit()
                    if restart:
                        save_high_score()
                        restart = False
                        spawn_rate = 2500
                        bullet_health = 1
                        score = 0
                        game_level = 0
                        enemy_list.clear()
                        bullet_list.clear()
                        enemy_bullet_list.clear()
                        player_rect.midbottom = (960, 900)
                        game_active = True
                        player_lives = 3
                        restart = False
                        gun_delay_value = 55
                        powerup_list.clear()
                        enemy_health = 1 
                        enemy_health_increase = 2
                        popup = False               
                elif choice_text_rect_NO.collidepoint(event.pos) and popup or choice_rect_NO.collidepoint(event.pos) and popup:
                    if exit:
                        exit = False
                    if restart:
                        restart = False
                    popup = False
                elif continue_rect.collidepoint(event.pos) and not popup:
                    if player_lives > 0:
                        game_active = True
                elif restart_rect.collidepoint(event.pos) and not popup:
                    restart = True
                    popup = True
                elif ESC_rect.collidepoint(event.pos) and not popup:
                    exit = True
                    popup = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and game_active:
                gun = False    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game_active == True:
                    game_active = False
                elif restart:
                    restart = False
                    popup = False
                elif not exit:
                    exit = True
                    popup = True
                elif exit:
                    exit = False
                    popup = False
            if event.key == pygame.K_z:
                easter_egg()    
            if event.key == pygame.K_p:
                if game_active == True:
                    game_active =False
                elif player_lives > 0:
                    game_active = True
            elif event.key == pygame.K_RETURN :
                if exit:
                    save_high_score()
                    pygame.quit()
                    sys.exit()
                if restart:
                    save_high_score()
                    restart = False
                    spawn_rate = 2500
                    bullet_health = 1
                    score = 0
                    game_level = 0
                    enemy_list.clear()
                    bullet_list.clear()
                    enemy_bullet_list.clear()
                    player_rect.midbottom = (960, 900)
                    game_active = True
                    player_lives = 3
                    restart = False
                    gun_delay_value = 55
                    powerup_list.clear()
                    enemy_health = 1 
                    enemy_health_increase = 2
                    popup = False    
            elif event.key == pygame.K_r and not game_active:
                restart = True
                popup = True
            if event.key == pygame.K_SPACE:
                gun = True

            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player_strafe_left = -5
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player_strafe_right = 5
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                player_strafe_up = -5
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player_strafe_down = 5
            if event.key == pygame.K_LSHIFT:
                player_shift = 1.4
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                gun = False
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player_strafe_left = 0
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player_strafe_right = 0
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                player_strafe_up = 0
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player_strafe_down = 0
            if event.key == pygame.K_LSHIFT:
                player_shift = 1
        if event.type == EXPLOSIONANIMATION and game_active:
            if len(enemy_explosion_list) > 0:
                enemy_explosion_animation()
            if len(enemy_bullet_explosion_list) > 0:
                enemy_bullet_explosion_animation()
        if event.type == ENEMYBULLETANIMATION and game_active:
            enemy_bullet_animation()
        if event.type == ENEMYSPAWN and game_active:
            enemy_list.append(spawn_enemy())
        if event.type == HEALTHINCREASE and game_active:
            enemy_health += enemy_health_increase
            enemy_health_increase += 1 
            game_level +=1
            if high_score[1] < game_level:
                high_score[1] = game_level

    #background
    screen.blit(bgSurface, (0, 0))
    if game_active:
        pygame.mouse.set_visible(False)
        if score> high_score[0]:
            high_score[0] = score
        # player
        if player_rect.centerx >= 60:
            player_rect.centerx += player_strafe_left * player_shift
        if player_rect.centerx <= 1860:
            player_rect.centerx += player_strafe_right * player_shift
        if player_rect.centery >= 80:
            player_rect.centery += player_strafe_up * player_shift
        if player_rect.centery <= 845:
            player_rect.centery += player_strafe_down * player_shift
        if player_lives <1:
            game_active = False

        if gun_delay >0:
            gun_delay -=1
        if gun:
            if gun_delay <= 0:
                a,b=spawn_bullet()
                bullet_list.append(a)
                bullet_list.append(b)
                gun_sound()
                gun_delay = gun_delay_value

        check_collision(enemy_list, bullet_list, enemy_bullet_list)
        display_powerups()
        display_player()
        display_score()
        display_player_stats()
        bullet_movement(bullet_list, enemy_bullet_list)
        display_bullets(bullet_list, enemy_bullet_list)
        # enemies
        enemy_list = enemy_movement(enemy_list)
        display_enemies(enemy_list)
        powerups_movement()
        display_explsions()
    else:
        pygame.mouse.set_visible(True)
        display_enemies(enemy_list)
        display_explsions()
        display_player()
        display_player_stats()
        display_powerups()
        display_bullets(bullet_list, enemy_bullet_list)
        screen.blit(PauseSurface, (0, 0))
        display_pause()
        display_score()
        if exit or restart:
            display_warning()

    pygame.display.update()
    clock.tick(120)