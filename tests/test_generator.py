import pytest
from mazegen import MazeGenerator

def test_maze_dimensions():
    """Verify the grid is created with the correct size."""
    width, height = 20, 15
    gen = MazeGenerator(width, height, seed=42)
    assert len(gen.grid) == height
    assert len(gen.grid[0]) == width

def test_perfect_maze_connectivity():
    """Verify that a perfect maze has a solution."""
    gen = MazeGenerator(15, 15, seed=123)
    # entry (0,0), exit (14,14)
    gen.generate(perfect=True, entry=(0, 0), exit_coord=(14, 14))
    assert gen.solution != ""
    assert all(c in "NESW" for c in gen.solution)

def test_invalid_path():
    """Verify solver handles impossible paths (if any)."""
    gen = MazeGenerator(10, 10, seed=1)
    # Manually block the exit by surrounding it with walls (value 15)
    gen.grid[9][9] = 15
    path = gen.solve((0, 0), (9, 9))
    assert path == ""

def test_42_pattern_presence():
    """Verify the 42 pattern is generated for large enough mazes."""
    gen = MazeGenerator(20, 20, seed=7)
    gen.generate(perfect=True, entry=(0, 0), exit_coord=(19, 19))
    assert gen.has_pattern is True
    assert len(gen.pattern_cells) > 0
