import pgzrun
import math
import random
from pygame import Rect

# --- Game Configuration ---
WIDTH = 800
HEIGHT = 600
TITLE = "Pixel Adventure Platformer"

# Physics Constants
GRAVITY = 0.5
JUMP_FORCE = -10
PLAYER_SPEED = 4
ENEMY_SPEED = 2

# Game Global Variables
game_state = "menu"  # Options: 'menu', 'game', 'game_over'
sound_on = True

# --- Classes ---

class Entity:
    """Base class for physical objects."""
    def __init__(self, x, y, image):
        self.actor = Actor(image, (x, y))
        self.width = self.actor.width
        self.height = self.actor.height

    def draw(self):
        self.actor.draw()

class AnimatedCharacter(Entity):
    """Handles sprite animation logic."""
    def __init__(self, x, y, idle_imgs, run_imgs):
        super().__init__(x, y, idle_imgs[0])
        self.idle_imgs = idle_imgs
        self.run_imgs = run_imgs
        self.frame_index = 0
        self.anim_timer = 0
        self.facing_right = True
        self.is_moving = False
        self.anim_speed = 10 # Higher number = slower animation

    def animate(self):
        """Cycles through images based on state."""
        self.anim_timer += 1
        if self.anim_timer % self.anim_speed == 0:
            self.frame_index += 1

        # Select image set
        if self.is_moving:
            current_set = self.run_imgs
        else:
            current_set = self.idle_imgs

        # Calculate frame loop
        idx = self.frame_index % len(current_set)
        img_name = current_set[idx]

        # Handle Direction (Left/Right)
        if not self.facing_right:
            # Check if a left version exists or logic needs it
            # The setup.py created files with '_left' suffix for the hero
            if "hero" in img_name: 
                img_name += "_left"
        
        self.actor.image = img_name

class Player(AnimatedCharacter):
    def __init__(self, x, y):
        super().__init__(x, y, ["hero_idle_1", "hero_idle_2"], ["hero_run_1", "hero_run_2"])
        self.vx = 0
        self.vy = 0
        self.on_ground = False

    def update(self, platforms):
        # 1. Reset horizontal speed
        self.vx = 0
        self.is_moving = False

        # 2. Input Handling
        if keyboard.left:
            self.vx = -PLAYER_SPEED
            self.facing_right = False
            self.is_moving = True
        elif keyboard.right:
            self.vx = PLAYER_SPEED
            self.facing_right = True
            self.is_moving = True

        if keyboard.up and self.on_ground:
            self.vy = JUMP_FORCE
            self.on_ground = False
            if sound_on:
                sounds.jump.play()

        # 3. Apply Gravity
        self.vy += GRAVITY

        # 4. Movement & Collision (X Axis)
        self.actor.x += self.vx
        for plat in platforms:
            if self.actor.colliderect(plat.actor):
                if self.vx > 0: # Moving right
                    self.actor.right = plat.actor.left
                elif self.vx < 0: # Moving left
                    self.actor.left = plat.actor.right

        # 5. Movement & Collision (Y Axis)
        self.actor.y += self.vy
        self.on_ground = False # Assume air until proven ground
        for plat in platforms:
            if self.actor.colliderect(plat.actor):
                if self.vy > 0: # Falling
                    self.actor.bottom = plat.actor.top
                    self.vy = 0
                    self.on_ground = True
                elif self.vy < 0: # Jumping up into block
                    self.actor.top = plat.actor.bottom
                    self.vy = 0

        # 6. Screen Boundaries
        if self.actor.left < 0: self.actor.left = 0
        if self.actor.right > WIDTH: self.actor.right = WIDTH
        
        # 7. Animation Trigger
        self.animate()

        # Check death (fall)
        if self.actor.y > HEIGHT + 50:
            return False # Dead
        return True # Alive

class Enemy(AnimatedCharacter):
    def __init__(self, x, y, limit_left, limit_right):
        super().__init__(x, y, ["enemy_1", "enemy_2"], ["enemy_1", "enemy_2"])
        self.limit_left = limit_left
        self.limit_right = limit_right
        self.speed = ENEMY_SPEED
        self.is_moving = True

    def update(self):
        self.actor.x += self.speed
        
        # Patrol Logic
        if self.actor.x > self.limit_right:
            self.speed = -ENEMY_SPEED
        elif self.actor.x < self.limit_left:
            self.speed = ENEMY_SPEED
            
        self.animate()

# --- Setup Functions ---

player = None
enemies = []
platforms = []
menu_buttons = []

def init_game():
    """Resets the game level."""
    global player, enemies, platforms
    player = Player(100, 300)
    
    # Define Ground and Platforms
    platforms = [
        Entity(400, 580, "block"),  # Floor 1
        Entity(100, 580, "block"),  # Floor 2
        Entity(700, 580, "block"),  # Floor 3
        Entity(300, 450, "block"),  # Floating Platform
        Entity(500, 350, "block"),
        Entity(100, 250, "block")
    ]
    # Stretch floor for visual trick (Actor scaling not ideal in pgzero basic, so we use multiple blocks or just one)
    # Since we can't scale simply without pygame transform, we just place blocks strategically.
    # Let's add more blocks to make a floor.
    for i in range(0, 850, 50):
        platforms.append(Entity(i, 580, "block"))

    # Define Enemies
    enemies = [
        Enemy(300, 420, 280, 320), # On floating platform
        Enemy(500, 550, 400, 600)  # On ground
    ]

def setup_menu():
    global menu_buttons
    # Buttons: Image, X, Y, Function Name
    menu_buttons = [
        {"actor": Actor("btn_start", (WIDTH//2, 200)), "action": "start"},
        {"actor": Actor("btn_sound", (WIDTH//2, 300)), "action": "toggle_sound"},
        {"actor": Actor("btn_exit", (WIDTH//2, 400)), "action": "exit"}
    ]

# --- Main Game Loops ---

def update():
    global game_state
    
    if game_state == "game":
        alive = player.update(platforms)
        if not alive:
            game_state = "menu"
            
        for enemy in enemies:
            enemy.update()
            if player.actor.colliderect(enemy.actor):
                game_state = "menu" # Game Over on touch

def draw():
    screen.clear()
    
    if game_state == "menu":
        screen.draw.text("PLATFORMER GAME", center=(WIDTH//2, 100), fontsize=60, color="white")
        
        status = "ON" if sound_on else "OFF"
        screen.draw.text(f"Sound is: {status}", center=(WIDTH//2, 500), fontsize=30, color="yellow")

        for btn in menu_buttons:
            btn["actor"].draw()
            # Draw labels manually since buttons are just blocks
            if btn["action"] == "start":
                screen.draw.text("START", center=btn["actor"].pos, fontsize=30, color="black")
            elif btn["action"] == "toggle_sound":
                screen.draw.text("SOUND", center=btn["actor"].pos, fontsize=30, color="black")
            elif btn["action"] == "exit":
                screen.draw.text("EXIT", center=btn["actor"].pos, fontsize=30, color="black")

    elif game_state == "game":
        for plat in platforms:
            plat.draw()
        for enemy in enemies:
            enemy.draw()
        player.draw()

def on_mouse_down(pos):
    global game_state, sound_on
    
    if game_state == "menu":
        for btn in menu_buttons:
            if btn["actor"].collidepoint(pos):
                if btn["action"] == "start":
                    init_game()
                    game_state = "game"
                    if sound_on:
                        try:
                            # Using 'music' because file is music.wav
                            music.play("music") 
                        except:
                            pass
                elif btn["action"] == "toggle_sound":
                    sound_on = not sound_on
                    if sound_on:
                        music.play("music")
                    else:
                        music.stop()
                elif btn["action"] == "exit":
                    quit()

# Initial Setup
setup_menu()
pgzrun.go()
