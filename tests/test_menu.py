from display.fake_maze import FakeMaze
from display.renderer import render_maze_ascii


def run_menu():
    """Menú interactivo básico (versión paso 3)."""

    maze = FakeMaze()
    show_path: bool = False
    color_scheme = 0

    while True:
        print("\n=== A-Maze-ing ===")
        print("1. Dibujar laberinto")
        print("2. Mostrar / Ocultar camino")
        print("3. Cambiar colores")
        print("4. Salir del laberinto")

        choice = input("Elige una opción: ").strip()

        if choice == "1":
            render_maze_ascii(maze, show_path, color_scheme)
        elif choice == "2":
            show_path = not show_path
            render_maze_ascii(maze, show_path, color_scheme)
        elif choice == "3":
            color_scheme = (color_scheme + 1) % 3
            print(f"Esquema de color cambiado a {color_scheme}")
            render_maze_ascii(maze, show_path, color_scheme)
        elif choice == "4":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida.")


run_menu()
