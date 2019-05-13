from UtilityFunctions import ensure_number, save_to_database, read_database, current_directory
from MineralDeposit import *
from BlockModel import *


class MineMapVariables:  # Entity
    def __init__(self):
        self.loaded_model = None
        self.mineral_deposits = {}
        self.grade_types = ["Ton", "%", "oz/ton", "ppm"]

    def load_mineral_deposits_from_database(self):
        try:
            self.mineral_deposits = read_database(current_directory + "\model_files\\mineral_deposits.db")
        except:
            self.mineral_deposits = {}

    def add_mineral_deposit_to_database(self, mineral_deposit_name, mineral_deposit):
        if not (isinstance(mineral_deposit, MineralDeposit)):
            raise TypeError("Given Mineral Deposit is not instance of the class.")
        self.mineral_deposits[mineral_deposit_name] = mineral_deposit
        save_to_database("mineral_deposits", self.mineral_deposits)

    @property
    def loaded_model(self):
        """Get block id"""
        return self._loaded_model

    @loaded_model.setter
    def loaded_model(self, model):
        """Set block id"""
        if not (isinstance(model, BlockModel) or isinstance(model, type(None))):
            raise TypeError("Model must be instance of Block Model")
        self._loaded_model = model

