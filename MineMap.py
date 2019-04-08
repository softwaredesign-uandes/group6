import sys
import pickle
import os
import glob

loaded_model = None
mineral_deposits = {}
mineral_types = ["Ton", "%", "oz/ton", "ppm"]
current_directory = os.path.dirname(os.path.abspath(__file__))


class MineralDeposit:
    def __init__(self, name, x, y, z, weight, grades):
        self.name = name
        self.x_coordinate_column = x
        self.y_coordinate_column = y
        self.z_coordinate_column = z
        self.weight_column = weight
        self.grades = grades


def load_mineral_deposits():
    global mineral_deposits
    try:
        mineral_deposits = read_database(current_directory + "\model_files\\mineral_deposits.db")
    except:
        mineral_deposits = {}


def marvin_model(filename):
    blocks_model_data = {}
    with open(filename) as f:
        for line in f.readlines():
            data = line.strip().split(' ')
            blocks_model_data[data[0]] = {
                'x': data[1],
                'y': data[2],
                'z': data[3],
                'weight': data[4],
                'au': data[5],
                'cu': data[6],
                'proc_profit': data[7]
            }
    return blocks_model_data


def zuck_small_model(filename):
    blocks_model_data = {}
    with open(filename) as f:
        for line in f.readlines():
            data = line.strip().split(' ')
            blocks_model_data[data[0]] = {
                'x': data[1],
                'y': data[2],
                'z': data[3],
                'weight': float(data[6])+float(data[7]),
                'cost': data[4],
                'value': data[5],
                'rock_tonnes': data[6],
                'ore_tonnes': data[7]
            }
    return blocks_model_data


def new_block_model(map_type):
    filename = input('please enter the location of the file:\n')
    if not os.path.isfile(filename):
        input("file not found...")
        return None
    blocks_model_data = []
    if map_type == 1:
        blocks_model_data = marvin_model(filename)
    elif map_type == 2:
        blocks_model_data = zuck_small_model(filename)
    return blocks_model_data


def save_to_database(filename, data):
    with open(current_directory + '\model_files\\'+filename+'.db', 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)


def read_database(filename):
    with open(filename, 'rb') as handle:
        return pickle.load(handle)


def load_map():
    """
    Function for loading maps on the database.
    """
    global loaded_model
    menu_keys = []
    os.chdir(current_directory + "\model_files")
    for file in glob.glob("*.db"):
        menu_keys.append(file)
    if len(menu_keys) == 0:
        input("you must first create a new map...")
        return None
    menu_keys.append("back")

    while True:
        print("load options:")
        for option_index in range(len(menu_keys)):
            print("{} - {}".format(option_index + 1, menu_keys[option_index]))
        selected_option = input("Select Option: ")
        try:
            selected_option = int(selected_option)
        except:
            print("You must enter a number...")
            continue
        if -1 < selected_option < len(menu_keys) + 1:
            menu_key = menu_keys[selected_option - 1]
            if menu_key == "back":
                break
            else:
                loaded_model = read_database(current_directory + "\model_files\\" + menu_key)
                break
        else:
            print("Unknown Option, please select one of the given ones...")


def new_map():
    """
    Function for creating new maps on the database.
    """
    global loaded_model
    new_map_menu_options = {
        "Marvin": 1,
        "Zuck small": 2,
        "Back": 0
    }
    new_map_keys = list(new_map_menu_options.keys())
    while True:
        print("Menu options:")
        for option_index in range(len(new_map_keys)):
            print("{} - {}".format(option_index + 1, new_map_keys[option_index]))
        selected_option = input("Select Option: ")
        try:
            selected_option = int(selected_option)
        except:
            print("You must enter a number...")
            continue
        if -1 < selected_option < len(new_map_keys) + 1:
            new_menu_key = new_map_keys[selected_option - 1]
            if new_menu_key == 0:
                break
            else:
                new_model = new_block_model(new_map_menu_options[new_menu_key])
            break
        else:
            print("Unknown Option, please select one of the given ones...")
    if new_model:
        filename = input("please enter a name for the model:\n")
        save_to_database(filename, new_model)
        loaded_model = new_model


def query_map():
    """
    Function for query a loaded map
    """
    if not loaded_model:
        input("you must first load a map...")
        return None
    while True:
        block_id = input("please enter a block id of the currently loaded model: ")
        try:
            int(block_id)
        except:
            print("You must enter a number...")
            continue
        if block_id in loaded_model:
            print("block " + block_id + " info: ")
            for data in loaded_model[block_id]:
                print("{0}: {1}".format(data, loaded_model[block_id][data]))
            break
        else:
            print("Invalid block id...")


def close_program():
    """
    Function for closing connection with database before exiting.
    """
    print("Closing program...")
    sys.exit()


def ensure_number(new_number, repeat_text):
    is_number = False
    while not is_number:
        try:
            new_number = int(new_number)
            is_number = True
        except:
            print("You must enter a number...")
            new_number = input(repeat_text)
            continue
    return new_number


def new_mineral_deposit():
    global mineral_deposits
    new_mineral_deposit_name = input("Enter name for new Mineral Deposit \nor Leave blank to go back:")
    if new_mineral_deposit_name != "":
        if new_mineral_deposit_name not in mineral_deposits:
            print("Parameters for new block models:")
            x_coordinate = input("Column number for x coordinate:")
            x_coordinate = ensure_number(x_coordinate, "Column number for x coordinate:")
            y_coordinate = input("Column number for y coordinate:")
            y_coordinate = ensure_number(y_coordinate, "Column number for y coordinate:")
            z_coordinate = input("Column number for z coordinate:")
            z_coordinate = ensure_number(z_coordinate, "Column number for z coordinate:")
            weight = input("Column number for weight:")
            weight = ensure_number(weight, "Column number for weight:")
            grades = {}
            print("Mineral Deposit Grades:")
            while True:
                print("Add new mineral?\n1-Yes\n2-No")
                new_mineral_option = input("Option:")
                new_mineral_option = ensure_number(new_mineral_option, "Option:")
                if new_mineral_option == 1:
                    new_mineral_column = input("Column number for the mineral:")
                    new_mineral_column = ensure_number(new_mineral_column, "Column number for the mineral:")
                    new_mineral_name = input("Enter mineral's name:")
                    while new_mineral_name == "":
                        new_mineral_name = input("Enter mineral's name:")
                    print("Mineral Types:")
                    for mineral_type in range(len(mineral_types)):
                        print("{} - {}".format(mineral_type + 1, mineral_types[mineral_type]))
                    while True:
                        new_mineral_type = input("Select Mineral Type:")
                        new_mineral_type = ensure_number(new_mineral_type, "Select Mineral Type:")
                        if 0 < new_mineral_type < len(mineral_types) + 1:
                            break
                        else:
                            print("Option out of range, try again...")
                    new_mineral = {
                        "mineral_column": new_mineral_column,
                        "mineral_type": new_mineral_type
                    }
                    grades[new_mineral_name] = new_mineral
                elif new_mineral_option == 2:
                    break
                else:
                    print("Unknown option, try again...")
            mineral_deposit = MineralDeposit(new_mineral_deposit_name, x_coordinate, y_coordinate, z_coordinate,
                                             weight, grades)
            mineral_deposits[new_mineral_deposit_name] = mineral_deposit
            save_to_database("mineral_deposits",mineral_deposits)
        else:
            input("There's already a Mineral Deposit with that name.")


def main_menu():
    main_menu_options = {
        "Create New Map": new_map,
        "Load Map": load_map,
        "Query Map": query_map,
        "Create New Mineral Deposit": new_mineral_deposit,
        "Exit": close_program
    }

    main_menu_keys = list(main_menu_options.keys())
    while True:
        print("Menu options:")
        for option_index in range(len(main_menu_keys)):
            print("{} - {}".format(option_index + 1, main_menu_keys[option_index]))
        selected_option = input("Select Option: ")
        try:
            selected_option = int(selected_option)
        except:
            print("You must enter a number...")
            continue
        if -1 < selected_option < len(main_menu_keys) + 1:
            main_menu_key = main_menu_keys[selected_option - 1]
            main_menu_options[main_menu_key]()
        else:
            print("Unknown Option, please select one of the given ones...")


load_mineral_deposits()
main_menu()
