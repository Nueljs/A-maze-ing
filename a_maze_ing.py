import sys

from mazegen.config_parser import MazeConfig, parse_config
from mazegen.generator import MazeGenerator
from display.renderer import render_maze_ascii


def call_parser() -> MazeConfig:
    if len(sys.argv) != 2:
        print("Error: usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)
    config: MazeConfig = parse_config(sys.argv[1])
    return config


def run_menu() -> None:
    """Menú interactivo básico."""

    if len(sys.argv) < 2:
        print("Uso: python test_manu.py <ruta_config>")
        sys.exit(1)

    config = call_parser()
    maze = MazeGenerator(config.width, config.height, config.entry,
                         config.exit_pos, config.output_file, config.perfect,
                         config.seed)

    show_path: bool = False
    color_scheme = 0

    while True:
        print("\n=== A-Maze-ing ===")
        print("1. Re-generage a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colors")
        print("4. Quit")

        choice = input("Choice? (1-4):").strip()

        if choice == "1":
            maze.generate()
            way = maze.solve()
            render_maze_ascii(maze, show_path, color_scheme, way)
        elif choice == "2":
            show_path = not show_path
            way = maze.solve()
            render_maze_ascii(maze, show_path, color_scheme, way)
        elif choice == "3":
            color_scheme = (color_scheme + 1) % 3
            print(f"Esquema de color cambiado a {color_scheme}")
            render_maze_ascii(maze, show_path, color_scheme, way)
        elif choice == "4":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    print(call_parser())
    run_menu()

