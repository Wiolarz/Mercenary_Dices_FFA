import random

''' Description:
Its a dice based FFA game. Each player goal is to increase their army by increasing it's size neutral forces.
In order to "convince" a neutral mercenary is to beat him in a fight.
Each fighter a X sided dice, which fights by rolling itself and counting it's score.

The gameplay consist only of making choices around placements of players army dices
in corresponding neutral fighters spots in order to attack them.

Structure:
1 initiate_game
    2Main
        cycle
            choice
        battle
last_fight 


current scope: no defense
'''


def choice(possibilities):
    return random.randint(0, possibilities)


def find_biggest_player(players):
    biggest_length = len(players[0])
    for player in players[1:]:
        if biggest_length < len(player):
            biggest_length = len(player)
    return biggest_length


def cycle(board, players):
    # during every round players consecutively place their dices

    table = []
    row_index = 0
    for neutral in board:
        table.append([])
        table[row_index].append([neutral])  # a neutral dice forces
        for player_index in players:
            table[row_index].append([])  # spot where player will place his dices
        row_index += 1

    biggest_player_length = find_biggest_player(players)
    for dice_index in range(biggest_player_length):
        player_index = 0
        for player in players:
            if (dice_index + 1) < len(player):  # if player has dices which he can still use
                # choosing which neutral dice to attack
                row = choice(len(table) - 1)

                # adding dice
                player_dice = player[dice_index]
                table[row][player_index].append(player_dice)  # adding dice to the pool
            player_index += 1
    won_neutral_dice = []
    for row in table:
        while True:
            # rolling the defender
            defense_score = 0
            for dice in row[0]:
                defense_score += random.randint(1, dice)
            top_score = (defense_score + 1)  # defender always wins draws

            player_index = 0
            winner_index = []
            for side in row[1:]:  # rolling players
                score = 0
                for dice in side:
                    score += random.randint(1, dice)
                if score == top_score:
                    winner_index.append(player_index)
                elif score > top_score:
                    top_score = score
                    winner_index = [player_index]
                player_index += 1

            if len(winner_index) < 2:  # neutral won / 1 player won
                if len(winner_index) == 1:
                    won_neutral_dice.append([row[0][0], winner_index[0]])
                break
    return won_neutral_dice


def last_fight(players):
    while True:
        player_index = 0
        winner_index = []
        top_score = 0
        for player in players:  # rolling players
            score = 0
            for dice in player:  # rolling player dices
                score += random.randint(1, dice)

            if score == top_score:  # draw
                winner_index.append(player_index)
            elif score > top_score:  # a winner
                top_score = score
                winner_index = [player_index]
            player_index += 1

        if len(winner_index) == 1:  # 1 player won
            return winner_index[0]


def full_game(number_of_players):
    board, players = initiate_game(number_of_players)
    number_of_cycles = 0
    while (len(board) > 0):
        number_of_cycles += 1
        if number_of_cycles == 1000:
            print("test")
        won_neutral_dice = cycle(board, players)
        for dice in won_neutral_dice:
            players[dice[1]].append(dice[0])
            board.remove(dice[0])
    return last_fight(players)


def initiate_game(number_of_players):
    table = [4, 6, 8, 10, 12, 20]
    players = []
    for i in range(number_of_players):
        players.append([4, 6, 6, 8])
    return [table, players]


def statistics_of_games(number_of_games, number_of_players):
    scoreboard = []
    for player in range(number_of_players):
        scoreboard.append(0)

    for i in range(number_of_games):
        score = full_game(number_of_players)
        # summing up scoreboard
        scoreboard[score] += 1
        print(scoreboard)


if __name__ == "__main__":
    print("Start")
    statistics_of_games(100, 3)
    print("End")




