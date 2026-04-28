class FakeMaze:
    def __init__(self) -> None:
        self.width = 5
        self.height = 4

        self.entry = (0, 0)
        self.exit = (4, 3)

        # Paredes inventadas: diccionario de paredes por celda
        self.walls: dict[tuple[int, int], dict[str, bool]]
        self.walls = {
            (0, 0): {"N": True,  "E": False, "S": True,  "W": True},
            (1, 0): {"N": True,  "E": False, "S": False, "W": False},
            (2, 0): {"N": True,  "E": True,  "S": False, "W": False},
            (3, 0): {"N": True,  "E": False, "S": True,  "W": True},
            (4, 0): {"N": True,  "E": True,  "S": True,  "W": False},

            (0, 1): {"N": True,  "E": True,  "S": False, "W": True},
            (1, 1): {"N": False, "E": False, "S": False, "W": True},
            (2, 1): {"N": False, "E": True,  "S": True,  "W": False},
            (3, 1): {"N": True,  "E": False, "S": False, "W": True},
            (4, 1): {"N": True,  "E": True,  "S": False, "W": False},

            (0, 2): {"N": False, "E": True,  "S": True,  "W": True},
            (1, 2): {"N": False, "E": False, "S": True,  "W": True},
            (2, 2): {"N": True,  "E": False, "S": False, "W": False},
            (3, 2): {"N": False, "E": True,  "S": False, "W": False},
            (4, 2): {"N": False, "E": True,  "S": True,  "W": True},

            (0, 3): {"N": True,  "E": False, "S": True,  "W": True},
            (1, 3): {"N": True,  "E": False, "S": True,  "W": False},
            (2, 3): {"N": False, "E": False, "S": True,  "W": False},
            (3, 3): {"N": False, "E": False, "S": True,  "W": False},
            (4, 3): {"N": False, "E": True,  "S": True,  "W": False},
        }

        # Camino inventado
        self.path: list[tuple[int, int]] = [
            (0, 0), (1, 0), (2, 0), (1, 1),
            (1, 2), (2, 1), (2, 2), (2, 3),
            (3, 3),
        ]

    def has_wall(self, x: int, y: int, direction: str) -> bool:
        return self.walls[(x, y)][direction]
