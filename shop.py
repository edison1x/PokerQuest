import pygame as pyg
import random
from ui import UI, Button, Text, TextRect
from joker import get_joker_description
from CONSTANTS import (
    DISPLAY_DIMENSIONS_X,
    DISPLAY_DIMENSIONS_Y,
    BUTTON_WIDTH ,
    BUTTON_HEIGHT ,
    BUTTON_SPACING ,
    OFF_WHITE,
    text_font,
    CARD_DIMENSIONS,
    UPGRADE_PRICE

)

class ShopRoom():
    """
    Class representing the shop room where players can purchase upgrades and Joker cards.

    This class manages the ui, handles player interactions, and processes purchases
    within the shop room.

    Attributes:
        __display (pyg.Surface): The surface for rendering the shop room.
        __bg (pyg.Surface): Background image for the shop room.
        __player (Player): The player object to manage player balance and items.
        __joker_deck (JokerDeck): The deck containing Joker cards.
        __scoring_system (ScoringSystem): The scoring system to manage hand upgrades.
        __UIManager (UI): The UI manager for handling UI elements.
        __purchase_joker_button (Button): Button to purchase the Joker card.
        __upgrade_hand_button (Button): Button to upgrade a hand.
        __joker (Joker): The Joker card selected for purchase.
        __joker_description (str): Description of the selected Joker card.
        __balance_text (Text): Text displaying the player's balance.
        __hand_to_upgrade (str): The hand selected for upgrading.
        __joker_purchased (bool): Flag indicating if a Joker card has been purchased.
        __hand_upgraded (bool): Flag indicating if the hand has been upgraded.
    """
    def __init__(self, display, bg, player, joker_deck, scoring_system):
        """
        Initialises the ShopRoom with display, background, player, joker deck, and scoring system.

        Parameters:
            display (pyg.Surface): The surface for rendering the shop room.
            bg (pyg.Surface): The background image for the shop room.
            player (Player): The player object to manage balance and inventory.
            joker_deck (JokerDeck): The deck containing Joker cards.
            scoring_system (ScoringSystem): The system for managing scoring and upgrades.
        """
        self.__display = display
        self.__bg = bg
        self.__player = player
        self.__joker_deck = joker_deck
        self.__scoring_system = scoring_system


    def setup_ui(self):
        """
        Sets up the ui for the shop room.

        This method initialises buttons and text elements for purchasing Jokers,
        upgrading hands, and displaying player balance.
        """
        #Setup buttons and text
        start_x = (DISPLAY_DIMENSIONS_X - 2 * (BUTTON_WIDTH + BUTTON_SPACING)) // 2
        self.__UIManager = UI(self.__display, x_pos=0, y_pos=0)
        self.__purchase_joker_button = Button(self.__display, BUTTON_WIDTH, BUTTON_HEIGHT, (DISPLAY_DIMENSIONS_X - 2 * (BUTTON_WIDTH + BUTTON_SPACING)) // 2 + BUTTON_WIDTH + BUTTON_SPACING, DISPLAY_DIMENSIONS_Y // 1.2 - 10 - BUTTON_HEIGHT, "Purchase Joker", text_font(15), self.purchase_joker)
        self.__hand_to_upgrade = random.choice(list(self.__scoring_system.base_hand_score_multiplier.keys()))

        next_button = Button(self.__display, BUTTON_WIDTH, BUTTON_HEIGHT, start_x , DISPLAY_DIMENSIONS_Y // 1.2, "Next", text_font(20), self.next)
        text = f"Upgrade Hand: {self.__hand_to_upgrade}"
        self.__upgrade_hand_button = Button(self.__display, 2*BUTTON_WIDTH, BUTTON_HEIGHT, DISPLAY_DIMENSIONS_X/ 3.5, DISPLAY_DIMENSIONS_Y // 1.2 - 10 - BUTTON_HEIGHT, text, text_font(20), self.upgrade_hand)
        #Randomly choose a joker from the tree
        self.__joker_to_buy = self.__joker_deck.weighted_select_joker()
        self.__joker_description = get_joker_description(self.__joker_to_buy._card_name)
        self.__joker_text = Text(self.__display, OFF_WHITE, text_font(15), self.__joker_description, DISPLAY_DIMENSIONS_X/2 , DISPLAY_DIMENSIONS_Y/2 + CARD_DIMENSIONS[1])
        #button will appear below joker
        self.__sell_joker_button = Button(self.__display, BUTTON_WIDTH, BUTTON_HEIGHT, 0, 0, f"Sell Joker for value", text_font(15), self.sell_joker)
        self.__joker_to_sell = None
        self.__player_balance = f"BALANCE: {str(self.__player.balance)}"
        self.__balance_text = Text(self.__display, OFF_WHITE, text_font(20), self.__player_balance, DISPLAY_DIMENSIONS_X/2 , BUTTON_HEIGHT)

        self.__UIManager.add_child(next_button)
        self.__UIManager.add_child(self.__joker_text)
        self.__UIManager.add_child(self.__balance_text)
        self.__UIManager.add_child(self.__upgrade_hand_button)

        self.__joker_purchased = False
        self.__hand_upgraded = False

        self.__message_text = None
        self.__message_duration = 1000
        self.__message_timer = 0

    def reset_items(self):
        """
        Resets the items available in the shop for a new round.

        This method randomly selects a new hand to upgrade and a new Joker card to purchase.
        """
        self.__hand_to_upgrade = random.choice(list(self.__scoring_system.base_hand_score_multiplier.keys()))
        self.__joker_to_buy = self.__joker_deck.weighted_select_joker()
        self.__joker_description = get_joker_description(self.__joker_to_buy._card_name)

    def start_new_shop(self, level):
        """
        Initialises a new shop.

        Parameters:
            level (int): The level or stage that initiated this shop session.
        """

        self.__running = True
        #Update Joker weights so in later levels player will have better chance of better jokers
        for category in self.__joker_deck.categories.values():
            if category.rarity == "common":
                category.weight = category.base_weight * (1 - 0.01 * level)  #Decrease common weight by 1% each level
            elif category.rarity == "uncommon":
                category.weight = category.base_weight * (1 - 0.005 * level)  #Decrease uncommon weight by 0.5% each level
            elif category.rarity == "rare":
                category.weight = category.base_weight * (1 + 0.01 * level)  #Increase rare weight by 1% each level
            elif category.rarity == "ultra-rare":
                category.weight = category.base_weight * (1 + 0.005 * level)  #Increase ultra-rare weight by 0.5% each level

        self.setup_ui()
        self.update_ui() #Load ui here because needs event to occur to update in loop
        self.shop_loop()

    def shop_loop(self):
        """ Main loop for handling the shop's event processing and rendering."""
        while self.__running:
            event_occured = self.handle_events()
            if event_occured:
                self.update_ui()
            else:
                continue

    def upgrade_hand(self):
        """
        Handles the upgrade of the player's hand.

        This method checks if the player has enough balance to upgrade their hand,
        processes the upgrade, and updates the ui accordingly.
        """
        #Default upgrade price
        if self.__player.balance >= UPGRADE_PRICE and not self.__hand_upgraded:
            #Update balance and hand level and display text
            self.__player.balance = -UPGRADE_PRICE
            self.__scoring_system.upgrade_hand_level(self.__hand_to_upgrade)
            self.__hand_upgraded = True
            self.__UIManager.remove_child(self.__upgrade_hand_button)
            text = f"Upgraded {self.__hand_to_upgrade} for 2!"
            self.__message_text = Text(self.__display, OFF_WHITE, text_font(20), text, DISPLAY_DIMENSIONS_X/3, DISPLAY_DIMENSIONS_Y/3- CARD_DIMENSIONS[1]/8)
            self.__message_timer = pyg.time.get_ticks()

    def purchase_joker(self):
        """
        Handles the purchase of the Joker card.

        This method checks if the player can afford the Joker, processes the purchase,
        and updates the ui accordingly. Displays a success or failure message.
        """
        if len(self.__player.joker_hand.cards) < 5: #Pllayer can have at most 5 joker cards
            if self.__player.balance >= self.__joker_to_buy.price and not self.__joker_purchased:
                #Update the balance and the player's joker cards
                self.__player.balance = -self.__joker_to_buy.price #Pass in the negative value, setter in player will then minus it.
                self.__player.joker_hand.add_joker(self.__joker_to_buy)
                self.__joker_purchased = True

                if self.__purchase_joker_button in self.__UIManager.children:
                        self.__UIManager.remove_child(self.__purchase_joker_button)
                if self.__joker_text in self.__UIManager._children:
                    self.__UIManager.remove_child(self.__joker_text)
                text = f"Purchased {self.__joker_to_buy._card_name} for {self.__joker_to_buy.price}!"
                self.__message_text = Text(self.__display, OFF_WHITE, text_font(20), text, DISPLAY_DIMENSIONS_X/2, DISPLAY_DIMENSIONS_Y/2 - CARD_DIMENSIONS[1]/8)
                self.__message_timer = pyg.time.get_ticks()
                self.__joker_to_buy = None
            else:
                text = "Insufficient balance!"
                self.__message_text = Text(self.__display, OFF_WHITE, text_font(20), text, DISPLAY_DIMENSIONS_X/2, DISPLAY_DIMENSIONS_Y/2 - CARD_DIMENSIONS[1]/8)
                self.__message_timer = pyg.time.get_ticks()
        else:
            text = "Max joker limit reached!"
            self.__message_text = Text(self.__display, OFF_WHITE, text_font(20), text, DISPLAY_DIMENSIONS_X/2, DISPLAY_DIMENSIONS_Y/2 - CARD_DIMENSIONS[1]/8)
            self.__message_timer = pyg.time.get_ticks()

    def sell_joker(self):
        """Sells a joker, removing it from a player's hand and increases their balance"""
        self.__player.joker_hand.remove_joker(self.__joker_to_sell)
        self.__player.balance = self.__joker_to_sell._sell_value
        if self.__sell_joker_button in self.__UIManager.children:
            self.__joker_to_sell = None
            self.__UIManager.remove_child(self.__sell_joker_button)


    def next(self):
        """Closes the shop room. Returns back to the map"""
        self.__running = False

    def handle_events(self):
        """
        Handles events within the shop room.

        This method processes mouse button events and triggers actions accordingly.

        Returns:
            bool: Returns True if an event was handled, otherwise False.
        """
        for event in pyg.event.get():
            if event.type == pyg.MOUSEBUTTONUP and event.button == 1:
                mouse_pos = pyg.mouse.get_pos()
                self.handle_click_on_joker(mouse_pos)
                self.handle_event(pyg.event.Event(pyg.MOUSEBUTTONDOWN, pos=mouse_pos, button=1))
                return True
            return False

    def handle_click_on_joker(self, mouse_pos):
        """
        Checks for clicks on the Joker card.

        If the Joker is clicked and not purchased, it toggles the purchase button.

        Parameters:
            mouse_pos (tuple): The (x, y) coordinates of the mouse click.
        """
        #Check for click on the joker to buy image
        if self.__joker_to_buy:
            if self.__joker_to_buy.rect.collidepoint(mouse_pos) and not self.__joker_purchased:
                if self.__purchase_joker_button in self.__UIManager.children:
                    self.__UIManager.remove_child(self.__purchase_joker_button)
                else:
                    self.__UIManager.add_child(self.__purchase_joker_button)
                return

        #Check for click on joker cards in the player's hand
        for joker in self.__player.joker_hand.cards:
            if joker.rect.collidepoint(mouse_pos):
                self.__sell_joker_button.set_text(f"Sell Joker for {joker._sell_value}")
                self.__sell_joker_button.x_pos = joker.x
                self.__sell_joker_button.y_pos = joker.y + BUTTON_HEIGHT + 100
                if self.__sell_joker_button in self.__UIManager.children:
                    self.__joker_to_sell = None
                    self.__UIManager.remove_child(self.__sell_joker_button)
                else:
                    self.__joker_to_sell = joker
                    self.__UIManager.add_child(self.__sell_joker_button)
                return

    def handle_event(self, event):
        """
        Handles UI events for child elements.

        Parameters:
            event (pygame.event.Event): The event to be handled.
        """
        for child in self.__UIManager.children:
                child.handle_event(event)

    def update_ui(self):
        """
        Updates the ui for the shop room.

        This method redraws the background, updates the balance text,
        and renders all UI elements.
        """
        self.__display.blit(self.__bg, (0, 0))
        if not self.__joker_purchased:
            self.__joker_to_buy.x = DISPLAY_DIMENSIONS_X/2
            self.__joker_to_buy.y = DISPLAY_DIMENSIONS_Y/2
            self.__display.blit(self.__joker_to_buy.image, (DISPLAY_DIMENSIONS_X/2, DISPLAY_DIMENSIONS_Y/2))
        self.__player.joker_hand.display_hand(DISPLAY_DIMENSIONS_X // 4, DISPLAY_DIMENSIONS_Y // 10)
        current_balance = f"BALANCE: {str(self.__player.balance)}"

        if self.__message_text and (pyg.time.get_ticks() - self.__message_timer < self.__message_duration):
            self.__message_text.draw_self()
        self.__balance_text.set_text(current_balance)
        self.__UIManager.draw()
        pyg.display.update()

