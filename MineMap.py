# -*- coding: utf-8 -*-

import sys
import pickle
import os
import glob

model_loaded = None


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
                'weight': data[6]+data[7],
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
    with open('model files\\'+filename+'.db', 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)


def read_database(filename):
    with open(filename, 'rb') as handle:
        return pickle.load(handle)


def load_map():
    """
    Function for loading maps on the database.
    """
    global model_loaded
    current_directory = os.path.dirname(os.path.abspath(__file__))
    menu_keys = []
    os.chdir(current_directory + "\model files")
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
                model_loaded = read_database(current_directory + "\model files\\" + menu_key)
                break
        else:
            print("Unknown Option, please select one of the given ones...")


def new_map():
    """
    Function for creating new maps on the database.
    """
    global model_loaded
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
        model_loaded = new_model


def query_map():
    """
    Function for query a loaded map
    """
    if not model_loaded:
        input("you must first load a map...")
        return None
    while True:
        block_id = input("please enter a block id of the currently loaded model")
        try:
            int(block_id)
        except:
            print("You must enter a number...")
            continue
        if block_id in model_loaded:
            print("block " + block_id + " info: ")
            for data in model_loaded[block_id]:
                print (data + ": " + model_loaded[block_id][data])
            break
        else:
            print("Invalid block id...")


def close_program():
    """
    Function for closing connection with database before exiting.
    """
    print("Closing program...")
    sys.exit()


def main_menu():
    main_menu_options = {
        "Create New Map": new_map,
        "Load Map": load_map,
        "Query Map": query_map,
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


main_menu()
