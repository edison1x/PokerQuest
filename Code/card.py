from CONSTANTS import DISPLAY_DIMENSIONS_X, DISPLAY_DIMENSIONS_Y

class Card:
    """
    An abstract class for a playing card and joker card.

    Attributes:
        _id (int)- uniquely identifies a card
        _selected (boolean) - If a card is selected then True else False
        _x (int)- the x coordinates of the card
        _y (int)- the y coordiantes of the card
        __image - the image of the card
    """
    def __init__(self, card):
        """
        Initialises a new Card instance.

        Parameters:
            card (str): The card notation (rank and suit) to create a unique ID.
        """
        self._id = self.create_id(card)
        self._selected = False
        self._x = 0
        self._y = 0

    def get_rect(self):
        """Gets the rectangle bounding the card's image, centred at the card's current position."""
        pass

    def id(self):
        """
        Gets the ID of the card.

        Returns:
            int: The unique identifier of the card."""
        return self._id

    def create_id(self, card):
        """"
        Creates a unique identifier for the card based on its rank and suit.

        Parameters:
            card (str): The card notation consisting of rank and suit.

        Returns:
            int: The unique identifier of the card.
        """
        pass


    @property
    def x(self):
        """
        Gets the x coordinate of the card.

        Returns:
            int: The x coordinate position of the card.
        """
        return self._x

    @x.setter
    def x(self, value):
        """
        Sets the x coordinate position of the card, ensuring it is within the display dimensions.

        Parameters:
            value (int) The new x coordinate position.

        Raises:
            ValueError: If the value is negative or exceeds the display width.
        """
        self._x = max(0, min(value, DISPLAY_DIMENSIONS_X - DISPLAY_DIMENSIONS_Y // 16))

    @property
    def y(self):
        """
        Gets the y coordinate of the card.

        Returns:
            int: The y coordinate position of the card.
        """
        return self._y

    @y.setter
    def y(self, value):
        """
        Sets the y coordinate of the card, ensuring it is within the display dimensions.

        Parameters:
            value (int): The new y coordinate position.
        Raises:
            ValueError: If the value is negative or exceeds the display height.
        """
        self._y = max(0, min(value, DISPLAY_DIMENSIONS_Y - DISPLAY_DIMENSIONS_Y // 6))

    @property
    def selected(self):
        """
        Checks if the card is selected.

        Returns:
            bool: True if the card is selected, False otherwise.
        """
        return self._selected

    def toggle_selected(self):
        """
        Toggles the selection status of the card.
        """
        self._selected = not self._selected
