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


class Block:  # Value Object
    def __init__(self, block_id, x, y, z, weight, grades):
        self.id = block_id
        self.x_coordinate = x
        self.y_coordinate = y
        self.z_coordinate = z
        self.weight = weight
        self.grades = grades
