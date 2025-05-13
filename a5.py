#
# Assignment 5 by Dylan Le Voguer
# May 12, 2025
#
import random

# Constants for the game
players = ["chosen_by_user", "CPU #1", "CPU #2", "CPU #3"]

dice_ranks = {
    1000: [1, 2, 3],  # LoCo!; 2 chips
    2000: [1, 1, 1],  # Three of a kinds; 3 chip
    3000: [2, 2, 2],
    4000: [3, 3, 3],
    5000: [4, 4, 4],
    6000: [5, 5, 5],
    7000: [6, 6, 6],
    8000: [4, 5, 6],  # PoCo! 4 chips
}

chip_deduction = {
    1000: 2,
    2000: 3,
    3000: 3,
    4000: 3,
    5000: 3,
    6000: 3,
    7000: 3,
    8000: 4,
}


# Helper functions
def printInBox(text):
    """Prints the text in a box"""
    print(f"+{'-' * (len(text) + 2)}+")
    print(f"| {text} |")
    print(f"+{'-' * (len(text) + 2)}+")

def printDiceRoll(roll):
    print(f"{player} rolled {player_rolls[player]}")
    
    for _ in range(5):
        for i in range(3):
            if i == 0 or i == 4:
                print((" -----  ")*3)
            else:
                if i == roll[i] == 1:
                print(f"| {roll[i]} |")
        

def calculate_score(roll):
    """Calculate the score for a given roll"""
    score = 0
    for num in roll:
        if num == 1:
            score += 100
        elif num == 6:
            score += 60
        else:
            score += num
    return score


def roll_dice(num_rolls, player):
    """Rolls the dice for the player and returns the num of rolls"""
    roll = [random.randint(1, 6) for _ in range(3)]
    times_rolled = 1

    while times_rolled < num_rolls:
        # Check if the roll is a special combination
        if roll in dice_ranks.values():
            break

        # Calculate the current score
        score = calculate_score(player_rolls[player])

        # Stop rolling if the score is between 100 and 200
        if 200 > score > 100:
            break

        dice_to_reroll = []

        if player == username:
            print(f"Your Roll: {roll}")
            deciding_rerolls = True
            while deciding_rerolls == True:
                reroll_choice = input("Do you want to reroll? (yes/no/all): ")

                if reroll_choice == "all":
                    # Reroll all dice
                    dice_to_reroll = [0, 1, 2]
                    deciding_rerolls = False
                elif reroll_choice == "no":
                    # Do not reroll
                    dice_to_reroll = []
                    deciding_rerolls = False
                elif reroll_choice == "yes":
                    # Ask which dice to reroll
                    reroll_input = input(
                        "Which dice would you like to reroll? (Enter di seperated by commas, e.g.1, 2, 3): "
                    )
                    dice_to_reroll = []
                    for i in reroll_input.split(","):
                        if (
                            i.strip().isdigit()
                        ):  # Checks validity of input, if its a number
                            index = int(i.strip()) - 1  # Converts to zero-based index
                            if 0 <= index <= 2:  # Ensures the index is valid
                                dice_to_reroll.append(index)
                    deciding_rerolls = False

                else:
                    print("Invalid input. Please try again.")
        else:
            # Check if dice should be rerolled for CPUS
            for i, die in enumerate(roll):
                if die == 1 or die == 6:
                    continue
                if roll.count(die) >= 2:
                    continue
                dice_to_reroll.append(i)

        for i in dice_to_reroll:
            roll[i] = random.randint(1, 6)

        times_rolled += 1

        if (
            roll in dice_ranks.values()
        ):  # Check again if the roll is a special combination
            break

    roll.sort()  # Sort the roll to make it easier to compare
    player_rolls[player] = roll
    printDiceRoll(player_rolls[player])
    return times_rolled


# Game setup
printInBox("Welcome to PoCoLoCo!")
print(
    "Rules: \n"
    "\t1. The first player can roll up to 3 dice \n"
    "\t2. Each roll, the player can choose to stop or to reroll up to 3 of their dice \n"
    "\t3. The player with the lowest score gains chips from the other players \n"
    "\t4. The first player to run out of chips is the winner"
)

# Ask the player for their name
players[0]
username = input("\nWhat is your name?: ")
players[0] = username
chip_count = {
    # Define the chips for each player
    players[0]: 10,
    players[1]: 10,
    players[2]: 10,
    players[3]: 10,
}

player_rolls = {
    # Define the rolls for each player
    players[0]: [],
    players[1]: [],
    players[2]: [],
    players[3]: [],
}

# Ask the player for the number of chips everyone starts with
num_chips = int(input("\nHow many chips do you want to start with?: "))
for player in chip_count.keys():
    chip_count[player] = num_chips

# Main Game Loop
round = 0
found_winner = False
while not found_winner:
    """Runs the game until a player wins by running out of chips"""

    # Prints the round number
    printInBox("Round " + str(round + 1))

    # Reset high and low scores
    high_score = 0
    high_score_player = None
    low_score = float("inf")
    low_score_player = None

    # Reset max rolls
    num_rolls = 3
    last_num_rolls = num_rolls
    # Reset player rolls
    for player in player_rolls:
        player_rolls[player] = []

    random.shuffle(players)
    
    for player in players:
        score = 0

        last_num_rolls = roll_dice(last_num_rolls, player)

        # Check if player_rolls[player] is a special combination
        for key, value in dice_ranks.items():
            if player_rolls[player] == value:
                score = key
                break
        else:
            score = calculate_score(player_rolls[player])

        # Set high and low scores
        if score > high_score:
            high_score = score
            high_score_player = player
        if score < low_score:
            low_score = score
            low_score_player = player
    round += 1

    # Determine how many chips to be taken from the winners
    if high_score in chip_deduction:
        taken_chips = chip_deduction.get(high_score, 0)
    else:
        taken_chips = 1  # Num of chips to be taken if not in the ranks

    # Deducts chips from the winners and adds them to the loser
    for player in chip_count:
        if player == low_score_player:
            chip_count[player] += (
                taken_chips * len(players) - 1
            )  # chip(s) taken from each player and given to the loser
        else:
            chip_count[player] -= taken_chips

    print(f"High score: {high_score_player} with {high_score}")
    print(f"Low score: {low_score_player} with {low_score}")

    print("Chips:")
    for player, chip in chip_count.items():
        if chip < 0:
            chip = 0
        print(player, "has", chip, "chips")

    for player, roll in player_rolls.items():
        print(player, "rolled", roll)

    for player in chip_count:
        if chip_count[player] <= 0:
            winner = player
            found_winner = True
            break

# Endgame Logic
if player_rolls[winner] in dice_ranks.values():
    if player_rolls[winner] == dice_ranks[1000]:
        print(f"{winner}wins the game with a LoCo!")
    elif player_rolls[winner] == dice_ranks[8000]:
        print(f"{winner} wins the game with a PoCo!")
    else:
        print(f"{winner} wins the game with a Three of a Kind!")
else:
    print(f"{winner} wins the game with the highest score!")
