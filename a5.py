#
# Assignment 5 by Dylan Le Voguer
# May 12, 2025
#
import random

high_score = 0
high_score_player = ""
low_score = 0
low_score_player = ""

players = ["player", "cpu1", "cpu2", "cpu3"]

found_winner = False

dice_ranks = {
    1000: [1, 2, 3],
    2000: [1, 1, 1],
    3000: [2, 2, 2],
    4000: [3, 3, 3],
    5000: [4, 4, 4],
    6000: [5, 5, 5],
    7000: [6, 6, 6],
    8000: [4, 5, 6],
}

chips = {
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

for players in chips:
    print(f"{players}")
    print(f"Chips: {chips[players]}")


# roll dice for player
def roll_dice():
    roll = []
    for _ in range(3):
        roll.append(random.randint(1, 6))
    roll.sort()
    return roll


for player in player_rolls:
    score = 0
    player_rolls[player] = roll_dice()
    if player_rolls[player] in dice_ranks.values():
        score = dice_ranks
    # if player_rolls[player] == dice_ranks[7]:
    #     print(f"{player} rolled a PoCo!")
    #     high_score_player = player
    # elif player_rolls[player] == dice_ranks[0]:
    #     print(f"{player} rolled a LoCo!")
    # elif player_rolls[player] in dice_ranks.values:
    #     player_rolls[player]
    else:
        for num in player_rolls[player]:
            if num == 1:
                score += 100
            elif num == 6:
                score += 60
            else:
                score += num


print(player_rolls)
