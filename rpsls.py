#!/usr/bin/env python3
import sys
import subprocess
from random import randrange


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


install("termcolor")

from termcolor import colored

"""This program plays a game of Rock, Paper, Scissors, Lizard, Spock between two Players,
and reports both Player's scores each round."""

moves = ["rock", "paper", "scissors", "lizard", "spock"]
moves_set = set(moves)
moves_size = len(moves)

"""The Player class is the parent class for all of the Players
in this game"""


class Player:
    def move(self):
        return "rock"

    def learn(self, my_move, their_move):
        pass


class RandomPlayer(Player):
    def __init__(self):
        super(RandomPlayer, self).__init__()

    def move(self):
        return moves[randrange(moves_size)]


class HumanPlayer(Player):
    def __init__(self):
        super(HumanPlayer, self).__init__()

    def move(self):
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


class ReflectPlayer(Player):
    def __init__(self):
        # First move: Random, Other moves: Reflection of the opponent.
        super(ReflectPlayer, self).__init__()
        self.my_next_move = moves[randrange(moves_size)]

    def move(self):
        return self.my_next_move

    def learn(self, my_move, their_move):
        self.my_next_move = their_move


class CyclePlayer(Player):
    def __init__(self):
        # First move: Random, Other moves: Cycling through other moves.
        super(CyclePlayer, self).__init__()
        self.my_next_move_index = randrange(moves_size)

    def move(self):
        my_next_move = moves[self.my_next_move_index]
        self.my_next_move_index = (self.my_next_move_index + 1) % moves_size
        return my_next_move

    def learn(self, my_move, their_move):
        self.my_next_move = their_move


def beats(one, two):
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
        self.p1 = p1
        self.p2 = p2
        self.p1_score, self.p2_score = 0, 0
        self.round_number = 1

    def play_round(self):
        move1 = self.p1.move()
        move2 = self.p2.move()

        if move1 == "quit" or move2 == "quit":
            return "quit"

        print(f"Player 1: {move1}  Player 2: {move2}")
        self.p1.learn(move1, move2)
        self.p2.learn(move2, move1)

        if move1 == move2:
            print(colored("** ROUND TIE **", "yellow"))
        elif beats(move1, move2):
            self.p1_score += 1
            print(colored("** PLAYER ONE WINS THIS ROUND. **", "green"))
        else:
            self.p2_score += 1
            print(colored("** PLAYER TWO WINS THIS ROUND. **", "red"))

        return "continue_playing"

    def play_game(self):
        print(colored("Game start!", "blue"))
        while True:
            print(colored("Round ", "blue"), self.round_number, ":")
            player_quit = self.play_round()
            if player_quit == "quit":
                break
            self.round_number += 1

        self.display_scores()

    def display_scores(self):
        print(colored("Scores:- ", "blue"))
        print(
            colored("Player 1: ", "green"),
            self.p1_score,
            colored("Player 2: ", "red"),
            self.p2_score,
        )

        if self.p1_score == self.p2_score:
            print(colored("*** GAME TIE ***", "yellow"))
        elif self.p1_score > self.p2_score:
            print(colored("*** PLAYER ONE WINS THE GAME ***", "green"))
        else:
            print(colored("*** PLAYER TWO WINS THE GAME ***", "red"))
        print(colored("Game over!", "blue"))


if __name__ == "__main__":

    # game = Game(HumanPlayer(), RandomPlayer())
    # game.play_game()

    # game = Game(HumanPlayer(), ReflectPlayer())
    # game.play_game()

    game = Game(HumanPlayer(), CyclePlayer())
    game.play_game()
