*This project has been created as part of the 42 curriculum by macerver, rpedreno.*

# A-Maze-ing

Create your own maze generator and display its result.

---

# Description

A-Maze-ing is a Python project developed for the 42 curriculum.

The objective of the project is to generate valid mazes from a configuration file, export them into a hexadecimal wall representation format, and provide a visual ASCII rendering directly in the terminal.

The project supports:

* Random maze generation
* Reproducible generation using seeds
* Perfect mazes
* ASCII visual rendering
* Path solving from entry to exit
* Reusable maze generation module
* Interactive terminal menu

The maze generator uses a recursive backtracking algorithm based on Depth-First Search (DFS).

---

# Features

* Generate random mazes
* Generate reproducible mazes using seeds
* Perfect maze support
* Automatic shortest path solving
* ASCII renderer with colors
* Interactive terminal controls
* Export maze to hexadecimal format
* Reusable Python package (`mazegen`)
* 42 pattern rendering inside the maze

---

# Project Structure

```text
.
├── a_maze_ing.py
├── config.txt
├── Makefile
├── requirements.txt
├── pyproject.toml
├── README.md
├── display/
│   └── renderer.py
└── mazegen/
    ├── __init__.py
    ├── config_parser.py
    └── generator.py
```

---

# Installation

## Clone the repository

```bash
git clone <repository_url>
cd a-maze-ing
```

## Install dependencies

```bash
make install
```

or manually:

```bash
pip install -r requirements.txt
```

---

# Usage

Run the project using:

```bash
python3 a_maze_ing.py config.txt
```

You can also use:

```bash
make run
```

---

# Interactive Controls

| Key | Action                  |
| --- | ----------------------- |
| 1   | Generate new maze       |
| 2   | Show/Hide solution path |
| 3   | Change maze colors      |
| 4   | Exit                    |

---

# Configuration File Format

The project uses a configuration file containing one `KEY=VALUE` pair per line.

Example:

```txt
WIDTH=20
HEIGHT=15
ENTRY=2,4
EXIT=4,12
OUTPUT_FILE=maze.txt
PERFECT=False
SEED=42
```

## Available Keys

| Key         | Description                     |
| ----------- | ------------------------------- |
| WIDTH       | Maze width                      |
| HEIGHT      | Maze height                     |
| ENTRY       | Entry coordinates               |
| EXIT        | Exit coordinates                |
| OUTPUT_FILE | Output filename                 |
| PERFECT     | Enables perfect maze generation |
| SEED        | Optional random seed            |

---

# Maze Output Format

The generated maze is stored using hexadecimal wall encoding.

Each hexadecimal digit represents the walls of a cell:

| Bit | Direction |
| --- | --------- |
| 0   | North     |
| 1   | East      |
| 2   | South     |
| 3   | West      |

Example:

```txt
b93b913d139551395553
86a86ac3eac3bac6913a
```

After the maze grid:

1. Entry coordinates
2. Exit coordinates
3. Shortest valid path using `N E S W`

---

# Maze Generation Algorithm

This project uses the **Recursive Backtracker** algorithm based on **Depth-First Search (DFS)**.

## Why this algorithm?

We chose DFS Recursive Backtracking because:

* It is simple and efficient
* It generates perfect mazes naturally
* It guarantees connectivity
* It creates visually interesting corridors
* It is widely used in procedural generation

The algorithm works by:

1. Starting from the entry point
2. Visiting random unvisited neighbors
3. Removing walls between cells
4. Backtracking when no neighbors remain

---

# Reusable Module

The maze generator is reusable through the `mazegen` package.

## Example

```python
from mazegen.generator import MazeGenerator

maze = MazeGenerator(
    width=20,
    height=15,
    entry=(0, 0),
    exit_pos=(19, 14),
    output_file="maze.txt",
    perfect=True,
    seed=42
)

maze.generate()
path = maze.solve()
```

## Accessible Methods

| Method       | Description                                |
| ------------ | ------------------------------------------ |
| generate()   | Generates the maze                         |
| solve()      | Solves the maze                            |
| get_cell()   | Returns cell wall bitmask                  |
| is_42_cell() | Checks if a cell belongs to the 42 pattern |

---

# Packaging

The reusable package can be built with:

```bash
make build
```

This generates:

* `.whl`
* `.tar.gz`

inside the `dist/` directory.

---

# Makefile Commands

| Command          | Description            |
| ---------------- | ---------------------- |
| make install     | Install dependencies   |
| make run         | Run project            |
| make debug       | Run with pdb           |
| make clean       | Remove cache files     |
| make lint        | Run flake8 + mypy      |
| make lint-strict | Strict static analysis |
| make build       | Build Python package   |

---

# Error Handling

The project handles:

* Invalid configuration files
* Missing files
* Invalid coordinates
* Invalid syntax
* Impossible maze dimensions
* Rendering errors

The program exits gracefully with descriptive error messages.

---

# Team Organization

## Team Members

| Login    | Role                                      |
| -------- | ----------------------------------------- |
| macerver | Maze generation, algorithm implementation |
| rpedreno | Rendering, UI, testing                    |

---

# Planning

## Initial Plan

* Build configuration parser
* Implement DFS generator
* Create ASCII renderer
* Add interactive menu
* Add packaging support

## Final Evolution

During development we improved:

* Error handling
* Maze validation
* ASCII rendering aesthetics
* Path visualization
* Code modularity

---

# What Worked Well

* Modular architecture
* Reusable maze package
* Interactive terminal rendering
* DFS generation quality

# What Could Be Improved

* Add graphical rendering with MLX or pygame
* Add multiple algorithms
* Improve generation performance
* Add animation support

---

# Tools Used

* Python 3.10+
* flake8
* mypy
* pytest
* setuptools
* build

---

# AI Usage

AI tools were used to:

* Review code structure
* Improve documentation
* Refactor some functions
* Detect edge cases
* Improve terminal UI ideas

All generated content was manually reviewed, tested, and understood before integration.

---

# Resources

* https://docs.python.org/3/
* https://mypy.readthedocs.io/
* https://flake8.pycqa.org/
* https://realpython.com/python-maze-solver/
* https://en.wikipedia.org/wiki/Maze_generation_algorithm
* https://en.wikipedia.org/wiki/Depth-first_search

---
