#
# PoCoLoco - Python Assignment 5 by Dylan Le Voguer
# May 14, 2025
#
import random
import re
import time

# Constants for the game
players = ["chosen_by_user", "CPU #1", "CPU #2", "CPU #3"]

special_combinations = {
    1000: [1, 2, 3],  # Loco!; 2 chips
    2000: [1, 1, 1],  # Three of a kinds; 3 chip
    3000: [2, 2, 2],
    4000: [3, 3, 3],
    5000: [4, 4, 4],
    6000: [5, 5, 5],
    7000: [6, 6, 6],
    8000: [4, 5, 6],  # PoCo! 4 chips
}

special_combination_names = {
    1000: "Loco!",
    2000: "Three of a kind",
    3000: "Three of a kind",
    4000: "Three of a kind",
    5000: "Three of a kind",
    6000: "Three of a kind",
    7000: "Three of a kind",
    8000: "PoCo!",
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

di_pieces = {
    "cap": " ----- ",
    "blank": "|     |",
    "left_one": "| o   |",
    "center_one": "|  o  |",
    "right_one": "|   o |",
    "two": "| o o |",
}


# Helper functions
def print_in_box(text):
    """Prints the text in a box"""
    visible_len = visible_length(text)
    print(f"\n+{'-' * (visible_len + 2)}+")
    print(f"| {text} |")
    print(f"+{'-' * (visible_len + 2)}+\n")


def visible_length(s):
    """Function to calculate visible length (ignoring ANSI codes) created by copilot"""
    return len(
        re.sub(r"\033\[[0-9;]*m", "", s)
    )  # Remove ANSI codes for length calculation


def score_string(score):
    if score in special_combination_names.keys():
        return f"\033[95m{special_combination_names[score]}\033[0m"
    else:
        return str(score)


def print_dice_roll(roll):
    """Prints the face of the dice using ASCII art horizontally"""
    str_score = score_string(calculate_score(roll))

    try:
        int(str_score)
        print(f"\n{player} rolled: {str_score} points")
    except ValueError:
        print(f"\n{player} rolled: {str_score}")
    # Declaring the 3 dice
    dice1 = assemble_di(roll[0], roll)
    dice2 = assemble_di(roll[1], roll)
    dice3 = assemble_di(roll[2], roll)

    # Printing the 3 dice properly spaced and aligned
    for i in range(len(dice1)):
        # Adjust alignment based on visible length
        line1 = dice1[i] + " " * (10 - visible_length(dice1[i]))
        line2 = dice2[i] + " " * (10 - visible_length(dice2[i]))
        line3 = dice3[i] + " " * (10 - visible_length(dice3[i]))
        print(f"{line1}{line2}{line3}")


def assemble_di(roll_value, roll):
    """Assembles the faces of the di in a list using the di_pieces dictionary"""
    di = []
    di.append(di_pieces["cap"])
    for i in range(3):  # fills the 3 rows of the di
        if i == 0:
            if roll_value == 1:
                di.append(di_pieces["blank"])
            elif roll_value in [2, 3]:
                di.append(di_pieces["left_one"])
            else:  # nums 4, 5, or 6
                di.append(di_pieces["two"])
        if i == 1:
            if roll_value == 6:
                di.append(di_pieces["two"])
            elif roll_value in [2, 4]:
                di.append(di_pieces["blank"])
            else:  # nums 1, 3, or 5
                di.append(di_pieces["center_one"])
        if i == 2:
            if roll_value == 1:
                di.append(di_pieces["blank"])
            elif roll_value in [2, 3]:
                di.append(di_pieces["right_one"])
            else:  # nums 4, 5, or 6
                di.append(di_pieces["two"])
    di.append(di_pieces["cap"])

    # Apply yellow colour if roll_value is 1 or 6
    if roll_value in [1, 6] and roll not in special_combinations.values():
        di = [f"\033[33m{line}\033[0m" for line in di]  # Apply yellow to each line

    # Apply purple coloyr if roll is a special combination
    if roll in special_combinations.values():
        di = [f"\033[95m{line}\033[0m" for line in di]  # Apply purple to each line
    return di


def calculate_score(roll):
    """Calculate the score for a given roll"""
    for key, value in special_combinations.items():
        if roll == value:
            score = key
            return score
    score = 0
    for num in roll:
        if num == 1:
            score += 100
        elif num == 6:
            score += 60
        else:
            score += num
    return score


def check_win_type(score):
    """Determine the type of win"""
    score_str = score_string(score)
    if len(score_str) > 3:
        win_type = score_str
    else:
        win_type = "default"
    return win_type


def roll_dice(remaining_rolls, player):
    """Rolls the dice for the player and returns the number of rolls."""
    roll = [random.randint(1, 6) for _ in range(3)]
    roll.sort()  # Sort the dice in ascending order
    times_rolled = 1
    done_rolling = False

    while not done_rolling:

        if player == username:
            # Player's turn
            input("\nPress enter to roll your dice")  # Wait for player to press Enter
            roll, done_rolling, times_rolled = handle_player_turn(roll, remaining_rolls)
        else:
            # CPU's turn
            roll, done_rolling, times_rolled = handle_cpu_turn(
                roll, player, remaining_rolls
            )

    roll.sort()
    player_rolls[player] = roll
    print(f"    That was {player}'s Final Roll.")
    return times_rolled


def handle_player_turn(roll, remaining_rolls):
    """Handles the player's turn, including reroll decisions."""
    roll.sort()  # Assure the dice are sorted low to high
    print_dice_roll(roll)
    rolls_taken = 1
    if remaining_rolls == 1:
        print("\nYou have no remaining rolls")
        return roll, True, rolls_taken
    else:
        while rolls_taken < remaining_rolls:
            reroll_choice = input("\nDo you want to reroll? (yes/no): ").strip().lower()
            if reroll_choice == "no":  # Player chooses not to reroll
                return roll, True, rolls_taken
            elif reroll_choice == "yes":
                reroll_input = (
                    input(
                        "\nWhich dice would you like to reroll? (Enter choice(s) separated by commas, e.g., 1, 2, 3 or 'all'): "
                    )
                    .strip()
                    .lower()
                )
                dice_to_reroll = parse_reroll_input(reroll_input)
                if dice_to_reroll is not None:
                    for i in dice_to_reroll:
                        roll[i] = random.randint(1, 6)
                    return roll, False, rolls_taken
            else:
                print("Invalid input. Please try again.")
            rolls_taken += 1
        return roll, True, rolls_taken


def handle_cpu_turn(roll, player, remaining_rolls):
    """Handles the CPU's turn, deciding which dice to reroll."""
    roll.sort()  # Assure the dice are sorted low to high
    print_dice_roll(roll)
    dice_to_reroll = []
    rolls_taken = 1
    print(f"{player} can roll {remaining_rolls} more time(s)")
    while (
        rolls_taken < remaining_rolls
    ):  # Allows CPU to roll until their rolls match the remaining rolls

        if roll in special_combinations.values():
            return roll, True, rolls_taken

        for i, die in enumerate(roll):
            dice_to_reroll = []
            # CPU logic: reroll dice that are not 1 or 6 and are not part of a pair
            if die not in [1, 6] and roll.count(die) < 2:
                dice_to_reroll.append(i)

        if dice_to_reroll:
            # Convert 0-based index to 1-based for simpler output
            reroll_indices = []
            for i in dice_to_reroll:
                reroll_indices.append(i + 1)

            # Create a string with the index of the rerolled dice
            reroll_string = ""
            for index in reroll_indices:
                if reroll_string:
                    reroll_string += ", "
                reroll_string += str(index)

            print(f"\n{player} rerolls {reroll_string}")

            for i in dice_to_reroll:
                roll[i] = random.randint(1, 6)
            rolls_taken += 1
            return roll, False, rolls_taken
        else:
            return roll, True, rolls_taken
    return roll, True, rolls_taken


def parse_reroll_input(reroll_input):
    """Parses the player's reroll input and returns a valid list of dice indices to reroll."""
    if reroll_input == "all":
        return [0, 1, 2]
    else:
        dice_to_reroll = []
        for i in reroll_input.split(","):
            if i.strip().isdigit():
                index = int(i.strip()) - 1  # Convert to zero-based index
                if 0 <= index <= 2:
                    dice_to_reroll.append(index)
        if dice_to_reroll:
            return dice_to_reroll
    print("Invalid input. Please try again.")
    return None


def tiebreaker(tied_players, type):
    """Handles the tiebreaker for players with equal scores."""
    print("\nTiebreaker! The following players are tied: ")
    for player in tied_players:
        print(f"- {player}")

    tiebreaker_scores = {}
    for player in tied_players:
        # Each player rolls 3 dice
        roll = []
        for _ in range(3):
            roll.append(random.randint(1, 6))
        tiebreaker_scores[player] = sum(roll)  # Sum of the 3 dice

    if type == "high":  # Return winner, for those who both reach 0 chips
        winner = max(tiebreaker_scores, key=tiebreaker_scores.get)
    elif type == "low":  # Return loser, for tied scores
        winner = min(tiebreaker_scores, key=tiebreaker_scores.get)
    return winner


# Game introduction
print_in_box("\033[32mWelcome to PoCoLoco!\033[0m")
print(
    "Rules: \n"
    "  1. The first player can roll up to 3 dice \n"
    "  2. Each roll, the player can choose to stop or to reroll up to 3 of their dice \n"
    "  3. The player with the lowest score gains chips from the other players \n"
    "  4. A tie is decided by each player rolling 3 dice \n"
    "  5. The first player to run out of chips is the winner \n"
)

# Ask the player for their name
while True:
    # While loop allows to take input until a valid name is entered
    try:
        username = input("\nWhat is your name?: ").strip().capitalize()
        if username == str(username) and username != "":
            break
        else:
            print("\nInvalid input. Please enter a name.")
    except ValueError:
        print("\nInvalid input. Please enter a name.")


players[0] = username  # Sets the player's name

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
while True:
    # While loop allows to take input until a valid number is entered
    try:
        num_chips = int(input("\nHow many chips do you want to start with?: "))
        if num_chips > 0:  # Checks if the number of chips is positive
            break
        else:  # If num_chips is not positive, asks for the player to enter a positive number
            print("\nInvalid input. Please enter a positive number.")
    except ValueError:
        print("\nInvalid input. Please enter a number.")

for player in chip_count.keys():
    chip_count[player] = num_chips


# Main Game Loop
round = 0
found_winner = False
while not found_winner:
    """Runs the game until a player wins by running out of chips"""

    # Prints the round
    print_in_box("Round " + str(round + 1))

    # Awaits player input before continuing to the next round
    input("Press enter to begin the round\n")

    # Reset high and low scores
    high_score = 0
    high_score_player = None
    low_score = float("inf")
    low_score_player = None

    # Reset max rolls
    num_rolls = 3
    last_num_rolls = num_rolls
    scores = {}
    # Reset player rolls
    for player in player_rolls:
        player_rolls[player] = []

    random.shuffle(players)

    for player in players:
        time.sleep(2)
        score = 0

        last_num_rolls = roll_dice(last_num_rolls, player)

        score = calculate_score(player_rolls[player])
        scores[player] = score
        # Set high score and player
        high_score = max(high_score, score)
        high_score_player = max(scores, key=scores.get)

        # Set low score and player
        low_score = min(scores.values())
        low_score_players = []  # List of players with lowest score in case of ties
        for player, score in scores.items():
            if score == low_score:
                low_score_players.append(player)

    if len(low_score_players) > 1:  # If there is a tie for loser
        low_score_player = tiebreaker(low_score_players, "low")
    else:
        low_score_player = low_score_players[0]

    round += 1

    # Determine how many chips to be taken from the winners
    if high_score in chip_deduction:
        taken_chips = chip_deduction.get(high_score, 0)
    else:
        taken_chips = 1  # Num of chips to be taken if not in the ranks

    # Deducts chips from the winners and adds them to the loser
    for player in chip_count:
        if player == low_score_player:
            chip_count[player] += taken_chips * (
                len(players) - 1
            )  # chip(s) taken from each player and given to the loser
        else:
            chip_count[player] -= taken_chips

    win_type = check_win_type(high_score)

    if win_type != "default":
        print(
            f"\n\033[32m{high_score_player}\033[0m wins the round with a {win_type} and each player gives \033[31m{low_score_player}\033[0m {taken_chips} chip(s)"
        )
    else:
        print(
            f"\n\033[32m{high_score_player}\033[0m wins the round with a score of {high_score} and each player gives \033[31m{low_score_player}\033[0m {taken_chips} chip(s)"
        )

    print_in_box(f"Chips after Round {round}:")
    for player, chips in chip_count.items():
        if chips < 0:
            chips = 0
        if player == low_score_player:
            print(
                f"\033[31m{player}\033[0m has {chips} chips (+\033[31m{taken_chips * 3}\033[0m)"
            )
        elif player == high_score_player:
            print(
                f"\033[32m{player}\033[0m has {chips} chips (-\033[32m{taken_chips}\033[0m)"
            )
        else:
            print(f"{player} has {chips} chips (-\033[32m{taken_chips}\033[0m)")

    winner = []
    for player in chip_count.keys():
        if chip_count[player] <= 0:
            winner.append(player)
            found_winner = True
            break
    if len(winner) > 1:
        winner = tiebreaker(winner, "high")
    str_winner = "".join(winner)
# Printing the final results
print_in_box(f"\033[32m{str_winner}\033[0m wins the game by reaching 0 chips!")
print_in_box(
    f"\033[31m{low_score_player}\033[0m loses the game with {chip_count[low_score_player]} chips!"
)
