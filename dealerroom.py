import pygame as pyg
from hand import Hand
from ui import UI, Button, TextRect, Text
from poker import PokerEval
from CONSTANTS import (
    DISPLAY_DIMENSIONS_X,
    DISPLAY_DIMENSIONS_Y,
    CARD_DIMENSIONS,
    CARD_ANIMATION_DELAY,
    CLICK_THRESHOLD,
    BUTTON_WIDTH ,
    BUTTON_HEIGHT ,
    BUTTON_SPACING ,
    TEXT_WIDTH,
    TEXT_HEIGHT ,
    DARK_GREY,
    OFF_WHITE,
    rank_map_points,
    text_font,
    PLAYER_CARDS_X,
    PLAYER_CARDS_Y_UNSELECTED,
    PLAYER_CARDS_Y_SELECTED,
    JOKER_CARDS_Y
)


class DealerRoom:
    """
    Manages a game round in the dealer's room.

    Attributes:
        __display_set_up (DisplaySetup): Object to manage display setup.
        __UIManager (UIManager): Manages UI elements and interactions.
        __player (Player): The current player.
        __scoring_system (ScoringSystem): The scoring system to be used.
        __pokereval (PokerEval): PokerEval object for evaluating poker hands.
        __deck (Deck): The current deck of cards.
        __player_hand (Hand): The player's hand in the current round.
        __selected_hand (Hand): The hand selected by the player to play or discard.
        __player_joker_hand (Hand): The player's joker cards.
        __round_number (int): The current round number.
        __dragging_card (Card): Card being dragged by the player.
        __drag_offset (Tuple[int, int]): Offset for dragging cards.
        __click_start_time (float): Time when the player clicked for card drag.
        __text_rects (List[Rect]): UI text elements displayed during the game.
        __hand_type (str): The current poker hand type.
    """
    def __init__(self, display_setup, player, scoring_system):
        """
        Initialises the DealerRoom with all the essential game components.

        Parameters:
            display_set_up (DisplaySetup): Object to manage display setup.
            player (Player): The player object.
            scoring_system (ScoringSystem): Object managing the scoring strategy.
        """
        self.display_setup = display_setup
        self.__UIManager = UI(self.display_setup.display, x_pos=0, y_pos=0)
        self.__player = player
        self.scoring_system = scoring_system

        self.init_game_state()
        self.setup_buttons()
        self.setup_text_rects()
        self.setup_text()

        self.__hand_type = self.__pokereval.determine_hand_type()[0]

    def init_game_state(self):
        """Initialises the game state for a new round, setting up player hands, the deck, and round variables."""
        self.__player_hand = Hand(self.display_setup.display)
        self.selected_hand = Hand(self.display_setup.display) #Needs to be accessed for debuffs
        self.__pokereval = PokerEval(self.selected_hand)
        self.__player_joker_hand = self.__player.joker_hand
        self.__round_number = None
        self.__dragging_card = None
        self.__dragging_joker_card = None
        self.__drag_offset = (0, 0)
        self.__click_start_time = 0

    def setup_buttons(self):
        """Sets up buttons for interacting with the game, such as 'Play Hand', 'Sort by Rank', 'Sort by Suit', and 'Discard'."""
        #Labels and corresponding actions for each button
        button_labels = ["Play Hand", "Sort by Rank", "Sort by Suit", "Discard"]
        button_actions = [self.play_hand, self.sort_by_rank, self.sort_by_suit, self.discard_cards]
        #Calculate the starting x coordinate to center buttons on the screen
        start_x = (DISPLAY_DIMENSIONS_X - len(button_labels) * (BUTTON_WIDTH + BUTTON_SPACING)) // 2
        #Create and position each button based on its index in button_labels
        for i, label in enumerate(button_labels):
            button_x = start_x + i * (BUTTON_WIDTH + BUTTON_SPACING)
            #Initialise a Button instance and add it to the UI manager
            button = Button(self.display_setup.display, BUTTON_WIDTH, BUTTON_HEIGHT, button_x, DISPLAY_DIMENSIONS_Y // 1.2, label, text_font(20), button_actions[i])
            self.__UIManager.add_child(button)

    def setup_text_rects(self):
        """Sets up text elements to display information like player scores, hand types, and rounds during gameplay."""
        text_positions = (DISPLAY_DIMENSIONS_X // 19, DISPLAY_DIMENSIONS_Y // 100)
        #Labels for each text element to be displayed in the UI
        text_labels = ["Dealer Type","Target Score:", "Player Score:", "Hand Type: ", "Hand Score:", "Multiplier:", "Hands Left:", "Discards Left:", "Round:", "Balance:"]
        text_rects = []
        #Create each text element at a unique y coordinate, incrementing with each label
        for pos, label in enumerate(text_labels):
            #Initialise a TextRect instance and add it to the UI manager
            text_rect = TextRect(self.display_setup.display, TEXT_WIDTH, TEXT_HEIGHT, text_positions[0],text_positions[1] + (pos*DISPLAY_DIMENSIONS_Y // 13), text_font(25), DARK_GREY, OFF_WHITE, label)
            self.__UIManager.add_child(text_rect)
            text_rects.append(text_rect)
        #Store all created text elements for future reference
        self.text_rects = text_rects

    def setup_text(self):
        self.__deck_card_count_text = Text(self.display_setup.display, OFF_WHITE, text_font(20), f"Cards left: {str(len(self.__player.deck))}", DISPLAY_DIMENSIONS_X //1.4,DISPLAY_DIMENSIONS_Y //1.5)
        self.__UIManager.add_child(self.__deck_card_count_text)

    def start_new_round(self, level, dealer):
        """
        Initialises a new round in the game based on the clicked room.

        Parameters:
            level (int): The current level or round number.
            dealer (Dealer): The dealer handling the game logic for that round.

        Returns:
            player_wins (Boolean): if the player won the round or not.
        """
        #Resetting the variables for a new round
        self.__round_number = level
        self.__dealer = dealer
        #Start the round for the dealer and set the debuff if it is a big boss
        self.__dealer.start_round(level)
        self.__player.start_round()
        self.__player_hand.clear()
        self.__player.deck.deal_cards(self.__player_hand)
        for joker in self.__player_joker_hand.cards:
            joker.reset_joker()
        running = True
        #Start the game round loop
        player_wins = self.game_loop(running)
        text = f"You have defeated {self.__dealer.name}"
        win_text = Text(self.display_setup.display, OFF_WHITE, text_font(30), text, DISPLAY_DIMENSIONS_X/2, DISPLAY_DIMENSIONS_Y/2)
        win_text.draw_self()
        pyg.display.update()
        pyg.time.delay(1000)
        return player_wins


    def game_loop(self, running):
        """
        The main game loop that keeps running until the round ends or the game is exited.

        Returns:
            player_wins (Boolean): if the player won the round or not.
        """
        event_occurred = False
        #Display debuff effect, if any, at start
        self.update_ui()
        if self.__dealer.debuff:
            self.__dealer.debuff.display_debuff_text(self)
        pyg.time.delay(1000)
        while running:
            event_occurred = self.handle_events()
            #Only update the ui if there is an event such as clicking a button
            if event_occurred:
                self.update_ui()
                event_occurred = False
            #Check if game is over and if so return True if the player won or false if not.
            game_over, player_wins = self.check_game_status()
            self.display_setup.main_clock.tick(30)
            if game_over:
                running = False

        return player_wins

    def check_game_status(self):
        """
        Checks if the game round is over and if the player won or lost.

        Returns:
            Tuple: (game_over (bool), player_wins (bool))
        """
        #Player has no remaining hands and did not reach the target score so game round over and player did not win
        if self.__player.number_of_hands_left == 0 and self.__player.current_score < self.__dealer.target_score:
            return True, False
        #Player exceeded the target score so game round over and player won.
        elif self.__player.current_score > self.__dealer.target_score:
            self.__player.balance = self.__dealer.reward #adds the money depending on the type of dealer it was.
            self.__player.balance = self.__player.number_of_hands_left #+1 for each remaining hand
            return True, True
        #Otherwise game is not over and player has not won.
        return False, False

    def handle_events(self):
        """
        Handles various events like quitting, dragging cards, and clicking buttons.

        Returns:
            Boolean: Indicates whether an event occurred.
        """
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                self.display_setup.exit()
                return True
            elif event.type == pyg.MOUSEBUTTONDOWN and event.button == 1:
                #Left click down so start timer to see if they are holding or clicking
                self.__click_start_time = pyg.time.get_ticks()
                self.start_drag(event.pos)
                return True
            elif event.type == pyg.MOUSEBUTTONUP and event.button == 1:
                #Left click up so check what might happen such as selecting card
                mouse_pos = pyg.mouse.get_pos()
                self.handle_mouse_up(mouse_pos, event.pos)
                return True
            elif event.type == pyg.MOUSEMOTION:
                if self.__dragging_card:
                    self.update_drag(event.pos, self.__dragging_card)
                if self.__dragging_joker_card:
                    self.update_drag(event.pos, self.__dragging_joker_card)

                return True

    def start_drag(self, mouse_pos):
        """
        Initiates dragging a card based on the mouse position.

        Parameters:
            mouse_pos (Tuple[int, int]): The current mouse position.
        """
        for card in self.__player_hand.cards:
            if card.rect.collidepoint(mouse_pos):
                self.__dragging_card = card
                self.__player_hand.dragging_card = card
                self.__drag_offset = (mouse_pos[0] - card.x, mouse_pos[1] - card.y)
                break

        for card in self.__player_joker_hand.cards:
            if card.rect.collidepoint(mouse_pos):
                self.__dragging_joker_card = card
                self.__player_joker_hand.dragging_card = card
                self.__drag_offset = (mouse_pos[0] - card.x, mouse_pos[1] - card.y)
                break
    def update_drag(self, mouse_pos, card):
        """
        Updates the position of the card being dragged.

        Parameters:
            mouse_pos (Tuple[int, int]): The current mouse position during dragging.
        """
        #Redrawing the card as it is moved around
        new_x = mouse_pos[0] - self.__drag_offset[0]
        new_y = mouse_pos[1] - self.__drag_offset[1]

        card.x = new_x
        card.y = new_y

    def handle_mouse_up(self, mouse_pos, event_pos):
        """
        Handles the action when the mouse button is released after dragging.

        Parameters:
            mouse_pos (Tuple[int, int]): The current mouse position.
            event_pos (Tuple[int, int]): The mouse position when the button was released.
        """
        click_duration = pyg.time.get_ticks() - self.__click_start_time
        #Check if player was clicking or dragging a card
        if click_duration < CLICK_THRESHOLD:
            #Player clicked the card and so now handle card selection process
            self.__dragging_card = None
            self.__player_hand.dragging_card = None
            self.handle_card_selection(mouse_pos)
            self.handle_event(pyg.event.Event(pyg.MOUSEBUTTONDOWN, pos=event_pos, button=1))
        else:
            #Player was dragging a card
            if self.__dragging_card:
                self.end_drag(mouse_pos, self.__dragging_card, self.__player_hand)
            if self.__dragging_joker_card:
                self.end_drag(mouse_pos, self.__dragging_joker_card, self.__player_joker_hand)

    def end_drag(self, mouse_pos, dragging_card, hand):
        """
        Updates the card positions if a card is dragged over another.

        Parameters:
            mouse_pos (Tuple[int, int]): The current mouse position during dragging.
        """
        for card in hand.cards:
            if card != dragging_card and card.rect.collidepoint(mouse_pos):
                #If the card being dragged is hovering over a different card, then swap
                self.swap_cards(dragging_card, card, hand)
                break
        dragging_card = None
        hand.dragging_card = None

    def swap_cards(self, card1, card2, hand):
        """
        Swaps the positions of two cards in the player's hand.

        Parameters:
            card1 (Card): The first card to swap.
            card2 (Card): The second card to swap.
        """
        index1 = hand.cards.index(card1)
        index2 = hand.cards.index(card2)
        hand.cards[index1], hand.cards[index2] = card2, card1
        hand.display_hand(PLAYER_CARDS_X, PLAYER_CARDS_Y_UNSELECTED)

    def handle_event(self, event):
        """
        Handles game events by passing on to the UIManager's children.

        Parameters:
            event (pyg.event.Event): A pygame event, such as a mouse click or keypress.
        """
        for child in self.__UIManager.children:
            child.handle_event(event)

    def handle_card_selection(self, mouse_pos):
        """
        Handles the player's card selection actions, either selecting a card from their hand or deselecting it.

        Parameters:
            mouse_pos (Tuple[int, int]): The current mouse position for detecting card selection.
        """
        if self.__dragging_card:
            return

        #Check if selecting a card from the player's hand
        for card in self.__player_hand.cards:
            if card.rect.collidepoint(mouse_pos):
                if len(self.selected_hand.cards) < 5:
                    self.player_select_card_to_play(card)
                    return
        #Check if deselecting a card from the selected hand
        for card in self.selected_hand.cards:
            if card.rect.collidepoint(mouse_pos):
                print(f"deselecting card {str(card)}")
                self.player_deselect_card_from_play(card)

    def play_hand(self):
        """This handles all the logic for when a player plays the hand. It calculates the points scored and after all the animation, resets the screen and updates"""
        #Apply the debuff if it exists and enforce its conditions
        if self.__dealer.debuff:
            if not self.__dealer.debuff.apply(self):  #Pass self to debuff to check game state
                self.__dealer.debuff.display_debuff_text(self)
                pyg.time.delay(1000)
                return
        #Check there are cards in the selected hand and the player has hands to play
        if len(self.selected_hand.cards) != 0 and self.__player.number_of_hands_left > 0:
            _, self.hand_cards = self.__pokereval.determine_hand_type()
            self.play_hand_animation()
            self.play_joker_animation(self.__player_joker_hand.cards)
            pyg.time.delay(CARD_ANIMATION_DELAY)
            #Update variables
            self.__player.add_to_current_score = self.scoring_system.calculate_score()
            self.selected_hand.clear()

            self.scoring_system.hand_score = 0
            self.__player.number_of_hands_left = 1
            self.__player.deck.deal_cards(self.__player_hand)
            self.update_deck_count_text()

            #Reset hand type, score, and multiplier
            self.update_hand_evaluation()

    def play_hand_animation(self):
        """This handles the animation for cards when a player plays their hand. It moves the card up and displays the number of points above the card."""
        for card in self.hand_cards:
             #Clear the previous card
             self.display_setup.display.blit(self.display_setup.background_image, (card.x, card.y), (card.x, card.y, card.image.get_width(), card.image.get_height()))
             card.y = PLAYER_CARDS_Y_SELECTED - (DISPLAY_DIMENSIONS_Y // 72)
             #Display the card moving up
             self.display_setup.display.blit(card.image, (card.x, card.y))
             pyg.time.delay(CARD_ANIMATION_DELAY)
             #Display points above the card
             card_score = rank_map_points[card.rank]
             self.__card_score_text= text_font(25).render(str(f"+{card_score}"), True, OFF_WHITE)
             self.display_setup.display.blit(self.__card_score_text, (card.x+(DISPLAY_DIMENSIONS_X // 64), card.y-(DISPLAY_DIMENSIONS_Y//22)))
             pyg.display.update()

             #Updates current hand score
             self.scoring_system.add_to_hand_score(card_score)
             self.update_hand_score_text()
             self.text_rects[4].draw_self()
             pyg.display.update()
             pyg.time.delay(CARD_ANIMATION_DELAY)


    def play_joker_animation(self, jokers):
        """
        This handles the animation for joker cards when a player plays their hand.
        It displays the ability of the joker below the card.

        Parameters:
            jokers (List[Joker]): A list of joker card objects that the player is playing.
            hand_cards (List[Card]): A list of the player's hand card objects.
        """
        joker_text_y = JOKER_CARDS_Y + CARD_DIMENSIONS[1]

        for joker in jokers:
            #Check conditions of joker card before performing ability
            if joker.conditions(self):
                x = joker.x
                y = joker_text_y
                joker_text = Text(self.display_setup.display, OFF_WHITE, text_font(20), joker.ability_text(), x, y)
                #Clear any previous text
                self.display_setup.display.blit(self.display_setup.background_image, (x, y), (x, y, joker_text._width, joker_text._height))
                #Display the ability text below the image
                joker_text.draw_self()
                pyg.display.update()
                pyg.time.delay(CARD_ANIMATION_DELAY)
                #Clear the text again
                self.display_setup.display.blit(self.display_setup.background_image, (x, y), (x, y, joker_text._width, joker_text._height))
                pyg.display.update()
                pyg.time.delay(CARD_ANIMATION_DELAY)
                #Perform the joker's ability and determine its effects on score or multiplier
                joker.perform_ability(self)



    def player_select_card_to_play(self, card):
        """Handles the selection of a card to play."""
        if card:
            card.toggle_selected()
            self.selected_hand.add_card(card)
            self.__player_hand.remove_card(card)
            self.update_hand_evaluation()

    def player_deselect_card_from_play(self, card):
         """Handles the deselection of a card from the selected hand."""
         if card:
            card.toggle_selected()
            removed_card = self.selected_hand.remove_card(card)
            self.__player_hand.add_card(removed_card)
            self.update_hand_evaluation()

    def sort_by_rank(self):
        """Sorts the hand by rank of the cards. Order: Ace, King, Queen, Jack, 10, 9, 8, 7, 6, 5, 4, 3, 2."""
        self.__player_hand.sort_by_rank()

    def sort_by_suit(self):
        """Sorts the hand by the suit of the cards. Order: Spades, Hearts, Clubs, Diamonds."""
        self.__player_hand.sort_by_suit()

    def discard_cards(self):
        """Discards the selected cards and removes the number of available discards by 1"""
        if self.__player.number_of_discards_left > 0 and len(self.selected_hand.cards) > 0:
            self.__player.number_of_discards_left = 1
            self.selected_hand.clear()
            self.__player.deck.deal_cards(self.__player_hand)

    def update_ui(self):
        """Updates the text, player hand, selected hand, and joker hand."""
        #Clear the background
        self.display_setup.display.blit(self.display_setup.background_image, (0, 0))
        self.update_text_rects()
        self.update_deck_count_text()
        self.__player_hand.display_hand(PLAYER_CARDS_X, PLAYER_CARDS_Y_UNSELECTED)
        if self.__dragging_card:
            self.display_setup.display.blit(self.__dragging_card.image, (self.__dragging_card.x, self.__dragging_card.y))
        self.selected_hand.display_hand(PLAYER_CARDS_X, PLAYER_CARDS_Y_SELECTED)
        self.__player_joker_hand.display_hand(PLAYER_CARDS_X, JOKER_CARDS_Y)

        self.__UIManager.draw()

        pyg.display.update()

    def update_text_rects(self):
        """Updates the text."""
        text_map = {
        0: f"{self.__dealer.name}",
        1: f"Target Score: {self.__dealer.target_score}",
        2: f"Player Score: {self.__player.current_score}",
        3: f"Hand Type: {self.__hand_type}",
        4: f"Hand Score: {str(self.scoring_system.hand_score)}",
        5: f"Hand Mult: {str(self.scoring_system.multiplier)}",
        6: f"Hands Left: {self.__player.number_of_hands_left}",
        7: f"Discards Left: {self.__player.number_of_discards_left}",
        8: f"Round: {self.__round_number}",
        9: f"Bal: {self.__player.balance}"}

        for index, text in text_map.items():
            self.text_rects[index].set_text(text)

    def update_hand_score_text(self):
        """Updates the text for the current hand score."""
        self.text_rects[4].set_text(f"Hand Score: {str(self.scoring_system.hand_score)}")

    def update_hand_multiplier_text(self):
        """Updates the text for the current hand multiplier."""
        self.text_rects[5].set_text(f"Hand Mult: {str(self.scoring_system.multiplier)}")

    def update_deck_count_text(self):
        """Updates the text for the current hand multiplier."""
        self.__deck_card_count_text.set_text(f"Cards left: {str(len(self.__player.deck))}")

    def update_hand_evaluation(self):
        """Updates the evaluation of the player's hand."""
        self.__hand_type = self.__pokereval.determine_hand_type()[0]
        self.scoring_system.multiplier = self.scoring_system.get_base_multiplier(self.__hand_type)
        self.scoring_system.hand_score = self.scoring_system.get_base_score(self.__hand_type)
