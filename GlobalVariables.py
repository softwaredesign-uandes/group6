import os
from UtilityFunctions import read_database, save_to_database, current_directory
from DomainObjects import MineralDeposit, BlockModel, Block

loaded_model = None
mineral_deposits = {}
grade_types = ["Ton", "%", "oz/ton", "ppm"]


def load_mineral_deposits():
    """
    Function for loading Mineral Deposits when starting the program, if available.
    """
    global mineral_deposits
    try:
        mineral_deposits = read_database(current_directory + "\model_files\\mineral_deposits.db")
    except:
        mineral_deposits = {}


def add_mineral_deposit(mineral_deposit_name, mineral_deposit):
    global mineral_deposits
    mineral_deposits[mineral_deposit_name] = mineral_deposit
    save_to_database("mineral_deposits", mineral_deposits)


def set_loaded_model(block_model):
    global loaded_model
    loaded_model = block_model


def get_mineral_deposits():
    return mineral_deposits



