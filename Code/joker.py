import pygame as pyg
import random
from typing import override
from card import Card
from CONSTANTS import (
    jokers_path,
    CARD_DIMENSIONS,
    DISPLAY_DIMENSIONS_X,
    code_path
)

def load_joker_descriptions():
    """
    Loads descriptions for the Joker cards from a file.
    Returns:
        dict: A dictionary with joker names as keys and their descriptions as values.
    """
    joker_descriptions = {}

    with open(f'{code_path}\\joker_descriptions.txt', 'r') as file:
        for line in file:
            if ':' in line:
                joker_name, description = line.strip().split(':', 1)
                joker_descriptions[joker_name.strip()] = description.strip()
    return joker_descriptions
joker_descriptions = load_joker_descriptions()

def get_joker_description(joker_name):
    """
    Gets the description for a specified joker.

    Parameters:
        joker_name (str): The name of the joker.

    Returns:
        str: The description of the joker.
    """
    return joker_descriptions.get(joker_name, "Description not found.")
#Abstract joker class

class JokerCard(Card):
    """
    A base class representing a Joker card.

    Attributes:
        id_count (int): A counter used to generate unique IDs for each Joker card.
        _card_name (str): The name of the card.
        _rarity (str): The rarity of the card.
        _weight (int): The weight used in selection of the card.
        price (int): The cost of the card
        _sell_value (int): The sell value of the card.
        _id (str): A unique identifier for the card.
        __image (pyg.Surface): The image representation of the card.
    """
    id_count = 1
    def __init__(self, card_name, rarity):
        """
        Initialises a new Joker card with the specified name and rarity.

        Parameters:
            card_name (str): The name of the card.
            rarity (str): The rarity level of the card.
        """
        super().__init__(card_name)
        self._card_name = card_name
        self._rarity = rarity
        self._weight = 0
        self.price = 0
        self._sell_value = 0
        self._id = self._generate_id()
        self.__image = pyg.image.load(f"{jokers_path}\\{card_name}.jpg")
        self.__image = pyg.transform.scale(self.__image, CARD_DIMENSIONS)

    @property
    def rect(self):
        """
        Gets the rectangle bounding the card's image, centred at the card's current position.

        Returns:
            pygame.Rect: The rectangle bounding the card's image.
        Raises:
            ValueError: If the card's coordinates are invalid.
        """
        if self._x is not None and self._y is not None:
            return self.__image.get_rect(topleft=(self._x, self._y))
        else:
            raise ValueError("Invalid coordinates for rect assignment.")

    def update_weight(self):
        """Updates the weight of the card based on its rarity."""
        #Same card rarity has the same weights, this is called when a new joker is instantiated to assign it a weight.
        rarity_weights = {"common": 5, "uncommon": 3, "rare": 1.5, "ultra-rare": 0.5}
        self._weight = rarity_weights.get(self._rarity, 0)

    def _generate_id(self):
        """
        Generates a unique ID for the Joker card.

        Returns:
            str: A unique identifier for the card.
        """
        #Create unique id's for potential to allow duplicates in the future
        unique_id = f"{self._card_name}-{JokerCard.id_count}"
        JokerCard.id_count += 1
        return unique_id

    def perform_ability(self, game_context):
        """
        Placeholder for Joker card's ability. To be overridden by subclasses.

        Parameters:
            game_context (object): The game context, used to access current game state.
        """
        pass

    @property
    def ability_text(self):
        """
        Placeholder for Joker card's ability description. To be overridden by subclasses.

        Returns:
            str: The ability description.
        """
        return ""

    @property
    def image(self):
        """
        Gets the image of the joker card

        Returns:
            The image of the joker card"""
        return self.__image

    def conditions(self, hand_cards):
        """
        Checks if any conditions for playing the Joker card are met.

        Returns:
            bool: True if conditions are met, otherwise False.
        """
        return True

    def reset_joker(self):
        """Resets any temporary state or attributes of the Joker card."""
        pass

#Joker cards
class MultiplierJoker(JokerCard):
    """A Joker card that increases the multiplier by a fixed amount."""
    def __init__(self, card_name, rarity):
        super().__init__(card_name, rarity)
        self._rarity = rarity
        self._multiplier = 5
        self.update_weight()
        self.price = 5
        self._sell_value = self.price//2

    @override
    def perform_ability(self, game_context):
        game_context.scoring_system.multiplier = self._multiplier + game_context.scoring_system.multiplier
        game_context.update_hand_multiplier_text()
        game_context.text_rects[5].draw_self()
        pyg.display.update()

    @override
    def ability_text(self):
        return f"+{self._multiplier} Multiplier"

class MoonJoker(JokerCard):
    """A Joker card that multiplies the current multiplier by a fixed amount."""
    def __init__(self, card_name, rarity):
        super().__init__(card_name, rarity)
        self._rarity = rarity
        self._multiplier = 4
        self.update_weight()
        self.price = 8
        self._sell_value = self.price/2

    @override
    def perform_ability(self, game_context):
        game_context.scoring_system.multiplier = self._multiplier * game_context.scoring_system.multiplier
        game_context.update_hand_multiplier_text()
        game_context.text_rects[5].draw_self()
        pyg.display.update()

    @override
    def ability_text(self):
        return f"x{self._multiplier} Multiplier"

class HeartSnakeJoker(JokerCard):
    """A Joker card that adds to the multiplier based on the number of Heart cards in the hand."""
    def __init__(self, card_name, rarity):
        super().__init__(card_name, rarity)
        self._rarity = rarity
        self._multiplier = 2
        self.update_weight()
        self.__number_heart_cards = 0
        self.price = 20
        self._sell_value = self.price//3

    @override
    def perform_ability(self, game_context):
        game_context.scoring_system.multiplier = game_context.scoring_system.multiplier*(self.__number_heart_cards*self._multiplier)
        game_context.update_hand_multiplier_text()
        game_context.text_rects[5].draw_self()
        pyg.display.update()
    @override
    def ability_text(self):
        return f"+{self._multiplier} Multiplier"

    @override
    def conditions(self, game_context):
        #Check if there are any hearts in the played hand, returning true if so.
        for card in game_context.hand_cards:
            if (card.suit).lower() == "h":
                self.__number_heart_cards += 1
        if self.__number_heart_cards > 0:
            return True
        return False

    @override
    def reset_joker(self):
        self.__number_heart_cards = 0

class CastleJoker(JokerCard):
    """A Joker card that adds 50 score and 2x multiplier for every king or queen in the hand."""
    def __init__(self, card_name, rarity):
        super().__init__(card_name, rarity)
        self._rarity = rarity
        self._extra_score = 50
        self._multiplier = 2
        self.update_weight()
        self.__number_of_cards = 0
        self.price = 40
        self._sell_value = self.price/4

    @override
    def perform_ability(self, game_context):
        game_context.scoring_system.hand_score = game_context.scoring_system.hand_score + (self.__number_of_cards*self._extra_score)
        game_context.scoring_system.multiplier = game_context.scoring_system.multiplier * (self.__number_of_cards*self._multiplier)
        game_context.update_hand_score_text()
        game_context.update_hand_multiplier_text()
        game_context.text_rects[4].draw_self()
        game_context.text_rects[5].draw_self()
        pyg.display.update()
    @override
    def ability_text(self):
        return f"+{self.__number_of_cards*self._extra_score} Score and x{self.__number_of_cards*self._multiplier}"

    @override
    def conditions(self, game_context):
        #Check if there are any kings or queens in the played hand, returning true if so.
        for card in game_context.hand_cards:
            if (card.rank).lower() == "k" or (card.rank).lower() == "q":
                self.__number_of_cards += 1
        if self.__number_of_cards > 0:
            return True
        return False

    @override
    def reset_joker(self):
        self.__number_of_cards = 0

#Joker cards management
class JokerHand:
    """
    Manages a player's Joker cards, allowing for display and interaction.

    Attributes:
        __joker_cards (list): A list of Joker cards.
        __display (pyg.Surface): The display surface for rendering the cards.
        __dragging_card (Joker): The card currently being dragged.
    """

    def __init__(self, display):
        self.__joker_cards = []
        self.__display = display
        self.__dragging_joker_card = None

    def add_joker(self, joker):
        """
        Adds a Joker card to the player's hand.

        Parameters:
            joker (Joker): The Joker card to be added.
        """
        self.__joker_cards.append(joker)

    def remove_joker(self, joker):
        """
        Removesa Joker card to the player's hand.

        Parameters:
            joker (Joker): The Joker card to be removed.
        """
        self.__joker_cards.remove(joker)

    def _show_joker_card(self, x, y, card, cardpos):
        """
        Displays a single Joker card at the specified position.

        Parameters:
            x (int): The x-coordinate for the card's position.
            y (int): The y-coordinate for the card's position.
            card (Joker): The Joker card to be displayed.
            cardpos (int): The position of the card in the player's hand.
        """
        gap_between_cards = DISPLAY_DIMENSIONS_X // 192
        if card != self.__dragging_joker_card:
            x = x + cardpos * (card.image.get_width() + gap_between_cards)
            card.x = x
            card.y = y
        self.__display.blit(card.image, (card.x, card.y))

    def display_hand(self, start_x, start_y):
        """
        Displays all Joker cards starting from the specified coordinates.

        Parameters:
            start_x (int): The starting x-coordinate.
            start_y (int): The starting y-coordinate.
        """
        for cardpos, card in enumerate(self.__joker_cards):
            self._show_joker_card(start_x, start_y, card, cardpos)

    @property
    def dragging_card(self):
        """
        Gets the dragging card

        Returns:
            The Card object being dragged."""
        return self.__dragging_joker_card

    @dragging_card.setter
    def dragging_card(self, card):
        """
        Sets the joker card currently being dragged.

        Parameters:
            card (Card): The Card object being dragged.
        """
        self.__dragging_joker_card = card

    @property
    def cards(self):
        """
        Gets the joker cards a player currently has

        Returns:
            The list of Joker cards.
        """
        return self.__joker_cards

class CategoryNode:
    """Represents a category of Joker cards (e.g., common, uncommon, etc.)."""
    def __init__(self, rarity, weight):
        self.rarity = rarity
        self.jokers = []
        self.weight = weight #Weight that will change depending on level
        self.base_weight = 0
        self.parent = None

    def add_joker_to_category(self, joker, weight):
        """
        Adds a Joker card to the category and updates its weight.

        Parameters:
            category (CategoryNode): The category to which the joker is added.
            joker (JokerCard): The Joker card being added.
            weight (int): The weight of the Joker card.
        """
        self.jokers.append(joker)
        self.weight += weight

    def remove_joker_from_category(self, joker, weight):
        self.jokers.remove(joker)
        self.weight -= weight

class JokerTree:
    """Manages a hierarchy of Joker card categories and allows weighted selection for the shop."""
    def __init__(self):
        self.root = CategoryNode("Root", 0)
        self.categories = {}

    def add_category(self, category_node):
        """
        Adds a category to the tree.

        Parameters:
            category_node (CategoryNode): The category node to add.
        """
        category_node.parent = self.root
        self.categories[category_node.rarity] = category_node
        self.update_weights(category_node)

    def add_joker(self, joker):
        """
        Adds a Joker card to the appropriate category based on its rarity and updates the weights.

        Parameters:
            joker (JokerCard): The Joker card to add.
        """
        if joker._rarity in self.categories:
            category = self.categories[joker._rarity]
            category.add_joker_to_category(joker, joker._weight)
            self.update_weights(category)

    def remove_joker(self, joker):
        if joker._rarity in self.categories:
            category = self.categories[joker._rarity]
            category.remove_joker_from_category(joker, joker._weight)
            self.update_weights(category)

    def update_weights(self, node):
        """
        Updates the cumulative weights of categories in the tree.

        Parameters:
            node (CategoryNode): The category node whose weights need to be updated.
        """
        #This method is called when a joker is added to the tree and it updates any parent categories weight recursively.
        while node:
            if node.parent:
                #Update parent's weight
                node.parent.weight = sum(category.weight for category in self.categories.values())
            node = node.parent  #Move up to update all ancestors up to root

    def weighted_select_joker(self):
        """
        Selects a Joker card based on weighted random selection.

        Returns:
            JokerCard: The randomly selected Joker card.
        """
        #Calculate the total cumulative weight across all categories and generate a random number within the range of the total weight.

        random_num = random.uniform(0, self.root.weight)
        #Now iterate through the categories to find the one corresponding to the random number.
        for category in self.categories.values():
            #If the random number is less than the category's cumulative weight then choose it.
            print(f"Category {category.rarity} has weights {category.weight}")
            if random_num < category.weight:
                joker = random.choice(category.jokers)
                self.remove_joker(joker)
                return joker #Returns a random joker in that category
            #Reduce randoom_num by the current category's cumulative weight, to look in the remaining range.
            random_num -= category.weight
        return None
