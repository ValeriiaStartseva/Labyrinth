import json
from typing import Dict, Tuple
from cells import StartCell, EmptyCell, WallCell, FireCell, KeyCell, Golem, HearthCell, Cell


def get_cell_pydantic(data, maze_map: dict):
    """
    :param data:
    :param maze_map:
    pars data in dictionary format
    """
    for key, value in data.items():
        x, y = eval(key)
        if "StartCell" in value:
            maze_map[(x, y)] = StartCell(x=x, y=y)
        elif "EmptyCell" in value:
            maze_map[(x, y)] = EmptyCell(x=x, y=y)
        elif "WallCell" in value:
            maze_map[(x, y)] = WallCell(x=x, y=y)
        elif "FireCell" in value:
            maze_map[(x, y)] = FireCell(x=x, y=y)
        elif "KeyCell" in value:
            maze_map[(x, y)] = KeyCell(x=x, y=y)
        elif "Golem" in value:
            maze_map[(x, y)] = Golem(x=x, y=y)
        elif "HearthCell" in value:
            maze_map[(x, y)] = HearthCell(x=x, y=y)


def generate_maze_map() -> dict:
    """
    :return: maze_map: dict for the start new game
    """
    with open("maze_map.json", "r") as f:
        data = json.load(f)

    maze_map: Dict[Tuple[int, int], Cell] = {}
    get_cell_pydantic(data, maze_map)
    return maze_map


def generate_saved_maze_map() -> dict:
    """
    :return: maze_map: dict for the continue saved game
    """
    with open("saved_maze_map.json", "r") as f:
        data = json.load(f)

    maze_map: Dict[Tuple[int, int], Cell] = {}
    get_cell_pydantic(data, maze_map)
    return maze_map


# class MazMap(BaseModel):
#     maze_map: Dict[Tuple[int, int], str] = Field(default_factory=dict)
#
# with open("maze_map.json", "r") as file:
#     json_data = json.load(file)
#
# converted_data = {eval(k): v for k, v in json_data.items()}
#
# maz_map = MazMap.parse_obj({"maze_map": converted_data})
#
# print(maz_map)
