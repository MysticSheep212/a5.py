#
# Assignment 5 by Dylan Le Voguer
# May 12, 2025
#
import random
import re

# Constants for the game
players = ["chosen_by_user", "CPU #1", "CPU #2", "CPU #3"]

dice_ranks = {
    1000: [1, 2, 3],  # Loco!; 2 chips
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


def print_dice_roll(roll):
    """Prints the face of the dice using ASCII art horizontally"""
    print(f"\n{player.capitalize()} rolled : {calculate_score(roll)} points")

    # Declaring the 3 dice
    dice1 = assemble_di(roll[0])
    dice2 = assemble_di(roll[1])
    dice3 = assemble_di(roll[2])

    # Printing the 3 dice properly spaced and aligned
    for i in range(len(dice1)):
        # Adjust alignment based on visible length
        line1 = dice1[i] + " " * (10 - visible_length(dice1[i]))
        line2 = dice2[i] + " " * (10 - visible_length(dice2[i]))
        line3 = dice3[i] + " " * (10 - visible_length(dice3[i]))
        print(f"{line1}{line2}{line3}")


def assemble_di(roll_value):
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
    if roll_value in [1, 6]:
        di = [f"\033[33m{line}\033[0m" for line in di]  # Apply yellow to each line

    return di


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


def check_win_type(score):
    """Determine the type of win"""
    if score == 1000:
        win_type = "\033[95mLoco!\033[0m"
    elif 1000 < score < 8000:
        win_type = "\033[95mThree of a kind\033[0m"
    elif score == 8000:
        win_type = "\033[95mPoCo!\033[0m"
    else:
        win_type = "default"
    return win_type


def roll_dice(num_rolls, player):
    """Rolls the dice for the player and returns the number of rolls."""
    roll = [random.randint(1, 6) for _ in range(3)]
    times_rolled = 1
    done_rolling = False

    while not done_rolling and times_rolled < num_rolls:
        # Check if the roll is a special combination
        if roll in dice_ranks.values():
            break

        # Calculate the current score
        score = calculate_score(player_rolls[player])

        # Stop rolling if the score is between 100 and 200
        if 200 > score > 100:
            break

        if player == username:
            # Player's turn
            roll = handle_player_turn(roll)
            done_rolling = roll is None  # If player chooses not to reroll
        else:
            # CPU's turn
            roll = handle_cpu_turn(roll)

        times_rolled += 1

        # Check again if the roll is a special combination
        if roll in dice_ranks.values():
            break

    roll.sort()  # Sort the roll to make it easier to compare
    player_rolls[player] = roll
    print_dice_roll(player_rolls[player])
    return times_rolled


def handle_player_turn(roll):
    """Handles the player's turn, including reroll decisions."""
    print_dice_roll(roll)
    while True:
        reroll_choice = input("\nDo you want to reroll? (yes/no): ").strip().lower()
        if reroll_choice == "no":
            return roll  # Player chooses not to reroll
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
                return roll
        else:
            print("Invalid input. Please try again.")


def handle_cpu_turn(roll):
    """Handles the CPU's turn, deciding which dice to reroll."""
    print_dice_roll(roll)
    dice_to_reroll = []
    for i, die in enumerate(roll):
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

        print(f"\nCPU rerolls: {reroll_string}")
    else:
        print("\nCPU does not reroll")
    for i in dice_to_reroll:
        roll[i] = random.randint(1, 6)
    return roll


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


# Game setup
print_in_box("\033[32mWelcome to PoCoLoco!\033[0m")
print(
    "Rules: \n"
    "  1. The first player can roll up to 3 dice \n"
    "  2. Each roll, the player can choose to stop or to reroll up to 3 of their dice \n"
    "  3. The player with the lowest score gains chips from the other players \n"
    "  4. The first player to run out of chips is the winner"
)

# Ask the player for their name
players[0]
username = input("\nWhat is your name?: ").strip()
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
    print_in_box("Round " + str(round + 1))

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
            chip_count[player] += taken_chips * (
                len(players) - 1
            )  # chip(s) taken from each player and given to the loser
        else:
            chip_count[player] -= taken_chips

    win_type = check_win_type(high_score)

    if win_type != "default":
        print(
            f"\n\033[32m{high_score_player}\033[0m wins the round with a {win_type} and each player gives \033[31m{low_score_player}\033[0m {taken_chips // 3} chips"
        )
    else:
        print(
            f"\n\033[32m{high_score_player}\033[0m wins the round with a score of {high_score} and each player gives \033[31m{low_score_player}\033[0m {taken_chips // 3} chips"
        )

    print_in_box(f"Chips after Round {round}:")
    for player, chip in chip_count.items():
        if chip < 0:
            chip = 0
        if player == low_score_player:
            print(f"\033[31m{player} has {chip} chips\033[0m")
        elif player == high_score_player:
            print(f"\033[32m{player} has {chip} chips\033[0m")
        else:
            print(player, "has", chip, "chips")

    for player in chip_count:
        if chip_count[player] <= 0:
            winner = player
            found_winner = True
            break

# Printing the final results
print_in_box(f"\033[32m{winner}\033[0m wins the game by reaching 0 chips!")
print_in_box(
    f"\033[31m{low_score_player}\033[0m loses the game with {chip_count[low_score_player]} chips!"
)
