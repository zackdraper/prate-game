import pygame
import random
import numpy as np
from pygame.locals import *
import pygame.mixer as mixer

width_buffer = 100
height_buffer = 0

screen_width = 1024
screen_height = 768

CANNON_BALLS = pygame.sprite.Group()
SMOKE = pygame.sprite.Group()
EXPLO = pygame.sprite.Group()

mixer.init()
sound_cannon_fire = mixer.Sound('sounds/cannon_shot.mp3')
sound_cannon_fire.set_volume(0.9)

sound_cannon_hit = mixer.Sound('sounds/cannon_hit.mp3')
sound_cannon_hit.set_volume(0.8)

cannon_fire_smoke = pygame.image.load('images/smoke_cannon.png')
cannon_fire_smoke = pygame.transform.scale(cannon_fire_smoke, (15,30))
cannon_fire_smoke = pygame.transform.rotate(cannon_fire_smoke, 0)

cannon_fire_explo = pygame.image.load('images/explosion.png')
cannon_fire_explo = pygame.transform.scale(cannon_fire_explo, (42,28))

class PlayerShip(pygame.sprite.Sprite):
    def __init__(self, x0, y0, angle, name):
        super(PlayerShip, self).__init__()
        image = pygame.image.load('images/ship.png').convert()

        image = pygame.transform.rotate(image, -90)
        image.set_colorkey((255, 255, 255), RLEACCEL)
        self.image_original = image
        self.image = self.image_original
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.x = x0
        self.y = y0
        self.size = self.image.get_size()
        self.port_shoot = 0
        self.starboard_shoot = 0
        self.name = name


        # Ship Properties
        self.hull = 5
        self.hull_speed = 1.
        self.speed = 0
        self.aoa = angle
        self.reload_time = 60*60

        self.rotate(self.aoa)

    def shoot(self,shoot_angle):
        ball = CanonBall(self.x,self.y,self.aoa-shoot_angle,self.name)
        smoke = Smoke(self.x,self.y,self.aoa-shoot_angle)
        sound_cannon_fire.play()
        ball.update()
        smoke.update()
        ball.add(CANNON_BALLS)
        smoke.add(SMOKE)

    def hit(self, ball):
        sound_cannon_hit.play()
        explosion = Explosion(ball.rect.x,ball.rect.y,ball.angle)
        explosion.update()
        explosion.add(EXPLO)

        if self.hull > 1:
            self.hull -= 1
        else:
            self.hull = 0
            self.kill()

        ball.kill()

    def rotate(self,angle):
        # rotate image of boat
        pos = (self.x, self.y)
        image = self.image_original
        originPos = (self.size[0]/2,self.size[1]/2)

        image_rect = image.get_rect(topleft = (pos[0]-originPos[0], pos[1]-originPos[1]))
        offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
        rotated_offset = offset_center_to_pivot.rotate(angle)
        rotated_image_center = (pos[0]-rotated_offset.x, pos[1]-rotated_offset.y)
        rotated_image = pygame.transform.rotate(image, -angle)
        rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)

        self.mask = pygame.mask.from_surface(rotated_image)

        return rotated_image,rotated_image_rect

    def update(self, pressed_keys, screen, opponent=None):

        # set wind conditions
        a=0.05
        aoa = self.aoa

        # fire cannons
        if pressed_keys["L"]:
            if (pygame.time.get_ticks() - self.port_shoot) > self.reload_time:
                self.shoot(90)
                self.port_shoot = pygame.time.get_ticks()

        if pressed_keys["R"]:
            if (pygame.time.get_ticks() - self.starboard_shoot) > self.reload_time:
                self.shoot(-90)
                self.starboard_shoot = pygame.time.get_ticks()

        # control movement

        if pressed_keys["UP"]:
            v = self.speed + a
            self.speed = min(v,self.hull_speed)
        if pressed_keys["DOWN"]:
            s = self.speed - 0.1
            self.speed = max(s,0)
        if pressed_keys["LEFT"]:
            aoa -= 1.0
        if pressed_keys["RIGHT"]:
            aoa += 1.0

        self.aoa = aoa % 360

        ship_rad = np.radians(self.aoa)
        x = self.x + self.speed * np.sin(ship_rad)
        y = self.y - self.speed * np.cos(ship_rad)

        self.x = max(width_buffer,min(x,screen_width-width_buffer))
        self.y = max(height_buffer,min(y,screen_height-height_buffer))

        self.rect.x = round(self.x)
        self.rect.y = round(self.y)

        rotated_image,rotated_image_rect = self.rotate(self.aoa)

        # Keep player on the screen
        if rotated_image_rect.left < width_buffer:
            rotated_image_rect.left = width_buffer
        elif rotated_image_rect.right > screen_width-width_buffer:
            rotated_image_rect.right = screen_width-width_buffer
        if rotated_image_rect.top <= height_buffer:
            rotated_image_rect.top = height_buffer
        elif rotated_image_rect.bottom >= screen_height-height_buffer:
            rotated_image_rect.bottom = screen_height-height_buffer

        screen.blit(rotated_image, rotated_image_rect)

        self.image = rotated_image
        self.rect = rotated_image_rect  

class Smoke(pygame.sprite.Sprite):
    def __init__(self,x0,y0,angle) -> None:
        pygame.sprite.Sprite.__init__(self,SMOKE)
        radians = np.radians(angle)
        self.image_original = cannon_fire_smoke
        self.rect = self.image_original.get_rect()
        self.x = x0 + 25 * np.sin(radians)
        self.y = y0 - 25 * np.cos(radians)
        self.alpha = 225
        self.size = self.image_original.get_size()
        self.angle = angle

        rotated_image,rotated_image_rect = self.rotate(self.angle)

        self.image = rotated_image
        self.rect = rotated_image_rect 

    def rotate(self,angle):
        # rotate image of boat
        pos = (self.x, self.y)
        image = self.image_original
        originPos = (self.size[0]/2,self.size[1]/2)

        image_rect = image.get_rect(topleft = (pos[0]-originPos[0], pos[1]-originPos[1]))
        offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
        rotated_offset = offset_center_to_pivot.rotate(angle)
        rotated_image_center = (pos[0]-rotated_offset.x, pos[1]-rotated_offset.y)
        rotated_image = pygame.transform.rotate(image, -angle)
        rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)

        return rotated_image,rotated_image_rect

    def update(self):
        self.alpha = max(0, self.alpha-5)  # alpha should never be < 0.
        rotated_image,rotated_image_rect = self.rotate(self.angle)
        rotated_image.fill((255, 255, 255, self.alpha), special_flags=pygame.BLEND_RGBA_MULT)
        self.image = rotated_image
        self.rect = rotated_image_rect        
        if self.alpha <= 0:  # Kill the sprite when the alpha is <= 0.
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self,x0,y0,angle) -> None:
        pygame.sprite.Sprite.__init__(self,SMOKE)
        self.image = cannon_fire_explo
        self.rect = (x0,y0)
        self.alpha = 225

        #FIXME: use angle to put explosion into ship

    def update(self):
        self.alpha = max(0, self.alpha-5)  # alpha should never be < 0.
        self.image.fill((255, 255, 255, self.alpha), special_flags=pygame.BLEND_RGBA_MULT)     
        if self.alpha <= 0:  # Kill the sprite when the alpha is <= 0.
            self.kill()   
        pass 


class CanonBall(pygame.sprite.Sprite):
    def __init__(self,x0,y0,angle,name):
        pygame.sprite.Sprite.__init__(self,CANNON_BALLS)
        self.image = pygame.Surface((3,3))
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.Mask((3,3),True)
        self.x = x0 
        self.y = y0
        self.angle = np.radians(angle)
        self.speed = 3
        self.name = name
        
    def update(self):
        self.x = self.x + self.speed * np.sin(self.angle)
        self.y = self.y - self.speed * np.cos(self.angle)

        self.rect.x = round(self.x)
        self.rect.y = round(self.y)

        if self.x < 0 or self.x > screen_width or self.y < 0 or self.y > screen_height:
            self.kill()

class Controller():
    def __init__(self,joystick):
        self.joystick = None

        self.button_map = {
            "X":0,
            "A":1,
            "B":2,
            "Y":3,
            "L":4,
            "R":5,
            "SEL":8,
            "STRT":9,
        }

        self.button_map_keyboard = {
            "X":K_w,
            "A":K_d,
            "B":K_s,
            "Y":K_a,
            "L":K_q,
            "R":K_e,
            "SEL":K_x,
            "STRT":K_c,
        }

        self.axis_map = {
            "LEFT":(0,"({:1f} < -0.5)"),
            "RIGHT":(0,"({:1f} > 0.5)"),
            "UP":(1,"({:1f} < -0.5)"),
            "DOWN":(1,"({:1f} > 0.5)"),
        }

        self.axis_map_keyboard = {
            "LEFT":K_LEFT,
            "RIGHT":K_RIGHT,
            "UP":K_UP,
            "DOWN":K_DOWN,
        }

        self.pressed_keys = dict.fromkeys(self.button_map, False)
        self.pressed_keys.update(dict.fromkeys(self.axis_map, False))
    
    def read_input(self):
        if self.joystick:
            for k,v in self.button_map.items():
                self.pressed_keys[k] = self.joystick.get_button(v)

            for k,(v,c) in self.axis_map.items():
                axis_cond = None
                axis_cond = eval(c.format(self.joystick.get_axis(v)))
                self.pressed_keys[k] = axis_cond
        else:
            keys = pygame.key.get_pressed()
            for k,v in self.button_map_keyboard.items():
                self.pressed_keys[k] = keys[v]

            for k,v in self.axis_map_keyboard.items():
                self.pressed_keys[k] = keys[v]

class AIShip(PlayerShip):
    def __init__(self, x0, y0, angle, name):
        super().__init__(x0, y0, angle, name)
        self.turn_dir = 0

    def update(self, pressed_keys, screen, opponent=None):

        a = 0.05

        #Constant Speed
        v = self.speed + a
        dx = screen_width/2 - self.x
        dy = screen_height/2 - self.y
        distance = (dx**2+dy**2)**0.5
        angle = np.arctan2(dy,dx)

        self.speed = min(v,self.hull_speed/2)

        # Turn about the center
        #print(np.arctan2(dy,dx)*180/math.pi)
        #print(angle*180/math.pi)
        if distance < 100:
            if self.turn_dir == 0:
                self.turn_dir = np.sign(angle)

        self.aoa += self.turn_dir * self.speed*60/(200)

        self.aoa = self.aoa % 360

        ship_rad = np.radians(self.aoa)
        x = self.x + self.speed * np.sin(ship_rad)
        y = self.y - self.speed * np.cos(ship_rad)

        self.x = max(width_buffer,min(x,screen_width-width_buffer))
        self.y = max(height_buffer,min(y,screen_height-height_buffer))

        self.rect.x = round(self.x)
        self.rect.y = round(self.y)

        rotated_image,rotated_image_rect = self.rotate(self.aoa)

        # Keep player on the screen
        if rotated_image_rect.left < width_buffer:
            rotated_image_rect.left = width_buffer
        elif rotated_image_rect.right > screen_width-width_buffer:
            rotated_image_rect.right = screen_width-width_buffer
        if rotated_image_rect.top <= height_buffer:
            rotated_image_rect.top = height_buffer
        elif rotated_image_rect.bottom >= screen_height-height_buffer:
            rotated_image_rect.bottom = screen_height-height_buffer

        screen.blit(rotated_image, rotated_image_rect)

        self.image = rotated_image
        self.rect = rotated_image_rect

class AI_Control():
    pass

def player_stats(screen,PlayerShip,num,side):

    strings = [
        "Player: "+str(int(num)),
        "Hull: % 1.0f" % PlayerShip.hull,
        "Knts: % 2.2f" % PlayerShip.speed,
        "AOA: % 3.0f" % PlayerShip.aoa,
    ]

    font = pygame.font.Font('freesansbold.ttf', 24)
    
    if side == 'right':
        for dy,s in enumerate(strings):
            stat = font.render(s, True, (255,255,255), (0,0,0))
            screen.blit(stat, (screen_width-150,dy*25))
    else:
        for dy,s in enumerate(strings):
            stat = font.render(s, True, (255,255,255), (0,0,0))
            screen.blit(stat, (0,dy*25))

def main():
    pygame.display.set_caption('Ship Battle')

    # initialize pygame
    pygame.init()

    # create the screen object
    screen = pygame.display.set_mode((screen_width, screen_height))

    #background
    background = pygame.Surface(screen.get_size())
    background.fill((0, 154, 255))

    # create players
    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

    rand_num = random.random()
    a1 = np.floor(rand_num * 360)
    a2 = a1 - 180 % 360

    a1_rad = np.deg2rad(a1)
    a2_rad = np.deg2rad(a2)

    r = (screen_height-100)/2
    x1 = r * np.sin(a1_rad) + screen_width/2
    y1 = -1 * r * np.cos(a1_rad) + screen_height/2

    x2 = r * np.sin(a2_rad) + screen_width/2
    y2 = -1 * r * np.cos(a2_rad) + screen_height/2

    if False:
        # 2 player battle
        player1 = PlayerShip(x1, y1, (a1-180) % 360)
        if len(joysticks) > 1:    
            controller1 = Controller(joysticks[0])

        player2 = PlayerShip(x2, y2, (a2-180) % 360)
        if len(joysticks) > 2:
            controller2 = Controller(joysticks[1])

        players = [(player1,controller1,player2),(player2,controller2,player1)]
    else:
        # 1 player vs AI
        player1 = PlayerShip(x1, y1, (a1-180) % 360, 'Name')
        controller1 = Controller(None)

        player2 = AIShip(x2, y2, (a2-180) % 360 + 10, 'Name2')
        ai_controller = AI_Control()

        players = [(player1,controller1,player2),(player2,ai_controller,player1)]

    #draw wind arrow
    wind_direction = 135

    wind_arrow = pygame.Surface((300,300), SRCALPHA, 32)
    wind_arrow = wind_arrow.convert_alpha()
    pygame.draw.polygon(wind_arrow, (0, 0, 0), ((0, 100), (0, 200), (200, 200), (200, 300), (300, 150), (200, 0), (200, 100)), width=0)
    wind_arrow = pygame.transform.rotate(wind_arrow, -wind_direction+90)
    wind_arrow = pygame.transform.scale(wind_arrow,(30,30))

    running = True

    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False
        
        for p,c,o in players:
            if isinstance(c, Controller):
                c.read_input()
                

        screen.blit(background, (0, 0))
        screen.blit(wind_arrow, (screen_width/2,0))

        for i,(p,c,o) in enumerate(players):
            if isinstance(c, Controller):
                pressed_keys = c.pressed_keys
            else:
                pressed_keys = []
            p.update(pressed_keys,screen,opponent=o)
            #Display Ship Stats
            if i == 0:
                player_stats(screen,p,1,'left')
            else:
                player_stats(screen,p,2,'right')
            pygame.draw.rect(screen, (255, 0, 0), (*p.rect.topleft, *p.image.get_size()),2)
            if pygame.sprite.spritecollideany(p, CANNON_BALLS):
                hitting_balls = pygame.sprite.spritecollide(p, CANNON_BALLS, False, collided=pygame.sprite.collide_mask)
                if any([p.name != b.name for b in hitting_balls]):
                    for b in hitting_balls:
                        o.hit(b) 

        CANNON_BALLS.update()
        CANNON_BALLS.draw(screen)

        SMOKE.update()
        SMOKE.draw(screen)

        EXPLO.update()
        EXPLO.draw(screen)

        pygame.display.flip()

        clock.tick(60)

if __name__ == '__main__':
    main()