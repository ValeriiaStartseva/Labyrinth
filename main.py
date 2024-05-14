from game import Game, signal_handler
import signal
from cells import GameOverException
from logging_set import logger


def main():
    game = Game()  # create game obg
    game.start_game()  # start the game

    def sigint_handler(signal, frame):
        signal_handler(signal, frame, game)

    signal.signal(signal.SIGINT, sigint_handler)
    signal.signal(signal.SIGTERM, sigint_handler)
    try:
        while True:
            game.play(game.maze_map)  # start playing rounds
            action = input("Action of hero or quit: ")
            if action == 'quit':
                break
        game.save_game(game.maze_map)
        game.end_game()
    except GameOverException as e:
        logger.info("Game over: %s", e)


if __name__ == "__main__":
    main()
