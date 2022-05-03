# Basic arcade OOP

import arcade as ar
import random as rn
import sys
import os

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
SCREEN_TITLE = 'Moretini Invaders'

SCALING_PLAYER = 0.5
SCALING_METEOR = 0.5
SCALING_PLASMA = 0.5
SCALING_LASER = 0.5
VELOCITY_LASER = 5


# Include this for pyinstaller
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)


class MoretiniInvaders(ar.Window):
    ''' Moretini Invaders is a 2D space shooting game.
    This is the main class.
    '''
    
    def __init__(self, width, height, title):
        ''' Initialise the game.
        '''

        # Call superclass constructor
        super().__init__(width, height, title)

        # Setup empty sprite lists
        self.meteor_list = ar.SpriteList()
        self.plasma_list = ar.SpriteList()
        self.laser_list = ar.SpriteList()
        self.explosions_list = ar.SpriteList()

        # Explosion texture list from png
        self.explosoin_png_list = []

    def setup(self):
        ''' Initialise the game to a known starting point.
        '''

        # Define paused
        self.paused = False

        # Define score
        self.score = 0

        # Set background
        ar.set_background_color(ar.color.ENGLISH_VIOLET)

        # Setup the player
        self.player = ar.Sprite('data/image/blue_ship.png', SCALING_PLAYER)
        self.player.center_x = self.height / 2
        self.player.bottom = 10

        # Spawn new meteors
        ar.schedule(self.add_meteor, 0.35)

        # Spawn a new plasma cloud
        ar.schedule(self.add_plasma_cloud, 1.5)

        # Load explosion texture
        pth = 'data/image/explosion.png'
        wdth = 256
        hght = 256
        cols = 16
        count = 60
        self.explosion_png_list = ar.load_spritesheet(pth, wdth, hght,
                                                      cols, count)

        # Load sounds
        self.laser_sound = ar.sound.load_sound('data/sound/laser2.wav')
        self.explosion_sound = ar.sound.load_sound('data/sound/explosion2.wav')


    def add_meteor(self, delta_time: float):
        ''' Adds a new meteor to the scene. Input is how much
        time has passed since last call.
        '''

        # Randomize meteor scaling
        scale = SCALING_METEOR * rn.uniform(0.5, 2)

        # Create a new meteor sprite
        meteor = FlyingSprite('data/image/meteor_medium.png', scale)

        # Set meteor position on top and off screen
        meteor.bottom = rn.randint(self.height, self.height + 80)
        meteor.left = rn.randint(10, self.width - 10)

        # Set meteor velocity
        meteor.velocity = (rn.randint(-3, 3), rn.randint(-15, -5))

        # Add to the meteor list
        self.meteor_list.append(meteor)

    def add_plasma_cloud(self, delta_time: float):
        ''' Add a new plasma cloud to the scene. Input is how
        much time has passed since the last call.
        '''

        # Randomize plazma scaling
        scale = SCALING_PLASMA * rn.uniform(0.5, 1.5)

        # Create a new plasma cloud sprite
        plasma = FlyingSprite('data/image/plasma_cloud.png',
                              scale,
                              flipped_vertically=True)

        # Set plasma cloud positions
        plasma.bottom = rn.randint(self.height, self.height + 80)
        plasma.left = rn.randint(10, self.width - 10)

        # Set plasma cloud velocity
        plasma.velocity = (0, rn.randint(-20, -10))

        # Add to the plasma list
        self.plasma_list.append(plasma)

    def on_update(self, delta_time: float):
        ''' Update positions and status of all game objects.
        '''

        # If paused, don't update
        if self.paused:
            return

        # Has the player been hit by a meteor
        if self.player.collides_with_list(self.meteor_list):
            ar.close_window()

        # Has the player been hit by the plasma cloud
        if self.player.collides_with_list(self.plasma_list):
            ar.close_window()

        # Check and update laser hits
        self.trigger_laser_hits()

        # Update all sprites
        self.player.update()
        self.meteor_list.update()
        self.plasma_list.update()
        self.laser_list.update()
        self.explosions_list.update()

        # Keep the player on the screen
        if self.player.top > self.height:
            self.player.top = self.height

        if self.player.right > self.width:
            self.player.right = self.width

        if self.player.bottom < 0:
            self.player.bottom = 0

        if self.player.left < 0:
            self.player.left = 0

    def trigger_laser_hits(self):
        ''' Check collision for all laser shots and trigger explosions.
        '''

        # Loop through all bullets
        for laser in self.laser_list:

            # Get the list of hits with meteors
            hit_lst = laser.collides_with_list(self.meteor_list)

            # If hits present
            if len(hit_lst) > 0:

                # Make an explosion
                explosion = Explosion(self.explosion_png_list)

                # Position explosion to meteor
                explosion.center_x = hit_lst[0].center_x
                explosion.center_y = hit_lst[0].center_y

                # Update explosion (to determine which png in sequence)
                explosion.update()

                # Add to lists
                self.explosions_list.append(explosion)

                # Remove laser
                laser.remove_from_sprite_lists()

            # Loop through all hit meteors
            for meteor in hit_lst:

                # Remove from lists and update score
                meteor.remove_from_sprite_lists()
                self.score += 1

                # Play hit sound
                ar.sound.play_sound(self.explosion_sound)

            # Remove laser if off screen
            if laser.bottom > self.height:
                laser.remove_from_sprite_lists()

    def on_draw(self):
        ''' Draw all game sprites.
        '''

        # Update all sprites
        self.clear()
        self.player.draw()
        self.meteor_list.draw()
        self.plasma_list.draw()
        self.laser_list.draw()
        self.explosions_list.draw()

        # Update score
        ar.draw_text(f'Score: {self.score}', 10, 20, ar.color.WHITE, 14)

    def on_key_press(self, symbol, modifiers):
        ''' Handle user keyboard input.
        '''

        if symbol == ar.key.Q:
            ar.close_window()

        if symbol == ar.key.P:
            self.paused = not self.paused

        if symbol == ar.key.UP:
            self.player.change_y = 5

        if symbol == ar.key.DOWN:
            self.player.change_y = -5

        if symbol == ar.key.LEFT:
            self.player.change_x = -5

        if symbol == ar.key.RIGHT:
            self.player.change_x = 5

        if symbol == ar.key.SPACE:
            self.trigger_laser_shot()

    def trigger_laser_shot(self):
        '''Play sound and create laser sprite.
        '''

        # Play sound
        ar.sound.play_sound(self.laser_sound)

        # Create a bullet
        laser = ar.Sprite('data/image/laserBlue01.png', SCALING_LASER)

        # Rotate image
        laser.angle = 90

        # Setup speed
        laser.change_y = VELOCITY_LASER

        # Position the laser
        laser.center_x = self.player.center_x
        laser.bottom = self.player.top

        # Add laser to lists
        self.laser_list.append(laser)

    def on_key_release(self, symbol: int, modifiers: int):
        ''' Rewrite movement attributes when keys released.
        '''

        if symbol == ar.key.UP or symbol == ar.key.DOWN:
            self.player.change_y = 0

        if symbol == ar.key.LEFT or symbol == ar.key.RIGHT:
            self.player.change_x = 0


class FlyingSprite(ar.Sprite):
    ''' Base class for ll moving sprites,
    overriding the original class.
    '''

    def update(self):
        ''' Update the position of the sprites,
        when it moves off the screen, remove it.
        '''

        # Move the sprite by inherited method
        super().update()

        # Remove if off screen
        if self.top < 0:
            self.remove_from_sprite_lists()


class Explosion(ar.Sprite):
    ''' Create explosion animation.
    '''

    def __init__(self, texture_list):
        ''' Initalise Explosion class.
        '''

        # Run constructor from the parent class
        super().__init__()

        # Start at the first frame
        self.current_texture = 0
        self.textures = texture_list

    def update(self):
        ''' Update to the next frame of animation. If at the end
        of explosion frames, delete this sprite.
        '''

        # Update texture counter
        self.current_texture += 1

        # Set current texture
        if self.current_texture < len(self.textures):
            self.set_texture(self.current_texture)

        else:
            self.remove_from_sprite_lists()


def main():
    ''' Run the main code here.
    '''

    game = MoretiniInvaders(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    ar.run()


# Main code
if __name__ == '__main__':
    main()
