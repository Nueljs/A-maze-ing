import sys
from mazegen.config_parser import MazeConfig, parse_config


def call_parser() -> MazeConfig:
    if len(sys.argv) != 2:
        print("Error: usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)
    config: MazeConfig = parse_config(sys.argv[1])
    return config


if __name__ == "__main__":
    print(call_parser())