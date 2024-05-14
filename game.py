from hero import Hero
from logging_set import logger
from cells import WallCell
from maze import Maze
import json
import os
from load_maze_map_from_json import generate_maze_map, generate_saved_maze_map
from dict_param import valid_actions


class Game:
    """
    The game class describe main methods of the game
    Attributes:
        heroes (list of Hero): The list of heroes
        maze_map (dict): The maze
    """

    def __init__(self):
        self.heroes: list = []
        self.maze_map: dict = {}

    def start_game(self):
        """
        func for starting the game. Ask user to load previous game from json file or start new game
        """
        if os.path.getsize("saved_game.json") == 0:
            self.start_new_game()       # there is no saved game. Start new game
        else:
            logger.info("There is a saved game")
            action = None
            while action not in ('yes', 'no'):
                action = input("Do you want to continue the game? (yes/no): ").lower()
                if action == 'yes':
                    self.load_game()
                elif action == 'no':
                    self.start_new_game()
                else:
                    logger.info("Please enter yes or no")

    def start_new_game(self):
        """
        func for starting new game
        ask and save number of heroes, and set coord as (0, 0)
        """
        self.maze_map = generate_maze_map()
        num_heroes = int(input("How many players?: "))
        for i in range(num_heroes):
            hero_name = input(f"Pls enter the name player № {i + 1}: ")
            self.heroes.append(Hero(hero_name, 0, 0))
        Maze.generate_fire_cells(self.maze_map)     # make fire on maze

    @staticmethod
    def find_heroes_in_same_cell(heroes: list, current_hero: Hero):
        """
        Func looking for heroes in the same cell

        Param:
        - heroes (list): list of heroes
        - current_hero (Hero): current hero
        Return:
        - other_hero (list): list of heroes that in the same cell as current_hero
        """
        other_hero = [hero for hero in heroes if hero != current_hero and (hero.x, hero.y) == (current_hero.x,
                                                                                               current_hero.y)]
        if len(other_hero) > 0:
            logger.info('Other heroes in the same cell: %s.', [hero.name for hero in other_hero])
        return other_hero

    def escape_cell(self, last_position1, hero: Hero, maze_map) -> None:
        """
        Func checks escape hero or no

        Param:
        - hero (Hero): current hero
        - maze_map (dict): maze map
        """

        cell_at_last_position = maze_map.get(hero.last_position)
        if (hero.x, hero.y) == last_position1 and cell_at_last_position.is_orange:
            logger.info("Not escape")

        elif (hero.x, hero.y) == last_position1:
            logger.info("Hero name: %s. escaped!", hero.name)
            hero.health = 0
            self.heroes.remove(hero)

    def check_hero_in_game(self):
        print('----------------------------------')
        if len(self.heroes) == 0:
            logger.info("All heroes are dead!")
            self.end_game()
            return True

    # def turn_direction(self, hero, action, other_heroes_in_same_cell, last_position1, maze_map) -> None:
    #     if other_heroes_in_same_cell and action == "attack":
    #         hero.attack(other_heroes_in_same_cell)
    #     elif action == "save":
    #         self.save_game(maze_map)
    #     else:
    #         hero.move(action)
    #         cell_at_new_position = maze_map.get((hero.x, hero.y))  # get t of cell
    #         if cell_at_new_position is None:
    #             WallCell(x=2, y=0, is_empty=False).action(hero)
    #         else:
    #             cell_at_new_position.action(hero)  # action after moving
    #             self.escape_cell(last_position1, hero, maze_map)  # func check escape hero

    def is_dead(self, hero):
        if hero.health <= 0 and hero.has_key_flag:
            Maze.generate_new_key(hero, self.maze_map)  # func generate new key after dying hero
            self.heroes.remove(hero)
            logger.info("Hero is dead")
        elif hero.health <= 0:
            self.heroes.remove(hero)
            logger.info("Hero is dead")

    def play(self, maze_map: dict) -> None:
        """
        func for describe main playing process
        1. Check if hero is alive
        2. Check if heroes are in the same cell
        3. hero choose action
        4. logging what happened with hero and pass the move to other hero
        """
        while True:
            if self.check_hero_in_game():
                break
            else:
                for current_player in self.heroes:
                    if current_player.is_alive():
                        other_heroes_in_same_cell = self.find_heroes_in_same_cell(self.heroes, current_player)
                        logger.info("Hero name: %s. Your turn!", current_player.name)
                        action = input("Enter action: heal, attack, save or move(up, right, down, left): ").lower()
                        while action not in valid_actions:
                            logger.info("Invalid action! Please enter: heal, attack, save or move!")
                            action = input("Enter action: heal, attack, save or move(up, right, down, left): ").lower()
                        last_position1 = current_player.last_position
                        if other_heroes_in_same_cell and action == "attack":
                            current_player.attack(other_heroes_in_same_cell)
                        elif action == "save":
                            self.save_game(maze_map)
                        else:
                            current_player.move(action)
                            cell_at_new_position = maze_map.get((current_player.x, current_player.y))  # get t of cell
                            if cell_at_new_position is None:
                                WallCell(x=2, y=0, is_empty=False).action(current_player)
                            else:
                                cell_at_new_position.action(current_player)  # action after moving
                                self.escape_cell(last_position1, current_player, maze_map)  # func check escape hero
                    else:
                        self.is_dead(current_player)

    def save_game(self, maze_map: dict) -> None:
        """
        func for saving game to json file
        """
        heroes_data = []
        for hero in self.heroes:
            hero_data = {
                "name": hero.name,
                "health": hero.health,
                "x": hero.x,
                "y": hero.y,
                "has_key_flag": hero.has_key_flag,
                "medkit": hero.medkit,
                "last_position": hero.last_position,
                "action": hero.action,
            }
            heroes_data.append(hero_data)

        game_state = {
            "heroes": heroes_data
        }
        print(game_state)

        maze_map_str_keys = {str(k): v.__class__.__name__ for k, v in maze_map.items()}

        with open("saved_game.json", 'w') as f:  # saving info about heroes to json
            json.dump(game_state, f)

        with open("saved_maze_map.json", 'w') as m:  # saving info about maze map to json
            json.dump(maze_map_str_keys, m, indent=4)

    def load_game(self):
        """
        func for loading game from json file
        """

        self.maze_map = generate_saved_maze_map()

        with open("saved_game.json", 'r') as game_file:
            game_state = json.load(game_file)
            heroes_data = game_state.get("heroes", [])

        self.heroes = [Hero(hero_data["name"], hero_data["x"], hero_data["y"]) for hero_data in heroes_data]

        logger.info("Game loaded successfully")

    @staticmethod
    def end_game():
        """
        func for ending game
        """
        logger.info("Game over")


def signal_handler(signal, frame, game):
    """

    :param signal:
    :param frame:
    :param game:
    функція відслідковує чи було штучно закрита гра і зберігає її
    """
    print("\nProgram interrupted. Saving game...")
    game.save_game(game.maze_map)
    print("Game saved successfully.")
    exit(0)
