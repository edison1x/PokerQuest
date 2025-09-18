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
## About the game
I was heavily inspired by "Balatro" and "Slay the Spire", both of which are deckbuilding games. I decided to take the core gameplay from Balatro and combined this with a similar procedurally generated map from Slay the Spire.
## How to play the game
### The map
Below is an example of what the map might look like.

![mapvideo mp4](https://github.com/user-attachments/assets/f41041a4-4f30-48f5-baca-8aecd2102fdb)
The player begins at the top of the map and attempts to reach the final level at the bottom by following a path of connected rooms. The player can only move forward and only to one of the connected rooms.

### Key
D - This letter stands for the dealer room. In this room, the player must reach a certain score by playing poker hands (more details about gameplay later).
![dealerroom](https://github.com/user-attachments/assets/f01fa6de-a9eb-405f-89cf-35a0f2c34c0c)

R - This letter stands for the reward room. In this room, the player receives a random amount of money. The rarity of the money pouch is decided based on the following probabilities.
+ £5 to £10 – 50% (Common).
+ £10 to £15 – 30% (Uncommon). 
+ £15 to £20 - 15% (Rare). 
+ £20 to £25 – 5% (Ultra-Rare).

Once the rarity is determined, a random number is chosen from that range and given to the player.

? - The question mark stands for the random room. In this room, the player has chances to find a small boss, big boss or a reward.

Note that there is also a shop room that appears after defeating a dealer. In the shop, the player can purchase joker cards that have unique effects to help score higher hands.

### Poker Hands

The game uses a standard deck of 52 cards. Each card has a specific point value:
![points](https://github.com/user-attachments/assets/a9ff9142-3669-42fe-be72-6692fb07c547)

Each poker hand also has a specific score:

![poker hands](https://github.com/user-attachments/assets/8440a938-e54a-4ed0-b5c9-c90517251171)

