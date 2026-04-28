from mazegen.config_parser import MazeConfig
from mazegen.generator import MazeGenerator
from display.renderer import render_maze_ascii


def test_render_maze_ascii() -> None:
    config = MazeConfig(
        width=5,
        height=4,
        entry=(0, 0),
        exit_pos=(4, 3),
        output_file='',
        perfect=True,
        seed=None,
    )
    maze = MazeGenerator(config)
    maze.generate()
    render_maze_ascii(maze, False, 0, [])
