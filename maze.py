from cells import FireCell, KeyCell
from logging_set import logger
from hero import Hero
import random


class Maze:
    """
    Maze class
    """

    def __init__(self, maze_map: dict):
        self.maze_map: dict = maze_map

    @staticmethod
    def generate_fire_cells(maze_map: dict) -> None:
        """
        found empty cells
        make 4 random empty cells to fire cells
        logging Fire cells to console
        """
        empty_cells = [(x, y) for (x, y), cell in maze_map.items() if cell.is_empty]
        fire_cells_positions = random.sample(empty_cells, 4)
        for position in fire_cells_positions:
            maze_map[position] = FireCell(position[0], position[1])

        logger.info(f"Fire cell at position: {fire_cells_positions}")

    @staticmethod
    def generate_new_key(hero: Hero, maze_map: dict) -> None:
        """
        generate new key after dying hero who care it
        """
        logger.info("Hero name: %s. is dead!", hero.name)
        maze_map[(hero.x, hero.y)] = KeyCell(hero.x, hero.y)
        logger.info("The key is generated in cell %s.", (hero.x, hero.y))
