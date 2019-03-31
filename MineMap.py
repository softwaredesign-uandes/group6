# -*- coding: utf-8 -*-

import sys


def load_map():
    """
    Function for loading maps on the database.
    """
    print("FUNCTION LOAD MAP")
    
    
def new_map():
    """
    Function for creating new maps on the database.
    """
    print("FUNCTION NEW MAP")


def close_program():
    """
    Function for closing connection with database before exiting.
    """
    print("Closing program...")
    sys.exit()


main_menu_options = {
    "Load Map": load_map,
    "Create New Map": new_map,
    "Exit": close_program
}


def main_menu():

    main_menu_keys = list(main_menu_options.keys())
        
    while True:
        
        print("Main Menu:")
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
