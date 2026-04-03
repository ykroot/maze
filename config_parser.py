"""
config_parser.py - Read and validate the maze configuration file.

The config file format:
    KEY=VALUE      (one per line)
    # comment      (lines starting with # are ignored)
    blank lines    (also ignored)

Mandatory keys:   WIDTH, HEIGHT, ENTRY, EXIT, OUTPUT_FILE, PERFECT
Optional keys:    SEED, ALGORITHM
"""

import os
from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class MazeConfig:
    """
    A simple container for all settings read from the config file.
    After parse_config() returns this object, every field is validated
    and ready to use.
    """

    width: int
    height: int
    entry: Tuple[int, int]  # (col, row)
    exit_coord: Tuple[int, int]  # (col, row)
    output_file: str
    perfect: bool
    seed: Optional[int] = None
    algorithm: str = "wilson"


def parse_config(filepath: str) -> MazeConfig:
    """
    Open the config file, parse every KEY=VALUE line, validate all values,
    and return a MazeConfig.

    Args:
        filepath : path to the config file (e.g. 'config.txt')

    Returns:
        A validated MazeConfig object.

    Raises:
        FileNotFoundError : if the file does not exist
        ValueError        : if a key is missing, has wrong type, or bad value
    """
    # Make sure the file exists
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"Config file not found: '{filepath}'")

    data: dict[str, str] = {}

    # Read every line
    with open(filepath, "r") as fh:
        for lineno, line in enumerate(fh, start=1):
            line = line.strip()

            # Skip empty lines and comments
            if not line or line.startswith("#"):
                continue

            # Every other line must be KEY=VALUE
            if "=" not in line:
                raise ValueError(
                    f"Line {lineno}: expected 'KEY=VALUE', got: '{line}'"
                )

            # Split on the FIRST '=' only (value might contain '=')
            key, _, value = line.partition("=")
            data[key.strip().upper()] = value.strip()

    # Check that all mandatory keys are present
    for key in ("WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"):
        if key not in data:
            raise ValueError(f"Missing mandatory config key: '{key}'")

    # Parse and validate each value
    width = positive_int(data["WIDTH"], "WIDTH")
    height = positive_int(data["HEIGHT"], "HEIGHT")
    entry = coordinate(data["ENTRY"], "ENTRY", width, height)
    exit_coord = coordinate(data["EXIT"], "EXIT", width, height)

    if entry == exit_coord:
        raise ValueError("ENTRY and EXIT must be different cells.")

    output_file = data["OUTPUT_FILE"]
    if not output_file:
        raise ValueError("OUTPUT_FILE cannot be empty.")

    perfect = boolean(data["PERFECT"], "PERFECT")

    # Optional: SEED
    seed: Optional[int] = None
    if "SEED" in data:
        seed = positive_int(data["SEED"], "SEED", allow_zero=True)

    # Optional: ALGORITHM  (only 'wilson' supported for now)
    algorithm = data.get("ALGORITHM", "wilson").lower()
    if algorithm != "wilson":
        raise ValueError(f"ALGORITHM must be 'wilson', got: '{algorithm}'")

    return MazeConfig(
        width=width,
        height=height,
        entry=entry,
        exit_coord=exit_coord,
        output_file=output_file,
        perfect=perfect,
        seed=seed,
        algorithm=algorithm,
    )


# helper functions


def positive_int(value: str, key: str, allow_zero: bool = False) -> int:
    """
    Convert `value` to an integer.
    Raises ValueError with a clear message if it fails or is <= 0.
    """
    try:
        n = int(value)
    except ValueError:
        raise ValueError(f"'{key}' must be an integer, got: '{value}'")

    if allow_zero and n < 0:
        raise ValueError(f"'{key}' must be 0 or more, got: {n}")
    if not allow_zero and n <= 0:
        raise ValueError(
            f"'{key}' must be a positive integer (> 0), got: {n}"
        )
    return n


def coordinate(
    value: str,
    key: str,
    width: int,
    height: int,
) -> Tuple[int, int]:
    """
    Parse a 'col,row' string. Validate that both numbers are integers
    and that the coordinate is inside the maze bounds.
    """
    parts = value.split(",")
    if len(parts) != 2:
        raise ValueError(
            f"'{key}' must be in 'col,row' format, got: '{value}'"
        )
    try:
        col = int(parts[0].strip())
        row = int(parts[1].strip())
    except ValueError:
        raise ValueError(
            f"'{key}' must contain two integers separated by a comma, "
            f"got: '{value}'"
        )
    if not (0 <= col < width and 0 <= row < height):
        raise ValueError(
            f"'{key}' ({col},{row}) is outside the maze "
            f"(valid range: col 0-{width - 1}, row 0-{height - 1})."
        )
    return col, row


def boolean(value: str, key: str) -> bool:
    """
    Parse 'True' / 'False'
    Also accepts '1'/'0' and 'yes'/'no'
    """
    if value.lower() in ("true", "1", "yes"):
        return True
    if value.lower() in ("false", "0", "no"):
        return False
    raise ValueError(f"'{key}' must be True or False, got: '{value}'")
