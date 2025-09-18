import random
import pygame as pyg
from .CONSTANTS import (
    DISPLAY_DIMENSIONS_X,
    DISPLAY_DIMENSIONS_Y,
    image_path,
    text_font,
    OFF_WHITE
)
from ui import Text

class RewardRoom():
    """
    Class representing a reward room where players can receive rewards.

    This class handles the display of reward options, calculates rewards based on rarity,
    and manages player interactions within the reward room.

    Attributes:
        __display (pygame.Surface): The display surface where rewards are shown.
        __bg (pygame.Surface): Background image for the reward room.
        __player (Player): The player object to update rewards.
        __pouch_image (pygame.Surface): The image of the pouch used to display rewards.
        reward_text (str): Text to display the reward message.
        reward_displayed (bool): Flag to track if the reward has been displayed.
    """
    def __init__(self, display, bg, player):
        """
        Initialises the RewardRoom with display, background, and player.

        Parameters:
            display (pygame.Surface): The surface for rendering the reward room.
            bg (pygame.Surface): The background image to display in the reward room.
            player (Player): The player object associated with the reward room.
        """
        self.__display = display
        self.__bg = bg
        self.__player = player
        self.__pouch_image = pyg.image.load(f"{image_path}\\money_bag.png")
        self.__pouch_image = pyg.transform.scale(self.__pouch_image, (DISPLAY_DIMENSIONS_X//5, DISPLAY_DIMENSIONS_Y//5))
        self.reward_text = ""
        self.reward_displayed = False
        self.__message_text = None
        self.__message_duration = 2000
        self.__message_timer = 0

    def start_new_reward(self):
        """
        Starts the process of displaying a new reward to the player.

        This method will repeatedly call to display reward options until a reward has been successfully displayed.
        """
        self.reward_displayed = False
        while not self.reward_displayed:
            self.display_reward_options()
            self.reward_displayed = self.handle_reward_events()


    def pouch_rewards(self):
        """
        Calculate the rewards based on the rarity level of the pouch.

        Uses weighted random choices to determine the rarity of the pouch and calculates
        the reward amount.

        Returns:
            tuple: A tuple containing the amount of reward and the rarity level as a string.
        """
        #Different weightings for different rarities
        #Rarer pouches give more money
        rarity = random.choices(
            ["common", "uncommon", "rare", "ultra-rare"],
            weights=[50, 30, 15, 5],
            k=1)[0]
        lower_limit = 5
        upper_limit = 10
        if rarity == "common":
            #Common rewards give between 5 and 10
            return random.randint(lower_limit,upper_limit), rarity
        elif rarity == "uncommon":
            #Uncommon rewards give between 10 and 15
            return random.randint(lower_limit+5, upper_limit+5), rarity
        elif rarity == "rare":
            #Rare rewards give between 15 and 20
            return random.randint(lower_limit+10, upper_limit+10), rarity
        elif rarity == "ultra-rare":
            #Ultra-rare rewards give between 20 and 25
            return random.randint(lower_limit+15, upper_limit+15), rarity

    def display_reward_options(self):
        """Display the reward options on the screen, centered in the middle."""
        #Clear background and display reward if not clicked
        self.__display.blit(self.__bg, (0, 0))
        if not self.reward_displayed:
            self.__display.blit(self.__pouch_image, (DISPLAY_DIMENSIONS_X // 2 - self.__pouch_image.get_width() // 2,
                                                DISPLAY_DIMENSIONS_Y // 2 - self.__pouch_image.get_height() // 2))
        pyg.display.update()

    def handle_reward_events(self):
        """
        Handles events specifically when in the reward room state.

        Returns:
            bool: Returns True if the reward has been displayed, False if the game should quit.
        """
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                return False
            if event.type == pyg.MOUSEBUTTONDOWN:
                self.handle_click(event)
                if self.reward_displayed:
                    return True
        return False
    def handle_click(self, event):
        """
        Handle mouse click events within the reward room UI.

        Parameters:
            event (pyg.event.Event): The event to handle, typically a mouse click.
        """
        #Check for click on image and display reward if so
        if event.type == pyg.MOUSEBUTTONDOWN and event.button == 1:
            pouch_rect = self.__pouch_image.get_rect(center=(DISPLAY_DIMENSIONS_X // 2, DISPLAY_DIMENSIONS_Y // 2))
            if pouch_rect.collidepoint(event.pos):
                self.display_reward()

    def display_reward(self):
        """
        Display the rewards to the player

        This method retrieves a reward based on the pouch's rarity, updates the player's balance,
        and shows the reward message on the screen.
        """
        self.__display.blit(self.__bg, (0, 0))
        reward_value, rarity = self.pouch_rewards()  #Adjust rarity as needed
        self.update_player(reward_value)
        self.reward_text = f"Reward: {reward_value}! (Rarity: {rarity.capitalize()})"
        self.reward_displayed = True
        self.__message_text = Text(self.__display, OFF_WHITE, text_font(40), self.reward_text, DISPLAY_DIMENSIONS_X // 2, DISPLAY_DIMENSIONS_Y // 2)
        self.__message_timer = pyg.time.get_ticks()
        while self.__message_text and (pyg.time.get_ticks() - self.__message_timer < self.__message_duration):
            self.__message_text.draw_self()
            pyg.display.update()

    def update_player(self, reward_value):
        """
        Update player data based on collected rewards.

        Parameters:
            reward_value (int): The amount of reward to add to the player's balance.
        """
        self.__player.balance = reward_value
        print(self.__player.balance)