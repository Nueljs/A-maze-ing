from .config_parser import MazeConfig
import random


# Direction constatns
N, E, S, W = 1, 2, 4, 8
opposite: dict[int, int] = {N: S, S: N, E: W, W: E}


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
        """Entry point coordinates (c, r)."""
        return self._config.entry

    @property
    def exit_pos(self) -> tuple[int, int]:
        """Exit point coordinates (c, r)."""
        return self._config.exit_pos

    def _get_unvisited_neighbors(
        self, c: int, r: int, visited: set[tuple[int, int]]
    ) -> list[tuple[int, int, int]]:
        """Return unvisited neighbors of cell (c, r)

        Args:
            c: column index.
            r: row index.
            visited: set of already visited cells.

        Returns:
            List of (nc, nr, direction) tuples where direction
            is the wall constant (N, E S, W)
        """
        neighbors: list[tuple[int, int, int]] = []
        candidates: list[tuple[int, int, int]] = [
            (c, r - 1, N), (c + 1, r, E), (c, r + 1, S), (c - 1, r, W)]
        for nc, nr, direction in candidates:
            if ((0 <= nc < self._width) and (0 <= nr < self._height)
                    and ((nc, nr) not in visited)):
                neighbors.append((nc, nr, direction))
        return neighbors

    def _run_dfs(self) -> None:
        """"
        Run recursive backtracker DFS (Depth-First Search) to carve the maze
        """
        visited: set[tuple[int, int]] = set()
        stack: list[tuple[int, int]] = []

        # First cell, we use entry as a start point
        start = self._config.entry
        visited.add(start)
        stack.append(start)

        while stack:
            current = stack[-1]
            not_visited: list[tuple[
                int, int, int]] = self._get_unvisited_neighbors(
                    current[0], current[1], visited
                )
            if not_visited:
                neighbor: tuple[int, int, int] = random.choice(not_visited)
                self._grid[current[1]][current[0]] &= ~neighbor[2]
                self._grid[neighbor[1]][neighbor[0]] &= ~opposite[
                    neighbor[2]]
                stack.append((neighbor[0], neighbor[1]))
                visited.add((neighbor[0], neighbor[1]))
            else:
                stack.pop()

    def _open_entry_exit(self) -> None:
        points: list[tuple[int, int]] = [
            self._config.entry,
            self._config.exit_pos
        ]

        for c, r in points:
            if c == 0:
                self._grid[r][c] &= ~W
            elif c == self._width - 1:
                self._grid[r][c] &= ~E
            elif r == 0:
                self._grid[r][c] &= ~N
            elif r == self._height - 1:
                self._grid[r][c] &= ~S

    def _place_42_pattern(self) -> None:
        

    def get_cells(self, c: int, r: int) -> int:
        """Return de wallt bitmask for cell (c, r).

        Args:
            c: Columns index.
            r: Row index.

        Returns:
            Integer 0-15 representing walls.
        """
        return self._grid[r][c]

    def is_42_cell(self, c: int, r: int) -> bool:
        """Return True if cell (c, r) is part of the '42' pattern

        Args:
            c: Column index
            r: Row index
        Returns:
        True if the cell belongs to the 42 pattern.
        """
        return (c, r) in self._42_cells 

    def generate(self) -> None:
        """Generate the maze using recursive backtracker (DFS)"""
        if self._config.seed is not None:
            random.seed(self._config.seed)

        self._grid = [[15] * self._width for _ in range(self._height)]

        self._run_dfs()
        self._open_entry_exit()
        self._place_42_pattern()