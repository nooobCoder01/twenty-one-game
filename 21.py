import time
import random

def display_rules():
    print("""
    _____________________________________________________________________________
    Twenty One is a game of chance where players take turns rolling two dice every 
    round until they decide to stop rolling and lock in their score or end up 
    going bust with a total over 21. The objective is to be the closest to 21 
    when everyone is done rolling.

    Rules are as per follows:
    - Players begin with a score of 0.
    - Each player has one turn to either roll or stop rolling each round.
    - Players can only do a regular roll of two dice until they 
        reach a score of at least 14.
    - Players with a score >= 14 have the option to only roll one dice.
    - If a player scores more than 21 they go bust and are out of the game.
    - The winning player is the one with the score closest to 21 when everyone 
        has finished rolling.
    - If all players go bust, no one wins.
    - If more than one player has the winning score, no one wins.
    _____________________________________________________________________________
    """)
    input("Press enter to go back")
    return


def display_main_menu():
    print("------------Main Menu------------")
    print("Welcome to Twenty One!")
    print("1. Solo")
    print("2. Local Multiplayer")
    print("3. Rules")
    print("4. Exit")
    print("---------------------------------")


def int_input(prompt="", restricted_to=None):
    """
    Helper function that modifies the regular input method,
    and keeps asking for input until a valid one is entered. Input 
    can also be restricted to a set of integers.

    Arguments:
    - prompt: String representing the message to display for input
    - restricted: List of integers for when the input must be restricted
                to a certain set of numbers

    Returns the input in integer type.
    """
    while True:
        player_input = input(prompt)
        try:
            int_player_input = int(player_input)
        except ValueError:
            continue
        if restricted_to is None:
            break
        elif int_player_input in restricted_to:
            break

    return int_player_input


def cpu_player_choice(score):
    """
    This function simply returns a choice for the CPU player based
    on their score.

    Arguments:
    - score: Int

    Returns an int representing a choice from 1, 2 or 3.
    """
    time.sleep(2)
    if score < 14:
        return 1
    elif score < 17:
        return 3
    else:
        return 2


def display_game_options(player):
    """
    Prints the game options depending on if a player's score is
    >= 14.

    Arguments:
    - player: A player dictionary object
    """

    print("------------" + player["name"] + "'s turn------------")
    print(player["name"]  + "'s score: " + str(player['score']))
    print("1. Roll\n2. Stay")
    if player['score'] >= 14:
        print("3. Roll One")


def display_round_stats(round, players):
    """
    Print the round statistics provided a list of players.

    Arguments:
    - round: Integer for round number
    - players: A list of player-dictionary objects
    """
    print("-----------Round " + str(round) + "-----------")
    for i in range(len(players)):
        print(players[i]["name"] + " is at " + str(players[i]["score"]))


def roll_dice(num_of_dice=1):
    """
    Rolls dice based on num_of_dice passed as an argument.

    Arguments:
    - num_of_dice: Integer for amount of dice to roll

    Returns the following tuple: (rolls, display_string)
    - rolls: A list of each roll result as an int
    - display_string: A string combining the dice art for all rolls into one string
    """
    die_art = {
    1: ["┌─────────┐", "│         │", "│    ●    │", "│         │", "└─────────┘"],
    2: ["┌─────────┐", "│  ●      │", "│         │", "│      ●  │", "└─────────┘"],
    3: ["┌─────────┐", "│  ●      │", "│    ●    │", "│      ●  │", "└─────────┘"],
    4: ["┌─────────┐", "│  ●   ●  │", "│         │", "│  ●   ●  │", "└─────────┘"],
    5: ["┌─────────┐", "│  ●   ●  │", "│    ●    │", "│  ●   ●  │", "└─────────┘"],
    6: ["┌─────────┐", "│  ●   ●  │", "│  ●   ●  │", "│  ●   ●  │", "└─────────┘"]
    }

    output = []
    dieResult = []
    dieArt = ""
    # For loop to create die results randomly between 1, 6 and store them in the dieResult list
    for i in range(num_of_dice):
        dieResult.append(random.randint(1,6))

    #for loop to print the die faces. The first line adds all the elemetnts inside the number we are looking at with a newline character after each item. The formed die face is added to the dieArt string
    #Then a new line character is added to make space for the next die face to print underneath.
    for i in dieResult: 
        dieArt += "\n".join(die_art[i])
        dieArt += "\n"

    #As output is a list of lists containing at 0 index is dieresult and 1st index the string of die faces.
    output = [dieResult, dieArt]
    return output


def execute_turn(player, player_input):
    """
    Executes one turn of the round for a given player.

    Arguments:
    - player: A player dictionary object

    Returns an updated player dictionary object.
    """
    # Executes for when player decides to roll both.
    if player_input == 1:
        print("Rolling both...")
        result = roll_dice(2)
        print(result[1])

        #updating the score value for the player
        for i in range(len(result[0])):
            player["score"] += result[0][i]
        #Updating the at 14 counter for the player
        if player["score"] >= 14:
            player["at_14"] = True

        print(player["name"] + " is now on " + str(player["score"]))
        #Updating the bust counter if player has gone above 21 after turn.
        if player["score"] > 21:
            player["bust"] = True
            print(player["name"] + " goes bust!")

    #Execute for when player decides to stay
    elif player_input == 2:
        print(player["name"] + " has stayed with a score of " + str(player["score"]))
        player["stayed"] = True

    #Execute for when player decides to roll one dice.
    elif player_input == 3:
        print("Rolling one...")
        result = roll_dice(1)
        print(result[1])

        #Updating the score for player
        player["score"] += result[0][0]

        print(player["name"] + " is now on " + str(player["score"]))

        #Updating the bust counter if player has gone above 21 after turn.
        if player["score"] > 21:
            player["bust"] = True
            print(player["name"] + " goes bust!")

    return player


def end_of_game(players):
    """
    Takes the list of all players and determines if the game has finished,
    returning false if not else printing the result before returning true.

    Arguments:
    - players: A list of player-dictionary objects

    Returns True if round has ended or False if not. If true results are
    printed before return.
    """

    bust_counter = 0
    stay_counter = 0
    winner_index = 0
    #To count if there is  draw in hte lsit of players. Value is -1 to count the match that is the winning score otherwise it will double count.
    draw_counter = -1
    winning_score = 21
    #for loop to loop over all player
    for i in range(len(players)):
        #bust counter that checks if a player is bust or not
        if players[i]["bust"] == True:
            bust_counter += 1
            #if player is bust we do not want to increase stay counter or check if player has winning score
            continue

        #To count the number of players who have stayed
        elif players[i]["stayed"] == True:
            stay_counter += 1

        #Winning score is initialised as 21 and updated after as 21 - player score.
        #check if player has a score less than winning score. The score lower than winning score is set as winning score. The index for winning scorer is also stored.
        if 21 - players[i]["score"] < winning_score:
            winning_score = 21 - players[i]["score"]
            winner_index = i

    #Game only ends if every player is bust or has stayed! Therefore bust & stay counter must equal length of players list.
    if (bust_counter + stay_counter) == len(players):
        #if bust counter is equal to length of players list. Then no one won.
        if bust_counter == len(players):
            print("Everyone's gone bust! No one wins :(")
            return True
        # To check if the game is a draw or not. It checks if 21 - players scores in players list = winning score. It increments draw counter by 1 if it is.
        for i in range(len(players)):
            if winning_score == 21-players[i]["score"]:
                draw_counter += 1
            
        #Draw counter has to be equal or greater than 1. To tell us that there are 2 or more matches with same winning score.
        if draw_counter >= 1:
            print("The game is a draw! No one wins :(")
            return True
        #Otherwise we return the player with the winning score
        else:
            print(players[winner_index]["name"] + " is the winner!")
            return True

    else:
        return False

def solo_game():
    """
    This function defines a game loop for a solo game of Twenty One against 
    AI.
    """
    #Intialise the players list
    players = [{'name': 'Player 1', 'score': 0, 'stayed': False, 'at_14': False, 'bust': False},
           {'name': 'CPU Player', 'score': 0, 'stayed': False, 'at_14': False, 'bust': False}]
    
    #Initialising round from 0
    round = 0
    #While loop runs until end  of game function returns True
    while end_of_game(players) == False:
        #Round stats are diaplyed before each round
        display_round_stats(round,players)

        #Options for player 1 are displayed
        display_game_options(players[0])
        #Player input is restricted to 1,2,3 as there is no other option a player shoudl be allowed to select
        player_input = int_input("Please enter an option: ",[1,2,3])
        execute_turn(players[0], player_input)

        #Options for CPU player are displayed
        display_game_options(players[1])
        #cpu player choice function is used to calculate cpu's input
        player_input = cpu_player_choice(players[1]["score"])
        execute_turn(players[1], player_input)

        #Round is incremented by 1 at the end of each round
        round += 1
      

def multiplayer_game(num_of_players):
    """
    This function defines a game loop for a local multiplayer game of Twenty One, 
    where each iteration of the while loop is a round within the game. 
    """

    #Creating player dictionaries for the number of players
    players = [0]*num_of_players
    for i in range(num_of_players):
        players[i] = {"name": ("Player " + str(i+1)), "score": 0, 'stayed': False, 'at_14': False, 'bust': False}

    #Initialising round from 0
    round = 0
    #loop will run while end of game returns False. When it returns true means the game as ended.
    while end_of_game(players) == False:
        display_round_stats(round,players)

        #Loop for displaying scores and executing turns for each player
        for i in range(len(players)):
            display_game_options(players[i])
            #if player has gone bust they should not be allowed to play anymore
            if players[i]["bust"] == True:
                print(players[i]["name"] + " goes bust!")
                continue
            #If player has decided to stay they should not be allowed to play anymore
            elif players[i]["stayed"] == True:
                print(players[i]["name"] + " has stayed with a score of " + str(players[i]["score"]))
                continue

            #If player is not bust or has not stayed. Ask for player input and execute turn for that input. Limiting the input to 1,2,3.
            player_input = int_input("Please enter an option: ",[1,2,3]) 
            execute_turn(players[i], player_input)

        round += 1


def main():

    while True:
        display_main_menu()

        input = int_input("Choose from the following options: ", [1,2,3,4])

        if input == 1:
            solo_game()
        elif input == 2:
            num_of_players = int_input("Number of players: ", [2,3,4,5,6,7,8,9,10,11,12,13,14,15])
            multiplayer_game(num_of_players)
        elif input == 3:
            display_rules()
        elif input == 4:
            break


main()