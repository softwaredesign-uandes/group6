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