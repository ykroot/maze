from typing import List, Tuple

class MazeGenerator:
    def __init__(self, width: int, height: int, seed: int, perfect: bool):
        self.width = width
        self.height = height
        self.seed = seed
        self.perfect = perfect
        # This will hold the grid (Student B will fill this)
        self.grid: List[List[int]] = [] 
        # This will hold the path (Student B will fill this)
        self.solution: str = "" 

    def generate(self) -> None:
        """
        Student B: This is where the 'Drunken Explorer' logic goes.
        It will fill self.grid with numbers.
        """
        pass

    def solve(self, start: Tuple[int, int], end: Tuple[int, int]) -> str:
        """
        Student B: This finds the shortest path.
        Returns a string like 'NNEESW'.
        """
        return ""

    def get_hex_representation(self) -> List[str]:
        """
        Student A: This turns the numbers in self.grid into 
        Hexadecimal strings (0-F) for the output file.
        """
        return []
