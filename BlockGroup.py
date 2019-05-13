import itertools
import math
from AbstractBlock import *
from Block import *

class BlockGroup(AbstractBlock):  # Value Object
    def __init__(self, blocks_to_group, reblock_factors):
        self._blocks = None
        self._reblock_factors = None
        #constructor validations:
        self.blocks = blocks_to_group
        self.reblock_factors = reblock_factors

    @property
    def blocks(self):
        """Get block group blocks"""
        return self._blocks

    @blocks.setter
    def blocks(self, value):
        """Set block group blocks"""
        if not (isinstance(value, list)): raise TypeError("blocks must be a list of blocks")
        if not value: raise ValueError("block group blocks cannot be empty")
        for block in value:
            if not (isinstance(block,(Block, BlockGroup))): raise TypeError("blocks must be either 'Block' class or 'BlockGroup' class")
        self._blocks = value

    @property
    def reblock_factors(self):
        """Get block group reblock factors"""
        return self._reblock_factors

    @reblock_factors.setter
    def reblock_factors(self,value):
        """Set block group reblock factors"""
        if not (isinstance(value, list)): raise TypeError("reblock factors must be a list of three integer numbers")
        for factor in value:
            if not (isinstance(factor, int)): raise TypeError("reblock factor must be integer number")
        self._reblock_factors = value

    @property
    def id(self):
        """Get block group id"""
        return str(self.x_coordinate)+","+str(self.y_coordinate)+","+str(self.z_coordinate)

    def x_coordinate(self, block):
        return block.x_coordinate

    def y_coordinate(self, block):
        return block.y_coordinate

    def z_coordinate(self, block):
        return block.z_coordinate

    def __look_for_coordinate_by_dimension(self,dimension_letter):
        if not isinstance(dimension_letter,str): raise TypeError("dimesion letter must be string")
        dimension = str.lower(dimension_letter)
        if dimension not in ["x","y","z"]: raise ValueError("invalid dimension letter, this must be 'x', 'y' or 'z'")
        reblock_factor = {"x": self.reblock_factors[0], "y": self.reblock_factors[1], "z": self.reblock_factors[2]}
        coodinate_values = []
        for block in self.blocks:
            if dimension == "x":
                coodinate_values.append(block.x_coordinate)
            elif dimension == "y":
                coodinate_values.append(block.y_coordinate)
            else:
                coodinate_values.append(block.z_coordinate)
        minimum_value = min(coodinate_values)
        return math.floor(minimum_value / reblock_factor[dimension])

    @property
    def x_coordinate(self):
        """Get block group x coordinate"""
        return self.__look_for_coordinate_by_dimension("x")

    @property
    def y_coordinate(self):
        """Get block group y coordinate"""
        return self.__look_for_coordinate_by_dimension("y")

    @property
    def z_coordinate(self):
        """Get block group z coordinate"""
        return self.__look_for_coordinate_by_dimension("z")

    @property
    def weight(self):
        """Get block group weight"""
        return sum(map(lambda b: b.weight, self.blocks))

    def __combine_grade_weight(self, mineral, blocks):
        if blocks[0].grades[mineral]["grade_type"] == 1:
            return sum(map(lambda b: b.grades[mineral]["value"], blocks)), blocks[0].grades[mineral]["grade_type"]
        else:
            total_mineral_weight = sum(map(lambda b: b.grades[mineral]["value"]*b.weight, blocks))
            total_weight = sum(map(lambda b: b.weight, blocks))
            return total_mineral_weight/total_weight, blocks[0].grades[mineral]["grade_type"]

    @property
    def grades(self):
        """Get block group grades"""
        minerals = self.blocks[0].grades.keys()
        new_grade_values_and_types_values = list(map(self.__combine_grade_weight, minerals,
                                                     itertools.repeat(self.blocks)))
        value_and_type_tags = ("value", "grade_type")
        new_grade_values_and_types = (list(map(lambda g: dict(zip(value_and_type_tags, g)),
                                               new_grade_values_and_types_values)))
        block_group_grades = dict(zip(minerals, new_grade_values_and_types))
        return block_group_grades