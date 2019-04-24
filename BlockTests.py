import unittest
from Block import *
from BlockModel import *
from MineralDeposit import *
#unit test

class BlockConstructorWithValidArguments(unittest.TestCase):
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

    def test_correct_block_id_assignment(self):
        self.assertEqual(self.block2.id, "0,123,321",
                         "incorrect block id assignment")

    def test_correct_block_x_coordinate_assignment(self):
        self.assertEqual(self.block2.x_coordinate,0,
                         "incorrect block x coordinate assignment")

    def test_correct_block_y_coordinate_assignment(self):
        self.assertEqual(self.block2.y_coordinate,123,
                         "incorrect block y coordinate assignment")

    def test_correct_block_z_coordinate_assignment(self):
        self.assertEqual(self.block2.z_coordinate,321,
                         "incorrect block z coordinate assignment")

class BlockConstructorWithInvalidId(unittest.TestCase):

    def setUp(self):
        self.valid_coordinate = 0
        self.valid_weight = float(0)
        self.valid_grades = {"Au": {"value": float(500), "grade_type": 1}}

    def test_id_assignment_integer(self):
        invalid_id = 0
        with self.assertRaises(TypeError):
            Block(invalid_id,
                                self.valid_coordinate,
                                self.valid_coordinate,
                                self.valid_coordinate,
                                self.valid_weight,
                                self.valid_grades)

    def test_id_assignment_float(self):
        invalid_id = float(0)
        with self.assertRaises(TypeError):
            Block(invalid_id,
                                self.valid_coordinate,
                                self.valid_coordinate,
                                self.valid_coordinate,
                                self.valid_weight,
                                self.valid_grades)

    def test_id_assignment_empty_string(self):
        invalid_id = ""
        with self.assertRaises(ValueError):
            Block(invalid_id,
                                self.valid_coordinate,
                                self.valid_coordinate,
                                self.valid_coordinate,
                                self.valid_weight,
                                self.valid_grades)

    def test_id_assignment_long_empty_string(self):
        invalid_id = "              "
        with self.assertRaises(ValueError):
            Block(invalid_id,
                                self.valid_coordinate,
                                self.valid_coordinate,
                                self.valid_coordinate,
                                self.valid_weight,
                                self.valid_grades)

    def test_id_assignment_list(self):
        invalid_id = [0, 0, 0]
        with self.assertRaises(TypeError):
            Block(invalid_id,
                                self.valid_coordinate,
                                self.valid_coordinate,
                                self.valid_coordinate,
                                self.valid_weight,
                                self.valid_grades)

    def test_id_assignment_dictionary(self):
        invalid_id = {"id": "0,0,0"}
        with self.assertRaises(TypeError):
            Block(invalid_id,
                                self.valid_coordinate,
                                self.valid_coordinate,
                                self.valid_coordinate,
                                self.valid_weight,
                                self.valid_grades)

class BlockConstructorWithInvalidCoordinates(unittest.TestCase):

    def setUp(self):
        self.valid_id = 0
        self.valid_weight = float(0)
        self.valid_grades = {"Au": {"value": float(500), "grade_type": 1}}

    def test_coordinate_assignment_string(self):
        invalid_coordinate = "0"
        with self.assertRaises(TypeError):
            Block(self.valid_id,
                                invalid_coordinate,
                                invalid_coordinate,
                                invalid_coordinate,
                                self.valid_weight,
                                self.valid_grades)

    def test_coordinate_assignment_list(self):
        invalid_coordinate = [0]
        with self.assertRaises(TypeError):
            Block(self.valid_id,
                                invalid_coordinate,
                                invalid_coordinate,
                                invalid_coordinate,
                                self.valid_weight,
                                self.valid_grades)

    def test_coordinate_assignment_dictionary(self):
        invalid_coordinate = {"coordinate": 0}
        with self.assertRaises(TypeError):
            Block(self.valid_id,
                                invalid_coordinate,
                                invalid_coordinate,
                                invalid_coordinate,
                                self.valid_weight,
                                self.valid_grades)

class BlockConstructorWithInvalidWeight(unittest.TestCase):

    def setUp(self):
        self.valid_coordinate = 0
        self.valid_id = "0,0,0"
        self.valid_grades = {"Au": {"value": float(500), "grade_type": 1}}

    def test_weight_assignment_string(self):
        invalid_weight = "0"
        with self.assertRaises(TypeError):
            Block(self.valid_id,
                                self.valid_coordinate,
                                self.valid_coordinate,
                                self.valid_coordinate,
                                invalid_weight,
                                self.valid_grades)

    def test_weight_assignment_list(self):
        invalid_weight = [0]
        with self.assertRaises(TypeError):
            Block(self.valid_id,
                                self.valid_coordinate,
                                self.valid_coordinate,
                                self.valid_coordinate,
                                invalid_weight,
                                self.valid_grades)

    def test_weight_assignment_dictionary(self):
        invalid_weight = {"weight":0}
        with self.assertRaises(TypeError):
            Block(self.valid_id,
                                self.valid_coordinate,
                                self.valid_coordinate,
                                self.valid_coordinate,
                                invalid_weight,
                                self.valid_grades)

    def test_weight_assignment_negative_number(self):
        invalid_weight = -1
        with self.assertRaises(ValueError):
            Block(self.valid_id,
                                self.valid_coordinate,
                                self.valid_coordinate,
                                self.valid_coordinate,
                                invalid_weight,
                                self.valid_grades)

class BlockConstructorWithInvaliGrades(unittest.TestCase):

    def setUp(self):
        self.valid_weight = "0"
        self.valid_coordinate = 0
        self.valid_id = 0

    def test_grades_assignment_string(self):
        invalid_grades = "Au"
        with self.assertRaises(TypeError):
            Block(self.valid_id,
                                self.valid_coordinate,
                                self.valid_coordinate,
                                self.valid_coordinate,
                                self.valid_weight,
                                invalid_grades)

    def test_grades_assignment_int(self):
        invalid_grades = 123
        with self.assertRaises(TypeError):
            Block(self.valid_id,
                                self.valid_coordinate,
                                self.valid_coordinate,
                                self.valid_coordinate,
                                self.valid_weight,
                                invalid_grades)

    def test_grades_assignment_list(self):
        invalid_grades = ["Au"]
        with self.assertRaises(TypeError):
            Block(self.valid_id,
                                self.valid_coordinate,
                                self.valid_coordinate,
                                self.valid_coordinate,
                                self.valid_weight,
                                invalid_grades)

    def test_grades_assignment_empty(self):
        invalid_grades = {}
        with self.assertRaises(TypeError):
            Block(self.valid_id,
                                self.valid_coordinate,
                                self.valid_coordinate,
                                self.valid_coordinate,
                                self.valid_weight,
                                invalid_grades)

    def test_grade_assignment_string(self):
        invalid_grades = {"Au":"bla"}
        with self.assertRaises(TypeError):
            Block(self.valid_id,
                                self.valid_coordinate,
                                self.valid_coordinate,
                                self.valid_coordinate,
                                self.valid_weight,
                                invalid_grades)

    def test_grade_assignment_list(self):
        invalid_grades = {"Au":["bla"]}
        with self.assertRaises(TypeError):
            Block(self.valid_id,
                                self.valid_coordinate,
                                self.valid_coordinate,
                                self.valid_coordinate,
                                self.valid_weight,
                                invalid_grades)

    def test_grade_assignment_without_value_key(self):
        invalid_grades = {"Au":{"grade_type":1}}
        with self.assertRaises(TypeError):
            Block(self.valid_id,
                                self.valid_coordinate,
                                self.valid_coordinate,
                                self.valid_coordinate,
                                self.valid_weight,
                                invalid_grades)

    def test_grade_assignment_without_grade_type_key(self):
        invalid_grades = {"Au":{"value":1}}
        with self.assertRaises(TypeError):
            Block(self.valid_id,
                                self.valid_coordinate,
                                self.valid_coordinate,
                                self.valid_coordinate,
                                self.valid_weight,
                                invalid_grades)

    def test_grade_assignment_with_string_value(self):
        invalid_grades = {"Au":{"value":"1","grade_type":1}}
        with self.assertRaises(TypeError):
            Block(self.valid_id,
                                self.valid_coordinate,
                                self.valid_coordinate,
                                self.valid_coordinate,
                                self.valid_weight,
                                invalid_grades)

    def test_grade_assignment_with_list_value(self):
        invalid_grades = {"Au":{"value":[1],"grade_type":1}}
        with self.assertRaises(TypeError):
            Block(self.valid_id,
                                self.valid_coordinate,
                                self.valid_coordinate,
                                self.valid_coordinate,
                                self.valid_weight,
                                invalid_grades)
    def test_grade_assignment_with_negative_value(self):
        invalid_grades = {"Au":{"value":-1,"grade_type":1}}
        with self.assertRaises(TypeError):
            Block(self.valid_id,
                                self.valid_coordinate,
                                self.valid_coordinate,
                                self.valid_coordinate,
                                self.valid_weight,
                                invalid_grades)

    def test_grade_assignment_with_string_grade_type(self):
        invalid_grades = {"Au":{"value":1,"grade_type":"1"}}
        with self.assertRaises(TypeError):
            Block(self.valid_id,
                                self.valid_coordinate,
                                self.valid_coordinate,
                                self.valid_coordinate,
                                self.valid_weight,
                                invalid_grades)

    def test_grade_assignment_with_negative_grade_type(self):
        invalid_grades = {"Au":{"value":1,"grade_type":-1}}
        with self.assertRaises(TypeError):
            Block(self.valid_id,
                                self.valid_coordinate,
                                self.valid_coordinate,
                                self.valid_coordinate,
                                self.valid_weight,
                                invalid_grades)

    def test_grade_assignment_with_zero_grade_type(self):
        invalid_grades = {"Au":{"value":1,"grade_type":0}}
        with self.assertRaises(TypeError):
            Block(self.valid_id,
                                self.valid_coordinate,
                                self.valid_coordinate,
                                self.valid_coordinate,
                                self.valid_weight,
                                invalid_grades)

if __name__ == '__main__':
    unittest.main()