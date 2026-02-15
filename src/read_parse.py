import sys


def read_config(file_name): str) -> None:

    try:
        with open(file_name, "r") as file:
            coords = {}
            for line_num, line in enumerate(file, start=1):
                if line.startswith('#') or not line.strip():
                    continue

                if '=' not in line or line.count('=') > 1:
                    print(f"Error on line {line_num}: invalid format")
                    file.close()
                    return
                key, value = line.split('=')
                coords[key] = [value]
                print("found key {key}, with value {value}")
        except FileNotFoundError:
            print(f"error, File {file_name} Not Found!")
            sys.exit(1)
    except Exception as e:
        print(f"an error occured: {e}")
        file.close()
        sys.exit(1)
    parse_coords(coords)


def parse_coords(coords: dict = {}):

    if "ENTRY" in coords and "EXIT" in coords and "PERFECT":
        ee_values = []
        ee_values.append(coords("ENTRY"))
        ee_values.append(coords("EXIT"))
        perfect_value = coords("PERFECT")
    else:
        print("Error: the config file misses one or more elements!")
        return

    coords.pop("ENTRY", None)
    coords.pop("EXIT", None)
    coords.pop("PERFECT", None)
    try:
        values = []
        for key, value in coords.items():
            values.append(int(value))

        if not isinstance(perfect_value, bool):
            raise ValueError(
            f"Error: {last_key} element has an invalid Value ({last_value})"
            )

        for value in values:
            if value < 0:
                raise ValueError(
                        f"Error: {coords.keys{value)} can not be negative!"
                        )

    ee_items = []
    for value in ee_values:

        parts = value.split(',')

        if value.count(',') != 1 or len(parts) != 2:
            raise ValueError("Error: the item {coords.key(value)} is invalid")

        x, y = int(parts[0]), int(parts[1])
        ee_items.append((x, y))
        """
        still needs a check if the width and length are inside the maze , (see GAS)
        and also check if the ee values are not None
        """
    except ValueError as e:
        if "invalid literal" in str(e):
            print(f"Error: an error happend while parsing")
        else:
            print(e)
        return
    except Exception as e:
        print(e)







if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 a_maze_ing.py config.txt")

    else:
        read_config(sys.argv[1])
