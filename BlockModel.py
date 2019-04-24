from Block import *
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

    def combine_blocks(self, blocksToCombine, newCoordinates):
        x,y,z = newCoordinates[0],newCoordinates[1],newCoordinates[2]
        newId = str(x)+","+str(y)+","+str(z)
        newWeight = 0
        for block in blocksToCombine:
            newWeight += block.weight
        newGrades = {}
        for mineral in blocksToCombine[0].grades.keys():
            for block in blocksToCombine:
                blockGradeValue = block.grades[mineral]["value"]
                blockGradetype = block.grades[mineral]["grade_type"]
                if mineral not in newGrades.keys():
                    newGrades[mineral] = {"value":blockGradeValue, "grade_type":blockGradetype}
                else:
                    if blockGradetype == 1:
                        newValue = newGrades[mineral]["value"] + block.grades[mineral]["value"]
                    else:
                        newValue = ((newWeight * newGrades[mineral]["value"])+(block.weight * blockGradeValue))/(newWeight+block.weight)
                    newGrades[mineral]["value"] = newValue
        newBlock = Block(newId, x, y, z, newWeight,newGrades)
        return newBlock