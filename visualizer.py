"""
visualizer.py - Draw the maze in the terminal and handle the interactive menu.

HOW THE DRAWING WORKS
----------------------
Each maze cell is rendered as a block that is 3 characters wide and 1 line tall
(plus one shared border line above it):

    Top border line:   CORNER + (wall or space) + CORNER
    Content line:      (left wall or space) + CELL_CONTENT(2 chars)

After all rows, one final bottom border line is drawn.

Characters used:
    █   = wall (solid block)
    ██  = two-char horizontal wall or pattern cell
    ··  = path marker (solution)
    EN  = entry cell
    EX  = exit cell
    (2 spaces) = empty floor

ANSI COLOUR CODES
-----------------
These are special escape sequences that colour text in the terminal.
Format:  \033[<code>m   (everything after this is coloured)
         \033[0m        (reset to default colour)
Example: \033[92m Hello \033[0m   →  prints "Hello" in bright green
"""

import sys
from typing import List, Tuple, Set, Callable

#  ANSI codes
RESET = "\033[0m"
BOLD = "\033[1m"
WHITE = "\033[97m"
CYAN = "\033[96m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[34m"

# ---- 4 colour schemes to cycle through ----
# Each scheme is a dict with keys: wall, path, entry, exit, pattern
SCHEMES = [
    {
        "name": "White",
        "wall": WHITE,
        "path": CYAN,
        "entry": GREEN,
        "exit": RED,
        "pattern": YELLOW,
    },
    {
        "name": "Yellow",
        "wall": YELLOW,
        "path": CYAN,
        "entry": GREEN,
        "exit": RED,
        "pattern": WHITE,
    },
    {
        "name": "Blue",
        "wall": BLUE,
        "path": CYAN,
        "entry": GREEN,
        "exit": RED,
        "pattern": YELLOW,
    },
    {
        "name": "Green",
        "wall": GREEN,
        "path": YELLOW,
        "entry": CYAN,
        "exit": RED,
        "pattern": WHITE,
    },
]

#  Drawing characters
WALL_H = "██"  # horizontal wall  (2 chars wide)
WALL_V = "█"  # vertical wall    (1 char wide)
CORNER = "█"  # corner           (1 char)
FLOOR = "  "  # empty cell       (2 chars)
PATH = "··"  # solution path    (2 chars)
PATTERN = "██"  # '42' solid cell  (2 chars)

class MazeVisualizer:
    """
    Draws the maze in the terminal using ANSI colour codes.

    Attributes:
        grid          -- 2D list of wall bitmasks (from MazeGenerator.grid)
        width         -- number of columns
        height        -- number of rows
        entry         -- (col, row) of entrance
        exit_coord    -- (col, row) of exit
        solution      -- list of N/E/S/W direction strings (shortest path)
        pattern_cells -- set of (row, col) forming the '42' shape
        color_idx     -- index of the active colour scheme (0-3)
        show_path     -- True = draw the solution path on screen
    """

    def __init__(
        self,
        grid: List[List[int]],
        width: int,
        height: int,
        entry: Tuple[int, int],
        exit_coord: Tuple[int, int],
        solution: str,
        pattern_cells: Set[Tuple[int, int]],
    ) -> None:
        self.grid = grid
        self.width = width
        self.height = height
        self.entry = entry
        self.exit_coord = exit_coord
        self.solution = solution
        self.pattern_cells = pattern_cells
        self.color_idx = 0
        self.show_path = False

    # (called from the interactive loop)

    def render(self) -> None:
        """Clear the screen and draw the full maze."""
        print("\033[2J\033[H", end="")  # clear terminal, cursor to top-left
        scheme = SCHEMES[self.color_idx]
        path_set = self._compute_path_cells() if self.show_path else set()

        for row in range(self.height):
            self._draw_top_border(row, scheme)
            self._draw_cell_row(row, scheme, path_set)
        self._draw_bottom_border(scheme)

    def toggle_path(self) -> None:
        """Switch the solution path on or off."""
        self.show_path = not self.show_path

    def next_color(self) -> None:
        """Move to the next colour scheme """
        """(cycles back to 0 after the last)."""
        self.color_idx = (self.color_idx + 1) % len(SCHEMES)

    def print_menu(self) -> None:
        """Print the interactive menu below the maze."""
        path_status = "ON" if self.show_path else "OFF"
        scheme_name = SCHEMES[self.color_idx]["name"]
        print(f"\n{BOLD}==== A-Maze-ing ===={RESET}")
        print("  1. Re-generate a new maze")
        print(f"  2. Show / Hide solution path  (currently: {path_status})")
        print(f"  3. Change wall colour         (currently: {scheme_name})")
        print("  4. Quit")
        print("Choice (1-4): ", end="", flush=True)

    # compute which cells are on the solution path

    def _compute_path_cells(self) -> Set[Tuple[int, int]]:
        """
        Walk self.solution step by step from the entry cell.
        Collect every (row, col) along the way.
        Returns a set so we can check membership while drawing.
        """
        move = {"N": (-1, 0), "E": (0, 1), "S": (1, 0), "W": (0, -1)}
        ec, er = self.entry
        r, c = er, ec
        cells: Set[Tuple[int, int]] = {(r, c)}
        for direction in self.solution:
            dr, dc = move[direction]
            r += dr
            c += dc
            cells.add((r, c))
        return cells

    # ----------------------------------------------------------------
    # Private: row-drawing helpers
    # ----------------------------------------------------------------

    def _has_wall(self, row: int, col: int, bit: int) -> bool:
        """Return True if the wall at `bit`
        position is closed for cell (row,col)."""
        return bool(self.grid[row][col] & (1 << bit))

    def _draw_top_border(self, row: int, scheme: dict) -> None:
        """
        Draw the top border line of a row.
        For each cell: print a CORNER, then either WALL_H or two spaces
        depending on whether the North wall (bit 0) is closed.
        End with a final CORNER.
        """
        w = scheme["wall"]
        line = ""
        for col in range(self.width):
            line += w + CORNER + RESET
            if self._has_wall(row, col, 0):  # bit 0 = North
                line += w + WALL_H + RESET
            else:
                line += "  "
        line += w + CORNER + RESET
        print(line)

    def _draw_cell_row(
        self,
        row: int,
        scheme: dict,
        path_set: Set[Tuple[int, int]],
    ) -> None:
        """
        Draw the content line of a row.
        For each cell: print the West wall (bit 3)
        if closed, then the cell content.
        After the last cell, close the East wall (bit 1) of that cell.
        """
        w = scheme["wall"]
        ec, er = self.entry
        xc, xr = self.exit_coord
        line = ""

        for col in range(self.width):
            # West wall (bit 3)
            if self._has_wall(row, col, 3):
                line += w + WALL_V + RESET
            else:
                line += " "

            # Cell content (always 2 characters)
            if row == er and col == ec:
                # This cell is the entry
                line += scheme["entry"] + BOLD + "EN" + RESET
            elif row == xr and col == xc:
                # This cell is the exit
                line += scheme["exit"] + BOLD + "EX" + RESET
            elif (row, col) in self.pattern_cells:
                # This cell is part of the '42' pattern (solid block)
                line += scheme["pattern"] + PATTERN + RESET
            elif (row, col) in path_set:
                # This cell is on the solution path
                line += scheme["path"] + PATH + RESET
            else:
                # Normal empty floor
                line += FLOOR

        # Close the right edge of the row (East wall of the last cell, bit 1)
        if self._has_wall(row, self.width - 1, 1):
            line += w + WALL_V + RESET
        else:
            line += " "

        print(line)

    def _draw_bottom_border(self, scheme: dict) -> None:
        """
        Draw the very last border line (South walls of the bottom row, bit 2).
        Same structure as _draw_top_border but checks South wall.
        """
        w = scheme["wall"]
        last = self.height - 1
        line = ""
        for col in range(self.width):
            line += w + CORNER + RESET
            if self._has_wall(last, col, 2):  # bit 2 = South
                line += w + WALL_H + RESET
            else:
                line += "  "
        line += w + CORNER + RESET
        print(line)


# ----------------------------------------------------------------
# Interactive loop (called from a_maze_ing.py)
# ----------------------------------------------------------------


def run_interactive_loop(
    viz: MazeVisualizer,
    regenerate: Callable[[], MazeVisualizer],
) -> None:
    """
    Show the maze and the menu. Wait for user input in a loop.
    React to choices 1-4 forever until the user quits.

    Args:
        viz        : the first MazeVisualizer to display
        regenerate : a function with no arguments that returns a brand-new
                     MazeVisualizer (called when the user presses 1)
    """
    viz.render()
    viz.print_menu()

    while True:
        try:
            choice = input().strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{GREEN}Goodbye!{RESET}")
            sys.exit(0)

        if choice == "1":
            viz = regenerate()
            viz.render()
            viz.print_menu()

        elif choice == "2":
            viz.toggle_path()
            viz.render()
            viz.print_menu()

        elif choice == "3":
            viz.next_color()
            viz.render()
            viz.print_menu()

        elif choice == "4":
            print(f"\n{GREEN}Goodbye!{RESET}")
            sys.exit(0)

        else:
            print("Please enter 1, 2, 3 or 4: ", end="", flush=True)
