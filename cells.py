from typing import Optional
from pydantic import BaseModel

from hero import Hero
from logging_set import logger

"""
This module contains the pydantic models of classed used in maze map 
+ 2 method that returns maze map for the new game and saved game
"""


class Cell(BaseModel):
    """
    Cell class represents a cell on the maze
    Attributes:
        x (int): x position of the cell
        y (int): y position of the cell
        is_empty (bool): True if the cell is empty, False otherwise
    """
    x: int
    y: int
    is_empty: Optional[bool] = False
    is_orange: Optional[bool] = False

    def action(self, hero: Hero) -> None:
        pass


class WallCell(Cell):
    """
        WallCell is a child class of Cell and represents a wall
    """
    def action(self, hero: Hero) -> None:
        logger.info("This is the Wall!")
        hero.health -= 1
        if hero.health <= 0:
            logger.info("Name: %s. Unfortunately, the hero is dead! You are leaving the game! [%s]", hero.name,
                        hero.health)
        else:
            logger.info("Name: %s. Health: %s", hero.name, hero.health)
        hero.x, hero.y = hero.last_position


class StartCell(Cell):
    """
    StartCell is a child class of Cell and represents a start
    """
    pass


class EmptyCell(Cell):
    """
    EmptyCell is a child class of Cell and represents an empty cell
    """
    is_empty: Optional[bool] = True

    def action(self, hero: Hero) -> None:
        logger.info("Free way!")


class FireCell(Cell):
    """
    FireCell is a child class of Cell and represents a fire
    """

    def __init__(self, x: int, y: int, **kwargs):
        super().__init__(x=x, y=y, **kwargs)

    def action(self, hero: Hero) -> None:
        """
            The method describes the actions with the hero's attributes after he lands on a Fire cell
        """
        logger.info("This is the fire cell! Be careful!")
        hero.health -= 1
        if hero.health <= 0:
            logger.info("Name: %s. Unfortunately, the hero is dead! You are leaving the game! [%s]", hero.name,
                        hero.health)
        else:
            logger.info("Name: %s. Health: %s", hero.name, hero.health)


class KeyEmptyCell(EmptyCell):
    """
    KeyEmptyCell is a child class of EmptyCell and represents an empty cell with a key
    """

    def __init__(self, x: int, y: int):
        super().__init__(x=x, y=y, is_orange=True)


class KeyCell(Cell):
    """
    KeyCell is a child class of Cell and represents a cell with key
    """

    def __init__(self, x: int, y: int, **kwargs):
        super().__init__(x=x, y=y, **kwargs)
        self.is_orange: Optional[bool] = True

    def action(self, hero: Hero) -> None:
        """
            The method describes the actions with the hero's attributes after he lands on a cell with a key
        """
        if not hero.has_key_flag:
            hero.has_key_flag = True
            logger.info("Name: %s. Key: %s", hero.name, hero.has_key_flag)
            logger.info("You picked up the key!")
            KeyEmptyCell(x=self.x, y=self.y)
            self.__class__ = KeyEmptyCell


class Golem(Cell):
    """
    Golem is a child class of Cell and represents a cell with a golem
    """
    def action(self, hero: Hero) -> None:
        """
            The method describes the actions with the hero's attributes after he lands on a cell with Golem
        """
        if hero.has_key_flag:
            logger.info("Game over. Hero: %s. win", hero.name)
            raise GameOverException("Hero has won!")
        else:
            logger.info("Hero: %s. was murdered by the Holem", hero.name)
            hero.health = 0


class HearthCell(Cell):
    """
    HearthCell is a child class of Cell and represents a cell with hearth
    """
    def __init__(self, x: int, y: int, **kwargs):
        super().__init__(x=x, y=y, **kwargs)
        self.is_orange: Optional[bool] = True

    def action(self, hero: Hero) -> None:
        """
            The method describes the actions with the hero's attributes after he lands on a cell with Hearth
        """
        hero.health = 5
        logger.info("Name: %s. Health: %s", hero.name, hero.health)

class GameOverException(Exception):
    pass