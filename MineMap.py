import sys
import pickle
import os
import glob

loaded_model = None
mineral_deposits = {}
mineral_types = ["Ton", "%", "oz/ton", "ppm"]
current_directory = os.path.dirname(os.path.abspath(__file__))


class MineralDeposit:  # Entity
    def __init__(self, name, x, y, z, weight, grades):
        self.name = name
        self.x_coordinate_column = x
        self.y_coordinate_column = y
        self.z_coordinate_column = z
        self.weight_column = weight
        self.grades = grades


class BlockModel:  # Entity
    def __init__(self, name, blocks, mineral_deposit):
        self.name = name
        self.blocks = blocks
        self.mineral_deposit = mineral_deposit


class Block:  # Value Object
    def __init__(self, block_id, x, y, z, weight, grades):
        self.id = block_id
        self.x_coordinate = x
        self.y_coordinate = y
        self.z_coordinate = z
        self.weight = weight
        self.grades = grades


def load_mineral_deposits():
    """
    Function for loading Mineral Deposits when starting the program, if available.
    """
    global mineral_deposits
    try:
        mineral_deposits = read_database(current_directory + "\model_files\\mineral_deposits.db")
    except:
        mineral_deposits = {}


def main_menu():
    main_menu_options = {
        "Create New Block Model": new_block_model,
        "Create New Mineral Deposit": new_mineral_deposit,
        "Load Block Model": load_block_model_from_database,
        "Query Block Model": query_block_model,
        "Exit": close_program
    }

    main_menu_keys = list(main_menu_options.keys())
    while True:
        print("Menu options:")
        for option_index in range(len(main_menu_keys)):
            print("{} - {}".format(option_index + 1, main_menu_keys[option_index]))
        selected_option = input("Select Option: ")
        selected_option = ensure_number(selected_option, "Select Option: ")
        if -1 < selected_option < len(main_menu_keys) + 1:
            main_menu_key = main_menu_keys[selected_option - 1]
            main_menu_options[main_menu_key]()
        else:
            print("Unknown Option, please select one of the given ones...")


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


def new_block_model():
    """
    Function for creating new Block Models for Mineral Deposits.
    """
    global loaded_model
    mineral_deposit_keys = list(mineral_deposits.keys())
    new_model = None
    if len(mineral_deposit_keys) == 0:
        input("No Mineral Deposits Available, you must create one first...")
        return None
    while True:
        print("Menu options:")
        for option_index in range(len(mineral_deposit_keys)):
            print("{} - {}".format(option_index + 1, mineral_deposit_keys[option_index]))
        print("0 - Back")
        selected_option = input("Select Mineral Deposit: ")
        selected_option = ensure_number(selected_option, "Select Mineral Deposit: ")
        if -1 < selected_option < len(mineral_deposit_keys) + 1:
            if selected_option == 0:
                break
            else:
                selected_deposit = mineral_deposit_keys[selected_option - 1]
                new_model = load_block_model_from_file(selected_deposit)
            break
        else:
            print("Unknown Option, please select one of the given ones...")
    if new_model:
        save_to_database(new_model.name, new_model)
        loaded_model = new_model


def load_block_model_from_file(selected_deposit):
    """
    Function for loading Block Models from blocks files.
    """
    filename = input('please enter the location of input file:\n')
    if not os.path.isfile(filename):
        input("file not found...")
        return None
    output_filename = input('please enter the location of output file:\n')
    x_coordinate_column = mineral_deposits[selected_deposit].x_coordinate_column
    y_coordinate_column = mineral_deposits[selected_deposit].y_coordinate_column
    z_coordinate_column = mineral_deposits[selected_deposit].z_coordinate_column
    weight_column = mineral_deposits[selected_deposit].weight_column
    mineral_deposit_grades = mineral_deposits[selected_deposit].grades
    blocks = []
    with open(filename) as f:
        for line in f.readlines():
            data = line.strip().split(' ')
            block_grades = {}
            for grade in mineral_deposit_grades:
                block_grades[grade] = {
                    "value": data[mineral_deposit_grades[grade]["mineral_column"]],
                    "grade_type": mineral_deposit_grades[grade]["mineral_type"]
                }
            block_id = data[x_coordinate_column]+","+data[y_coordinate_column]+","+data[z_coordinate_column]
            block_x_coordinate = data[x_coordinate_column]
            block_y_coordinate = data[y_coordinate_column]
            block_z_coordinate = data[z_coordinate_column]
            block_weight = data[weight_column]
            new_block = Block(block_id, block_x_coordinate, block_y_coordinate, block_z_coordinate, block_weight,
                              block_grades)
            blocks.append(new_block)
    block_model = BlockModel(output_filename, blocks, selected_deposit)
    return block_model


def save_to_database(filename, data):
    with open(current_directory + '\model_files\\'+filename+'.db', 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)


def read_database(filename):
    with open(filename, 'rb') as handle:
        return pickle.load(handle)


def new_mineral_deposit():
    """
    Function for creating new Mineral Deposits.
    """
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


def load_block_model_from_database():
    """
    Function for loading Block Models from the database.
    """
    global loaded_model
    menu_keys = []
    os.chdir(current_directory + "\model_files")
    for file in glob.glob("*.db"):
        menu_keys.append(file)
    if len(menu_keys) == 0:
        input("No Block Maps Available, you must create one first...")
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


def query_block_model():
    """
    Function for querying a loaded Block Model.
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


load_mineral_deposits()
main_menu()
