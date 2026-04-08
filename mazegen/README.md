# mazegen

A standalone Python library for generating and solving mazes using
Depth-First Search (DFS) for generation and Breadth-First Search (BFS)
for solving.

The package includes:
- `MazeGenerator` — generates and solves the maze
- `parse_config` — reads and validates a configuration file
- `write_output` — writes the maze to a file in the required format
- `MazeVisualizer` — renders the maze in the terminal
- `run_interactive_loop` — handles the interactive terminal menu

---

## 1. Installation

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

Or in editable mode from source:

```bash
pip install -e .
```

---

## 2. MazeGenerator

This is the core of the package. It generates the maze and solves it.

### Instantiation

```python
from mazegen import MazeGenerator

gen = MazeGenerator(w=20, h=10, seed=42)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `w` | `int` | Number of cells horizontally, must be greater than 0 |
| `h` | `int` | Number of cells vertically, must be greater than 0 |
| `seed` | `int` | Seed for the random number generator, same seed always produces the same maze |

### Generating the maze

```python
gen.generate(
    perfect=True,
    entry=(0, 0),
    exit_coord=(19, 9)
)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `perfect` | `bool` | `True` = one path only between any two cells, `False` = loops added (approx. 5% of walls removed) |
| `entry` | `tuple` | `(col, row)` of the entrance, must be inside the maze bounds |
| `exit_coord` | `tuple` | `(col, row)` of the exit, must be inside the maze bounds and different from entry |

### Accessing the results

#### `gen.grid`
The maze is stored as a 2D list of integers. Each integer is a bitmask
encoding which walls are closed for that cell:

| Bit | Value | Direction | Meaning when set |
|-----|-------|-----------|-----------------|
| 0 | 1 | North | North wall is closed |
| 1 | 2 | East | East wall is closed |
| 2 | 4 | South | South wall is closed |
| 3 | 8 | West | West wall is closed |

A wall being closed means it exists (blocked). Open means passage is free.

```python
cell = gen.grid[row][col]   # access a specific cell

# check if north wall is closed
if cell & 1:
    print("north wall exists")

# check if east wall is closed
if cell & 2:
    print("east wall exists")
```

Example: a cell with value `9` (binary `1001`) has North and West walls
closed, East and South walls open.

All border cells keep their outer walls intact. The grid is initialized
with all walls closed (value `15`, binary `1111`) and walls are
selectively removed during generation.

#### `gen.solution`
The shortest path from entry to exit as a string of cardinal directions:

```
"NNEESSWW..."
```

- `N` = move North (row - 1)
- `E` = move East  (col + 1)
- `S` = move South (row + 1)
- `W` = move West  (col - 1)

If no path exists, `gen.solution` is an empty string `""`.

#### `gen.has_pattern`
A boolean that is `True` if the "42" pattern was successfully embedded
in the maze. The pattern requires the maze to be at least 15 wide and
9 tall. If the maze is too small, this is `False`.

#### `gen.pattern_cells`
A set of `(row, col)` tuples representing the cells that form the
"42" pattern. These cells are fully closed (all 4 walls intact) and
are intentionally disconnected from the rest of the maze.

#### `gen.to_hex_grid()`
Returns the maze as a list of strings, one per row, where each
character is a hexadecimal digit representing the wall bitmask of
that cell:

```python
hex_rows = gen.to_hex_grid()
# example: ["FFF", "F0F", "FFF"]
```

This is the format expected by `write_output`.

### Complete example

```python
from mazegen import MazeGenerator

gen = MazeGenerator(w=20, h=10, seed=42)
gen.generate(
    perfect=True,
    entry=(0, 0),
    exit_coord=(19, 9)
)

print("solution:", gen.solution)
print("has 42 pattern:", gen.has_pattern)

for row in gen.grid:
    print(row)
```

---

## 3. parse_config

Reads and validates a configuration file and returns a `MazeConfig`
object with all settings ready to use.

```python
from mazegen.config_parser import parse_config, MazeConfig

config = parse_config("config.txt")

print(config.width)       # int
print(config.height)      # int
print(config.entry)       # (col, row)
print(config.exit_coord)  # (col, row)
print(config.output_file) # str
print(config.perfect)     # bool
print(config.seed)        # int or None
```

### Config file format

```
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=true
# SEED=42
```

### Errors raised

Your main file is expected to catch these:

| Exception | When |
|-----------|------|
| `FileNotFoundError` | Config file does not exist |
| `ValueError` | Missing key, wrong type, bad value, entry equals exit, coordinates out of bounds |

```python
try:
    config = parse_config("config.txt")
except FileNotFoundError as err:
    print(f"Error: {err}")
except ValueError as err:
    print(f"Config error: {err}")
```

---

## 4. write_output

Writes the finished maze to a file in the required format.

```python
from mazegen.output_writer import write_output

write_output(
    filepath=config.output_file,
    hex_rows=gen.to_hex_grid(),
    entry=gen.entry,
    exit_coord=gen.exit,
    solution=gen.solution,
)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `filepath` | `str` | Path of the file to create or overwrite |
| `hex_rows` | `List[str]` | Output of `gen.to_hex_grid()` |
| `entry` | `tuple` | `(col, row)` of the entrance |
| `exit_coord` | `tuple` | `(col, row)` of the exit |
| `solution` | `str` | The solution string from `gen.solution` |

### Output file format

```
<hex row 0>
<hex row 1>
...
<hex row HEIGHT-1>

entry_col,entry_row
exit_col,exit_row
NNEESS...
```

### Errors raised

| Exception | When |
|-----------|------|
| `OSError` | File cannot be written (permissions, bad path) |

```python
try:
    write_output(...)
except OSError as err:
    print(f"Error writing output: {err}")
```

---

## 5. MazeVisualizer and run_interactive_loop

Renders the maze in the terminal and handles the interactive menu.

```python
from mazegen.visualizer import MazeVisualizer, run_interactive_loop

viz = MazeVisualizer(
    grid=gen.grid,
    width=gen.width,
    height=gen.height,
    entry=gen.entry,
    exit_coord=gen.exit,
    solution=gen.solution,
    pattern_cells=gen.pattern_cells,
)

def regenerate() -> MazeVisualizer:
    # build and return a new MazeVisualizer here
    ...

run_interactive_loop(viz, regenerate)
```

### MazeVisualizer parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `grid` | `List[List[int]]` | The maze grid from `gen.grid` |
| `width` | `int` | Number of columns |
| `height` | `int` | Number of rows |
| `entry` | `tuple` | `(col, row)` of the entrance |
| `exit_coord` | `tuple` | `(col, row)` of the exit |
| `solution` | `str` | Solution string from `gen.solution` |
| `pattern_cells` | `Set[Tuple[int,int]]` | From `gen.pattern_cells` |

### run_interactive_loop

Takes a `MazeVisualizer` and a `regenerate` callback. The callback
must take no arguments and return a new `MazeVisualizer`. It is called
when the user requests a new maze.

The interactive menu provides:
- Re-generate a new maze
- Show / Hide the solution path
- Change wall colour scheme
- Quit