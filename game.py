import sys
import random
import pygame as pyg
from dealerroom import DealerRoom
from reward import RewardRoom
from shop import ShopRoom
from player import Player
from map import MapGenerator, MapVisualiser
from dealer import Dealers
from poker import DefaultScoringStrategy
from CONSTANTS import DISPLAY_DIMENSIONS, DISPLAY_DIMENSIONS_Y, background_path, cards_path
from joker import (
    JokerTree,
    CategoryNode,
    MultiplierJoker,
    MoonJoker,
    HeartSnakeJoker,
    CastleJoker
)

class DisplaySetup:
    """
    Sets up the display and initialises the Pygame environment.

    Attributes:
        __background_img (Surface): Background image for the display.
        __main_clock (Clock): Main clock controlling the frame rate.
        __display (Surface): The Pygame display surface.
        __icon (Surface): Icon for the Pygame window.
    """
    def __init__(self):
        pyg.init()
        self.__background_img = pyg.image.load(background_path)
        self.__main_clock = pyg.time.Clock()
        self.__display = pyg.display.set_mode(DISPLAY_DIMENSIONS)
        self.__icon = pyg.image.load(f"{cards_path}\\AS.png")

        pyg.display.set_icon(self.__icon)
        pyg.display.set_caption("Prototype")

    @staticmethod
    def exit():
        """Exits the Pygame environment and closes the application."""
        sys.exit()

    @property
    def main_clock(self):
        """Returns the main clock for controlling the frame rate."""
        return self.__main_clock
    @property
    def display(self):
        """Returns the Pygame display surface."""
        return self.__display
    @display.setter
    def display(self, display):
        """Sets the Pygame display surface."""
        self.__display = display

    @property
    def background_image(self):
        """Returns the background image for the display."""
        return self.__background_img

class Game:
    """
    Manages the game state and flow.

    Attributes:
        __display_setup (DisplaySetUp): The display setup instance.
        __game_state (str): The current state of the game (e.g. map, main_game, shop_room).
        __player (Player): The player instance.
        __dealers (Dealers): Contains the three types of dealers
        __dealer_type (Dealer): The current dealer type.
        __scoring_system (DefaultScoringStrategy): The scoring system instance
        __joker_deck (JokerTree): The deck of jokers.
        __map_generator (MapGenerator): The map generator instance.
        __current_node (Node): The current node in the map.
        __map_visualiser (MapVisualiser): The visualiser for the map.
    """
    def __init__(self):
        self.__display_setup = DisplaySetup()
        self.__game_state = "map"
        self.__player = Player(self.__display_setup.display)
        self.__dealers = Dealers()
        self.__dealer_type = None
        self.__scoring_system = DefaultScoringStrategy()
        self.__joker_deck = JokerTree()
        self.__rooms = Rooms(self.__display_setup.display, self.__display_setup,
                             self.__player, self.__scoring_system, self.__joker_deck)
        self.setup_joker_deck()

        self.__map_generator = MapGenerator()
        self.__current_node = self.__map_generator.starting_node
        self.__map_visualiser = MapVisualiser(self.__map_generator, self.__display_setup.display)

    def game_loop(self):
        """The main loop of the game that manages the game state and updates the display."""
        while True:
            if self.__game_state == "map":
                #Visualise the graph and check for clicks
                self.handle_map_events()
                self.__map_visualiser.visualise_graph(self.__current_node)
            elif self.__game_state == "main_game":
                player_wins = self.__current_node.visit(self.__rooms, self.__map_visualiser.current_level, self.__dealer_type)
                if player_wins:
                    #Player won so update completed nodes and the current level
                    self.__map_visualiser.completed_nodes.append(self.__current_node)
                    self.__map_visualiser.current_level += 1
                    #Check if player completed the first boss (level 11)
                    if self.__current_node.level == 22:
                        print("Congratulations! You've completed the game!")
                    #Player continues to the shop room now
                else:
                    sys.exit()
                self.__game_state = "shop_room"
            elif self.__game_state == "reward_room":
                self.__rooms.reward_room.start_new_reward()
                #Player has collected reward so update completed nodes and the current level
                self.__map_visualiser.current_level += 1
                self.__map_visualiser.completed_nodes.append(self.__current_node)
                #Player has finished in the reward room and goes back to map
                self.__game_state = "map"
            elif self.__game_state == "shop_room":
                self.__rooms.shop_room.start_new_shop(self.__map_visualiser.current_level)
                #Player has finished in the shop and goes back to map
                self.__game_state = "map"

            pyg.display.flip()
            self.__display_setup.main_clock.tick(30)

    def handle_map_events(self):
        """Handles events related to the map, such as clicks and quitting the game."""
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                self.__display_setup.exit()
            elif event.type == pyg.MOUSEBUTTONDOWN:
                clicked_room = self.__map_visualiser.handle_click(event.pos)
                #Check if a room was clicked on
                if clicked_room:
                    self.handle_room_click(clicked_room)
            elif event.type == pyg.MOUSEWHEEL:
                scroll = 0.1 * DISPLAY_DIMENSIONS_Y
                if event.y == 1: #Scroll up
                    if self.__map_visualiser.scroll_level > 0: #Ensure we cannot scroll above starting node
                        self.__map_visualiser.scroll_level -=1
                elif event.y == -1:
                    if self.__map_visualiser.scroll_level < 13: #Ensure we cannot scroll below endnode
                        print(self.__map_visualiser.scroll_level)
                        self.__map_visualiser.scroll_level +=1




    def handle_room_click(self, clicked_room):
        is_valid_move = False
        #Only allow clicking the starting node if no rooms completed
        if not clicked_room.visited and clicked_room.level == 0:
            is_valid_move = True
        else:
            #Check if clicked room is valid (connected to the last completed room)
            if self.__map_visualiser.completed_nodes:
                last_completed = self.__map_visualiser.completed_nodes[-1]
                if clicked_room in last_completed.edges and clicked_room.level > last_completed.level:
                    is_valid_move = True

        if is_valid_move:
            self.__current_node = clicked_room
            if self.__current_node.room_type == "D":
                #Default dealer room
                self.__game_state = "main_game"
                self.__dealer_type = self.__dealers.default_dealer
            elif self.__current_node.room_type == "?":
                #Random room that has a chance of being a reward, small boss or a big boss
                self.__game_state = self.randomly_pick_room()
                if self.__game_state == "main_game":
                    #main_game state was selected so randomly decide if it is a small boss or big boss dealer
                    self.__dealer_type = random.choice((self.__dealers.small_boss_dealer, self.__dealers.big_boss_dealer))
            elif self.__current_node.room_type == "R":
                #Reward room
                self.__game_state = "reward_room"
            elif self.__current_node.room_type == "B":
                #Big boss room
                self.__game_state = "main_game"
                self.__dealer_type = self.__dealers.big_boss_dealer

    def randomly_pick_room(self):
        """
        Randomly selects a room type based on previous choices.

        Returns:
            str: Chosen room type ("reward_room" or "main_game").
        """
        default_reward_weight = 0.3
        default_main_weight = 0.7
        reward_weight = default_reward_weight
        main_weight = default_main_weight

        #Adjustment factors based on the number of recent rooms (up to 3). Most recent rooms have most weight.
        if len(self.__rooms.recent_random_rooms) == 1:
            adjustment_factors = [3]
        elif len(self.__rooms.recent_random_rooms) == 2:
            adjustment_factors = [3, 2]
        else:
            adjustment_factors = [3, 2, 1]

        #Calculate the weight change based on recent rooms to reduce the chance of a streak of a certain room.
        reward_weight_change = 0
        for j, room in enumerate(self.__rooms.recent_random_rooms):
            if room == "main_game":
                reward_weight_change += 0.05 * adjustment_factors[j]
            else:
                reward_weight_change -= 0.05 * adjustment_factors[j]

        reward_weight = reward_weight + reward_weight_change
        reward_weight = max(0, min(1, reward_weight))
        main_weight = 1 - reward_weight

        #Now randomly choose one of the room types with the newly adjusted weights
        choice = random.choices(
            population=("reward_room", "main_game"),
            weights=(reward_weight, main_weight),
            k=1
        )[0]

        #Check if the last chosen room is different from the current choice
        if self.__rooms.recent_random_rooms and self.__rooms.recent_random_rooms[-1] != choice:
            #Reset to default values if streak is broken
            reward_weight = default_reward_weight
            main_weight = default_main_weight

        #Update recent rooms (keeping only the last 3)
        if len(self.__rooms.recent_random_rooms) > 2:
            self.__rooms.recent_random_rooms.pop(0)
        self.__rooms.recent_random_rooms.append(choice)
        return choice

    def setup_joker_deck(self):
        """Sets up the joker deck by adding various categories and jokers."""
        self.__joker_deck.add_category(CategoryNode("common", weight=50))
        self.__joker_deck.add_category(CategoryNode("uncommon", weight= 30))
        self.__joker_deck.add_category(CategoryNode("rare", weight=15))
        self.__joker_deck.add_category(CategoryNode("ultra-rare", weight=5))

        self.add_jokers()
        #Assign the base weights of the categories
        for category in self.__joker_deck.categories.values():
            category.base_weight = category.weight

    #Have only implemented one type of joker in each category but many times
    def add_jokers(self):
        """Adds specific jokers to the joker deck."""
        for _ in range(100):
            self.__joker_deck.add_joker(MultiplierJoker("MultiplierJoker", "common"))
            self.__joker_deck.add_joker(MoonJoker("MoonJoker", "rare"))
            self.__joker_deck.add_joker(HeartSnakeJoker("HeartSnakeJoker", "uncommon"))
            self.__joker_deck.add_joker(CastleJoker("CastleJoker", "ultra-rare"))


class Rooms:
    """
    Contains the different room three types

    Parameters:
        display (pygame.Surface): The Pygame display surface.
        display_setup (DisplaySetUp): The display setup instance.
        main_clock (pygame.time.Clock): The main clock for controlling the frame rate.
        player (Player): The player instance.
        scoring_system (DefaultScoringStrategy): The scoring system instance
        __joker_deck (JokerTree): The deck of jokers.

    Attributes:
        round (DealerRoom): The current dealer room.
        reward (RewardRoom): The current reward room.
        shop (ShopRoom): The current shop room.
        recent_random_rooms (list): The three most recent rooms from the random room.
    """
    def __init__(self, display, display_setup, player, scoring_system, joker_deck):
        self.dealer_room = DealerRoom(display_setup,  player, scoring_system)
        self.reward_room = RewardRoom(display, display_setup.background_image, player)
        self.shop_room = ShopRoom(display, display_setup.background_image, player, joker_deck, scoring_system)
        self.recent_random_rooms = []


game = Game()
game.game_loop()
