from Block import *
from BlockGroup import *
from UtilityFunctions import chunks
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
            if not (isinstance(block,(Block, BlockGroup))): raise TypeError("Block model blocks must be of 'Block' class")
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

    def combine_grade_weight(self, mineral, blocks):
        if blocks[0].grades[mineral]["grade_type"] == 1:
            return sum(map(lambda b: b.grades[mineral]["value"], blocks)), blocks[0].grades[mineral]["grade_type"]
        else:
            total_mineral_weight = sum(map(lambda b: b.grades[mineral]["value"]*b.weight, blocks))
            total_weight = sum(map(lambda b: b.weight, blocks))
            return total_mineral_weight/total_weight, blocks[0].grades[mineral]["grade_type"]

    def combine_blocks(self, blocks_to_combine, new_coordinates):
        x, y, z = new_coordinates[0], new_coordinates[1], new_coordinates[2]
        new_id = str(x)+","+str(y)+","+str(z)
        new_weight = sum(map(lambda b: b.weight, blocks_to_combine))
        minerals = blocks_to_combine[0].grades.keys()
        new_grade_values_and_types_values = list(map(self.combine_grade_weight, minerals,
                                                     itertools.repeat(blocks_to_combine)))
        value_and_type_tags = ("value", "grade_type")
        new_grade_values_and_types = (list(map(lambda g: dict(zip(value_and_type_tags, g)),
                                               new_grade_values_and_types_values)))
        new_grades = dict(zip(minerals, new_grade_values_and_types))
        new_block = Block(new_id, x, y, z, new_weight, new_grades)
        return new_block

    def combine_chunks(self, chunks_to_combine, block_id_positions, x_coordinates_chunks, y_coordinates_chunks,
                       z_coordinates_chunks, virtual_reblocking, reblock_factor):
        """If the reblock is virtual, the method will produce Block Groups, it will produce new Blocks otherwise."""
        x_chunk = chunks_to_combine[0]
        y_chunk = chunks_to_combine[1]
        z_chunk = chunks_to_combine[2]
        combine_block_ids_list = list(map(lambda x: "{},{},{}".format(x[0], x[1], x[2]),
                                          itertools.product(x_chunk, y_chunk, z_chunk)))
        combine_block_ids_list = list(filter(lambda x: x in block_id_positions, combine_block_ids_list))
        if len(combine_block_ids_list) > 0:
            combine_blocks_list = list(map(lambda x: self.blocks[block_id_positions[x]], combine_block_ids_list))
            combine_blocks_coordinates = (x_coordinates_chunks.index(x_chunk), y_coordinates_chunks.index(y_chunk),
                                          z_coordinates_chunks.index(z_chunk))
            if virtual_reblocking:
                new_block = BlockGroup(combine_blocks_list, reblock_factor)
            else:
                new_block = self.combine_blocks(combine_blocks_list, combine_blocks_coordinates)
            return new_block

    def reblock_model(self, Rx, Ry, Rz, virtual):
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

        block_id_positions = dict(map(lambda x: (x[1].id, x[0]), enumerate(self.blocks)))

        x_coordinates = list(range(x_limit+1))
        y_coordinates = list(range(y_limit+1))
        z_coordinates = list(range(z_limit+1))

        x_coordinates_chunks = list(chunks(x_coordinates, Rx))
        y_coordinates_chunks = list(chunks(y_coordinates, Ry))
        z_coordinates_chunks = list(chunks(z_coordinates, Rz))

        reblocked_blocks = list(map(self.combine_chunks,
                                    itertools.product(x_coordinates_chunks, y_coordinates_chunks, z_coordinates_chunks),
                                    itertools.repeat(block_id_positions),
                                    itertools.repeat(x_coordinates_chunks),
                                    itertools.repeat(y_coordinates_chunks),
                                    itertools.repeat(z_coordinates_chunks),
                                    itertools.repeat(virtual),
                                    itertools.repeat([Rx, Ry, Rz]),))
        reblocked_blocks = list(filter(None.__ne__, reblocked_blocks))
        self.blocks = reblocked_blocks
