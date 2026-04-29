from mazegen.config_parser import MazeConfig
import random
import sys


# Direction constatns
N, E, S, W = 1, 2, 4, 8
opposite: dict[int, int] = {N: S, S: N, E: W, W: E}
PATTERN_42: list[tuple[int, int]] = [
    # "4"
    (0, 0), (2, 0),
    (0, 1), (2, 1),
    (0, 2), (1, 2), (2, 2),
    (2, 3),
    (2, 4),
    # "2"
    (4, 0), (5, 0),
    (5, 1),
    (4, 2), (5, 2),
    (4, 3),
    (4, 4), (5, 4)
]


class MazeGenerator:
    """Generates a maze using recursive backtraket (DFS).

    Args:
        config: Parsed maze configuration
    """
    def __init__(self, width: int = 3, height: int,
    entry: tuple[int, int],
    exit_pos: tuple[int, int],
    output_file: str,
    perfect: bool,
    seed: int | None = None) -> None:
        self._grid: list[list[int]] = []
        self._entry: tuple[int, int] = entry
        self._exit_pos: tuple[int, int] = exit_pos
        self._output_file: str = output_file
        self._perfect: bool = perfect
        self._seed: int | None = seed
        self._width: int = width
        self._height: int = height
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
        return self._entry

    @property
    def exit_pos(self) -> tuple[int, int]:
        """Exit point coordinates (c, r)."""
        return self._exit_pos

    def _is_3x3_open(self, sc: int, sr: int) -> bool:
        """Check if the 3x3 square with top-left corner (sc, sr) is fully open.

        Args:
            sc: Column index of top-left corner.
            sr: Row index of top-left corner.

        Returns:
            True if all interior walls are open.
        """
        if sc < 0 or sr < 0 or sc + 2 >= self._width or sr + 2 >= self._height:
            return False
        for r in range(sr, sr + 3):
            for c in range(sc, sc + 2):
                if self._grid[r][c] & E != 0:
                    return False
        for r in range(sr, sr + 2):
            for c in range(sc, sc + 3):
                if self._grid[r][c] & S != 0:
                    return False
        return True

    def _would_create_3x3(self, c: int, r: int, nc: int, nr: int) -> bool:
        """Check if opening the wall between (c, r) and (nc, nr)
        would create a 3x3 open area.

        Args:
            c: Column of current cell.
            r: Row of current cell.
            nc: Column of neighbor cell.
            nr: Row of neighbor cell.

        Returns:
            True if the move would create a forbidden 3x3 area.
        """
        if nc == c:  # movimiento vertical
            top_r = min(r, nr) - 1
            corners = [(c - 2, top_r), (c - 1, top_r), (c, top_r)]
        else:  # movimiento horizontal
            left_c = min(c, nc) - 1
            corners = [(left_c, r - 2), (left_c, r - 1), (left_c, r)]
        return any(self._is_3x3_open(sc, sr) for sc, sr in corners)

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
                    and ((nc, nr) not in visited)
                    and (nc, nr) not in self._42_cells
                    and not self._would_create_3x3(c, r, nc, nr)):
                neighbors.append((nc, nr, direction))
        return neighbors

    def _run_dfs(self) -> None:
        """"
        Run recursive backtracker DFS (Depth-First Search) to carve the maze
        """
        visited: set[tuple[int, int]] = set()
        stack: list[tuple[int, int]] = []

        start = self._entry
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

    def __get_accesible_neighbors(
        self, c: int, r: int, visited: set[tuple[int, int]]
    ) -> list[tuple[int, int]]:
        """Return accesible unvisited neighbors of cell (c, r)

        Arg:
            c: Column index.
            r: Row index
            visited: SEt of alredy visited cells.
        Returns:
            List if (nc, nr) coordinates reachable from (c, r).
        """
        neighbors: list[tuple[int, int]] = []
        candidates: list[tuple[int, int, int]] = [
            (c, r - 1, N), (c + 1, r, E), (c, r + 1, S), (c - 1, r, W)
        ]
        for nc, nr, direction in candidates:
            if ((0 <= nc < self.width) and (0 <= nr < self._height)
                    and (nc, nr) not in visited
                    and self._grid[r][c] & direction == 0):
                neighbors.append((nc, nr))
        return neighbors

    def solve(self) -> list[tuple[int, int]]:
        """Find the path from entry to exit using DFS.

        Returns:
            List of (c, r) coordinates from entry to exit,
            or empty list if no path found
        """
        visited: set[tuple[int, int]] = set()
        stack: list[tuple[int, int]] = []

        start = self._entry
        visited.add(start)
        stack.append(start)
        while stack:
            current = stack[-1]
            if current == self._exit_pos:
                return stack
            neighbors = self.__get_accesible_neighbors(
                current[0], current[1], visited)
            if neighbors:
                next_cell = neighbors[0]
                stack.append((next_cell))
                visited.add((next_cell))
            else:
                stack.pop()

        return []

    def _open_entry_exit(self) -> None:
        points: list[tuple[int, int]] = [
            self._entry,
            self._exit_pos
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
        if self._width < 6 or self._height < 5:
            print("Error: Maze is not bigger enougth for 42 pattern")
            return

        origin_c: int = (self._width - 6) // 2
        origin_r: int = (self._height - 5) // 2
        new_pattern: list[tuple[int, int]] = [
            (c + origin_c, r + origin_r) for c, r in PATTERN_42
        ]
        for cell in new_pattern:
            c, r = cell
            self._grid[r][c] = 15
            self._42_cells.add(cell)

    def get_cell(self, c: int, r: int) -> int:
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

    def _validate_config(self) -> bool:
        if self._entry == self._exit_pos:
            print("Error: entry and exit must be different")
            return False

        c, r = self._entry
        if not (0 <= c < self._width and 0 <= r < self._height):
            print("Error: Entry point out of bounds")
            return False
        if not (c == 0 or r == 0 or c == self._width - 1 or
                r == self._height - 1):
            print("Error: entry point must be on a border cell")
            return False

        c, r = self._exit_pos
        if not (0 <= c < self._width and 0 <= r < self._height):
            print("Error: exit point out of bounds")
            return False
        if not (c == 0 or r == 0 or c == self._width - 1 or
                r == self._height - 1):
            print("Error: exit point must be on a border cell")
            return False

        return True

    def generate(self) -> None:
        """Generate the maze using recursive backtracker (DFS)"""
        if not self._validate_config():
            sys.exit(1)

        if self._seed is not None:
            random.seed(self._seed)

        self._grid = [[15] * self._width for _ in range(self._height)]

        self._place_42_pattern()
        self._run_dfs()
        self._open_entry_exit()

