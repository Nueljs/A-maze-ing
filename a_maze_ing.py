import sys
import os
import time

from mazegen.config_parser import MazeConfig, parse_config
from mazegen.generator import MazeGenerator
from display.renderer import render_maze_ascii


# =========================
# 🎨 UI / ESTÉTICA
# =========================

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_title():
    print(r"""
 █████╗ ███╗   ███╗ █████╗ ███████╗███████╗
██╔══██╗████╗ ████║██╔══██╗╚══███╔╝██╔════╝
███████║██╔████╔██║███████║  ███╔╝ █████╗  
██╔══██║██║╚██╔╝██║██╔══██║ ███╔╝  ██╔══╝  
██║  ██║██║ ╚═╝ ██║██║  ██║███████╗███████╗
╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝

        🧩 A-MAZE-ING GENERATOR 🧩
""")


def print_menu(show_path: bool, color_scheme: int):
    print("\n╔══════════════════════════════╗")
    print("║           🧭 MENU            ║")
    print("╠══════════════════════════════╣")
    print("║ 1. 🔄 Generate new maze      ║")
    print(f"║ 2. 🧩 Toggle path [{'ON ' if show_path else 'OFF'}]      ║")
    print(f"║ 3. 🎨 Change colors [{color_scheme}]      ║")
    print("║ 4. 🚪 Exit                   ║")
    print("╚══════════════════════════════╝")


def pause():
    input("\n⏎ Press ENTER to continue...")


# =========================
# ⚙️ CONFIG
# =========================

def call_parser() -> MazeConfig:
    if len(sys.argv) != 2:
        print("Error: usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)
    return parse_config(sys.argv[1])


# =========================
# 🚀 MAIN MENU
# =========================

def run_menu() -> None:

    if len(sys.argv) < 2:
        print("Uso: python test_manu.py <ruta_config>")
        sys.exit(1)

    config = call_parser()

    maze = MazeGenerator(
        config.width,
        config.height,
        config.entry,
        config.exit_pos,
        config.output_file,
        config.perfect,
        config.seed
    )

    show_path: bool = False
    color_scheme: int = 0
    way = []
    maze_generated: bool = False

    while True:
        clear_screen()
        print_title()
        print_menu(show_path, color_scheme)

        choice = input("\n👉 Choose an option (1-4): ").strip()

        if choice == "1":
            try:
                clear_screen()
                print("🛠 Generating maze...\n")
                time.sleep(0.5)

                maze.generate()
                way = maze.solve()
                maze_generated = True

                render_maze_ascii(maze, show_path, color_scheme, way)
                pause()
            except ValueError as e:
                print(f"Error: {e}")
                sys.exit(1)

        elif choice == "2":
            if not maze_generated:
                print("\n❌ You must generate the maze first (option 1).")
                pause()
                continue

            show_path = not show_path

            clear_screen()
            print("🧩 Toggling path...\n")

            way = maze.solve()
            render_maze_ascii(maze, show_path, color_scheme, way)
            pause()

        elif choice == "3":
            color_scheme = (color_scheme + 1) % 3

            clear_screen()
            print(f"🎨 Color scheme changed to {color_scheme}\n")

            render_maze_ascii(maze, show_path, color_scheme, way)
            pause()

        elif choice == "4":
            clear_screen()
            print("\n👋 Exiting A-MAZE-ING...\n")
            time.sleep(0.5)
            break

        else:
            print("\n❌ Invalid option.")
            pause()


# =========================
# 🏁 ENTRY POINT
# =========================

if __name__ == "__main__":
    clear_screen()
    print_title()
    run_menu()
