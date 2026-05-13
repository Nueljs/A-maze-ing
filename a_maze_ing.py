import os
import sys
import time

from display.renderer import render_maze_ascii
from mazegen.config_parser import MazeConfig, parse_config
from mazegen.generator import MazeGenerator


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def print_title() -> None:
    print(r"""
 █████╗ ███╗   ███╗ █████╗ ███████╗███████╗
██╔══██╗████╗ ████║██╔══██╗╚══███╔╝██╔════╝
███████║██╔████╔██║███████║  ███╔╝ █████╗
██╔══██║██║╚██╔╝██║██╔══██║ ███╔╝  ██╔══╝
██║  ██║██║ ╚═╝ ██║██║  ██║███████╗███████╗
╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝

        🧩 A-MAZE-ING GENERATOR 🧩
""")


def print_menu(show_path: bool, color_scheme: int) -> None:
    print("\n╔══════════════════════════════╗")
    print("║           🧭 MENU            ║")
    print("╠══════════════════════════════╣")
    print("║ 1. 🔄 Generate new maze      ║")
    print(f"║ 2. 🧩 Toggle path [{'ON ' if show_path else 'OFF'}]      ║")
    print(f"║ 3. 🎨 Change colors [{color_scheme}]      ║")
    print("║ 4. 🚪 Exit                   ║")
    print("╚══════════════════════════════╝")


def pause() -> None:
    input("\n⏎ Press ENTER to continue...")


def call_parser() -> MazeConfig:
    if len(sys.argv) != 2:
        print("Error: usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)
    return parse_config(sys.argv[1])


def create_maze(config: MazeConfig) -> MazeGenerator:
    return MazeGenerator(
        config.width,
        config.height,
        config.entry,
        config.exit_pos,
        config.output_file,
        config.perfect,
        config.seed,
    )


def generate_maze(maze: MazeGenerator) -> list[tuple[int, int]]:
    maze.generate()
    path = maze.solve()
    if not path:
        raise ValueError("no valid path found from entry to exit")
    return path


def safe_render(
    maze: MazeGenerator,
    show_path: bool,
    color_scheme: int,
    path: list[tuple[int, int]],
) -> None:
    try:
        render_maze_ascii(maze, show_path, color_scheme, path)
    except (IndexError, KeyError, ValueError, OSError) as error:
        print(f"Error while rendering maze: {error}")


def run_menu() -> None:
    config = call_parser()
    maze = create_maze(config)

    show_path = False
    color_scheme = 0

    try:
        path = generate_maze(maze)
    except (ValueError, OSError) as error:
        print(f"Error: {error}")
        sys.exit(1)

    while True:
        clear_screen()
        print_title()
        safe_render(maze, show_path, color_scheme, path)
        print_menu(show_path, color_scheme)

        choice = input("\n👉 Choose an option (1-4): ").strip()

        if choice == "1":
            try:
                clear_screen()
                print("🛠 Generating maze...\n")
                time.sleep(0.5)

                maze = create_maze(config)
                path = generate_maze(maze)

                clear_screen()
                print_title()
                safe_render(maze, show_path, color_scheme, path)
                pause()
            except (ValueError, OSError) as error:
                print(f"Error: {error}")
                pause()

        elif choice == "2":
            show_path = not show_path

        elif choice == "3":
            color_scheme = (color_scheme + 1) % 5

        elif choice == "4":
            clear_screen()
            print("\n👋 Exiting A-MAZE-ING...\n")
            time.sleep(0.5)
            break

        else:
            print("\n❌ Invalid option.")
            pause()


if __name__ == "__main__":
    try:
        run_menu()
    except KeyboardInterrupt:
        print("\n\n👋 Exiting A-MAZE-ING...\n")
        sys.exit(0)