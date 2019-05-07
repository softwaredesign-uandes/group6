from Block import *
import itertools


class BlockModel:  # Entity
    def __init__(self, name, blocks, mineral_deposit):
        self._name = None
        self._blocks = None
        self._mineral_deposit = None
        #validations
        self.name = name
        self.blocks = blocks
        self.mineral_deposit = mineral_deposit

    @property
    def name(self):
        """Get block model name"""
        return self._name

    @name.setter
    def name(self, value):
        """Set block model name"""
        if not (isinstance(value, str)): raise TypeError("block model name must be string")
        if not value.strip(): raise ValueError("block model name cannot be empty")
        self._name = value

    @name.deleter
    def name(self):
        """delete block model name"""
        del self._name

    @property
    def blocks(self):
        """Get block model blocks"""
        return self._blocks

    @blocks.setter
    def blocks(self, block_model_blocks):
        """Set block model blocks"""
        if not (isinstance(block_model_blocks, list)): raise TypeError("block model blocks must be a list of blocks")
        if not block_model_blocks: raise ValueError("block model blocks cannot be empty")
        for block in block_model_blocks:
            if not (isinstance(block,Block)): raise TypeError("Block model blocks must be of 'Block' class")
        self._blocks = block_model_blocks

    @blocks.deleter
    def blocks(self):
        """delete block model blocks"""
        del self._blocks

    @property
    def mineral_deposit(self):
        """Get block model mineral deposit parent"""
        return self._mineral_deposit

    @mineral_deposit.setter
    def mineral_deposit(self, value):
        """Set block model mineral deposit parent"""
        if not (isinstance(value, str)): raise TypeError("mineral deposit parent must be string")
        if not value.strip(): raise ValueError("mineral deposit parent cannot be empty")
        self._mineral_deposit = value

    @mineral_deposit.deleter
    def id(self):
        """delete block model mineral deposit parent"""
        del self._mineral_deposit

    def count_blocks(self):
        block_quantity = len(self.blocks)
        return block_quantity

    def total_weight(self):
        total_weight = sum(block.weight for block in self.blocks)
        return total_weight

    def total_mineral_weight(self):
        grade_and_types = self.get_block_model_structure()
        mineral_weight_results = {}
        for grade in grade_and_types:
            grade_weight = 0
            grade_type = grade_and_types[grade]
            for block in self.blocks:
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
            mineral_weight_results[grade] = grade_weight
        return mineral_weight_results

    def air_blocks_percentage(self):
        air_blocks = sum(block.weight == 0 for block in self.blocks)
        total_blocks = len(self.blocks)
        air_blocks_percentage = (air_blocks/total_blocks)*100
        return air_blocks_percentage

    def get_block_model_structure(self):
        grade_template = self.blocks[0].grades
        grade_and_types = {}
        for grade in grade_template:
            grade_and_types[grade] = grade_template[grade]["grade_type"]
        return grade_and_types

    def get_border_limits(self):
        x_coordinate_limit = max(block.x_coordinate for block in self.blocks)
        y_coordinate_limit = max(block.y_coordinate for block in self.blocks)
        z_coordinate_limit = max(block.z_coordinate for block in self.blocks)
        return [x_coordinate_limit, y_coordinate_limit, z_coordinate_limit]

    def combine_blocks(self, blocks_to_combine, new_coordinates):
        x, y, z = new_coordinates[0], new_coordinates[1], new_coordinates[2]
        new_id = str(x)+","+str(y)+","+str(z)
        new_weight = 0
        for block in blocks_to_combine:
            new_weight += block.weight
        new_grades = {}
        for mineral in blocks_to_combine[0].grades.keys():
            for block in blocks_to_combine:
                block_grade_value = block.grades[mineral]["value"]
                block_grade_type = block.grades[mineral]["grade_type"]
                if mineral not in new_grades.keys():
                    new_grades[mineral] = {"value": block_grade_value, "grade_type": block_grade_type}
                else:
                    if block_grade_type == 1:
                        new_value = new_grades[mineral]["value"] + block.grades[mineral]["value"]
                    else:
                        new_value = ((new_weight * new_grades[mineral]["value"])+(block.weight * block_grade_value)) / \
                                    (new_weight+block.weight)
                    new_grades[mineral]["value"] = new_value
        new_block = Block(new_id, x, y, z, new_weight, new_grades)
        return new_block

    def reblock_model(self, Rx, Ry, Rz):
        if not isinstance(Rx, int):
            raise TypeError('Rx must be int')
        if not isinstance(Ry, int):
            raise TypeError('Ry must be int')
        if not isinstance(Rz, int):
            raise TypeError('Rz must be int')

        if Rx < 1:
            raise ValueError('Rx must be equal or greater than one')
        if Ry < 1:
            raise ValueError('Ry must be equal or greater than one')
        if Rz < 1:
            raise ValueError('Rz must be equal or greater than one')

        x_limit, y_limit, z_limit = self.get_border_limits()
        block_id_positions = {}
        for i in range(len(self.blocks)):
            block_id_positions[self.blocks[i].id] = i

        new_x_coordinate = 0
        reblocked_blocks = []
        x_axis = 0
        while x_axis <= x_limit:
            y_axis = 0
            new_y_coordinate = 0
            while y_axis <= y_limit:
                z_axis = 0
                new_z_coordinate = 0
                while z_axis <= z_limit:
                    x_range = list(range(x_axis, x_axis + Rx))
                    y_range = list(range(y_axis, y_axis + Ry))
                    z_range = list(range(z_axis, z_axis + Rz))
                    combine_blocks_list = []

                    for coordinates in itertools.product(x_range, y_range, z_range):
                        block_id = "{},{},{}".format(coordinates[0], coordinates[1], coordinates[2])
                        if block_id in block_id_positions:
                            combine_blocks_list.append(self.blocks[block_id_positions[block_id]])
                    if len(combine_blocks_list) > 0:
                        combine_blocks_coordinates = (new_x_coordinate, new_y_coordinate, new_z_coordinate)
                        new_block = self.combine_blocks(combine_blocks_list, combine_blocks_coordinates)
                        reblocked_blocks.append(new_block)
                    z_axis += Rz
                    new_z_coordinate += 1
                y_axis += Ry
                new_y_coordinate += 1
            x_axis += Rx
            new_x_coordinate += 1
        self.blocks = reblocked_blocks
