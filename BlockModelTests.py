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


class BlockModelReblockWithValidArguments(unittest.TestCase):
    def setUp(self):
        self.block1 = Block("0,0,0"
                            , 0
                            , 0
                            , 0
                            , float(1000)
                            , {"Au": {"value": float(100), "grade_type": 1}
                                , "Cu": {"value": float(100), "grade_type": 2}
                                , "Ag": {"value": float(100), "grade_type": 3}
                                , "Li": {"value": float(100), "grade_type": 4}}
                            )
        self.block2 = Block("0,123,321"
                            , 0
                            , 123
                            , 321
                            , float(1000)
                            , {"Au": {"value": float(100), "grade_type": 1}
                                , "Cu": {"value": float(100), "grade_type": 2}
                                , "Ag": {"value": float(100), "grade_type": 3}
                                , "Li": {"value": float(100), "grade_type": 4}
                               }
                            )

        self.block3 = Block("0,0,2"
                            , 0
                            , 0
                            , 2
                            , float(1000)
                            , {"Au": {"value": float(100), "grade_type": 1}
                                , "Cu": {"value": float(100), "grade_type": 2}
                                , "Ag": {"value": float(100), "grade_type": 3}
                                , "Li": {"value": float(100), "grade_type": 4}
                               }
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

        self.newCoordinates = (0,0,0)

        x, y, z = self.newCoordinates[0], self.newCoordinates[1], self.newCoordinates[2]
        newId = str(x) + "," + str(y) + "," + str(z)
        newWeight = 3000
        newGrades = {"Au": {"value": float(300), "grade_type": 1}
                        , "Cu": {"value": float(100), "grade_type": 2}
                        , "Ag": {"value": float(100), "grade_type": 3}
                        , "Li": {"value": float(100), "grade_type": 4}
                     }
        self.correctCombinedBlock = Block(newId
                            , x
                            , y
                            , z
                            , newWeight
                            , newGrades
                            )

    def test_block_model_get_border_limits_function_exists(self):
        self.blockModel.get_border_limits()

    def test_correct_block_model_get_border_limits(self):
        self.assertEqual(self.blockModel.get_border_limits(), [0, 123, 321],
                         "incorrect block model border limits")

    def test_combine_blocks_function_exists(self):
        self.blockModel.combine_blocks(self.blocks, self.newCoordinates)

    def test_correct_combine_blocks(self):
        combinedblock = self.blockModel.combine_blocks(self.blocks, self.newCoordinates)
        self.assertEqual(self.correctCombinedBlock.id,combinedblock.id,
                         "Incorrect new id in combined block.")
        self.assertEqual(self.correctCombinedBlock.x_coordinate, combinedblock.x_coordinate,
                         "Incorrect new x coordinate in combined block.")
        self.assertEqual(self.correctCombinedBlock.y_coordinate, combinedblock.y_coordinate,
                         "Incorrect new y coordinate in combined block.")
        self.assertEqual(self.correctCombinedBlock.z_coordinate, combinedblock.z_coordinate,
                         "Incorrect new z coordinate in combined block.")
        self.assertEqual(self.correctCombinedBlock.weight, combinedblock.weight,
                         "Incorrect new weight in combined block.")
        for grade in self.correctCombinedBlock.grades.keys():
            self.assertTrue(grade in combinedblock.grades.keys(),
                            "Incorrect preservation of minerals in new block")
            self.assertEqual(self.correctCombinedBlock.grades[grade]["value"],
                             combinedblock.grades[grade]["value"],
                             "Incorrect new grade value.")
            self.assertEqual(self.correctCombinedBlock.grades[grade]["grade_type"],
                             combinedblock.grades[grade]["grade_type"],
                             "Incorrect new grade type.")

    def test_block_model_reblock_model_function_exists(self):
        self.blockModel.reblock_model(3, 3, 3)

    def test_block_model_reblock_model_correct_block_quantity(self):
        self.blockModel.reblock_model(3, 3, 3)
        self.assertEqual(len(self.blockModel.blocks), 2,
                         "Incorrect reblocked model block count.")

    def test_block_model_reblock_model_correct_total_weight(self):
        total_weight_before_reblock = self.blockModel.total_weight()
        self.blockModel.reblock_model(2, 2, 2)
        total_weight_after_reblock = self.blockModel.total_weight()
        self.assertEqual(total_weight_after_reblock, total_weight_before_reblock,
                         "Incorrect total weight after reblock.")

    def test_block_model_reblock_model_correct_mineral_total_weight(self):
        mineral_total_weight_before_reblock = self.blockModel.total_mineral_weight()
        self.blockModel.reblock_model(2, 2, 2)
        mineral_total_weight_after_reblock = self.blockModel.total_mineral_weight()
        self.assertAlmostEqual(mineral_total_weight_after_reblock, mineral_total_weight_before_reblock,
                               "Incorrect mineral total weight after reblock.")

    def test_block_model_reblock_model_correct_new_border_limits(self):
        self.blockModel.reblock_model(2, 2, 2)
        new_border_limits = self.blockModel.get_border_limits()
        self.assertEqual(new_border_limits, [0, 61, 160],
                         "Incorrect border limits after reblock.")


class BlockModelReblockWithInvalidArguments(unittest.TestCase):
    def setUp(self):
        self.block1 = Block("0,0,0"
                            , 0
                            , 0
                            , 0
                            , float(1000)
                            , {"Au": {"value": float(100), "grade_type": 1}
                                , "Cu": {"value": float(100), "grade_type": 2}
                                , "Ag": {"value": float(100), "grade_type": 3}
                                , "Li": {"value": float(100), "grade_type": 4}}
                            )
        self.block2 = Block("0,123,321"
                            , 0
                            , 123
                            , 321
                            , float(1000)
                            , {"Au": {"value": float(100), "grade_type": 1}
                                , "Cu": {"value": float(100), "grade_type": 2}
                                , "Ag": {"value": float(100), "grade_type": 3}
                                , "Li": {"value": float(100), "grade_type": 4}
                               }
                            )

        self.block3 = Block("0,0,2"
                            , 0
                            , 0
                            , 2
                            , float(1000)
                            , {"Au": {"value": float(100), "grade_type": 1}
                                , "Cu": {"value": float(100), "grade_type": 2}
                                , "Ag": {"value": float(100), "grade_type": 3}
                                , "Li": {"value": float(100), "grade_type": 4}
                               }
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

        self.newCoordinates = (0,0,0)

        x, y, z = self.newCoordinates[0], self.newCoordinates[1], self.newCoordinates[2]
        newId = str(x) + "," + str(y) + "," + str(z)
        newWeight = 3000
        newGrades = {"Au": {"value": float(300), "grade_type": 1}
                        , "Cu": {"value": float(100), "grade_type": 2}
                        , "Ag": {"value": float(100), "grade_type": 3}
                        , "Li": {"value": float(100), "grade_type": 4}
                     }
        self.correctCombinedBlock = Block(newId
                            , x
                            , y
                            , z
                            , newWeight
                            , newGrades
                            )

    def test_block_model_reblock_model_invalid_types(self):
        with self.assertRaises(TypeError):
            self.blockModel.reblock_model("A", {}, self.blocks)

    def test_block_model_reblock_model_invalid_values(self):
        with self.assertRaises(ValueError):
            self.blockModel.reblock_model(-1, 1, 1)

class BlockModelReblockWithDimensionsThatAreNotDivisibleByReblockFactors(unittest.TestCase):
    def setUp(self):
        self.block1 = Block("0,0,0"
                            , 0
                            , 0
                            , 0
                            , float(1000)
                            , {"Au": {"value": float(100), "grade_type": 1}
                                , "Cu": {"value": float(100), "grade_type": 2}
                                , "Ag": {"value": float(100), "grade_type": 3}
                                , "Li": {"value": float(100), "grade_type": 4}}
                            )
        self.block2 = Block("8,2,4"
                            , 8
                            , 2
                            , 4
                            , float(1000)
                            , {"Au": {"value": float(100), "grade_type": 1}
                                , "Cu": {"value": float(100), "grade_type": 2}
                                , "Ag": {"value": float(100), "grade_type": 3}
                                , "Li": {"value": float(100), "grade_type": 4}
                               }
                            )

        self.block3 = Block("6,4,2"
                            , 6
                            , 4
                            , 2
                            , float(1000)
                            , {"Au": {"value": float(100), "grade_type": 1}
                                , "Cu": {"value": float(100), "grade_type": 2}
                                , "Ag": {"value": float(100), "grade_type": 3}
                                , "Li": {"value": float(100), "grade_type": 4}
                               }
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

        self.newCoordinates = (0,0,0)

        x, y, z = self.newCoordinates[0], self.newCoordinates[1], self.newCoordinates[2]
        newId = str(x) + "," + str(y) + "," + str(z)
        newWeight = 3000
        newGrades = {"Au": {"value": float(300), "grade_type": 1}
                        , "Cu": {"value": float(100), "grade_type": 2}
                        , "Ag": {"value": float(100), "grade_type": 3}
                        , "Li": {"value": float(100), "grade_type": 4}
                     }
        self.correctCombinedBlock = Block(newId
                            , x
                            , y
                            , z
                            , newWeight
                            , newGrades
                            )

    def test_block_model_reblock_model_by_zero_at_x_coordinate(self):
        with self.assertRaises(ValueError):
            self.blockModel.reblock_model(0, 1, 1)

    def test_block_model_reblock_model_by_zero_at_y_coordinate(self):
        with self.assertRaises(ValueError):
            self.blockModel.reblock_model(1, 0, 1)

    def test_block_model_reblock_model_by_zero_at_z_coordinate(self):
        with self.assertRaises(ValueError):
            self.blockModel.reblock_model(1, 1, 0)

    def test_block_model_reblock_model_by_zero_at_all_coordinates(self):
        with self.assertRaises(ValueError):
            self.blockModel.reblock_model(0, 0, 0)

    def test_block_model_reblock_model_not_divisible_at_x_coordinate(self):
        old_block_quantity = self.blockModel.count_blocks()
        self.blockModel.reblock_model(3, 2, 2)
        new_block_quantity = self.blockModel.count_blocks()
        self.assertTrue(old_block_quantity >= new_block_quantity,
                        "is not being filled correctly with air blocks when it is not divisible at x coordinate")

    def test_block_model_reblock_model_not_divisible_at_y_coordinate(self):
        old_block_quantity = self.blockModel.count_blocks()
        self.blockModel.reblock_model(2, 3, 2)
        new_block_quantity = self.blockModel.count_blocks()
        self.assertTrue(old_block_quantity >= new_block_quantity,
                        "is not being filled correctly with air blocks when it is not divisible at y coordinate")

    def test_block_model_reblock_model_not_divisible_at_z_coordinate(self):
        old_block_quantity = self.blockModel.count_blocks()
        self.blockModel.reblock_model(2, 2, 3)
        new_block_quantity = self.blockModel.count_blocks()
        self.assertTrue(old_block_quantity >= new_block_quantity,
                        "is not being filled correctly with air blocks when it is not divisible at z coordinate")

    def test_block_model_reblock_model_not_divisible_at_all_coordinates(self):
        old_block_quantity = self.blockModel.count_blocks()
        self.blockModel.reblock_model(3, 3, 3)
        new_block_quantity = self.blockModel.count_blocks()
        self.assertTrue(old_block_quantity >= new_block_quantity,
                        "is not being filled correctly with air blocks when it is not divisible at all coordinates")

if __name__ == '__main__':
    unittest.main()