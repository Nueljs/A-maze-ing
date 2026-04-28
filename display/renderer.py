from typing import cast

from mazegen.generator import MazeGenerator

# Constantes de dirección (igual que en generator.py)
N, E, S, W = 1, 2, 4, 8
DIR_MAP = {"N": N, "E": E, "S": S, "W": W}


def has_wall(maze: MazeGenerator, x: int, y: int, direction: str) -> bool:
    """Traduce la interfaz string → bitmask del MazeGenerator."""
    cell = maze.get_cell(x, y)
    return bool(cell & DIR_MAP[direction])


def render_maze_ascii(
    maze: MazeGenerator,
    show_path: bool,
    color_scheme: int,
    way: list[tuple[int, int]],
) -> None:
    """Dibuja el laberinto en ASCII."""
    RESET = "\033[0m"

    if color_scheme == 0:
        WALL = "\033[0m"
    elif color_scheme == 1:
        WALL = "\033[34m"
    elif color_scheme == 2:
        WALL = "\033[32m"
    else:
        WALL = "\033[0m"

    # maze.exit_pos en lugar de maze.exit
    path = cast(set[tuple[int, int]], getattr(maze, 'path', set()))

    for y in range(maze.height):
        # 1. Paredes norte
        top_row = ""
        for x in range(maze.width):
            top_row += WALL + "+" + RESET
            if has_wall(maze, x, y, "N"):
                top_row += WALL + "---" + RESET
            else:
                top_row += "   "
        top_row += WALL + "+" + RESET
        print(top_row)

        # 2. Paredes oeste + contenido + este
        middle_row = ""
        for x in range(maze.width):
            if has_wall(maze, x, y, "W"):
                middle_row += WALL + "|" + RESET
            else:
                middle_row += " "

            if (x, y) == maze.entry:
                middle_row += " E "
            elif (x, y) == maze.exit_pos:   # <-- exit_pos
                middle_row += " X "
            elif show_path and (x, y) in path:
                middle_row += " . "
            elif maze.is_42_cell(x, y):
                middle_row += " * "
            elif show_path and (x, y) in way:
                middle_row += " . "
            else:
                middle_row += "   "

        if has_wall(maze, maze.width - 1, y, "E"):
            middle_row += WALL + "|" + RESET
        else:
            middle_row += " "

        print(middle_row)

    # 3. Última fila sur
    bottom_row = ""
    for x in range(maze.width):
        bottom_row += WALL + "+" + RESET
        if has_wall(maze, x, maze.height - 1, "S"):
            bottom_row += WALL + "---" + RESET
        else:
            bottom_row += "   "
    bottom_row += WALL + "+" + RESET
    print(bottom_row)
