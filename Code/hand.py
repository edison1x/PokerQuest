from .CONSTANTS import DISPLAY_DIMENSIONS_X

class Hand:
    """
    A class representing a player's hand of cards.

    Attributes:
        __cards (list): A list of Card objects in the hand.
        __display (pygame.Surface): The display surface for rendering the hand.
        __dragging_card (Card): The card currently being dragged.
    """
    def __init__(self, display):
        """
        Initialises a Hand object with an empty list of cards and a display surface.

        Parameters:
            display (pygame.Surface): The display surface for rendering the hand.
        """
        self.__cards = []
        self.__display = display
        self.__dragging_card = None

    def add_card(self, card):
        """
        Adds a card to the hand.

        Parameters:
            card (Card): The Card object to be added.
        """
        self.__cards.append(card)

    def remove_card(self, card):
        """
        Removes a card from the hand.

        Parameters:
            card (Card): The Card object to be removed.

        Returns:
            Card: The removed Card object.
        """
        self.__cards.remove(card)
        return card

    @property
    def cards(self):
        """
        Gets the list of cards in the hand

        Returns:
            list: The list of Card objects in the hand."""
        return self.__cards

    @property
    def dragging_card(self):
        """
        Gets the dragging card

        Returns:
            The Card object being dragged."""
        return self.__dragging_card

    @dragging_card.setter
    def dragging_card(self, card):
        """
        Sets the card currently being dragged.

        Parameters:
            card (Card): The Card object being dragged.
        """
        self.__dragging_card = card

    def clear(self):
        """Clears all cards from the hand."""
        self.__cards.clear()

    def display_hand(self, start_x, start_y, y_selected=None):
        """
        Displays the hand of cards on the screen, with the y coordinate being determined from if the card is selected or not.

        Parameters:
            start_x (int): The starting x-coordinate for the hand.
            start_y (int): The starting y-coordinate for the hand.
            y_selected (int, optional): The y-coordinate for selected cards. Defaults to None.
        """
        gap_between_cards = DISPLAY_DIMENSIONS_X // 192
        for cardpos, card in enumerate(self.__cards):
            #Cards currently being dragged shouldn't be drawn in its fixed position (it will be drawn using different logic)
            if card == self.__dragging_card:
                continue
            #Determine the x coordinates of a card based on the position of it in the Hand
            x_pos = start_x + cardpos * (card.image.get_width() + gap_between_cards)
            #Determine the y coordinates of a card based on if it has been selected or not
            if y_selected is not None and card.selected:
                y_pos = y_selected
            else:
                y_pos = start_y

            card.x = x_pos
            card.y = y_pos
            self.__display.blit(card.image, (x_pos, y_pos))

    def sort_by_rank(self):
        """Sorts the hand by rank, and by suit within each rank."""
        self.__cards.sort(key=lambda card: (card.id, card.suit), reverse=True)

    def sort_by_suit(self):
        """Sorts the hand by suit, and by rank within each suit."""
        #After sorting by suit the cards will be further sorted by rank
        self.__cards.sort(key=lambda card: (card.suit, card.id), reverse=True)

    def __len__(self):
        """
        Gets the number of cards currently in the hand

        Returns:
            The number of cards in the hand
        """
        return len(self.__cards)
