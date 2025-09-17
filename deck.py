import random
from playing_card import PlayingCard
from CONSTANTS import rank_map_id, suit_map

class Deck:
    """
    A class representing a standard deck of playing cards.

    Attributes:
        __base_deck (list): A list containing the original 52-card deck.
        __deck (list): A list containing the current shuffled deck.
    """
    def __init__(self):
        """Initialises a Deck object with a standard deck of 52 cards and shuffles it."""
        self.__base_deck = self._generate_base_deck()
        self.__deck = []

    def _generate_base_deck(self):
        """
        Generates a standard deck of 52 cards.

        Returns:
            list: A list containing the 52-card deck.

        """
        deck = []
        for rank in rank_map_id:
            for suit in suit_map:
                if suit.isupper():
                    deck.append(PlayingCard(f"{rank}{suit}"))
        return deck

    def reset_deck(self):
        """
        Resets the deck to the original base configuration and shuffles it.

        Raises:
            ValueError: If the base deck is not initialized.
        """
        self.__deck = list(self.__base_deck)
        self.shuffle()


    def shuffle(self):
        """
        Shuffles the deck in place.

        Raises:
            ValueError: If the deck is empty and cannot be shuffled.
        """
        if not self.__deck:
            raise ValueError("Deck is empty, cannot shuffle.")
        random.shuffle(self.__deck)

    def draw_from_top(self):
        """
        Deals a card from the top of the deck.

        Returns:
            PlayingCard: The dealt card object.

        Raises:
            ValueError: If there are no more cards to draw.
        """
        if not self.__deck:
            raise ValueError("No more cards in the deck")
        card = self.__deck.pop(0)
        return card

    def deal_cards(self, hand):
        """
        Deals a hand of 7 cards from the deck.

        Parameters:
            hand (Hand): The hand to be dealt.
        """
        while len(hand) < 7:
            card = self.draw_from_top()
            hand.add_card(card)

    @property
    def deck(self):
        """
        Gets the current deck of cards.

        Returns:
            list: The list of cards in the deck.
        """
        return self.__deck

    def __len__(self):
        """
        Gets the number of cards currently in the deck.

        Returns:
            int: The number of cards in the deck.
        """
        return len(self.__deck)
