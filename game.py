# Basic arcade OOP

import arcade as ar
import random as rn
import sys
import os

# Include this for pyinstaller
# https://api.arcade.academy/en/latest/tutorials/bundling_with_pyinstaller/index.html
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
SCREEN_TITLE = 'Moretini Invaders'

SCALING_PLAYER = 0.5
SCALING_METEOR = 0.5
SCALING_PLASMA = 0.5


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
        self.all_sprites = ar.SpriteList()

    def setup(self):
        ''' Initialise the game to a known starting point.
        '''

        # Define paused
        self.paused = False

        # Set background
        ar.set_background_color(ar.color.ENGLISH_VIOLET)

        # Setup the player
        self.player = ar.Sprite('data/blue_ship.png', SCALING_PLAYER)
        self.player.center_x = self.height / 2
        self.player.bottom = 10
        self.all_sprites.append(self.player)

        # Spawn new meteors
        ar.schedule(self.add_meteor, 0.35)

        # Spawn a new plasma cloud
        ar.schedule(self.add_plasma_cloud, 1.5)

    def add_meteor(self, delta_time: float):
        ''' Adds a new meteor to the scene. Input is how much
        time has passed since last call.
        '''

        # Randomize meteor scaling
        scale = rn.uniform(0.5, 2)

        # Create a new meteor sprite
        meteor = FlyingSprite('data/meteor_medium.png',
                              scale * SCALING_METEOR)

        # Set meteor position on top and off screen
        meteor.bottom = rn.randint(self.height, self.height + 80)
        meteor.left = rn.randint(10, self.width - 10)

        # Set meteor velocity
        meteor.velocity = (rn.randint(-3, 3), rn.randint(-15, -5))

        # Add to the meteor list
        self.meteor_list.append(meteor)
        self.all_sprites.append(meteor)

    def add_plasma_cloud(self, delta_time: float):
        ''' Add a new plasma cloud to the scene. Input is how
        much time has passed since last call.
        '''

        # Randomize plazma scaling
        scale = rn.uniform(0.5, 1.5)

        # Create a new plasma cloud sprite
        plasma = FlyingSprite('data/plasma_cloud.png',
                              scale * SCALING_PLASMA,
                              flipped_vertically=True)

        # Set plasma cloud positions
        plasma.bottom = rn.randint(self.height, self.height + 80)
        plasma.left = rn.randint(10, self.width - 10)

        # Set plasma cloud velocity
        plasma.velocity = (0, rn.randint(-20, -10))

        # Add to the plasma list
        self.plasma_list.append(plasma)
        self.all_sprites.append(plasma)

    def on_update(self, delta_time: float):
        ''' Update positions and status of all game objects.
        '''

        # If paused, don't update
        if self.paused:
            return

        # Has the eplayer been hit by a meteor
        if self.player.collides_with_list(self.meteor_list):
            ar.close_window()

        # Has the player been hit by the plasma cloud
        if self.player.collides_with_list(self.plasma_list):
            ar.close_window()

        # Update all sprites
        self.all_sprites.update()

        # Keep the player on the screen
        if self.player.top > self.height:
            self.player.top = self.height

        if self.player.right > self.width:
            self.player.right = self.width

        if self.player.bottom < 0:
            self.player.bottom = 0

        if self.player.left < 0:
            self.player.left = 0

    def on_draw(self):
        ''' Draw all game sprites.
        '''

        ar.start_render()
        self.all_sprites.draw()

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


def main():
    ''' Run the main code here.
    '''

    game = MoretiniInvaders(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    ar.run()


# Main code
if __name__ == '__main__':
    main()
