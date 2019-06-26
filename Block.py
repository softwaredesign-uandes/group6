from AbstractBlock import *

class Block(AbstractBlock):  # Value Object
    def __init__(self, block_id, x, y, z, weight, grades, extras={}):
        self._id = None
        self._x_coordinate = None
        self._y_coordinate = None
        self._z_coordinate = None
        self._weight = None
        self._grades = None
        #constructor validations:
        self.x_coordinate = x
        self.y_coordinate = y
        self.z_coordinate = z
        self.id = block_id
        self.weight = weight
        self.grades = grades
        self.extras = extras

    @property
    def id(self):
        """Get block id"""
        return self._id

    @id.setter
    def id(self, value):
        """Set block id"""
        if not (isinstance(value, str)): raise TypeError("id must be string")
        if not value.strip(): raise ValueError("id cannot be empty")
        if not (value == str(self.x_coordinate)+","+str(self.y_coordinate)+","+str(self.z_coordinate)):
            raise ValueError("The id must match the coordinates")
        self._id = value

    @id.deleter
    def id(self):
        """delete block id"""
        del self._id

    @property
    def x_coordinate(self):
        """Get block x coordinate"""
        return self._x_coordinate

    @x_coordinate.setter
    def x_coordinate(self, value):
        try:
            self._x_coordinate = int(value)
        except TypeError:
            print("x coodinate must be integer")

    @x_coordinate.deleter
    def x_coordinate(self):
        del self._x_coordinate

    @property
    def y_coordinate(self):
        """Get block y coordinate"""
        return self._y_coordinate

    @y_coordinate.setter
    def y_coordinate(self, value):
        try:
            self._y_coordinate = int(value)
        except TypeError:
            print("y coodinate must be integer")

    @y_coordinate.deleter
    def y_coordinate(self):
        del self._y_coordinate

    @property
    def z_coordinate(self):
        """Get block z coordinate"""
        return self._z_coordinate

    @z_coordinate.setter
    def z_coordinate(self, value):
        try:
            self._z_coordinate = int(value)
        except TypeError:
            print("z coodinate must be integer")

    @z_coordinate.deleter
    def z_coordinate(self):
        del self._z_coordinate

    @property
    def weight(self):
        """Get block weight"""
        return self._weight

    @weight.setter
    def weight(self, value):
        """Set block weight"""
        if not (isinstance(value, (int, float))): raise TypeError("weight must be either integer or float")
        if not (value >= 0): raise ValueError("weight must be non negative")
        self._weight = value

    @weight.deleter
    def weight(self):
        del self._weight

    @property
    def grades(self):
        """Get block grades"""
        return self._grades

    @grades.setter
    def grades(self, block_grades):
        """Set block grades"""
        if not (isinstance(block_grades, dict)): raise TypeError("grades must be defined in a dictionary")
        if not block_grades: raise ValueError("grades cannot be empty")
        for mineral in block_grades.keys():
            if not (isinstance(block_grades[mineral],dict)):
                raise TypeError("grade value and grade type must be defined in a dictionary")
            if not ("value" in block_grades[mineral].keys()):
                raise SyntaxError("Grade dictionary must have a 'value' key")
            if not ("grade_type" in block_grades[mineral].keys()):
                raise SyntaxError("Grade dictionary must have a 'grade_type' key")
            if not (isinstance(block_grades[mineral]["value"],(int,float))):
                raise TypeError("value of a grade must be either integer or float")
            if not (block_grades[mineral]["value"] >= 0):
                raise ValueError("value of a grade must be non negative")
            if not (isinstance(block_grades[mineral]["grade_type"], int)):
                raise TypeError("index of grade type must be integer")
            if not (block_grades[mineral]["grade_type"] >= 0):
                raise ValueError("index of grade type must be greater than zero")
        self._grades = block_grades

    @grades.deleter
    def grades(self):
        del self._grades