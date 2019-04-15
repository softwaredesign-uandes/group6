import unittest
import DomainObjects
#unit test
class TestHappyPathDomainLogic(unittest.TestCase):
    def setUp(self):
        self.block1 = DomainObjects.Block("0,0,0"
                                          , 0
                                          , 0
                                          , 0
                                          , float(1000),
                                          {"Au": {"value": float(500), "grade_type": 1}}

                                          )
        self.block2 = DomainObjects.Block("0.0,123.321,321.123"
                                          , 0.0
                                          , 123.321
                                          , 321.123
                                          , float(1000),
                                          {"Au": {"value": float(500), "grade_type": 1}}
                                          )

        self.block3 = DomainObjects.Block("0,0,2"
                                          , 0
                                          , 0
                                          , 2
                                          , float(1000),
                                          {"Au": {"value": float(500), "grade_type": 1}}
                                          )

        self.blocks = [self.block1,
                       self.block2,
                       self.block3]

        self.mineralDeposit = DomainObjects.MineralDeposit("testMineralDeposit",
                                                           0,
                                                           1,
                                                           2,
                                                           3,
                                                           {"Au":{"mineral_column": 4,"grade_type": 1}}
                                                           )

        self.blockModel = DomainObjects.BlockModel("testBlockModel", self.blocks, self.mineralDeposit.name)

    def test_correct_block_id_assignment(self):
        self.assertEqual(self.block2.id, "0.0,123.321,321.123",
                         "incorrect block id assignment")

    def test_correct_block_x_coordinate_assignment(self):
        self.assertEqual(self.block2.x_coordinate,0.0,
                         "incorrect block x coordinate assignment")

    def test_correct_block_y_coordinate_assignment(self):
        self.assertEqual(self.block2.y_coordinate,123.321,
                         "incorrect block y coordinate assignment")

    def test_correct_block_z_coordinate_assignment(self):
        self.assertEqual(self.block2.z_coordinate,321.123,
                         "incorrect block z coordinate assignment")

    def test_correct_mineral_deposit_name_assignment(self):
        self.assertEqual(self.mineralDeposit.name,"testMineralDeposit",
                         "incorrect mineral deposit name assignment")

    def test_correct_mineral_deposit_x_coordinate_column_assignment(self):
        self.assertEqual(self.mineralDeposit.x_coordinate_column,0,
                         "incorrect mineral deposit x coordinate column assignment")

    def test_correct_mineral_deposit_y_coordinate_column_assignment(self):
        self.assertEqual(self.mineralDeposit.y_coordinate_column,1,
                         "incorrect mineral deposit y coordinate column assignment")

    def test_correct_mineral_deposit_z_coordinate_column_assignment(self):
        self.assertEqual(self.mineralDeposit.z_coordinate_column,2,
                         "incorrect mineral deposit z coordinate column assignment")

    def test_correct_mineral_deposit_weight_column_assignment(self):
        self.assertEqual(self.mineralDeposit.weight_column,3,
                         "incorrect mineral deposit weight column assignment")

    def test_correct_mineral_deposit_grades_assignment(self):
        self.assertEqual(self.mineralDeposit.grades,{"Au":{"mineral_column": 4,"grade_type": 1}},
                         "incorrect mineral deposit grades assignment")

    def test_correct_block_model_name_assignment(self):
        self.assertEqual(self.blockModel.name,"testBlockModel",
                         "incorrect block model name assignment")

    def test_correct_block_model_blocks_assignment(self):
        self.assertEqual(self.blockModel.blocks,self.blocks,
                         "incorrect block model blocks assignment")

    def test_correct_block_model_mineral_deposit_assignment(self):
        self.assertEqual(self.blockModel.mineral_deposit,"testMineralDeposit",
                         "incorrect block model mineral deposit assignment")

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

class TestSadPathDomainLogic(unittest.TestCase):
    def setUp(self):
        self.block1 = DomainObjects.Block("0,0,0"
                                          , 0
                                          , 0
                                          , 0
                                          , float(1000),
                                          {"Au": {"value": float(500), "grade_type": 1}}

                                          )
        self.block2 = DomainObjects.Block(123
                                          , 0.0
                                          , 123.321
                                          , 321.123
                                          , float(1000),
                                          {"Au": {"value": float(500), "grade_type": 1}}
                                          )

        self.block3 = DomainObjects.Block("0,0,2"
                                          , 0
                                          , 0
                                          , 2
                                          , float(1000),
                                          {"Au": {"value": float(500), "grade_type": 1}}
                                          )

        self.blocks = ["block0",
                       self.block1,
                       self.block2,
                       self.block3,
                       ]

        self.mineralDeposit = DomainObjects.MineralDeposit(9999,
                                                           0,
                                                           1,
                                                           2,
                                                           3,
                                                           {"Au":{"mineral_column": 4,"grade_type": 1}}
                                                           )

        self.blockModel = DomainObjects.BlockModel("testBlockModel", self.blocks, self.mineralDeposit.name)

    @unittest.expectedFailure
    def test_correct_block_id_assignment(self):
        for block in self.blocks:
            self.assertEqual(block.id,
                             str(block.x_coordinate)+","+str(block.y_coordinate)+","+str(block.z_coordinate),
                             "incorrect block id assignment")

    @unittest.expectedFailure
    def test_incorrect_block_model_count_blocks(self):
        self.assertEqual(self.blockModel.count_blocks(),3,
                         "incorrect block model count blocks")

    @unittest.expectedFailure
    def test_correct_block_model_total_weight(self):
        self.assertEqual(self.blockModel.total_weight(),float(3000),
                         "incorrect block model total weight")

    @unittest.expectedFailure
    def test_correct_block_model_total_mineral_weight(self):
        self.assertEqual(self.blockModel.total_mineral_weight(),{"Au":float(1500)},
                         "incorrect block model total mineral weight")

    @unittest.expectedFailure
    def test_correct_block_model_air_blocks_percentage(self):
        self.assertEqual(self.blockModel.air_blocks_percentage(),0,
                         "incorrect block model air block percentage")

    @unittest.expectedFailure
    def test_correct_block_model_get_block_model_structure(self):
        self.assertEqual(self.blockModel.get_block_model_structure(),{"Au":1})


if __name__ == '__main__':
    unittest.main()