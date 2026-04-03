import random
from collections import deque
from typing import List, Tuple, Set, Dict


class MazeGenerator:
    """A class to generate and solve mazes."""
    def __init__(self, w: int, h: int, seed: int):
        self.width: int = w
        self.height: int = h
        self.seed: int = seed
        random.seed(self.seed)

        self.grid: List[List[int]] = [[15 for _ in range(w)] for _ in range(h)]
        self.entry: Tuple[int, int] = (0, 0)
        self.exit: Tuple[int, int] = (0, 0)
        self.solution: str = ""
        self.has_pattern: bool = False
        self.pattern_cells: Set[Tuple[int, int]] = set()

        self.dirs: Dict[str, Tuple[int, int, int, int]] = {
            'N': (0, -1, 1, 4),
            'E': (1, 0, 2, 8),
            'S': (0, 1, 4, 1),
            'W': (-1, 0, 8, 2)
        }

    def generate(self, perfect: bool, entry: Tuple[int, int],
                 exit_coord: Tuple[int, int]) -> None:
        self.entry = entry
        self.exit = exit_coord

        self.pattern_cells = self._get_42_points()
        visited: Set[Tuple[int, int]] = set()
        for r, c in self.pattern_cells:
            visited.add((c, r))

        start_node = self.entry
        stack: List[Tuple[int, int]] = [start_node]
        visited.add(start_node)

        while stack:
            cx, cy = stack[-1]
            neighbors = []
            for _, (dx, dy, wall, opp) in self.dirs.items():
                nx, ny = cx + dx, cy + dy
                if (0 <= nx < self.width and 0 <= ny < self.height
                        and (nx, ny) not in visited):
                    neighbors.append((nx, ny, wall, opp))
            if neighbors:
                nx, ny, wall, opp = random.choice(neighbors)
                self.grid[cy][cx] -= wall
                self.grid[ny][nx] -= opp
                visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                stack.pop()

        if not perfect:
            self._add_loops()

        self.solve(self.entry, self.exit)

    def _get_42_points(self) -> Set[Tuple[int, int]]:
        """Returns (row, col) coordinates for a recognizable 42 pattern."""
        if self.width < 15 or self.height < 9:
            self.has_pattern = False
            return set()

        self.has_pattern = True
        start_row = (self.height - 5) // 2
        start_col = (self.width - 7) // 2

        for px, py in [self.entry, self.exit]:
            if ((start_col <= px < start_col + 7)
                    and (start_row <= py < start_row + 5)):
                if py < self.height // 2:
                    start_row += 2
                else:
                    start_row -= 2
                if px < self.width // 2:
                    start_col += 2
                else:
                    start_col -= 2

        pattern_cells: Set[Tuple[int, int]] = set()

        for r in range(5):
            if r < 3:
                pattern_cells.add((start_row + r, start_col))
            if r == 2:
                pattern_cells.add((start_row + r, start_col + 1))
            pattern_cells.add((start_row + r, start_col + 2))

        c2 = start_col + 4
        for r in range(5):
            if r in [0, 2, 4]:
                for c in range(3):
                    pattern_cells.add((start_row + r, c2 + c))
            elif r == 1:
                pattern_cells.add((start_row + r, c2 + 2))
            elif r == 3:
                pattern_cells.add((start_row + r, c2))

        return pattern_cells

    def _add_loops(self) -> None:
        walls: List[Tuple[int, int, str]] = []
        for y in range(self.height):
            for x in range(self.width):
                if x < self.width - 1:
                    walls.append((x, y, 'E'))
                if y < self.height - 1:
                    walls.append((x, y, 'S'))

        random.shuffle(walls)
        target = int((self.width * self.height) * 0.05)
        broken = 0
        for x, y, d in walls:
            if broken >= target:
                break
            nx, ny = x + self.dirs[d][0], y + self.dirs[d][1]

            if (y, x) in self.pattern_cells or (ny, nx) in self.pattern_cells:
                continue

            wall_bit, opp_bit = self.dirs[d][2], self.dirs[d][3]
            if self.grid[y][x] & wall_bit and self._is_safe(x, y, d):
                self.grid[y][x] -= wall_bit
                self.grid[ny][nx] -= opp_bit
                broken += 1

    def _is_safe(self, x: int, y: int, d: str) -> bool:
        if d == 'E':
            if (y > 0
                and not (self.grid[y-1][x] & 4)
                and not (self.grid[y-1][x+1] & 4)
                    and not (self.grid[y-1][x] & 2)):
                return False
            if (y < self.height-1
                and not (self.grid[y][x] & 4)
                and not (self.grid[y][x+1] & 4)
                    and not (self.grid[y+1][x] & 2)):
                return False
        else:
            if (x > 0
                and not (self.grid[y][x-1] & 2)
                and not (self.grid[y+1][x-1] & 2)
                    and not (self.grid[y][x-1] & 4)):
                return False
            if (x < self.width-1
                and not (self.grid[y][x] & 2)
                and not (self.grid[y+1][x] & 2)
                    and not (self.grid[y][x+1] & 4)):
                return False
        return True

    def solve(self, start: Tuple[int, int], end: Tuple[int, int]) -> str:
        queue = deque([(start, "")])
        visited = {start}
        while queue:
            (cx, cy), path = queue.popleft()
            if (cx, cy) == end:
                self.solution = path
                return path
            for d_char, (dx, dy, wall, _) in self.dirs.items():
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if (not (self.grid[cy][cx] & wall)
                            and (nx, ny) not in visited):
                        visited.add((nx, ny))
                        queue.append(((nx, ny), path + d_char))
        return ""

    def to_hex_grid(self) -> List[str]:
        return ["".join(f"{c:X}" for c in row) for row in self.grid]
