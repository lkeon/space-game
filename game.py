# -------------------------------------------
#           MORETINI INVADERS
# -------------------------------------------
# Game based on Python Arcade.
# Artwork from https://kenney.nl

import arcade as ar
import random as rn
import copy
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

TIME_LEVEL = 20
TIME_ADD = 5
SPAWN_METEOR = 0.75
SPAWN_PLASMA = 1.5
SPAWN_SCALE = 1.01
VELOCITY_FACTOR = 0.6
LEVEL_FACTOR = 1.1


# Include this for pyinstaller
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)


class MenuView(ar.View):
    def on_show(self):
        ar.set_background_color(ar.color.JAPANESE_VIOLET)

    def on_draw(self):
        self.clear()
        ar.draw_text("Moretini Invaders", SCREEN_WIDTH/2, SCREEN_HEIGHT*3/4,
                     ar.color.WHITE, font_size=25, anchor_x="center",
                     font_name="Kenney Rocket")

        txt = ("Once upon a time in a galaxy far, far away the "
               "Moretinians were facing extinction.\n\nAs a commander "
               "of the resistance force you were tasked to extract them "
               "to safety.")
        
        ar.draw_text(txt,
                     50, SCREEN_HEIGHT/2 + 100,
                     ar.color.WHITE, 16,
                     multiline=True, width=(SCREEN_WIDTH-100))

        ar.draw_text("Press any key to continue.",
                     SCREEN_WIDTH/2, 150,
                     ar.color.KELLY_GREEN, font_size=14, anchor_x="center")

    def on_key_press(self, symbol, modifiers):
        instructions_view = InstructionView()
        self.window.show_view(instructions_view)


class InstructionView(ar.View):
    def on_show(self):
        ar.set_background_color(ar.color.JAPANESE_VIOLET)

    def on_draw(self):
        self.clear()
        ar.draw_text("Moretini Invaders", SCREEN_WIDTH/2, SCREEN_HEIGHT*3/4,
                     ar.color.WHITE, font_size=25, anchor_x="center",
                     font_name="Kenney Rocket")

        txt = ("Your job is to fly through the meteor shower and plasma "
               "clouds to reach New London on planet Plimius.\n\n"
               "Use navigation keys to move your space vessel around and "
               "space bar to activate your laser gun.\n\nGood luck, commander!")
        
        ar.draw_text(txt,
                     50, SCREEN_HEIGHT/2 + 100,
                     ar.color.WHITE, 16,
                     multiline=True, width=(SCREEN_WIDTH-100))

        ar.draw_text("Press any key to continue.",
                     SCREEN_WIDTH/2, 150,
                     ar.color.KELLY_GREEN, font_size=14, anchor_x="center")

    def on_key_press(self, symbol, modifiers):
        game_view = MoretiniInvaders()
        game_view.setup()
        self.window.show_view(game_view)


class GameOverView(ar.View):
    def __init__(self):
        super().__init__()
        self.time_taken = 0
        self.message = ""

    def on_show(self):
        ar.set_background_color(ar.color.JAPANESE_VIOLET)
        messages = ["You suck.", "Your performance is unacceptable.",
                    "You are such a failure.", "You have failed.",
                    "Try better next time.",
                    "How incompetent can you really be?",
                    "You are a disgrace for humanity.",
                    "You will be court martialed."]
        select = rn.randint(0, len(messages) - 1)
        self.message = messages[select]

    def on_draw(self):
        self.clear()
        """
        Draw "Game over" across the screen.
        """
        ar.draw_text("GAME OVER", SCREEN_WIDTH/2, SCREEN_HEIGHT*3/4,
                     ar.color.WHITE, font_size=25, anchor_x="center",
                     font_name="Kenney Rocket")

        ar.draw_text(self.message,
                     SCREEN_WIDTH/2, SCREEN_HEIGHT/2, ar.color.WHITE,
                     font_size=18, anchor_x="center")

        ar.draw_text("All Moretinians were massacred.",
                     SCREEN_WIDTH/2, SCREEN_HEIGHT/2-35, ar.color.WHITE,
                     font_size=18, anchor_x="center")

        ar.draw_text("Press enter to restart.",
                     SCREEN_WIDTH/2, 150,
                     ar.color.KELLY_GREEN, font_size=14, anchor_x="center")

        time_taken_formatted = f"{round(self.time_taken, 2)} seconds"
        ar.draw_text(f"Terminated in: {time_taken_formatted}",
                     20, 70, ar.color.DUST_STORM,
                     font_size=12)

        output_total = f"Total meteors shot: {self.window.total_score}"
        ar.draw_text(output_total, 20, 45, ar.color.DUST_STORM, 12)

        level = f"Max level reached: {self.window.current_level - 1}"
        ar.draw_text(level, 20, 20, ar.color.DUST_STORM, 12)

    def on_key_press(self, symbol, modifiers):
        if symbol == ar.key.ENTER:

            self.window.total_score = 0
            self.window.current_level = 1
            self.window.current_level_factor = 1
            self.window.level_duration = TIME_LEVEL
            self.window.current_spawn_factor = SPAWN_SCALE

            game_view = MoretiniInvaders()
            game_view.setup()
            self.window.show_view(game_view)


class NextLevelView(ar.View):
    def __init__(self):
        super().__init__()
        self.time_taken = 0

    def on_show(self):
        ar.set_background_color(ar.color.JAPANESE_VIOLET)
        messages = ["Excellent job!",
                    "Hero of the Space Union!",
                    "Keep up with good work!",
                    "Well done!",
                    "Your courage is exemplary.",
                    "Your gallantry will be awarded!",
                    "Ditinguisged Flying Cross earned!"]
        select = rn.randint(0, len(messages) - 1)
        self.message = messages[select]

    def on_draw(self):
        self.clear()
        """
        Draw "Game over" across the screen.
        """
        level = str(self.window.current_level)
        ar.draw_text("LEVEL " + level,
                     SCREEN_WIDTH/2, SCREEN_HEIGHT*3/4,
                     ar.color.WHITE, font_size=25, anchor_x="center",
                     font_name="Kenney Rocket")

        ar.draw_text("COMPLETED",
                     SCREEN_WIDTH/2, SCREEN_HEIGHT*3/4 - 40,
                     ar.color.WHITE, font_size=25, anchor_x="center",
                     font_name="Kenney Rocket")

        ar.draw_text(self.message,
                     SCREEN_WIDTH/2, SCREEN_HEIGHT/2, ar.color.WHITE,
                     font_size=18, anchor_x="center")

        ar.draw_text("Moretinians are awaiting rescue.",
                     SCREEN_WIDTH/2, SCREEN_HEIGHT/2-35, ar.color.WHITE,
                     font_size=18, anchor_x="center")

        ar.draw_text("Press enter to continue.",
                     SCREEN_WIDTH/2, 150,
                     ar.color.KELLY_GREEN, font_size=14, anchor_x="center")

        time_taken_formatted = f"{round(self.time_taken, 2)} seconds"
        ar.draw_text(f"Finished in: {time_taken_formatted}",
                     20, 45, ar.color.DUST_STORM,
                     font_size=12)

        output_total = f"Total meteors shot: {self.window.total_score}"
        ar.draw_text(output_total, 20, 20, ar.color.DUST_STORM, 12)

    def on_key_press(self, symbol, modifiers):
        if symbol == ar.key.ENTER:

            self.window.current_level += 1
            self.window.current_level_factor *= LEVEL_FACTOR
            self.window.current_spawn_factor *= SPAWN_SCALE
            self.window.level_duration += TIME_ADD

            game_view = MoretiniInvaders()
            game_view.setup()
            self.window.show_view(game_view)


class MoretiniInvaders(ar.View):
    ''' Moretini Invaders is a 2D space shooting game.
    This is the main class.
    '''
    
    def __init__(self):
        ''' Initialise the game.
        '''

        # Call superclass constructor
        super().__init__()

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

        # Progression level factors
        self.vel_fact = VELOCITY_FACTOR * self.window.current_level_factor
        self.time_level = self.window.level_duration

        # Define score
        self.score = 0

        # Define timer
        self.timer = 0

        # Set background
        ar.set_background_color(ar.color.ENGLISH_VIOLET)

        # Setup the player
        self.player = ar.Sprite('data/image/blue_ship.png', SCALING_PLAYER)
        self.player.center_x = SCREEN_HEIGHT / 2
        self.player.bottom = 10

        # Setup bullet
        self.laser = ar.Sprite('data/image/laserBlue01.png', SCALING_LASER)
        self.laser.angle = 90
        self.laser.change_y = VELOCITY_LASER

        # Spawn new meteors
        spawn_time = SPAWN_METEOR / self.window.current_spawn_factor
        ar.schedule(self.add_meteor, spawn_time)

        # Spawn a new plasma cloud
        spawn_time = SPAWN_PLASMA / self.window.current_spawn_factor
        ar.schedule(self.add_plasma_cloud, spawn_time)

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
        self.game_over_sound = ar.sound.load_sound('data/sound/gameover4.wav')
        self.next_level_sound = ar.sound.load_sound('data/sound/upgrade3.wav')

    def add_meteor(self, delta_time: float):
        ''' Adds a new meteor to the scene. Input is how much
        time has passed since last call.
        '''

        # Randomize meteor scaling
        scale = SCALING_METEOR * rn.uniform(0.5, 2)

        # Create a new meteor sprite
        meteor = FlyingSprite('data/image/meteor_medium.png', scale)

        # Set meteor position on top and off screen
        meteor.bottom = rn.randint(SCREEN_HEIGHT, SCREEN_HEIGHT + 80)
        meteor.left = rn.randint(10, SCREEN_WIDTH - 10)

        # Set meteor velocity
        meteor.velocity = (self.vel_fact * rn.randint(-3, 3),
                           self.vel_fact * rn.randint(-10, -5))

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
        plasma.bottom = rn.randint(SCREEN_HEIGHT, SCREEN_HEIGHT + 80)
        plasma.left = rn.randint(10, SCREEN_WIDTH - 10)

        # Set plasma cloud velocity
        plasma.velocity = (0, self.vel_fact * rn.randint(-12, -10))

        # Add to the plasma list
        self.plasma_list.append(plasma)

    def on_update(self, delta_time: float):
        ''' Update positions and status of all game objects.
        '''

        # Update time
        self.timer += delta_time

        # If paused, don't update
        if self.paused:
            return

        # Has the player been hit by a meteor
        if self.player.collides_with_list(self.meteor_list):
            self.trigger_game_over()

        # Has the player been hit by the plasma cloud
        if self.player.collides_with_list(self.plasma_list):
            self.trigger_game_over()

        # Check if time has passed to progress to next level
        if self.timer >= self.time_level:
            self.trigger_next_level()

        # Check and update laser hits
        self.trigger_laser_hits()

        # Update all sprites
        self.player.update()
        self.meteor_list.update()
        self.plasma_list.update()
        self.laser_list.update()
        self.explosions_list.update()

        # Keep the player on the screen
        if self.player.top > SCREEN_HEIGHT:
            self.player.top = SCREEN_HEIGHT

        if self.player.right > SCREEN_WIDTH:
            self.player.right = SCREEN_WIDTH

        if self.player.bottom < 0:
            self.player.bottom = 0

        if self.player.left < 0:
            self.player.left = 0

    def trigger_game_over(self):
        ''' Actions to trigger before game over.
        '''

        ar.sound.play_sound(self.game_over_sound)
        game_over_view = GameOverView()
        game_over_view.time_taken = self.timer
        self.window.show_view(game_over_view)

    def trigger_next_level(self):
        ''' Progress to the next level.
        '''

        ar.sound.play_sound(self.next_level_sound)
        next_level_view = NextLevelView()
        next_level_view.time_taken = self.timer
        self.window.show_view(next_level_view)


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
                self.window.total_score += 1

                # Play hit sound
                ar.sound.play_sound(self.explosion_sound)

            # Remove laser if off screen
            if laser.bottom > SCREEN_HEIGHT:
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

        # Reference laser sprite
        laser = copy.deepcopy(self.laser)

        # Position the laser
        laser.center_x = self.player.center_x
        laser.bottom = self.player.top

        # Copy laser to lists
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

    window = ar.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.total_score = 0
    window.current_level = 1
    window.current_level_factor = 1
    window.current_spawn_factor = SPAWN_SCALE
    window.level_duration = TIME_LEVEL
    menu_view = MenuView()
    window.show_view(menu_view)
    ar.run()


# Main code
if __name__ == '__main__':
    main()
