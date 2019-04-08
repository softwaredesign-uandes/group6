import glob
import os
from DomainObjects import MineralDeposit, BlockModel, Block
import GlobalVariables
from UtilityFunctions import ensure_number, save_to_database, read_database, close_program, current_directory


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


def new_block_model():
    """
    Function for creating new Block Models for Mineral Deposits.
    """
    mineral_deposit_keys = list(GlobalVariables.mineral_deposits.keys())
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
        GlobalVariables.set_loaded_model(new_model)


def load_block_model_from_file(selected_deposit):
    """
    Function for loading Block Models from blocks files.
    """
    filename = input('please enter the location of input file:\n')
    if not os.path.isfile(filename):
        input("file not found...")
        return None
    output_filename = input('please enter the location of output file:\n')
    x_coordinate_column = GlobalVariables.mineral_deposits[selected_deposit].x_coordinate_column
    y_coordinate_column = GlobalVariables.mineral_deposits[selected_deposit].y_coordinate_column
    z_coordinate_column = GlobalVariables.mineral_deposits[selected_deposit].z_coordinate_column
    weight_column = GlobalVariables.mineral_deposits[selected_deposit].weight_column
    mineral_deposit_grades = GlobalVariables.mineral_deposits[selected_deposit].grades
    blocks = []
    with open(filename) as f:
        for line in f.readlines():
            data = line.strip().split(' ')
            block_grades = {}
            for grade in mineral_deposit_grades:
                block_grades[grade] = {
                    "value": float(data[mineral_deposit_grades[grade]["mineral_column"]]),
                    "grade_type": mineral_deposit_grades[grade]["grade_type"]
                }
            block_id = data[x_coordinate_column]+","+data[y_coordinate_column]+","+data[z_coordinate_column]
            block_x_coordinate = data[x_coordinate_column]
            block_y_coordinate = data[y_coordinate_column]
            block_z_coordinate = data[z_coordinate_column]
            block_weight = float(data[weight_column])
            new_block = Block(block_id, block_x_coordinate, block_y_coordinate, block_z_coordinate, block_weight,
                              block_grades)
            blocks.append(new_block)
    block_model = BlockModel(output_filename, blocks, selected_deposit)
    return block_model


def new_mineral_deposit():
    """
    Function for creating new Mineral Deposits.
    """
    new_mineral_deposit_name = input("Enter name for new Mineral Deposit \nor Leave blank to go back:")
    if new_mineral_deposit_name != "":
        if new_mineral_deposit_name not in GlobalVariables.mineral_deposits:
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
                    for grade_type in range(len(GlobalVariables.grade_types)):
                        print("{} - {}".format(grade_type + 1, GlobalVariables.grade_types[grade_type]))
                    while True:
                        new_mineral_type = input("Select Mineral Type:")
                        new_mineral_type = ensure_number(new_mineral_type, "Select Mineral Type:")
                        if 0 < new_mineral_type < len(GlobalVariables.grade_types) + 1:
                            break
                        else:
                            print("Option out of range, try again...")
                    new_mineral = {
                        "mineral_column": new_mineral_column,
                        "grade_type": new_mineral_type
                    }
                    grades[new_mineral_name] = new_mineral
                elif new_mineral_option == 2:
                    break
                else:
                    print("Unknown option, try again...")
            mineral_deposit = MineralDeposit(new_mineral_deposit_name, x_coordinate, y_coordinate, z_coordinate,
                                             weight, grades)
            GlobalVariables.add_mineral_deposit(new_mineral_deposit_name, mineral_deposit)
        else:
            input("There's already a Mineral Deposit with that name.")


def load_block_model_from_database():
    """
    Function for loading Block Models from the database.
    """
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
                GlobalVariables.set_loaded_model(read_database(current_directory + "\model_files\\" + menu_key))
                break
        else:
            print("Unknown Option, please select one of the given ones...")


def query_block_model():
    """
    Function for querying the loaded Block Model.
    """
    query_options = {
        "Information of specific block": query_block,
        "Total weight of model": total_weight_block_model,
        "Total Mineral weight of model": total_mineral_weight_block_model,
        "Percentage of Air Blocks in model": percentage_air_blocks_block_model
    }
    if not GlobalVariables.loaded_model:
        input("you must first load a map...")
        return None
    query_keys = list(query_options.keys())
    while True:
        print("Query options:")
        for option_index in range(len(query_keys)):
            print("{} - {}".format(option_index + 1, query_keys[option_index]))
        print("0 - Back")
        selected_option = input("Select Option: ")
        selected_option = ensure_number(selected_option, "Select Option: ")
        if -1 < selected_option < len(query_keys) + 1:
            if selected_option == 0:
                break
            else:
                query_key = query_keys[selected_option - 1]
                query_options[query_key]()
        else:
            print("Unknown Option, please select one of the given ones...")


def query_block():
    """
    Function for querying specific Block from loaded Block Model.
    """
    x_coordinate = input("X coordinate of the block:")
    x_coordinate = ensure_number(x_coordinate, "X coordinate of the block:")
    y_coordinate = input("Y coordinate of the block:")
    y_coordinate = ensure_number(y_coordinate, "Y coordinate of the block:")
    z_coordinate = input("Z coordinate of the block:")
    z_coordinate = ensure_number(z_coordinate, "Z coordinate of the block:")
    block_id = str(x_coordinate) + "," + str(y_coordinate) + "," + str(z_coordinate)
    for block in GlobalVariables.loaded_model.blocks:
        if block.id == block_id:
            print("X,Y,Z: {}".format(block_id))
            print("Weigth: {}".format(block.weight))
            for grade in block.grades:
                print("{}: {} {}".format(grade, block.grades[grade]["value"],
                                         GlobalVariables.grade_types[block.grades[grade]["grade_type"]-1]))


def count_model_blocks():
    print("Number of blocks: {}.".format(len(GlobalVariables.loaded_model.blocks)))


def total_weight_block_model():
    total_weight = sum(block.weight for block in GlobalVariables.loaded_model.blocks)
    print("Total weight: {} tons.".format(total_weight))


def total_mineral_weight_block_model():
    loaded_model_mineral_deposit = GlobalVariables.mineral_deposits[GlobalVariables.loaded_model.mineral_deposit]
    model_blocks = GlobalVariables.loaded_model.blocks
    for grade in loaded_model_mineral_deposit.grades:
        grade_weight = 0
        grade_type = loaded_model_mineral_deposit.grades[grade]["grade_type"]
        for block in model_blocks:
            block_grades = block.grades
            for block_grade in block_grades:
                if block_grade == grade:
                    if grade_type == 1:
                        grade_weight += block_grades[block_grade]["value"]
                    elif grade_type == 2:
                        grade_weight += block_grades[block_grade]["value"] * block.weight
                    elif grade_type == 3:
                        grade_weight += block_grades[block_grade]["value"] * block.weight / 35273.962
                    elif grade_type == 4:
                        grade_weight += block_grades[block_grade]["value"] * block.weight * 0.0001
        print("Total weight of {} is {} metric tons.".format(grade, grade_weight))


def percentage_air_blocks_block_model():
    air_blocks = sum(block.weight == 0 for block in GlobalVariables.loaded_model.blocks)
    total_blocks = len(GlobalVariables.loaded_model.blocks)
    print("Percentage of Air blocks: {}%.".format((air_blocks/total_blocks)*100))


GlobalVariables.load_mineral_deposits()
main_menu()
