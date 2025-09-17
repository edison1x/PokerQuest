import pygame as pyg
from CONSTANTS import DISPLAY_DIMENSIONS_X,DISPLAY_DIMENSIONS_Y, ROYAL_BLUE, OFF_WHITE
from typing import override


class UI:
    """
    This manages the common properties and functions of UI components, such as displaying and handling events.

    Attributes:
        _display (pyg.Surface): The Pygame surface on which UI elements are drawn.
        _width (int): The width of the UI element.
        _height (int): The height of the UI element.
        _x_pos (int): The x coordinate of the UI element's position.
        _y_pos (int): The y coordinate of the UI element's position.
        __children (list): A list of child UI elements.
    """
    def __init__(self, display, x_pos, y_pos):
        """
        Initialises the UI component with display surface and position.

        Parameters:
            display (pyg.Surface): The Pygame surface on which the UI will be drawn.
            x_pos (int): The x-coordinate of the UI element's position.
            y_pos (int): The y-coordinate of the UI element's position.
        """
        self._display = display
        self._width = DISPLAY_DIMENSIONS_X
        self._height = DISPLAY_DIMENSIONS_Y
        self._x_pos = x_pos
        self._y_pos = y_pos
        self._children = []
        self._text = None
    def add_child(self, child):
        """
        Add a child UI element to this UI component.

        Parameters:
            child (UI): The child UI element to add.
        """
        self._children.append(child)

    def remove_child(self, child):
        """
        Remove a child UI element from this UI component.

        Parameters:
            child (UI): The child UI element to remove.
        """
        self._children.remove(child)

    def draw(self):
        """Draw the UI element and all its children on the display."""
        self.draw_self()
        for child in self._children:
            child.draw_self()

    def draw_self(self):
        """Protected method to be overridden by subclasses to draw the specific UI element."""
        pass

    def handle_event(self, event):
        """
        Iterates through all the children so they can handle an event.

        Parameters:
            event (pygame.event.Event): The event to handle.
        """
        for child in self._children:
            child.handle_event(event)

    def set_text(self, text):
        """
        Set the text to display in the text rectangle.

        Parameters:
            text (str): The text to display.
        """
        self._text = text
        if text == None:
            return 0

    @property
    def display(self):
        """
        Get the Pygame surface on which UI elements are drawn.

        Returns:
            pyg.Surface: The surface used for rendering UI elements.
        """
        return self._display

    @property
    def width(self):
        """
        Gets the width of the UI element.

        Returns:
            int: The width of the UI element
        """
        return self._width

    @width.setter
    def width(self, width):
        """
        Set the width of the UI element.

        Parameters:
            width (int): The new width to set for the UI elements.
        """
        self._width = width

    @property
    def height(self):
        """
        Get the height of the UI element.

        Returns:
            int: The current height of the UI element.
        """
        return self._height

    @height.setter
    def height(self, height):
        """
        Set the height of the UI element.

        Parameters:
            height (int): The new height to set for the UI element.
        """
        self._height = height

    @property
    def x_pos(self):
        """
        Get the x coordinate of the UI element's position.

        Returns:
            int: The x-coordinate of the UI element.
        """
        return self._x_pos

    @x_pos.setter
    def x_pos(self, x_pos):
        """
        Set the x coordinate of the UI element's position.

        Parameters:
            x_pos (int): The new x-coordinate for the UI element.
        """
        self._x_pos = x_pos

    @property
    def y_pos(self):
        """
        Get the y-coordinate of the UI element's position.

        Returns:
            int: The y-coordinate of the UI element.
        """
        return self._y_pos

    @y_pos.setter
    def y_pos(self, y_pos):
        """
        Set the y-coordinate of the UI element's position.

        Parameters:
            y_pos (int): The new y-coordinate for the UI element.
        """
        self._y_pos = y_pos

    @property
    def children(self):
        """
        Get the list of child UI elements.

        Returns:
            list: A list containing the child UI elements associated with this UI component.
        """
        return self._children


class Button(UI):
    """
    A UI button element that responds to clicks.

    Attributes:
        width (int): The width of the button
        height(int): The height of the button
        _button (pygame.Rect): The rectangle representing the button's position and size.
        _text (str): The text displayed on the button.
        _font (pygame.font.Font): The font used for the button text.
        _action (function): The function to call when the button is clicked.
    """
    def __init__(self, display, width, height, x_pos, y_pos, text, font, action):
        """
        Initialise a Button instance.

        Parameters:
            display (pygame.Surface): The surface on which the button will be drawn.
            width (int): The width of the button.
            height (int): The height of the button.
            x_pos (int): The x-coordinate of the button's position.
            y_pos (int): The y-coordinate of the button's position.
            text (str): The text to display on the button.
            font (pygame.font.Font): The font to use for the button text.
            action (function): The function to be called when the button is clicked.
        """
        super().__init__(display, x_pos, y_pos)
        self.width = width
        self.height = height
        self._text = text
        self._button = pyg.Rect(self.x_pos, self.y_pos, self.width, self.height)
        self._font = font
        self._action = action

    @override
    def draw_self(self):
        self._button = pyg.Rect(self.x_pos, self.y_pos, self.width, self.height) #If position of button changes then the rectangle changes pos
        pyg.draw.rect(self.display, ROYAL_BLUE, self._button)
        text_surface = self._font.render(self._text, True, OFF_WHITE)
        text_rect = text_surface.get_rect(center=(self.x_pos + self.width // 2, self.y_pos + self.height // 2))
        self.display.blit(text_surface, text_rect)

    @override
    def handle_event(self, event):
        if event.type == pyg.MOUSEBUTTONDOWN and event.button == 1:
            if (self.x_pos <= event.pos[0] <= self.x_pos + self.width) and (self.y_pos <= event.pos[1] <= self.y_pos + self.height):
                return self._action()

    @property
    def button(self):
        """
        Get the rectangle representing the button's position and size.

        Returns:
            pygame.Rect: The rectangle that defines the button's position and size.
        """
        return self._button


class TextRect(UI):
    """
    A UI element that displays a block of text within a rectangle.

    Attributes:
        width (int): The width of the TextRect
        height(int): The height of the TextRect
        _box_colour (pygame.Color): The background color of the text rectangle.
        _text_colour (pygame.Color): The color of the text.
        _font (pygame.font.Font): The font used for the text.
        _rect (pygame.Rect): The rectangle representing the text box's position and size.
        _text (str): The text to display.
    """
    def __init__(self, display, width, height, x_pos, y_pos, font, box_colour, text_colour, text):
        super().__init__(display, x_pos, y_pos)
        self.width = width
        self.height = height
        self._box_colour = box_colour
        self._text_colour = text_colour
        self._font = font
        self._rect = pyg.Rect(self.x_pos, self.y_pos, self.width, self.height)
        self._text = text

    def draw_self(self):
        """
        Draw the text rectangle and its text on the display.
        """
        pyg.draw.rect(self.display, self._box_colour, self._rect)
        text_surface = self._font.render(self._text, True, self._text_colour)
        text_width, text_height = text_surface.get_size()
        text_x = self.x_pos + (self.width - text_width) // 2
        text_y = self.y_pos + (self.height - text_height) // 2
        self.display.blit(text_surface, (text_x, text_y))

    def handle_event(self, event):
        pass

    @property
    def rect(self):
        """
        Get the rectangle representing the text box's position and size.
        """
        return self._rect

class Text(UI):
    """
    A UI element that displays text.

    Attributes:
        _width (int): The width of the TextRect
        _height(int): The height of the TextRect
        _text_colour (pygame.Color): The color of the text.
        _font (pygame.font.Font): The font used for the text.
        _text (str): The text to display.
    """
    def __init__(self, display, text_colour, font, text, x_pos, y_pos):
        super().__init__(display, x_pos, y_pos)
        self._width = 0
        self._height = 0
        self._text_colour = text_colour
        self._font = font
        self._text = text

    def draw_self(self):
        """Draw the text on the display for 1 second."""
        text_surface = self._font.render(self._text, True, self._text_colour)
        self._width, self._height = text_surface.get_size()
        self.display.blit(text_surface, (self._x_pos, self._y_pos))
        pyg.display.update()

    def handle_event(self, event):
        pass
