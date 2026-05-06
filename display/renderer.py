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
    """Dibuja el laberinto en ASCII (modo holograma sci-fi)."""

    RESET = "\033[0m"

    # Paleta holográfica rotatoria
    HOLO_COLORS = [
        "\033[96m",  # cian neón
        "\033[95m",  # magenta neón
        "\033[92m",  # verde neón
        "\033[93m",  # amarillo neón
        "\033[97m",  # blanco brillante
    ]

    HOLO = HOLO_COLORS[color_scheme % len(HOLO_COLORS)]
    WALL = HOLO

    # 🔥 Camino siempre rojo
    RED = "\033[91m"

    # Símbolos holográficos
    CROSS = "╬"
    H_WALL = "═══"
    V_WALL = "║"

    CELL_ENTRY = "▶"
    CELL_EXIT = "◆"
    CELL_PATH = "◉"   # camino
    CELL_42 = "✦"
    CELL_EMPTY = "·"

    # maze.exit_pos en lugar de maze.exit
    path = cast(set[tuple[int, int]], getattr(maze, 'path', set()))

    for y in range(maze.height):
        # 1. Paredes norte
        top_row = ""
        for x in range(maze.width):
            top_row += WALL + CROSS + RESET
            if has_wall(maze, x, y, "N"):
                top_row += WALL + H_WALL + RESET
            else:
                top_row += "   "
        top_row += WALL + CROSS + RESET
        print(top_row)

        # 2. Paredes oeste + contenido + este
        middle_row = ""
        for x in range(maze.width):
            if has_wall(maze, x, y, "W"):
                middle_row += WALL + V_WALL + RESET
            else:
                middle_row += " "

            # Contenido de la celda
            if (x, y) == maze.entry:
                middle_row += f" {HOLO}{CELL_ENTRY}{RESET} "
            elif (x, y) == maze.exit_pos:
                middle_row += f" {HOLO}{CELL_EXIT}{RESET} "
            elif show_path and (x, y) in path:
                middle_row += f" {RED}{CELL_PATH}{RESET} "   # 🔥 camino rojo
            elif maze.is_42_cell(x, y):
                middle_row += f" {HOLO}{CELL_42}{RESET} "
            elif show_path and (x, y) in way:
                middle_row += f" {RED}{CELL_PATH}{RESET} "   # 🔥 camino rojo
            else:
                middle_row += f" {CELL_EMPTY} "

        if has_wall(maze, maze.width - 1, y, "E"):
            middle_row += WALL + V_WALL + RESET
        else:
            middle_row += " "

        print(middle_row)

    # 3. Última fila sur
    bottom_row = ""
    for x in range(maze.width):
        bottom_row += WALL + CROSS + RESET
        if has_wall(maze, x, maze.height - 1, "S"):
            bottom_row += WALL + H_WALL + RESET
        else:
            bottom_row += "   "
    bottom_row += WALL + CROSS + RESET
    print(bottom_row)
