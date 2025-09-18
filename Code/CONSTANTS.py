import os
import pygame as pyg

code_path = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.dirname(code_path)
image_path = os.path.join(root_path, "Images")
cards_path = os.path.join(image_path, "cards")
jokers_path = os.path.join(image_path, "jokers")
background_path = os.path.join(image_path, "background.jpg")
text_font_path = os.path.join(root_path, "Roboto-Black.ttf")


rank_map_id = {
    "2": 0, "3": 1, "4": 2, "5": 3, "6": 4, "7": 5, "8": 6, "9": 7,
    "T": 8, "J": 9, "Q": 10, "K": 11, "A": 12,
}

rank_map_points = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
    "T": 10, "J": 10, "Q": 10, "K": 10, "A": 11,
}
suit_map = {
    "D": 0, "C": 1, "H": 2, "S": 3,
    "d": 0, "c": 1, "h": 2, "s": 3,
}

def text_font(size):
        return pyg.font.Font(text_font_path, size)

jokers = {}
DISPLAY_DIMENSIONS_Y = 900
DISPLAY_DIMENSIONS_X = 1500
DISPLAY_DIMENSIONS = (DISPLAY_DIMENSIONS_X, DISPLAY_DIMENSIONS_Y)
CARD_ANIMATION_DELAY = 500
CLICK_THRESHOLD = 300
BUTTON_WIDTH = DISPLAY_DIMENSIONS_X // 9
BUTTON_HEIGHT = DISPLAY_DIMENSIONS_Y // 15
BUTTON_SPACING = DISPLAY_DIMENSIONS_X // 100
TEXT_WIDTH = DISPLAY_DIMENSIONS_X // 6
TEXT_HEIGHT = DISPLAY_DIMENSIONS_Y // 15
CARD_DESCRIPTION_LENGTH = 2
OFF_WHITE = (240, 240, 240)
ROYAL_BLUE = (65, 105, 225)
GOLD = (239, 119, 4)
DARK_GREY = (45, 45, 45)
CARD_DIMENSIONS = (120, 180)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
UPGRADE_PRICE = 4
PLAYER_CARDS_X = DISPLAY_DIMENSIONS_X // 4
PLAYER_CARDS_Y_UNSELECTED = DISPLAY_DIMENSIONS_Y - (DISPLAY_DIMENSIONS_Y//2.7)
PLAYER_CARDS_Y_SELECTED = PLAYER_CARDS_Y_UNSELECTED - (DISPLAY_DIMENSIONS_Y // 5)
JOKER_CARDS_Y = DISPLAY_DIMENSIONS_Y // 10