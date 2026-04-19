# PokerQuest

A deckbuilding card game that combines poker mechanics to score high point hands to defeat levels in a procedurally generated map.

## Run

1. Clone the repository:
```
git clone https://github.com/edison1x/PokerQuest.git
```
2. Navigate to the directory the code is saved:
```
cd PokerQuest
```
3. Install pygame
```
pip install pygame
```
4. Run the program
```
python -m Code.game
```
## About the Game

I was heavily inspired by **Balatro** and **Slay the Spire**, both of which are deckbuilding games. I decided to take the core gameplay from Balatro and combined this with a similar procedurally generated map from Slay the Spire.

---

## How to Play the Game

### The Map

Below is an example of what the map might look like.

![mapvideo mp4](https://github.com/user-attachments/assets/f41041a4-4f30-48f5-baca-8aecd2102fdb)

The player begins at the top of the map and attempts to reach the final level at the bottom by following a path of connected rooms. The player can only move forward, and only into one of the connected rooms ahead.

---

### Room Types

#### 🟦 D — Dealer Room

The player must reach a target score by playing poker hands.

![dealerroom](https://github.com/user-attachments/assets/f01fa6de-a9eb-405f-89cf-35a0f2c34c0c)

#### 🟦 R — Reward Room

The player receives a random amount of money. The rarity of the money pouch is decided based on the following probabilities, and a random amount within that range is awarded:

| Rarity | Range | Probability |
|---|---|---|
| Common | £5 – £10 | 50% |
| Uncommon | £10 – £15 | 30% |
| Rare | £15 – £20 | 15% |
| Ultra-Rare | £20 – £25 | 5% |

#### 🟦 ? — Random Room

The player has a chance to encounter a small boss, a big boss, or receive a reward.

> There is also a **shop room** that appears after defeating any dealer. In the shop, the player can purchase joker cards that have unique effects to help score higher hands.
> 
### Poker Hands

The game uses a standard deck of 52 cards. Each card has a specific point value:
![points](https://github.com/user-attachments/assets/a9ff9142-3669-42fe-be72-6692fb07c547)

### Scoring Formula

The total score for a hand is calculated as:

**Total Points = (Base Score + Card Values) × Multiplier**

Only the cards that form the highest-ranked hand are scored — any extra selected cards are ignored. For example, if you select J♠ J♦ J♣ J♥ 3♠, only the four Jacks contribute to the score.

Each hand type can also be upgraded in the shop, which increases its base score by +20 and its multiplier by +1 per level above 1.

![poker hands](https://github.com/user-attachments/assets/8440a938-e54a-4ed0-b5c9-c90517251171)

### Dealer Room Mechanics

Each dealer room works as follows:

- You are dealt **7 cards** from the deck at the start of the round.
- You have **5 hands** and **3 discards** to reach the target score.
- Each hand, you select up to 5 cards and click **Play Hand** to score them.
- The played cards are replaced by new cards from the top of the deck. Unplayed cards remain in your hand.
- If you **discard**, the selected cards are removed and replaced with new cards until you have 7 again. This uses one discard.
- If you reach the target score within 5 hands, you win the round. Any remaining hands are converted to money (+£1 each).
- If you fail to reach the target score, **the run ends**.

### The Shop

A shop appears after every dealer room. It contains:

- One randomly selected joker card available to purchase.
- One randomly selected hand type available to upgrade.

**Joker rarity and prices:**
| Rarity | Price | Base Probability |
|---|---|---|
| Common | £5 | 50% |
| Uncommon | £10 | 30% |
| Rare | £20 | 15% |
| Ultra-Rare | £40 | 5% |

As you progress through levels, the probability of common and uncommon jokers decreases while rare and ultra-rare jokers become more likely.

**Rules:**
- You can hold a maximum of **5 jokers** at once.
- To buy the shop joker, click it to reveal the **Purchase Joker** button.
- To sell a joker from your hand, click it to reveal the **Sell** button.
- Upgrading a hand costs **£4** and permanently increases that hand's base score by +20 and multiplier by +1.
- Each shop offers one upgrade and one joker — click **Next** to return to the map.

### Random Room (?)

When you enter a random room, the outcome is determined by weighted probability:

- **70%** chance of a dealer encounter (split equally between small boss and big boss).
- **30%** chance of a reward.

The system tracks your 3 most recent random room outcomes and adjusts probabilities to prevent streaks — it is impossible to receive 3 rewards in a row.

### Dealer Types

There are three types of dealer you can encounter:

| Dealer | Target Score | Reward on Win | Special |
|---|---|---|---|
| Default Dealer (D) | Base score for that floor | +£5 | None |
| Small Boss Dealer | 1.5× base score | +£10 | Found only in "?" rooms |
| Big Boss Dealer (B) | 2.25× base score | +£15 | Applies a debuff each round |

**Debuffs** are only applied by big boss dealers and add an extra challenge. Examples include:
- *Play Five Cards* — you must select exactly 5 cards or your hand will not be processed.
- *Base Score Reduced* — the base score of every hand is halved before card values are added.

### Joker Cards

There are four joker cards in the game, each with a different rarity:

| Joker | Rarity | Effect | Condition |
|---|---|---|---|
| MultiplierJoker | Common | +5 multiplier | None |
| HeartSnakeJoker | Uncommon | ×2 multiplier | Per Heart card scored in the hand |
| MoonJoker | Rare | ×4 multiplier | None |
| CastleJoker | Ultra-Rare | +50 score and ×2 multiplier | Per King or Queen scored in the hand |

Joker effects are applied **left to right** after card scoring. You can reorder your jokers by dragging them in the dealer room.

### Node Colours

| Colour | Meaning |
|---|---|
| 🔴 Red | Your current position |
| 🟡 Gold | Rooms you can move to next |
| 🔵 Blue | All other rooms |
## Win and Loss Conditions

- **Winning:** Defeat the final big boss dealer at level 22. A congratulations message will appear.
- **Losing:** Fail to reach the target score within the 5 hands in any dealer room. The run ends immediately with no option to continue.

## Prerequisites

- Python 3.6 or above
- pygame (`pip install pygame`)

The following files and folders must remain in their original locations relative to the project root:

```
PokerQuest/
├── Code/
│   ├── game.py               # Main game loop and state management
│   ├── map.py                # Procedural map generation and visualisation
│   ├── poker.py              # Poker hand evaluator
│   ├── dealer.py             # Dealer class hierarchy (Default, SmallBoss, BigBoss)
│   ├── dealerroom.py         # Dealer room gameplay logic
│   ├── shop.py               # Shop room logic
│   ├── reward.py             # Reward room logic
│   ├── card.py               # PlayingCard and JokerCard classes
│   ├── CONSTANTS.py          # All constants, colours, dimensions, file paths
│   └── TargetScoreCalculator.py  # Target score lookup by floor level
├── imgs/
│   ├── cards/                # 52 playing card PNGs (e.g. 2C.png, TH.png, AS.png)
│   ├── jokers/               # Joker card images
│   └── background.jpg        # Table background image
└── Roboto-Black.ttf          # Font file — must stay in the root directory
```
