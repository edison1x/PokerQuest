import pygame as pyg
from typing import override
from card import Card
from CONSTANTS import (
    cards_path,
    DISPLAY_DIMENSIONS_X,
    DISPLAY_DIMENSIONS_Y,
    rank_map_id,
    suit_map,
)

rank_reverse_map = {value: key for key, value in rank_map_id.items()}
suit_reverse_map = {value: key for key, value in suit_map.items() if key.islower()}

class PlayingCard(Card):
    """
    A class representing a playing card.

    Attributes:
        __id (int): A unique identifier for the card, generated based on its rank and suit.
        __image (pygame.Surface): The image representation of the card.
        __selected (bool): True if card is selected. False if not.
        __x (int): The x-coordinate position of the card on the screen.
        __y (int): The y-coordinate position of the card on the screen.
    """

    def __init__(self, card):
        """
        Initialises a Card object with the notation (e.g., '2H' for 2 of Hearts).
        The card image is loaded and scaled to predefined dimensions.

        Parameters:
            card (str): The card notation consisting of rank and suit (e.g., '2H').
        """
        super().__init__(card)
        self.__id = self.create_id(card)
        self.__image = pyg.image.load(f"{cards_path}\\{self.rank}{self.suit}.png")
        self.__image = pyg.transform.scale(self.__image, (DISPLAY_DIMENSIONS_X//16, DISPLAY_DIMENSIONS_Y//6))

    @property
    def id(self):
        """
        Gets the unique identifier of the card

        Returns:
            int: The unique identifier of the card
        """
        return self.__id

    @override
    def create_id(self, card):
        """"
        Creates a unique identifier for the card based on its rank and suit.

        Parameters:
            card (str): The card notation consisting of rank and suit.

        Returns:
            int: The unique identifier of the card.
        """
        #Extract the rank (first character) and suit (last character) from the card
        rank = card[0]
        suit = card[1]
        #Get the numeric ID associated with the rank and suit from predefined maps
        rank_id = rank_map_id[rank]
        suit_id = suit_map[suit]
        #Calculate a unique ID for the card by combining the rank and suit IDs
        return rank_id * 4 + suit_id

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
    @property
    def image(self):
        """
        Gets the image of the card

        Returns:
            image of the card"""
        return self.__image

    @property
    def rank(self):
        """
        Gets the rank of the card.

        Returns:
            str: The rank of the card.
        """
        return rank_reverse_map[self.__id // 4]

    @property
    def suit(self):
        """
        Gets the suit of the card.

        Returns:
            str: The suit of the card.
        """
        return suit_reverse_map[self.__id % 4]

    def __str__(self):
        """
        Returns a string representation of the card.

        Returns:
            str: The card notation (e.g., '2H' for 2 of Hearts).
        """
        return f"{self.rank.upper()}{self.suit.upper()}"

