"""
This module defines classes and methods for evaluating a poker hand
and managing the point scoring system.
"""
from collections import Counter
from CONSTANTS import rank_map_id


class PokerEval:
    """
    Evaluates the played hand to determine its type and the cards that form the type.

    Attributes:
        hand: An instance of the Hand class that has the cards to be evaluated
    """
    def __init__(self, hand):
        self.hand = hand

    def sort_hand_by_rank(self):
        """Sorts the hand by rank of the cards. Order: A, K, Q, J, 10, 9, 8, 7, 6, 5, 4, 3, 2."""
        self.hand.sort_by_rank()

    def sort_hand_by_suit(self):
        """Sorts the hand by the suit of the cards. Order: Spades, Hearts, Clubs, Diamonds."""
        self.hand.sort_by_suit()

    def is_hand_length_valid(self, minimum_length):
        """
        Checks if the hand is valid based on the number of cards provided compared
        to the minimum expected to form a specific hand type.

        Parameters:
            minimum_length: the minimum length of cards needed to make a hand valid.

        Returns:
            A tuple (is_valid, cards) where is_valid is a boolean to show if the hand is valid,
            and cards is the list of cards in the hand.
        """
        return len(self.hand.cards) >= minimum_length, self.hand.cards

    def get_cards_in_hand(self, num_of_cards_to_check):
        """
        Selects the cards that form the hand type and will therefore score points.

        This method is used to help determine the highest ranked hand type of a hand.

        Parameters:
            hand:  An instance of the Hand class that has the cards to be evaluated
            num_of_cards_to_check: The number of appearances of a card rank that we should check for.
                E.g a pair has 2 appearances of the same rank

        Returns:
            Tuple (Counter, List[Card]): A tuple (rank_counts, cards) where:
            - rank_counts is a Counter object containing the rank and number of appearances,
            - cards is a list of Card instances in the hand.
        """
        rank_counts = Counter()
        cards = []
        #Count appearances of each rank in the hand
        for card in self.hand.cards:
            rank_counts[card.rank] += 1

        #Check for ranks that match the specified number
        for key, value in rank_counts.items():
            if value == num_of_cards_to_check: #If the rank count matches the hand type criteria
                rank = key
                #Collect cards in the hand that match the identified rank
                for card in self.hand.cards:
                    if card.rank == rank:
                        cards.append(card)
        return rank_counts, cards  #Return the rank counts and selected scoring cards

    def is_flush(self):
        """
        Checks if the hand is a flush (5 cards are of the same suit).

        Returns:
            A tuple (is_flush, cards) where is_flush is a boolean to show if the hand is a flush,
            and cards is a list of cards.
        """
        #First check if the hand has the correct number of cards
        valid, hand = self.is_hand_length_valid(5)
        if not valid:
            return False, []
        #Use a set because if all cards are the same, there should only be one suit as no duplicates
        suits = {card.suit for card in hand}
        return len(suits) == 1, hand

    def is_straight(self):
        """
        Checks if the hand is a straight (5 cards are in consecutive order).

        Returns:
            A tuple (is_straight, cards) where is_straight is a boolean to show if the hand is a straight,
            and cards is a list of cards.
        """
        #First, check if the hand has exactly 5 cards
        valid, hand = self.is_hand_length_valid(5)
        if not valid:
            return False, []
        #Sort the hand by rank in descending order.
        self.sort_hand_by_rank()
        #Set test to one less than the highest card in the hand to see if the next cards are consecutive
        test = rank_map_id[hand[0].rank] - 1
        #Iterate through the remaining cards to check if each card is one rank lower than the previous.
        for i in range(1, 5):
            if rank_map_id[hand[i].rank] != test:
                return False, []
            test -= 1
        return True, hand

    def is_royal_flush(self):
        is_straight_flush, flush_cards = self.is_straight_flush()
        royal_flush_ranks = ['A', 'K', 'Q', 'J', 'T']
        for card in flush_cards:
            if card.rank in royal_flush_ranks:
                continue
            else:
                return False, []
        return True, flush_cards

    def is_straight_flush(self):
        """
        Checks if the hand is a straight flush (5 cards are of the same suit and in consecutive order).

        Returns:
            A tuple (is_straight_flush, cards) where is_straight_flush is a boolean to show if the hand is a straight flush,
            and cards is a list of cards.
        """
        #A straight flush must both be a flush and a straight so check if both are true
        is_flush, flush_cards = self.is_flush()
        is_straight, _= self.is_straight()

        if is_flush and is_straight:
            return True, flush_cards
        return False, []


    def is_four_of_a_kind(self):
        """
        Checks if the hand is a four of a kind (4 cards of the same rank).

        Returns:
            A tuple (is_four_of_a_kind, cards) where is_four_of_a_kind is a boolean to show if the hand is a four of a kind,
            and cards is a list of cards.
        """
        #First, check if the hand has atleast 4 cards
        valid, hand = self.is_hand_length_valid(minimum_length=4)
        if not valid:
            return False, []
        #Only get the 4 cards that form part of the four of a kind.
        _, four_of_a_kind_cards = self.get_cards_in_hand(4)
        #If there are exactly 4 cards of the same rank, return True with these cards.
        if len(four_of_a_kind_cards) == 4:
            return True, four_of_a_kind_cards
        return False, []

    def is_full_house(self):
        """
        Checks if the hand is a full house (three cards of the same rank and two cards of the same rank that is different to the three).

        Returns:
            A tuple (is_full_house, cards) where is_full_house is a boolean to show if the hand is a full house,
            and cards is a list of cards.
        """
        #First, check if the hand has exactly cards
        valid, hand = self.is_hand_length_valid(5)
        if not valid:
            return False, []

        _, three_of_a_kind_cards = self.get_cards_in_hand(3)
        _, pair_cards = self.get_cards_in_hand(2)

        #if there are cards in both lists this must mean that it is a full house
        if three_of_a_kind_cards and pair_cards:
            return True, three_of_a_kind_cards + pair_cards

        return False, []

    def is_three_of_a_kind(self):
        """
        Checks if the hand is a three of a kind (3 cards are of the same rank)

        Returns:
            A tuple (is_three_of_a_kind, cards) where is_three_of_a_kind is a boolean to show if the hand is a three of a kind,
            and cards is a list of cards.
        """
        #First, check if the hand has atleast 3 cards
        valid, hand = self.is_hand_length_valid(3)
        if not valid:
            return False, []

        _ ,three_of_a_kind_cards = self.get_cards_in_hand(3)
        #If there are exactly 3 cards of the same rank, return True with these cards.
        if len(three_of_a_kind_cards) == 3:
            return True, three_of_a_kind_cards
        return False, []

    def is_two_pair(self):
        """
        Checks if the hand is a two pair(two different pairs of cards)

        Returns:
            A tuple (is_two_pair, cards) where is_two_pair is a boolean to show if the hand is a two pair,
            and cards is a list of cards.
        """
        #First, check if the hand has atleast 4 cards
        valid, hand = self.is_hand_length_valid(4)
        if not valid:
            return False, []

        _, two_pair_cards = self.get_cards_in_hand(2)

        #If there are exactly 2 pairs, return True with these cards.
        if len(two_pair_cards) == 4:
            return True, two_pair_cards

        return False, []


    def is_one_pair(self):
        """
        Checks if the hand is a one pair(Two cards of the same rank)

        Returns:
            A tuple (is_one_pair, cards) where is_one_pair is a boolean to show if the hand is a one pair,
            and cards is a list of cards.
        """
        #First, check if the hand has atleast 2 cards
        valid, hand = self.is_hand_length_valid(2)
        if not valid:
            return False, []

        _, pair_cards = self.get_cards_in_hand(2)
        #If there are exactly 2 cards of the same rank, return True with these cards.
        if len(pair_cards) == 2:
            return True, pair_cards

        return False, []

    def is_high_card(self):
        """
        Checks if the hand is a high card (A single card)

        Returns:
            A tuple (is_high_card, cards) where is_high_card is a boolean to show if the hand is a high card,
            and cards is a list of cards.
        """
        if not (self.is_straight_flush()[0] or self.is_four_of_a_kind()[0] or
                self.is_full_house()[0] or self.is_flush()[0] or self.is_straight()[0] or
                self.is_three_of_a_kind()[0] or self.is_two_pair()[0] or self.is_one_pair()[0]):
            self.sort_hand_by_rank()
            return True, self.hand.cards[:1]
        return False, []

    def determine_hand_type(self):
        """
        Determines the hand type of a hand and the cards that formed the hand.

        Returns:
            A tuple (hand_type, cards) where hand_type is a string describing the hand type,
            and cards is a list of cards.
        """
        possible_hand_types_functions = []
        possible_hand_types = []
        if len(self.hand.cards) == 0:
            return None, []
        elif len(self.hand.cards) == 1:
            #Only possible hand is "High Card"
            return "High Card", self.hand.cards
        elif len(self.hand.cards) == 2:
            #Possible hands: "One Pair" or "High Card"
            possible_hand_types_functions = [self.is_one_pair, self.is_high_card]
            possible_hand_types = ["One Pair", "High Card"]
        elif len(self.hand.cards) == 3:
            #Possible hands: "Three of a Kind", "One Pair", or "High Card"
            possible_hand_types_functions = [self.is_three_of_a_kind, self.is_one_pair, self.is_high_card]
            possible_hand_types = ["Three of a Kind", "One Pair", "High Card"]
        elif len(self.hand.cards) == 4:
            #Possible hands: "Four of a Kind", "Three of a Kind", "Two Pair", "One Pair", or "High Card"
            possible_hand_types_functions = [self.is_four_of_a_kind, self.is_three_of_a_kind, self.is_two_pair, self.is_one_pair, self.is_high_card]
            possible_hand_types = ["Four of a Kind", "Three of a Kind", "Two Pair", "One Pair", "High Card"]
        elif len(self.hand.cards) == 5:
            #All hands are possible
            possible_hand_types_functions = [self.is_royal_flush, self.is_straight_flush, self.is_four_of_a_kind, self.is_full_house, self.is_flush, self.is_straight, self.is_three_of_a_kind, self.is_two_pair, self.is_one_pair, self.is_high_card]
            possible_hand_types = ["Royal Flush", "Straight Flush", "Four of a Kind", "Full House", "Flush", "Straight", "Three of a Kind", "Two Pair", "One Pair", "High Card"]

        for i, check_function in enumerate(possible_hand_types_functions):
            check_function = possible_hand_types_functions[i]
            hand_type = possible_hand_types[i]
            is_hand_type, hand_cards = check_function()
            if is_hand_type:
                return hand_type, hand_cards
        return None, []

    @property
    def hand_type(self):
        """
        Gets the hand type

        Returns:
            hand_type (str): returns the text to describe a hand type
        """
        return self.determine_hand_type()[0]

class ScoringStrategy:
    """
    Base class for defining scoring strategies in the game.

    This class provides a mapping of hand types to their base scores, multipliers, and levels.

    Attributes:
        base_hand_score_multiplier (dict): A dictionary mapping hand types to their score, multiplier, and level.
    """
    def __init__(self):
        self.base_hand_score_multiplier = {
        "High Card": {"score": 5, "multiplier": 1, "level": 1},
        "One Pair": {"score": 10, "multiplier": 2, "level": 1},
        "Two Pair": {"score": 20, "multiplier": 3, "level": 1},
        "Three of a Kind": {"score": 35, "multiplier": 3, "level": 1},
        "Straight": {"score": 50, "multiplier": 4, "level": 1},
        "Flush": {"score": 55, "multiplier": 4, "level": 1},
        "Full House": {"score": 60, "multiplier": 4, "level": 1},
        "Four of a Kind": {"score": 75, "multiplier": 6, "level": 1},
        "Straight Flush": {"score": 100, "multiplier": 8, "level": 1},
        "Royal Flush": {"score": 100, "multiplier": 10, "level": 1}
    }


    def calculate_score(self, hand_type, level):
        """
        Calculates the score for a given hand type and level.

        This method should be implemented in subclasses to provide specific scoring logic.

        Parameters:
            hand_type (str): The type of hand to calculate the score for.
            level (int): The level of the hand to adjust the scoring multiplier.

        Returns:
            int: The calculated score for the hand type at the specified level.
        """
        pass


class DefaultScoringStrategy(ScoringStrategy):
    """
    Default scoring strategy for the game.

    This class extends the ScoringStrategy base class and provides methods to calculate
    and manage the player's hand score and multiplier based on the base scoring rules.

    Attributes:
        _hand_score (int): The current hand score of the player.
        _multiplier (int): The current multiplier for the hand score.
    """
    def __init__(self):
        super().__init__()
        self._hand_score = 0
        self._multiplier = 0

    def calculate_score(self):
        """
        Calculates the total score based on the current hand score and multiplier.

        Returns:
            int: The total score calculated by multiplying the hand score with the multiplier.
        """
        return self.hand_score * self.multiplier

    def add_to_hand_score(self, score):
        """
        Adds the base score for the given hand type to the current hand score.

        Parameters:
            hand_type (str): The type of hand to add to the hand score.
        """
        self.hand_score += score

    @property
    def hand_score(self):
        """
        Gets the current hand score.

        Returns:
            int: The current hand score.
        """
        return self._hand_score

    @hand_score.setter
    def hand_score(self, score):
        """
        Sets the current hand score to the specified value.

        Parameters:
            score (int): The new hand score to set.
        """
        self._hand_score = score

    @property
    def multiplier(self):
        """
        Gets the current multiplier.

        Returns:
            int: The current multiplier.
        """
        return self._multiplier

    @multiplier.setter
    def multiplier(self, mult):
        """
        Sets the current multiplier to the specified value.

        Parameters:
            mult (int): The new multiplier to set.
        """
        self._multiplier = mult

    def get_base_score(self, hand_type):
        """
        Gets the base score for the given hand type.

        Parameters:
            hand_type (str): The type of hand to get the base score for.

        Returns:
            int: The base score for the hand type, adjusted by level.
        """
        #Add 20 score for each level above 1
        if hand_type:
            return self.base_hand_score_multiplier[hand_type]["score"] + 20*(self.base_hand_score_multiplier[hand_type]["level"]-1)
        return 0

    def get_base_multiplier(self, hand_type):
        """
        Gets the base multiplier for the given hand type.

        Parameters:
            hand_type (str): The type of hand to get the base multiplier for.

        Returns:
            int: The base multiplier for the hand type, adjusted by level.
        """
        #Add 1 mult for each level above 1
        if hand_type:
            return self.base_hand_score_multiplier[hand_type]["multiplier"] + (self.base_hand_score_multiplier[hand_type]["level"]-1)
        return 0

    def upgrade_hand_level(self, hand):
        """
        Upgrades the level of the specified hand type.

        Parameters:
            hand (str): The type of hand to upgrade.
        """
        self.base_hand_score_multiplier[hand]["level"] += 1
