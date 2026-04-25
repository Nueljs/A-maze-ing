from .config_parser import MazeConfig
import random


# Direction constatns
N, E, S, W = 1, 2, 4, 8


class MazeGenerator:
    """Generates a maze using recursive backtraket (DFS).

    Args:
        config: Parsed maze configuration
    """
    def __init__(self, config: MazeConfig) -> None:
        self._grid: list[list[int]] = []
        self._config: MazeConfig = config
        self._width: int = config.width
        self._height: int = config.height
        self._42_cells: set[tuple[int, int]] = set()

    @property
    def width(self) -> int:
        """Maze width in cells."""
        return self._width

    @property
    def height(self) -> int:
        """Maze height in cells."""
        return self._height

    @property
    def entry(self) -> tuple[int, int]:
        """Entry point coordinates (x, y)."""
        return self._config.entry

    @property
    def exit_pos(self) -> tuple[int, int]:
        """Exit point coordinates (x, y)."""
        return self._config.exit_pos

    def get_cells(self, x: int, y: int) -> int:
        """Return de wallt bitmask for cell (x, y).

        Args:
            x: Columns index.
            y: Row index.

        Returns:
            Integer 0-15 representing walls.
        """
        return self._grid[y][x]

    def is_42_cell(self, x: int, y: int) -> bool:
        """Return True if cell (x, y) is part of the '42' pattern

        Args:
            x: Column index
            y: Row index
        Returns:
        True if the cell belongs to the 42 pattern.
        """
        return (x, y) in self._42_cells 

    def generate(self) -> None:
        """Generate the maze using recursive backtracker (DFS)"""
        if self._config.seed is not None:
            random.seed(self._config.seed)

        self._grid = [[15] * self._width for _ in range(self._height)]

        self._run_dfs()
        self._open_entry_exit()
        self._place_42_pattern()