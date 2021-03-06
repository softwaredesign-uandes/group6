import glob
import os
from Block import *
from BlockModel import *
from MineralDeposit import *
from MineMapVariables import *
from UtilityFunctions import ensure_number, save_to_database, read_database, close_program, current_directory,\
    get_reblock_params


def main_menu():
    main_menu_options = {
        "Create New Block Model": new_block_model,
        "Create New Mineral Deposit": new_mineral_deposit,
        "Load Block Model": load_block_model_from_database,
        "Query Block Model": query_block_model,
        "Reblock Block Model": reblock_block_model,
        "Virtual Reblock Block Model": virtual_reblock_block_model,
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
    mineral_deposit_keys = list(mine_map_variables.mineral_deposits.keys())
    new_model = None
    if len(mineral_deposit_keys) == 0:
        input("No Mineral Deposits Available, you must create one first...")
        return None
    while True:
        print("Menu options:")
        list(map(lambda option: print("{} - {}".format(option + 1, mineral_deposit_keys[option])),
                 range(len(mineral_deposit_keys))))
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
        mine_map_variables.loaded_model = new_model


def load_block_model_from_file(selected_deposit):
    """
    Function for loading Block Models from blocks files.
    """
    filename = input('please enter the location of input file:\n')
    if not os.path.isfile(filename):
        input("file not found...")
        return None
    output_filename = input('please enter the location of output file:\n')
    x_coordinate_column = mine_map_variables.mineral_deposits[selected_deposit].x_coordinate_column
    y_coordinate_column = mine_map_variables.mineral_deposits[selected_deposit].y_coordinate_column
    z_coordinate_column = mine_map_variables.mineral_deposits[selected_deposit].z_coordinate_column
    weight_column = mine_map_variables.mineral_deposits[selected_deposit].weight_column
    mineral_deposit_grades = mine_map_variables.mineral_deposits[selected_deposit].grades
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
        if new_mineral_deposit_name not in mine_map_variables.mineral_deposits:
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
                    for grade_type in range(len(mine_map_variables.grade_types)):
                        print("{} - {}".format(grade_type + 1, mine_map_variables.grade_types[grade_type]))
                    while True:
                        new_mineral_type = input("Select Mineral Type:")
                        new_mineral_type = ensure_number(new_mineral_type, "Select Mineral Type:")
                        if 0 < new_mineral_type < len(mine_map_variables.grade_types) + 1:
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
            mine_map_variables.add_mineral_deposit_to_database(new_mineral_deposit_name, mineral_deposit)
        else:
            input("There's already a Mineral Deposit with that name.")


def load_block_model_from_database():
    """
    Function for loading Block Models from the database.
    """
    os.chdir(current_directory + "\model_files")
    menu_keys = list(map(lambda file: file, glob.glob("*.db")))
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
                mine_map_variables.loaded_model = read_database(current_directory + "\model_files\\" + menu_key)
                break
        else:
            print("Unknown Option, please select one of the given ones...")


def query_block_model():
    """
    Function for querying the loaded Block Model.
    """
    query_options = {
        "Information of specific block": query_block,
        "Number of Blocks in model": query_block_model_blocks_quantity,
        "Total weight of model": query_block_model_total_weight,
        "Total Mineral weight of model": query_block_model_total_mineral_weight,
        "Percentage of Air Blocks in model": query_block_model_air_block_percentage
    }
    if not mine_map_variables.loaded_model:
        input("you must first load a map...")
        return None
    query_keys = list(query_options.keys())
    while True:
        print("Query options:")
        list(map(lambda option: print("{} - {}".format(option + 1, query_keys[option])), range(len(query_keys))))
        print("0 - Back")
        selected_option = input("Select Option: ")
        selected_option = ensure_number(selected_option, "Select Option: ")
        if -1 < selected_option < len(query_keys) + 1:
            if selected_option == 0:
                break
            else:
                query_key = query_keys[selected_option - 1]
                query_options[query_key](mine_map_variables.loaded_model)
        else:
            print("Unknown Option, please select one of the given ones...")


def query_block(block_model):
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
    target_block = list(filter(lambda block: block.id == block_id, block_model.blocks))
    if len(target_block) > 0:
        print("X,Y,Z: {}".format(block_id))
        print("Weigth: {}".format(target_block[0].weight))
        list(map(lambda grade: print("{}: {} {}".format(grade, target_block[0].grades[grade]["value"],
                                                        mine_map_variables.grade_types[target_block[0]
                                                        .grades[grade]["grade_type"]-1])),
                 target_block[0].grades))


def query_block_model_blocks_quantity(block_model):
    blocks_quantity = block_model.count_blocks()
    print("Number of blocks: {}.".format(blocks_quantity))


def query_block_model_total_weight(block_model):
    total_weight = block_model.total_weight()
    print("Total weight: {} tons.".format(total_weight))


def query_block_model_total_mineral_weight(block_model):
    mineral_weights = block_model.total_mineral_weight()
    for mineral_weight in mineral_weights:
        mineral = mineral_weight
        weight = mineral_weights[mineral_weight]
        print("Total weight of {} is {} metric tons.".format(mineral, weight))


def query_block_model_air_block_percentage(block_model):
    air_blocks_percentage = block_model.air_blocks_percentage()
    print("Percentage of Air blocks: {}%.".format(air_blocks_percentage))


def reblock_block_model():
    if not mine_map_variables.loaded_model:
        input("you must first load a map...")
        return None
    limits = mine_map_variables.loaded_model.get_border_limits()
    reblock_params = get_reblock_params(limits)
    if reblock_params:
        mine_map_variables.loaded_model.reblock_model(reblock_params[0], reblock_params[1], reblock_params[2], False)


def virtual_reblock_block_model():
    if not mine_map_variables.loaded_model:
        input("you must first load a map...")
        return None
    limits = mine_map_variables.loaded_model.get_border_limits()
    reblock_params = get_reblock_params(limits)
    if reblock_params:
        mine_map_variables.loaded_model.reblock_model(reblock_params[0], reblock_params[1], reblock_params[2], True)


mine_map_variables = MineMapVariables()
mine_map_variables.load_mineral_deposits_from_database()
main_menu()
