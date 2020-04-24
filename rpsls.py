#!/usr/bin/env python3
import sys
import subprocess
from random import randrange

try:
    from termcolor import colored
except Exception as e:
    # print(e)
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "termcolor"])
    from termcolor import colored

"""This program plays a game of Rock, Paper, Scissors, Lizard, Spock between
two Players, and reports both Player's scores each round."""

moves = ["rock", "paper", "scissors", "lizard", "spock"]
moves_set = set(moves)
moves_size = len(moves)


class Player:
    """
    The Player class is the generic class for all of the other Player
    Classes: which in-turn extends from the Player Class.
    """

    def move(self):
        """
        Returns:
            "rock"
        Dummy method.
        """
        return "rock"

    def learn(self, my_move, their_move):
        """
        Args:
            my_move: Move of the Player 1.
            their_move: Move of the Player 2.
        Dummy method.
        """
        pass


class RandomPlayer(Player):
    def __init__(self):
        """
        Calling constuctor of its super class, Player.
        """
        super(RandomPlayer, self).__init__()

    def move(self):
        """
        Returns:
            Random move on the basis of the random number generated
            in the range of the size of available moves.
        """
        return moves[randrange(moves_size)]


class HumanPlayer(Player):
    def __init__(self):
        """
        Calling constuctor of its super class, Player.
        """
        super(HumanPlayer, self).__init__()

    def move(self):
        """
        Returns:
            Valid move from the available moves:(
            "rock", "paper", "scissors", "lizard", "spock") OR "quit"
        The user is supposed to either input a valid move or "quit".
        In case of an invalid input: The input prompt appears again.
        """
        while True:
            user_input = input(
                colored(
                    "(Type 'quit' to quit the game)Rock, paper, scissors,"
                    " lizard, spock? > ",
                    "blue",
                )
            )
            user_input_lower_case = user_input.lower()

            if user_input_lower_case == "quit":
                return "quit"

            if user_input_lower_case in moves_set:
                return user_input_lower_case

            print(colored("Invalid Input: Try again.", "blue"))


class ReflectPlayer(Player):
    def __init__(self):
        """
        Calling constuctor of its super class, Player.
        First move: Random, Other moves: Reflection of the opponent.
        """
        super(ReflectPlayer, self).__init__()
        self.my_next_move = moves[randrange(moves_size)]

    def move(self):
        """
        Returns:
            The "my_next_move" as determined by "learn" method.
        """
        return self.my_next_move

    def learn(self, my_move, their_move):
        """
        Args:
            my_move: Move of the Player 1.
            their_move: Move of the Player 2.
        The next move of this Player would
        be the previous move of its opponent.
        """
        self.my_next_move = their_move


class CyclePlayer(Player):
    def __init__(self):
        """
        Calling constuctor of its super class, Player.
        First move: Random, Other moves: Cycling through other moves.
        """
        super(CyclePlayer, self).__init__()
        self.my_next_move_index = randrange(moves_size)

    def move(self):
        """
        Returns:
            The first move is a random move. The next moves iterate over
            all the other possible moves one
            by one and process keeps on repeating.
        """
        my_next_move = moves[self.my_next_move_index]
        self.my_next_move_index = (self.my_next_move_index + 1) % moves_size
        return my_next_move


def beats(one, two):
    """
    Args:
        one: Move of Player one
        two: Move of Player two
    Returns:
        Boolean value of whether Player "one" move beats Player "two"
        move in a round acccording to the Game logic.(In a
        case when the moves are different)
    """
    return (
        (one == "rock" and two == "scissors")
        or (one == "scissors" and two == "paper")
        or (one == "paper" and two == "rock")
        or (one == "rock" and two == "lizard")
        or (one == "lizard" and two == "spock")
        or (one == "spock" and two == "scissors")
        or (one == "scissors" and two == "lizard")
        or (one == "lizard" and two == "paper")
        or (one == "paper" and two == "spock")
        or (one == "spock" and two == "rock")
    )


class Game:
    def __init__(self, p1, p2):
        """
        The instance data is intialised:
        p1, p2: Instances of the both Player Classes(or of the
        classes that extended Player Class)
        p1_score, p2_score: To keep track of current scores of
        Player 1 and Player 2.
        round_number: To keep track of current round number of the game.
        """
        self.p1 = p1
        self.p2 = p2
        self.p1_score, self.p2_score = 0, 0
        self.round_number = 1

    def play_round(self):
        """
        Returns:
            "quit", if the human player's move is "quit".
            "continue_playing" otherwise.
        1. Calls the "move" method of the instance of Player Class or
        of any of the Classes extended by Player Class to determine the valid
        move of a player or to validate if the human player wants to quit.
        2. Return "quit" if the move entered by human player is "quit"(case
        insensitive).
        3. If the human player enters a valid move, the "learn" methods of
        the instances of both Player Classes(or of the classes that extended
        Player Class) are called.
        4. Finally, the winner of the round is declared, the scores
        are displayed and "continue_playing" is returned.
        """
        move1 = self.p1.move()
        move2 = self.p2.move()

        if move1 == "quit" or move2 == "quit":
            return "quit"

        print(f"Player 1: {move1}  Player 2: {move2}")
        self.p1.learn(move1, move2)
        self.p2.learn(move2, move1)

        self.declare_winner_of_round(move1, move2)

        self.display_scores()

        return "continue_playing"

    def declare_winner_of_round(self, move1, move2):
        """
        Args:
            move1: Either of the five available moves:
            "rock", "paper", "scissors", "lizard", "spock"
            move2: Either of the five available moves:
            "rock", "paper", "scissors", "lizard", "spock"
        Displays the winner of the round on the basis of the moves
        of Player 1 and Player 2 with the help of "beats" method.
        """
        if move1 == move2:
            print(colored("** ROUND TIE **", "yellow"))
        elif beats(move1, move2):
            self.p1_score += 1
            print(colored("** PLAYER ONE WINS THIS ROUND. **", "green"))
        else:
            self.p2_score += 1
            print(colored("** PLAYER TWO WINS THIS ROUND. **", "red"))

    def play_game(self):
        """
        Calls the method "play_round" until the human player
        calls it quits("quit"
        is returned by "play_round" method in that case.)
        If the human player quits the game, "display_scores" and
        "declare_winner_of_game" methods are called in order to
        display the scores and winner of the game.
        """
        print(colored("Game start!", "blue"))
        while True:
            print(colored("Round ", "blue"), self.round_number, ":")
            player_quit = self.play_round()
            if player_quit == "quit":
                break
            self.round_number += 1

        self.display_scores()
        self.declare_winner_of_game()

    def display_scores(self):
        """
        Displays the scores (Instance variables: p1_score and p2_score)
        of Player 1 and Player 2 after every round.
        """
        print(colored("Scores:- ", "blue"))
        print(
            colored("Player 1: ", "green"),
            self.p1_score,
            colored("Player 2: ", "red"),
            self.p2_score,
        )

    def declare_winner_of_game(self):
        """
        Displays the winner of the game on the basis of the scores
        (Instance variables: p1_score and p2_score) of Player 1 and Player 2.
        """
        if self.p1_score == self.p2_score:
            print(colored("*** GAME TIE ***", "yellow"))
        elif self.p1_score > self.p2_score:
            print(colored("*** PLAYER ONE WINS THE GAME ***", "green"))
        else:
            print(colored("*** PLAYER TWO WINS THE GAME ***", "red"))
        print(colored("Game over!", "blue"))


if __name__ == "__main__":
    """
    An instance of Game Class is instantiated with instances of
    HumanPlayer Class and CyclePlayer Class.
    "play_game" method is called to start the game with a human
    player and a computer-programmed opponent.
    """

    # game = Game(HumanPlayer(), RandomPlayer())
    # game.play_game()

    # game = Game(HumanPlayer(), ReflectPlayer())
    # game.play_game()

    game = Game(HumanPlayer(), CyclePlayer())
    game.play_game()
