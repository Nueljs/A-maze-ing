from dataclasses import dataclass
import sys


@dataclass
class MazeConfig:
    """
    Configuration data for maze generation.

    Attributes:
        width: Number of columns in the maze.
        height: Number of rows in the maze.
        entry: (x, y) coordinates of the maze entry point.
        exit_pos: (x, y) coordinates of the maze exit point.
        output_file: Path to the file where the maze will be saved.
        perfect: If True, generates a perfect maze (no loops, one solution).
        seed: Optional seed for the random number generator.
    """
    width: int
    height: int
    entry: tuple[int, int]
    exit_pos: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int | None = None


def parse_config(path: str) -> MazeConfig:
    """
    Parse a maze configuration file and return a MazeConfig instance.

    The config file must use KEY=VALUE format, one entry per line.
    Lines starting with '#' are treated as comments and ignored.
    Empty lines are also ignored.

    Mandatory keys: WIDTH, HEIGHT, ENTRY, EXIT, OUTPUT_FILE, PERFECT.
    Optional keys: SEED.

    Args:
        path: Path to the configuration file.

    Returns:
        A MazeConfig instance populated with the values from the file.

    Raises:
        SystemExit: If the file is not found, permission is denied,
                    a mandatory key is missing, or a value has an invalid
                    format.
    """
    try:
        with open(path, 'r') as f:
            raw: dict = {}
            for line in f:
                if line.strip() == '':
                    continue
                if line[0] == '#':
                    continue
                else:
                    data: list = line.split('=', 1)
                    if len(data) != 2:
                        print("Error: invalid line in config:"
                              f" '{line.strip()}'")
                        sys.exit(1)
                    raw[data[0]] = data[1].strip()
            config: MazeConfig = MazeConfig(
                width=int(raw['WIDTH']),
                height=int(raw['HEIGHT']),
                entry=(
                    int(raw['ENTRY'].split(',')[0]),
                    int(raw['ENTRY'].split(',')[1])),
                exit_pos=(
                    int(raw['EXIT'].split(',')[0]),
                    int(raw['EXIT'].split(',')[1])),
                output_file=raw['OUTPUT_FILE'],
                perfect=raw['PERFECT'] == 'True',
                seed=int(raw["SEED"]) if "SEED" in raw else None
            )
    except FileNotFoundError:
        print(f"Error: config file '{path}' not found")
        sys.exit(1)
    except PermissionError:
        print(f"Error: You don't have permission on file '{path}'")
        sys.exit(1)
    except KeyError as e:
        print(f"Error: missing mandatory key {e} in config file")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    return config
