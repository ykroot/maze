"""
output_writer.py - Write the finished maze to a file.

Required output format (from the project PDF):
    <hex row 0>\n
    <hex row 1>\n
    ...
    <hex row N-1>\n
    \n                    ← empty line separator
    entry_col,entry_row\n
    exit_col,exit_row\n
    SSEENNWW...\n         ← shortest path as N/E/S/W letters

Each hex character (0-F) is the wall bitmask of one cell.
"""

from typing import List, Tuple


def write_output(
    filepath: str,
    hex_rows: List[str],
    entry: Tuple[int, int],
    exit_coord: Tuple[int, int],
    solution: List[str],
) -> None:
    """
    Write the maze file.

    Args:
        filepath   : path of the file to create / overwrite
        hex_rows   : list of strings, one per maze row
                     (from MazeGenerator.to_hex_grid)
        entry      : (col, row) of the entrance
        exit_coord : (col, row) of the exit
        solution   : list of 'N'/'E'/'S'/'W' direction letters (shortest path)

    Raises:
        OSError : if the file cannot be written
    """
    ec, er = entry
    xc, xr = exit_coord
    path_str = "".join(solution)

    with open(filepath, "w") as fh:
        # hex grid
        for row in hex_rows:
            fh.write(row + "\n")

        # empty separator line
        fh.write("\n")

        # entry, exit, solution
        fh.write(f"{ec},{er}\n")
        fh.write(f"{xc},{xr}\n")
        fh.write(path_str + "\n")
