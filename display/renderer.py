from display.fake_maze import FakeMaze

maze = FakeMaze()


def render_maze_ascii(maze, show_path: bool, color_scheme):
    """Dibuja el laberinto en ASCII (versión básica)."""
    
    RESET = "\033[0m"

    if color_scheme == 0:
        WALL = "\033[0m"      # blanco
    elif color_scheme == 1:
        WALL = "\033[34m"     # azul
    elif color_scheme == 2:
        WALL = "\033[32m"     # verde

    for y in range(maze.height):
        # 1. Dibujar paredes norte
        top_row = ""
        for x in range(maze.width):
            top_row += WALL + "+" + RESET
            if maze.has_wall(x, y, "N"):
                top_row += WALL + "---" + RESET
            else:
                top_row += "   "
        top_row += WALL + "+" + RESET
        print(top_row)

        # 2. Dibujar paredes oeste + contenido + este
        middle_row = ""
        for x in range(maze.width):
            if maze.has_wall(x, y, "W"):
                middle_row += WALL + "|" + RESET
            else:
                middle_row += " "

            # Contenido de la celda
            if (x, y) == maze.entry:
                middle_row += " E "
            elif (x, y) == maze.exit:
                middle_row += " X "
            elif show_path and (x, y) in maze.path:
                middle_row += " . "
            else:
                middle_row += "   "

        # Última pared este de la fila
        if maze.has_wall(maze.width - 1, y, "E"):
            middle_row += WALL + "|" + RESET
        else:
            middle_row += " "

        print(middle_row)

    # 3. Dibujar la última fila de paredes sur
    bottom_row = ""
    for x in range(maze.width):
        bottom_row += WALL + "+" + RESET
        if maze.has_wall(x, maze.height - 1, "S"):
            bottom_row += WALL + "---" + RESET
        else:
            bottom_row += "   "
    bottom_row += WALL + "+" + RESET
    print(bottom_row)
