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

    if "ENTRY" in coords and "EXIT" in coords and "PERFECT" in coords:
        ee_values = []
        ee_values.append(coords("ENTRY"))
        ee_values.append(coords("EXIT"))
        perfect_value = coords("PERFECT")
    else:
        print("Error: the config file misses one or more elements!")
        return

    try:
        values = []
        for key, value in coords.items():
            if key == "ENTRY" or key == "EXIT" or key == "PERFECT":
                continue
            values.append(int(value))

        if not isinstance(perfect_value, bool):
            raising(
            f"Error: {last_key} element has an invalid Value ({last_value})"
            )

        for value in values:
            if value < 0:
                raising(
                        f"Error: {coords.keys(value)} can not be negative!"
                    )

    for value in ee_values:

        parts = value.split(',')

        if value.count(',') != 1 or len(parts) != 2:
            raising("Error: the item {coords.key(value)} is invalid")

        x, y = int(parts[0]), int(parts[1]):
        coords[ #i need to make sure that the values of ee's are converted to int and are a tuples
 
        validation(coords)
    except ValueError as e:
        print(e)
        return
    except Exception as e:
        print(e)
        return


def validation(coords: dict):
    """
    still needs a check if the width and length are inside the maze , (see GAS)
    and also check if the ee values are not None
    """ 

def raising(err_msg: str):
    raise ValueError(message)
    exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 a_maze_ing.py config.txt")

    else:
        read_config(sys.argv[1])
