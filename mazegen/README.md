# mazegen

A standalone Python library for generating and solving mazes using Depth-First Search (DFS) and Breadth-First Search (BFS).

## 1. Installation

You can install this module directly from the wheel file:

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

Or install it in editable mode from the source directory:

```bash
pip install -e .
```

## 2. Basic Example

Here is the quickest way to instantiate and use the generator:

```python
from mazegen import MazeGenerator

# 1. Instantiate with dimensions and seed
# width: 20, height: 10, seed: 42
gen = MazeGenerator(width=20, height=10, seed=42)

# 2. Generate the maze
# perfect: True (single path), entry: (0,0), exit_coord: (19,9)
gen.generate(perfect=True, entry=(0, 0), exit_coord=(19, 9))

# 3. Access the results
print("Maze Structure (Grid):", gen.grid)
print("Shortest Path (Solution):", gen.solution)
```

## 3. Passing Custom Parameters

### `MazeGenerator(width, height, seed)`
- **width** (*int*): Number of cells in the X direction.
- **height** (*int*): Number of cells in the Y direction.
- **seed** (*int*): The seed for the pseudo-random number generator to ensure reproducibility.

### `generate(perfect, entry, exit_coord)`
- **perfect** (*bool*): If `True`, the algorithm generates a "Perfect Maze" (exactly one path between any two cells). If `False`, it adds loops (approx. 5% of walls removed).
- **entry** (*tuple*): `(x, y)` coordinates for the starting point.
- **exit_coord** (*tuple*): `(x, y)` coordinates for the end point.

## 4. Accessing the Generated Structure

### The Grid (`gen.grid`)
The maze is stored as a 2D list of integers (`List[List[int]]`). Each integer is a bitmask representing the walls of that cell:
- **Bit 0 (Value 1):** North Wall
- **Bit 1 (Value 2):** East Wall
- **Bit 2 (Value 4):** South Wall
- **Bit 3 (Value 8):** West Wall

*Example: A cell value of `9` (binary `1001`) means the North and West walls are closed, while East and South are open.*

### The Solution (`gen.solution`)
The solution is stored as a string of cardinal directions:
- `N`: North
- `E`: East
- `S`: South
- `W`: West

### Hexadecimal Representation (`gen.to_hex_grid()`)
Returns a list of strings where each string represents a row of the maze in hexadecimal format (one character per cell).