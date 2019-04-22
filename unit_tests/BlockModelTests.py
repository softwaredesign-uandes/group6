import unittest
from Block import *
from BlockModel import *
from MineralDeposit import *
#unit test
class BlockModelConstructorWithValidArguments(unittest.TestCase):
    def setUp(self):
        self.block1 = Block("0,0,0"
                                          , 0
                                          , 0
                                          , 0
                                          , float(1000),
                                          {"Au": {"value": float(500), "grade_type": 1}}

                                          )
        self.block2 = Block("0,123,321"
                                          , 0
                                          , 123
                                          , 321
                                          , float(1000),
                                          {"Au": {"value": float(500), "grade_type": 1}}
                                          )

        self.block3 = Block("0,0,2"
                                          , 0
                                          , 0
                                          , 2
                                          , float(1000),
                                          {"Au": {"value": float(500), "grade_type": 1}}
                                          )

        self.blocks = [self.block1,
                       self.block2,
                       self.block3]

        self.mineralDeposit = MineralDeposit("testMineralDeposit",
                                                           0,
                                                           1,
                                                           2,
                                                           3,
                                                           {"Au":{"mineral_column": 4,"grade_type": 1}}
                                                           )

        self.blockModel = BlockModel("testBlockModel", self.blocks, self.mineralDeposit.name)

    def test_correct_block_model_name_assignment(self):
        self.assertEqual(self.blockModel.name,"testBlockModel",
                         "incorrect block model name assignment")

    def test_correct_block_model_blocks_assignment(self):
        self.assertEqual(self.blockModel.blocks,self.blocks,
                         "incorrect block model blocks assignment")

    def test_correct_block_model_mineral_deposit_assignment(self):
        self.assertEqual(self.blockModel.mineral_deposit,"testMineralDeposit",
                         "incorrect block model mineral deposit assignment")

class BlockModelConstructorWithInvalidName(unittest.TestCase):

    def setUp(self):
        self.valid_block = Block("0,0,0"
                                          , 0
                                          , 0
                                          , 0
                                          , float(1000),
                                          {"Au": {"value": float(500), "grade_type": 1}}
                                               )

        self.valid_blocks = [self.valid_block,self.valid_block,self.valid_block]

        self.valid_mineral_deposit = MineralDeposit("testMineralDeposit",
                                                           0,
                                                           1,
                                                           2,
                                                           3,
                                                           {"Au":{"mineral_column": 4,"grade_type": 1}}
                                                           )

    def test_name_assignment_integer(self):
        invalid_name = 0
        with self.assertRaises(TypeError):
            BlockModel(invalid_name,self.valid_blocks,self.valid_mineral_deposit)

    def test_name_assignment_float(self):
        invalid_name = float(0)
        with self.assertRaises(TypeError):
            BlockModel(invalid_name,self.valid_blocks,self.valid_mineral_deposit)

    def test_name_assignment_list(self):
        invalid_name = ["name"]
        with self.assertRaises(TypeError):
            BlockModel(invalid_name,self.valid_blocks,self.valid_mineral_deposit)

    def test_name_assignment_dict(self):
        invalid_name = {"name": "value"}
        with self.assertRaises(TypeError):
            BlockModel(invalid_name,self.valid_blocks,self.valid_mineral_deposit)

    def test_name_assignment_empty_string(self):
        invalid_name = ""
        with self.assertRaises(ValueError):
            BlockModel(invalid_name,self.valid_blocks,self.valid_mineral_deposit)

    def test_name_assignment_long_empty_string(self):
        invalid_name = "             "
        with self.assertRaises(ValueError):
            BlockModel(invalid_name,self.valid_blocks,self.valid_mineral_deposit)

class BlockModelConstructorWithInvalidBlocks(unittest.TestCase):

    def setUp(self):
        self.valid_name = "block model valid name"

        self.valid_mineral_deposit = MineralDeposit("testMineralDeposit",
                                                           0,
                                                           1,
                                                           2,
                                                           3,
                                                           {"Au":{"mineral_column": 4,"grade_type": 1}}
                                                           )

    def test_blocks_assignment_integer(self):
        invalid_blocks = 0
        with self.assertRaises(TypeError):
            BlockModel(self.valid_name,invalid_blocks,self.valid_mineral_deposit)

    def test_blocks_assignment_float(self):
        invalid_blocks = float(0)
        with self.assertRaises(TypeError):
            BlockModel(self.valid_name,invalid_blocks,self.valid_mineral_deposit)

    def test_blocks_assignment_list_of_strings(self):
        invalid_blocks = ["name"]
        with self.assertRaises(TypeError):
            BlockModel(self.valid_name,invalid_blocks,self.valid_mineral_deposit)

    def test_blocks_assignment_dict(self):
        invalid_blocks = {"name": "value"}
        with self.assertRaises(TypeError):
            BlockModel(self.valid_name,invalid_blocks,self.valid_mineral_deposit)

    def test_blocks_assignment_empty_list(self):
        invalid_blocks = []
        with self.assertRaises(ValueError):
            BlockModel(self.valid_name,invalid_blocks,self.valid_mineral_deposit)

    def test_blocks_assignment_string_blocks(self):
        invalid_blocks = ["block1", "block2"]
        with self.assertRaises(TypeError):
            BlockModel(self.valid_name,invalid_blocks,self.valid_mineral_deposit)

    def test_blocks_assignment_int_blocks(self):
        invalid_blocks = [1, 2]
        with self.assertRaises(TypeError):
            BlockModel(self.valid_name,invalid_blocks,self.valid_mineral_deposit)

    def test_blocks_assignment_float_blocks(self):
        invalid_blocks = [float(1), float(2)]
        with self.assertRaises(TypeError):
            BlockModel(self.valid_name,invalid_blocks,self.valid_mineral_deposit)

class BlockModelConstructorWithInvalidMineralDeposit(unittest.TestCase):

    def setUp(self):

        self. valid_name = "block model valid name"

        self.valid_block = Block("0,0,0"
                                          , 0
                                          , 0
                                          , 0
                                          , float(1000),
                                          {"Au": {"value": float(500), "grade_type": 1}}
                                               )

        self.valid_blocks = [self.valid_block,self.valid_block,self.valid_block]

        self.valid_mineral_deposit = MineralDeposit("testMineralDeposit",
                                                           0,
                                                           1,
                                                           2,
                                                           3,
                                                           {"Au":{"mineral_column": 4,"grade_type": 1}}
                                                           )

    def test_Mineral_deposit_assignment_integer(self):
        invalid_mineral_deposit = 0
        with self.assertRaises(TypeError):
            BlockModel(self.valid_name,self.valid_blocks,invalid_mineral_deposit)

    def test_Mineral_deposit_assignment_float(self):
        invalid_mineral_deposit = float(0)
        with self.assertRaises(TypeError):
            BlockModel(self.valid_name,self.valid_blocks,invalid_mineral_deposit)

    def test_Mineral_deposit_assignment_list(self):
        invalid_mineral_deposit = ["name"]
        with self.assertRaises(TypeError):
            BlockModel(self.valid_name,self.valid_blocks,invalid_mineral_deposit)

    def test_Mineral_deposit_assignment_dict(self):
        invalid_mineral_deposit = {"name": "value"}
        with self.assertRaises(TypeError):
            BlockModel(self.valid_name,self.valid_blocks,invalid_mineral_deposit)

    def test_Mineral_deposit_assignment_empty_string(self):
        invalid_mineral_deposit = ""
        with self.assertRaises(ValueError):
            BlockModel(self.valid_name,self.valid_blocks,invalid_mineral_deposit)

    def test_Mineral_deposit_assignment_long_empty_string(self):
        invalid_mineral_deposit = "             "
        with self.assertRaises(ValueError):
            BlockModel(self.valid_name,self.valid_blocks,invalid_mineral_deposit)

class BlockModelStatistics(unittest.TestCase):
    def setUp(self):
        self.block1 = Block("0,0,0"
                                          , 0
                                          , 0
                                          , 0
                                          , float(1000),
                                          {"Au": {"value": float(500), "grade_type": 1}}

                                          )
        self.block2 = Block("0,123,321"
                                          , 0
                                          , 123
                                          , 321
                                          , float(1000),
                                          {"Au": {"value": float(500), "grade_type": 1}}
                                          )

        self.block3 = Block("0,0,2"
                                          , 0
                                          , 0
                                          , 2
                                          , float(1000),
                                          {"Au": {"value": float(500), "grade_type": 1}}
                                          )

        self.blocks = [self.block1,
                       self.block2,
                       self.block3]

        self.mineralDeposit = MineralDeposit("testMineralDeposit",
                                                           0,
                                                           1,
                                                           2,
                                                           3,
                                                           {"Au":{"mineral_column": 4,"grade_type": 1}}
                                                           )

        self.blockModel = BlockModel("testBlockModel", self.blocks, self.mineralDeposit.name)

    def test_correct_block_model_count_blocks(self):
        self.assertEqual(self.blockModel.count_blocks(),3,
                         "incorrect block model count blocks")

    def test_correct_block_model_total_weight(self):
        self.assertEqual(self.blockModel.total_weight(),float(3000),
                         "incorrect block model total weight")

    def test_correct_block_model_total_mineral_weight(self):
        self.assertEqual(self.blockModel.total_mineral_weight(),{"Au":float(1500)},
                         "incorrect block model total mineral weight")

    def test_correct_block_model_air_blocks_percentage(self):
        self.assertEqual(self.blockModel.air_blocks_percentage(),0,
                         "incorrect block model air block percentage")

    def test_correct_block_model_get_block_model_structure(self):
        self.assertEqual(self.blockModel.get_block_model_structure(),{"Au":1})

if __name__ == '__main__':
    unittest.main()