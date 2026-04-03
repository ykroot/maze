"""
a_maze_ing.py - Main entry point.

Usage:
    python3 a_maze_ing.py config.txt

What this file does (in order):
    1. Check that exactly one argument was given (the config file path).
    2. Call config_parser.parse_config() to read and validate the config.
    3. Call MazeGenerator to build the maze.
    4. Call output_writer.write_output() to save the maze to a file.
    5. Call the visualizer to draw the maze and show the interactive menu.
"""

import sys
import random

from config_parser import parse_config, MazeConfig
from output_writer import write_output
from visualizer import MazeVisualizer, run_interactive_loop
from mazegen import MazeGenerator


def build_maze(config: MazeConfig) -> MazeGenerator:
    """
    Create a MazeGenerator from the config settings and run it.

    If the config has no SEED, a new random seed is chosen each time.
    This is what makes 're-generate' produce a different maze.

    Args:
        config : validated MazeConfig from parse_config()

    Returns:
        A MazeGenerator object whose .grid, .solution, etc. are all filled.
    """
    seed = (
        config.seed if config.seed is not None else random.randint(0, 2**31)
    )

    gen = MazeGenerator(w=config.width, h=config.height, seed=seed)
    gen.generate(
        perfect=config.perfect,
        entry=config.entry,
        exit_coord=config.exit_coord,
    )

    # Warn the user if the maze was too small for the '42' pattern
    if not gen.has_pattern:
        print(
            "Warning: maze is too small to embed the '42' pattern "
            "(minimum size: 15 wide and 9 tall).",
            file=sys.stderr,
        )

    return gen


def make_visualizer(gen: MazeGenerator, config: MazeConfig) -> MazeVisualizer:
    """
    Save the maze to the output file, then create a MazeVisualizer.

    Args:
        gen    : finished MazeGenerator
        config : config (we need config.output_file)

    Returns:
        A MazeVisualizer ready to call .render() on.
    """
    write_output(
        filepath=config.output_file,
        hex_rows=gen.to_hex_grid(),
        entry=gen.entry,
        exit_coord=gen.exit,
        solution=gen.solution,
    )

    if not gen.solution:
        print(
            "Warning: no solution path found. " "The maze may be invalid.",
            file=sys.stderr,
        )

    return MazeVisualizer(
        grid=gen.grid,
        width=gen.width,
        height=gen.height,
        entry=gen.entry,
        exit_coord=gen.exit,
        solution=gen.solution,
        pattern_cells=gen.pattern_cells,
    )


def main() -> None:
    """
    Entry point: parse arguments, generate maze, display it.
    """
    # ---- 1. Argument check ----
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>", file=sys.stderr)
        sys.exit(1)

    # ---- 2. Parse config ----
    try:
        config = parse_config(sys.argv[1])
    except FileNotFoundError as err:
        print(f"Error: {err}", file=sys.stderr)
        sys.exit(1)
    except ValueError as err:
        print(f"Config error: {err}", file=sys.stderr)
        sys.exit(1)

    # ---- 3 & 4. Generate + save ----
    try:
        gen = build_maze(config)
        viz = make_visualizer(gen, config)
    except (ValueError, OSError) as err:
        print(f"Error: {err}", file=sys.stderr)
        sys.exit(1)

    # ---- 5. Interactive display ----
    # 'regenerate' is the callback the visualizer
    # calls when the user presses 1.
    # It creates a brand-new maze (with a new random seed)
    # and returns a new viz.
    def regenerate() -> MazeVisualizer:
        """Generate a new random maze and return a fresh MazeVisualizer."""
        try:
            new_config = MazeConfig(
                width=config.width,
                height=config.height,
                entry=config.entry,
                exit_coord=config.exit_coord,
                output_file=config.output_file,
                perfect=config.perfect,
                seed=None,  # None = pick a new random seed
                algorithm=config.algorithm,
            )
            new_gen = build_maze(new_config)
            new_viz = make_visualizer(new_gen, new_config)
            new_viz.color_idx = (
                viz.color_idx
            )  # keep the colour the user chose
            new_viz.show_path = viz.show_path  # keep path visibility
            return new_viz
        except Exception as err:
            print(f"\nError during regeneration: {err}", file=sys.stderr)
            return viz  # on error, keep showing the current maze

    run_interactive_loop(viz, regenerate)


if __name__ == "__main__":
    main()
