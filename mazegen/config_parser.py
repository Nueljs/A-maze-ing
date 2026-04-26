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
