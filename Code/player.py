from .joker import JokerHand
from .deck import Deck



class Player:
    """
    A class representing a player in the game.

    This class manages the player's score, balance, hands, and card deck.
    It allows for the handling of hands, discards, and maintaining a joker hand.

    Attributes:
        __current_score (int): The current score of the player.
        __balance (int): The player's balance, starting at 5.
        __base_number_of_hands (int): The base number of hands the player can play.
        __number_of_hands_left (int): The number of hands left for the player to play.
        __base_number_of_discards (int): The base number of discards available to the player.
        __number_of_discards_left (int): The number of discards left for the player.
        __player_deck (Deck): The deck of cards available to the player.
        __player_joker_hand (JokerCards): The joker hand held by the player.

    Parameters:
        display (object): The display object for rendering the joker hand.
    """
    def __init__(self, display):
        self.__current_score = 0
        self.__balance = 5
        self.__base_number_of_hands = 5
        self.__number_of_hands_left = self.__base_number_of_hands
        self.__base_number_of_discards = 3
        self.__number_of_discards_left = self.__base_number_of_discards
        self.__player_deck = Deck()
        self.__player_joker_hand = JokerHand(display)

    @property
    def joker_hand(self):
        """
        Returns the player's joker hand object.

        Returns:
            JokerCards: The joker hand of the player.
        """
        return self.__player_joker_hand

    @property
    def deck(self):
        """
        Returns the player's deck instance.

        Returns:
            Deck: The player's deck.
        """
        return self.__player_deck

    @property
    def balance(self):
        """
        Returns the player's current balance.

        Returns:
            int: The current balance of the player.
        """
        return self.__balance

    @balance.setter
    def balance(self, value):
        """
        Updates the player's balance by adding the specified value.

        Parameters:
            value (int): The value to add to the current balance.
        """
        self.__balance += value

    @property
    def current_score(self):
        """
        Returns the player's current score.

        Returns:
            int: The current score of the player.
        """
        return self.__current_score

    @current_score.setter
    def add_to_current_score(self, score):
        """
        Adds the specified score to the player's current score.

        Parameters:
            score (int): The score to be added.
        """
        self.__current_score += score

    def reset_score(self):
        """Resets the player's current score to zero."""
        self.__current_score = 0

    def reset_deck(self):
        """Resets the player's deck to its initial state."""
        self.__player_deck.reset_deck()

    @property
    def number_of_hands_left(self):
        """
        Gets the number of hands left.

        Returns:
            int: The number of hands left for the player.
        """
        return self.__number_of_hands_left

    @number_of_hands_left.setter
    def number_of_hands_left(self, num):
        """
        Decreases the number of hands left by the specified amount if possible.

        Parameters:
            num (int): The number of hands to reduce.
        """
        if self.__number_of_hands_left > 0:
            self.__number_of_hands_left -= num

    def reset_number_of_hands(self):
        """Resets the number of hands left to the base number."""
        self.__number_of_hands_left = self.__base_number_of_hands

    @property
    def number_of_discards_left(self):
        """
        Gets the number of discards left.

        Returns:
            int: The number of discards left for the player.
        """
        return self.__number_of_discards_left

    @number_of_discards_left.setter
    def number_of_discards_left(self, num):
        """
        Decreases the number of discards left by the specified amount if possible.

        Parameters:
            num (int): The number of discards to reduce.
        """
        if self.__number_of_discards_left > 0:
            self.__number_of_discards_left -= num

    def reset_number_of_discards(self):
        """Resets the number of discards left to the base number."""
        self.__number_of_discards_left = self.__base_number_of_discards

    def start_round(self):
        self.reset_score()
        self.reset_number_of_hands()
        self.reset_number_of_discards()
        self.reset_deck()




