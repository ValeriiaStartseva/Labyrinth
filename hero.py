from logging_set import logger


class Hero:
    """
    Hero class
    Attributes:
    name(str): Name of hero
    x(int): X position of the hero
    y(int): Y position of the hero
    health(int): Health of the hero
    action(int): Action taken by the hero
    medkit(int): Medkit
    has_key_flag(bool): has key hero or no
    last_position(tuple): Last position of the hero
    """
    def __init__(self, name: str, x: int, y: int) -> None:
        self.name:  str = name
        self.x: int = x
        self.y: int = y
        self.health: int = 5
        self.action: int = 1
        self.medkit: int = 3
        self.has_key_flag = False
        self.last_position = None

    def move(self, action: str):
        """
        save last position of the hero. made action of hero: healing, attack or change position
        """
        self.last_position = (self.x, self.y)

        if action == 'heal':
            self.self_heal()
        elif action == 'up':
            self.y += 1
        elif action == 'down':
            self.y -= 1
        elif action == 'right':
            self.x += 1
        elif action == 'left':
            self.x -= 1
        else:
            logger.error("Pls enter a valid direction")

    def self_heal(self):
        """
        using medical health and heal hero by 1 point
        """
        if self.medkit > 0:
            self.medkit -= 1
            self.health += 1
            logger.info("Name: %s. Health: %s. Medkit: %s", self.name, self.health, self.medkit)
        else:
            logger.error("You don't have enough medkit")

    def attack(self, other_heroes_in_same_cell: list):
        """
        attack other hero
        """
        other_hero = input("Enter the name of hero which you would like to attack: ")
        other_hero = next((hero for hero in other_heroes_in_same_cell if hero.name == other_hero), None)
        if other_hero:
            other_hero.health -= 1
            logger.info("Name: %s. have been attacked Health: %s", other_hero.name, other_hero.health)
            self.action -= 1
        else:
            logger.info("Invalid hero name. Please try again.")

    def is_alive(self):
        """
        check if hero is alive for continue the game
        """
        if self.health > 0:
            return True


