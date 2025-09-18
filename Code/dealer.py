import random
from typing import override
import pygame as pyg
from .TargetScoreCalculator import TargetScoreCalculator
from .ui import Text
from .CONSTANTS import(
    OFF_WHITE,
    text_font,
    DISPLAY_DIMENSIONS_X,
    DISPLAY_DIMENSIONS_Y

)

class Dealer:
    """
    An abstract base class for dealers.

    Attributes:
        _TargetScoreCalculator (TargetScoreCalculator): Instantiates a TargetScoreCalculator object
        _target_score (int): The target score a player will need to beat
        reward (int): The money earnt for defeating the dealer.
        debuff (Debuff): The debuff object a big boss dealer will set.
    """
    def __init__(self):
        """Initialises Dealer with a TargetScoreCalculator instance and a default target score."""
        self._target_score_calculator = TargetScoreCalculator()
        self._target_score = 0
        self.reward = 5
        self.debuff = None

    def start_round(self, level):
        """
        Sets the target score based on the level provided and sets up any debuffs.
        This method will be overriden

        Parameters:
            level (int): The current level of the game, used to determine the target score.
        """
        pass

    @property
    def target_score(self):
        """
        Gets the target score for the player to beat.

        Returns:
            int: The target score.
        """
        return self._target_score


class DefaultDealer(Dealer):
    """
    Dealer for standard encounters, inheriting from Dealer.

    Sets a base target score for these encounters.
    """
    def __init__(self):
        """Initialises the DefaultDealer with a base target score."""
        super().__init__()
        self.name = "Default Dealer"

    @override
    def start_round(self, level):
        """
        Sets the target score based on the level provided.

        Parameters:
            level (int): The current level of the game, used to determine the target score.
        """
        self._target_score = self._target_score_calculator.get_score_requirements(level)["Base Score"]

class SmallBossDealer(Dealer):
    """
    Dealer class for a small boss encounter, inheriting from Dealer.

    Sets a specific target score for small bosses.
    """
    def __init__(self):
        """Initialises the SmallBossDealer."""
        super().__init__()
        self.name = "Small Boss"
        self.reward = 10

    def start_round(self, level):
        """
        Sets the target score based on the level provided.

        Parameters:
            level (int): The level of the game, used to determine the target score.
        """
        self._target_score = self._target_score_calculator.get_score_requirements(level)["Small Boss"]


class BigBossDealer(Dealer):
    """
    Dealer class for big boss encounters, inheriting from Dealer.

    Sets a target score specific to big bosses.
    """
    def __init__(self):
        """Initialises the BigBossDealer."""
        super().__init__()
        self.name = "Big Boss"
        self.reward = 15
        self.debuff_pool = [play_five_cards_debuff, base_score_reduced_debuff]

    def start_round(self, level):
        """
        Sets the target score based on the level provided and randomly chooses debuff

        Parameters:
            level (int): The level of the game, used to determine the target score.
        """
        self._target_score = self._target_score_calculator.get_score_requirements(level)["Big Boss"]
        self.debuff = random.choice(self.debuff_pool)

    def end_round(self):
        """At the end of the round reset the debuff to none"""
        self.debuff = None

class Dealers:
    """
    Contains the three dealers

    Attributes:
        default_dealer (DefaultDealer): The instance of a default dealer
        small_boss_dealer (SmallBossDealer): The instance of the small boss dealer
        big_boss_dealer (BigBossDealer): The insatance of big boss dealer
        current_dealer: The current dealer, used for the game rounds.
    """
    def __init__(self):
        self.default_dealer = DefaultDealer()
        self.small_boss_dealer = SmallBossDealer()
        self.big_boss_dealer = BigBossDealer()
        self.current_dealer = None

class Debuff:
    def __init__(self, name, effect):
        """
        Initialize a debuff with a name and an effect function.

        Parameters:
            name (str): Name of the debuff.
            effect (function): A function that defines the debuff effect.
        """
        self.name = name
        self.effect = effect

    def apply(self, game_context):
        """
        Apply the debuff's effect.
        """
        return self.effect(game_context)

    def display_debuff_text(self, game_context):
        """
        Displays the debuff text

        Parameters:
            game_context (self): The current context of the game round
        """
        debuff_text = f"Debuff: {self.name}"
        text = Text(game_context.display_setup.display, OFF_WHITE, text_font(50), debuff_text, DISPLAY_DIMENSIONS_X/2,DISPLAY_DIMENSIONS_Y/2)
        text.draw_self()
        pyg.display.update()


def play_five_cards(game_context):
    """
    Enforce a debuff requiring exactly 5 cards to be played.

    Parameters:
        game_context (object): The game context, used to access current game state.

    Returns:
        bool: True if the player is allowed to proceed, False otherwise.
    """
    selected_cards = game_context.selected_hand.cards
    if len(selected_cards) != 5:
        return False  #Prevents player from proceeding if they haven't played exactly 5 cards
    return True

def base_score_reduced(game_context):
    """
    Enforce a debuff that reduces the player's base score by halve.

    Parameters:
        game_context (object): The game context, used to access current game state.

    Returns:
        True: Player can continue but base score is halved
    """
    game_context.scoring_system.hand_score = game_context.scoring_system.hand_score // 2
    game_context.update_hand_score_text()
    game_context.text_rects[3].draw_self()
    pyg.display.update()
    pyg.time.delay(1000)
    return True


play_five_cards_debuff = Debuff("Play Five Cards", play_five_cards)
base_score_reduced_debuff = Debuff("Base Score Reduced", base_score_reduced)