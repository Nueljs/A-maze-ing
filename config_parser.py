from dataclasses import dataclass
import sys


@dataclass
class MazeConfig:
    width: int
    height: int
    entry: tuple[int, int]
    exit_pos: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int | None = None


def parse_config(path: str) -> MazeConfig:
    try:
        with open(path, 'r') as f:
            config: MazeConfig
            for line in f:
                if line[0] == '#':
                    continue
                if line == '\0':
                    continue
                else:
                    data: list = line.split('=')
                    if data[0] == "width" or data[0] == "height" or data[0] == "seed":
                        config.data[0] = int(data[1])
                    
    except FileNotFoundError:
        print(f"Error: config file '{path}' not found")
        sys.exit(1)
    except PermissionError:
        print(f"Error: You don't have permission on file '{path}'")
        sys.exit(1)
    return config