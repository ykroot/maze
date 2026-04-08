*This project has been created as part of the 42 curriculum by <ysenhaji>, <mouaguil>.*

# A-Maze-ing

## Description

A-Maze-ing is a maze generator written in Python. It generates random mazes from a
configuration file, displays them in the terminal with an interactive menu, and writes
the result to an output file. The maze generation logic is packaged as a standalone
reusable Python module called `mazegen` that can be installed and used in future projects.

Key features:
- Random maze generation using Depth-First Search (DFS)
- Perfect mazes (single path) or imperfect mazes (with loops)
- Reproducible mazes via a seed
- A visible "42" pattern embedded in the maze
- Shortest path solver using BFS
- Interactive terminal display with colour schemes

---

## Instructions

### Requirements
- Python 3.10 or later
- A virtual environment is recommended

### Setup and run

```bash
# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
make install

# Run the program
make run
```

The program takes a configuration file as its only argument:
```bash
python3 a_maze_ing.py config.txt
```

### Other Makefile commands

```bash
make debug       # Run in debug mode with pdb
make clean       # Remove caches and build artifacts
make lint        # Run flake8 and mypy
make build-pkg   # Build the mazegen package
```

---

## Configuration file

The configuration file must follow this format:
- One `KEY=VALUE` pair per line
- Lines starting with `#` are comments and are ignored
- Blank lines are ignored

### Mandatory keys

| Key | Description | Example |
|-----|-------------|---------|
| `WIDTH` | Number of cells horizontally | `WIDTH=20` |
| `HEIGHT` | Number of cells vertically | `HEIGHT=15` |
| `ENTRY` | Entry coordinates as `col,row` | `ENTRY=0,0` |
| `EXIT` | Exit coordinates as `col,row` | `EXIT=19,14` |
| `OUTPUT_FILE` | Path to the output file | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | Perfect maze if True | `PERFECT=true` |

### Optional keys

| Key | Description | Example |
|-----|-------------|---------|
| `SEED` | Fixed seed for reproducibility | `SEED=42` |

### Example config file

```
# A-Maze-ing configuration
WIDTH=40
HEIGHT=40
ENTRY=1,3
EXIT=3,1
OUTPUT_FILE=maze.txt
PERFECT=false
# SEED=42
```

---

## Maze generation algorithm

The maze is generated using **Depth-First Search (DFS)**, also known as the recursive
backtracker algorithm.

### How it works

```
1. Start at the entry cell, mark it visited
2. Pick a random unvisited neighbor
3. Carve a passage between the current cell and the neighbor
4. Move to the neighbor and repeat
5. If no unvisited neighbors exist, backtrack
6. Repeat until all cells are visited
```

### Why DFS

DFS was chosen for several reasons:
- It is straightforward to understand and implement correctly
- It naturally produces a perfect maze (a spanning tree with no cycles)
- It generates mazes with long winding corridors which are visually interesting
- It was recommended by peers who had explored multiple algorithms
- It is fast and works well for mazes up to 40x40

For imperfect mazes (`PERFECT=false`), approximately 5% of remaining walls are
randomly removed after generation to introduce loops.

---

## Reusable module: mazegen

The maze generation logic is packaged as a standalone module that can be installed
with pip and reused in any future Python project.

### Installation

Build and install from source:
```bash
# In a virtual environment
make install
make build-pkg
pip install mazegen-1.0.0-py3-none-any.whl
```

Or install directly from the wheel file:
```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

### Basic example

```python
from mazegen import MazeGenerator

# Create a 20x10 maze with seed 42
gen = MazeGenerator(w=20, h=10, seed=42)

# Generate a perfect maze
gen.generate(
    perfect=True,
    entry=(0, 0),
    exit_coord=(19, 9)
)

# Access the results
print(gen.grid)       # 2D list of wall bitmasks
print(gen.solution)   # shortest path as N/E/S/W string
print(gen.has_pattern) # whether the 42 pattern was embedded
```

### Parameters

#### `MazeGenerator(w, h, seed)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `w` | `int` | Number of cells horizontally |
| `h` | `int` | Number of cells vertically |
| `seed` | `int` | Seed for reproducibility |

#### `generate(perfect, entry, exit_coord)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `perfect` | `bool` | True = one path only, False = loops added |
| `entry` | `tuple` | `(col, row)` of the entrance |
| `exit_coord` | `tuple` | `(col, row)` of the exit |

### Accessing the generated structure

#### `gen.grid`
A 2D list of integers. Each integer is a bitmask of the walls of that cell:

| Bit | Value | Direction |
|-----|-------|-----------|
| 0 | 1 | North |
| 1 | 2 | East |
| 2 | 4 | South |
| 3 | 8 | West |

A wall being closed sets the bit to 1, open means 0.

Example: cell value `9` (binary `1001`) means North and West walls are closed,
East and South are open.

#### `gen.solution`
A string of cardinal directions representing the shortest path from entry to exit:
```
"NNEESSWW..."
```

#### `gen.to_hex_grid()`
Returns the maze as a list of strings in hexadecimal format, one character per cell.
This is the format used in the output file.

---

## Output file format

The output file contains:
1. `HEIGHT` lines of `WIDTH` hexadecimal characters (one per cell)
2. An empty line
3. The entry coordinates as `col,row`
4. The exit coordinates as `col,row`
5. The shortest path as a string of `N`, `E`, `S`, `W` directions

Example:
```
FFFF
F00F
FFFF

0,0
3,2
EESSWWNN
```

---

## Team and project management

### Team members

| Login | Role |
|-------|------|
| `<ysenhaji>` | Maze generation algorithm, packaging |
| `<mouaguil>` | Configuration parsing, visualization |

### Project management

We used **Git** for version control and **Discord** for communication.

The project was split clearly between the two members from the start, with each person
responsible for their own modules. Integration of the two parts happened after the core
modules were individually completed. We ran into some issues connecting the parts
together and some debugging was needed at that stage, along with a few decisions about
the final structure. Overall the project went well with no major blockers.

What worked well:
- Clear separation of responsibilities from the start
- Good communication throughout

What could be improved:
- Starting integration testing earlier rather than after each part was individually finished

---

## Resources

### References

- [Python `random` module documentation](https://docs.python.org/3/library/random.html)
- [Maze generation algorithms - Jamis Buck's blog](http://weblog.jamisbuck.org/2011/2/7/maze-generation-algorithm-recap)
- [Think Like a Graph: maze generation explained](https://www.redblobgames.com/pathfinding/maze/introduction.html)
- [Python packaging guide](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
- [Depth-First Search and spanning trees](https://en.wikipedia.org/wiki/Maze_generation_algorithm#Randomized_depth-first_search)
- [BFS shortest path](https://en.wikipedia.org/wiki/Breadth-first_search)

### AI usage

AI tools were used throughout this project for:
- Understanding maze generation algorithms and graph theory concepts
- Debugging and understanding error messages
- Understanding Python packaging and virtual environments
- Drafting and structuring this README

All AI-generated content was reviewed, tested, and validated by the team before
being included in the project.