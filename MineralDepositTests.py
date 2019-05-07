import unittest
from Block import *
from BlockModel import *
from MineralDeposit import *
#unit test
class MineralDepositConstructorWithValidArguments(unittest.TestCase):
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

class MineralDepositConstructorWithInvalidName(unittest.TestCase):

    def setUp(self):
        self.valid_column_coordinate = 0
        self.valid_weight = float(0)
        self.valid_grades = {"Au": {"mineral_column": 4, "grade_type": 1}}

    def test_name_assignment_integer(self):
        invalid_name = 0
        with self.assertRaises(TypeError):
            MineralDeposit(invalid_name,
                                self.valid_column_coordinate,
                                self.valid_column_coordinate,
                                self.valid_column_coordinate,
                                self.valid_weight,
                                self.valid_grades)

    def test_name_assignment_float(self):
        invalid_name = float(0)
        with self.assertRaises(TypeError):
            MineralDeposit(invalid_name,
                                self.valid_column_coordinate,
                                self.valid_column_coordinate,
                                self.valid_column_coordinate,
                                self.valid_weight,
                                self.valid_grades)

    def test_name_assignment_empty_string(self):
        invalid_name = ""
        with self.assertRaises(ValueError):
            MineralDeposit(invalid_name,
                                self.valid_column_coordinate,
                                self.valid_column_coordinate,
                                self.valid_column_coordinate,
                                self.valid_weight,
                                self.valid_grades)

    def test_name_assignment_long_empty_string(self):
        invalid_name = "              "
        with self.assertRaises(ValueError):
            MineralDeposit(invalid_name,
                                self.valid_column_coordinate,
                                self.valid_column_coordinate,
                                self.valid_column_coordinate,
                                self.valid_weight,
                                self.valid_grades)

    def test_name_assignment_list(self):
        invalid_name = ["name1","name2"]
        with self.assertRaises(TypeError):
            MineralDeposit(invalid_name,
                                self.valid_column_coordinate,
                                self.valid_column_coordinate,
                                self.valid_column_coordinate,
                                self.valid_weight,
                                self.valid_grades)

    def test_name_assignment_dictionary(self):
        invalid_name = {"name": "bla"}
        with self.assertRaises(TypeError):
            MineralDeposit(invalid_name,
                                self.valid_column_coordinate,
                                self.valid_column_coordinate,
                                self.valid_column_coordinate,
                                self.valid_weight,
                                self.valid_grades)

class MineralDepositConstructorWithInvalidColumnCoordinates(unittest.TestCase):

    def setUp(self):
        self.valid_name = "testMineralDeposit"
        self.valid_weight = float(0)
        self.valid_grades = {"Au": {"mineral_column": 4, "grade_type": 1}}

    def test_column_coordinate_assignment_string(self):
        invalid_column_coordinate = "0"
        with self.assertRaises(TypeError):
            MineralDeposit(self.valid_name,
                                invalid_column_coordinate,
                                invalid_column_coordinate,
                                invalid_column_coordinate,
                                self.valid_weight,
                                self.valid_grades)

    def test_column_coordinate_assignment_negative(self):
        invalid_column_coordinate = -1
        with self.assertRaises(ValueError):
            MineralDeposit(self.valid_name,
                                invalid_column_coordinate,
                                invalid_column_coordinate,
                                invalid_column_coordinate,
                                self.valid_weight,
                                self.valid_grades)

    def test_column_coordinate_assignment_float(self):
        invalid_column_coordinate = float(0)
        with self.assertRaises(TypeError):
            MineralDeposit(self.valid_name,
                                invalid_column_coordinate,
                                invalid_column_coordinate,
                                invalid_column_coordinate,
                                self.valid_weight,
                                self.valid_grades)

    def test_column_coordinate_assignment_list(self):
        invalid_column_coordinate = [0]
        with self.assertRaises(TypeError):
            MineralDeposit(self.valid_name,
                                invalid_column_coordinate,
                                invalid_column_coordinate,
                                invalid_column_coordinate,
                                self.valid_weight,
                                self.valid_grades)

    def test_column_coordinate_assignment_dictionary(self):
        invalid_column_coordinate = {"coordinate": 0}
        with self.assertRaises(TypeError):
            MineralDeposit(self.valid_name,
                                invalid_column_coordinate,
                                invalid_column_coordinate,
                                invalid_column_coordinate,
                                self.valid_weight,
                                self.valid_grades)

class MineralDepositConstructorWithInvalidWeight(unittest.TestCase):

    def setUp(self):
        self.valid_name = "testMineralDeposit"
        self.valid_column_coordinate = 0
        self.valid_grades = {"Au": {"mineral_column": 4, "grade_type": 1}}

    def test_weight_assignment_string(self):
        invalid_weight = "0"
        with self.assertRaises(TypeError):
            MineralDeposit(self.valid_name,
                                self.valid_column_coordinate,
                                self.valid_column_coordinate,
                                self.valid_column_coordinate,
                                invalid_weight,
                                self.valid_grades)

    def test_weight_assignment_list(self):
        invalid_weight = [0]
        with self.assertRaises(TypeError):
            MineralDeposit(self.valid_name,
                                self.valid_column_coordinate,
                                self.valid_column_coordinate,
                                self.valid_column_coordinate,
                                invalid_weight,
                                self.valid_grades)

    def test_weight_assignment_dictionary(self):
        invalid_weight = {"weight":0}
        with self.assertRaises(TypeError):
            MineralDeposit(self.valid_name,
                                self.valid_column_coordinate,
                                self.valid_column_coordinate,
                                self.valid_column_coordinate,
                                invalid_weight,
                                self.valid_grades)

    def test_weight_assignment_negative_number(self):
        invalid_weight = -1
        with self.assertRaises(ValueError):
            MineralDeposit(self.valid_name,
                                self.valid_column_coordinate,
                                self.valid_column_coordinate,
                                self.valid_column_coordinate,
                                invalid_weight,
                                self.valid_grades)

class MineralDepositConstructorWithInvaliGrades(unittest.TestCase):

    def setUp(self):
        self.valid_name = "testMineralDeposit"
        self.valid_column_coordinate = 0
        self.valid_weight = float(0)

    def test_grades_assignment_string(self):
        invalid_grades = "Au"
        with self.assertRaises(TypeError):
            MineralDeposit(self.valid_name,
                                self.valid_column_coordinate,
                                self.valid_column_coordinate,
                                self.valid_column_coordinate,
                                self.valid_weight,
                                invalid_grades)

    def test_grades_assignment_int(self):
        invalid_grades = 123
        with self.assertRaises(TypeError):
            MineralDeposit(self.valid_name,
                                self.valid_column_coordinate,
                                self.valid_column_coordinate,
                                self.valid_column_coordinate,
                                self.valid_weight,
                                invalid_grades)

    def test_grades_assignment_list(self):
        invalid_grades = ["Au"]
        with self.assertRaises(TypeError):
            MineralDeposit(self.valid_name,
                                self.valid_column_coordinate,
                                self.valid_column_coordinate,
                                self.valid_column_coordinate,
                                self.valid_weight,
                                invalid_grades)

    def test_grades_assignment_empty(self):
        invalid_grades = {}
        with self.assertRaises(TypeError):
            MineralDeposit(self.valid_name,
                                self.valid_column_coordinate,
                                self.valid_column_coordinate,
                                self.valid_column_coordinate,
                                self.valid_weight,
                                invalid_grades)

    def test_grade_assignment_string(self):
        invalid_grades = {"Au":"bla"}
        with self.assertRaises(TypeError):
            MineralDeposit(self.valid_name,
                                self.valid_column_coordinate,
                                self.valid_column_coordinate,
                                self.valid_column_coordinate,
                                self.valid_weight,
                                invalid_grades)

    def test_grade_assignment_list(self):
        invalid_grades = {"Au":["bla"]}
        with self.assertRaises(TypeError):
            MineralDeposit(self.valid_name,
                                self.valid_column_coordinate,
                                self.valid_column_coordinate,
                                self.valid_column_coordinate,
                                self.valid_weight,
                                invalid_grades)

    def test_grade_assignment_without_mineral_column_key(self):
        invalid_grades = {"Au":{"grade_type":1}}
        with self.assertRaises(TypeError):
            MineralDeposit(self.valid_name,
                                self.valid_column_coordinate,
                                self.valid_column_coordinate,
                                self.valid_column_coordinate,
                                self.valid_weight,
                                invalid_grades)

    def test_grade_assignment_without_grade_type_key(self):
        invalid_grades = {"Au":{"mineral_column":1}}
        with self.assertRaises(TypeError):
            MineralDeposit(self.valid_name,
                                self.valid_column_coordinate,
                                self.valid_column_coordinate,
                                self.valid_column_coordinate,
                                self.valid_weight,
                                invalid_grades)

    def test_grade_assignment_with_string_mineral_column(self):
        invalid_grades = {"Au":{"mineral_column":"1","grade_type":1}}
        with self.assertRaises(TypeError):
            MineralDeposit(self.valid_name,
                                self.valid_column_coordinate,
                                self.valid_column_coordinate,
                                self.valid_column_coordinate,
                                self.valid_weight,
                                invalid_grades)

    def test_grade_assignment_with_list_mineral_column(self):
        invalid_grades = {"Au":{"mineral_column":[1],"grade_type":1}}
        with self.assertRaises(TypeError):
            MineralDeposit(self.valid_name,
                                self.valid_column_coordinate,
                                self.valid_column_coordinate,
                                self.valid_column_coordinate,
                                self.valid_weight,
                                invalid_grades)

    def test_grade_assignment_with_negative_mineral_column(self):
        invalid_grades = {"Au":{"mineral_column":-1,"grade_type":1}}
        with self.assertRaises(TypeError):
            MineralDeposit(self.valid_name,
                                self.valid_column_coordinate,
                                self.valid_column_coordinate,
                                self.valid_column_coordinate,
                                self.valid_weight,
                                invalid_grades)

    def test_grade_assignment_with_string_grade_type(self):
        invalid_grades = {"Au":{"mineral_column":1,"grade_type":"1"}}
        with self.assertRaises(TypeError):
            MineralDeposit(self.valid_name,
                                self.valid_column_coordinate,
                                self.valid_column_coordinate,
                                self.valid_column_coordinate,
                                self.valid_weight,
                                invalid_grades)

    def test_grade_assignment_with_negative_grade_type(self):
        invalid_grades = {"Au":{"mineral_column":1,"grade_type":-1}}
        with self.assertRaises(TypeError):
            MineralDeposit(self.valid_name,
                                self.valid_column_coordinate,
                                self.valid_column_coordinate,
                                self.valid_column_coordinate,
                                self.valid_weight,
                                invalid_grades)

    def test_grade_assignment_with_zero_grade_type(self):
        invalid_grades = {"Au":{"mineral_column":1,"grade_type":0}}
        with self.assertRaises(TypeError):
            MineralDeposit(self.valid_name,
                                self.valid_column_coordinate,
                                self.valid_column_coordinate,
                                self.valid_column_coordinate,
                                self.valid_weight,
                                invalid_grades)

if __name__ == '__main__':
    unittest.main()