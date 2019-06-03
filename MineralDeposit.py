class MineralDeposit:  # Entity
    def __init__(self, name, x, y, z, weight, grades):
        self._name = None
        self._x_coordinate_column = None
        self._y_coordinate_column = None
        self._z_coordinate_column = None
        self._weight_column = None
        self._grades = None
        #validations:
        self.name = name
        self.x_coordinate_column = x
        self.y_coordinate_column = y
        self.z_coordinate_column = z
        self.weight_column = weight
        self.grades = grades

    @property
    def name(self):
        """Get mineral deposit name"""
        return self._name

    @name.setter
    def name(self, value):
        """Set mineral deposit name"""
        if not (isinstance(value, str)): raise TypeError("block model name must be string")
        if not value.strip(): raise ValueError("block model name cannot be empty")
        self._name = value

    @name.deleter
    def name(self):
        """delete mineral deposit name"""
        del self._name

    @property
    def x_coordinate_column(self):
        """Get mineral deposit x coordinate column"""
        return self._x_coordinate_column

    @x_coordinate_column.setter
    def x_coordinate_column(self, value):
        """Set mineral deposit x_coordinate_column"""
        if not (isinstance(value, int)): raise TypeError("mineral deposit x coordinate columns must be integer")
        if not (value >= 0): raise ValueError("mineral deposit x coordinate columns must be non negative")
        self._x_coordinate_column = value

    @x_coordinate_column.deleter
    def x_coordinate_column(self):
        """delete mineral deposit x_coordinate_column"""
        del self._x_coordinate_column

    @property
    def y_coordinate_column(self):
        """Get mineral deposit y coordinate column"""
        return self._y_coordinate_column

    @y_coordinate_column.setter
    def y_coordinate_column(self, value):
        """Set mineral deposit y_coordinate_column"""
        if not (isinstance(value, int)): raise TypeError("mineral deposit y coordinate columns must be integer")
        if not (value >= 0): raise ValueError("mineral deposit y coordinate columns must be non negative")
        self._y_coordinate_column = value

    @y_coordinate_column.deleter
    def y_coordinate_column(self):
        """delete mineral deposit y_coordinate_column"""
        del self._y_coordinate_column

    @property
    def z_coordinate_column(self):
        """Get mineral deposit z coordinate column"""
        return self._z_coordinate_column

    @z_coordinate_column.setter
    def z_coordinate_column(self, value):
        """Set mineral deposit z_coordinate_column"""
        if not (isinstance(value, int)): raise TypeError("mineral deposit z coordinate columns must be integer")
        if not (value >= 0): raise ValueError("mineral deposit z coordinate columns must be non negative")
        self._z_coordinate_column = value

    @z_coordinate_column.deleter
    def z_coordinate_column(self):
        """delete mineral deposit z_coordinate_column"""
        del self._z_coordinate_column

    @property
    def weight_column(self):
        """Get mineral deposit weight_column"""
        return self._weight_column

    @weight_column.setter
    def weight_column(self, value):
        """Set mineral deposit weight_column"""
        if not (isinstance(value, int)): raise TypeError("mineral deposit weight_column must be int")
        if not (value >= 0): raise ValueError("mineral deposit weight_column must be non negative")
        self._weight_column = value

    @weight_column.deleter
    def weight_column(self):
        """delete mineral deposit weight_column"""
        del self._weight_column

    @property
    def grades(self):
        """Get mineral deposit grades"""
        return self._grades

    def __validate_minerals(self,mineral_deposit_grades):
        for mineral in mineral_deposit_grades.keys():
            if not (isinstance(mineral_deposit_grades[mineral],dict)):
                raise TypeError("Grades value and grade type must be defined in a dictionary")
            if not ("mineral_column" in mineral_deposit_grades[mineral].keys()):
                raise SyntaxError("Grades dictionary must have a 'mineral_column' key")
            if not ("grade_type" in mineral_deposit_grades[mineral].keys()):
                raise SyntaxError("Grades dictionary must have a 'grade_type' key")
            if not (isinstance(mineral_deposit_grades[mineral]["mineral_column"],int)):
                raise TypeError("Value of a grade column must be integer")
            if not (mineral_deposit_grades[mineral]["mineral_column"] >= 0):
                raise ValueError("Value of a grade column must be non negative")
            if not (isinstance(mineral_deposit_grades[mineral]["grade_type"], int)):
                raise TypeError("Index of grade type must be integer")
            if not (mineral_deposit_grades[mineral]["grade_type"] >= 0):
                raise ValueError("Index of grade type must be greater than zero")

    @grades.setter
    def grades(self, mineral_deposit_grades):
        """Set mineral deposit grades"""
        if not (isinstance(mineral_deposit_grades, dict)): raise TypeError("Mineral deposit grades must be defined in a dictionary")
        if not mineral_deposit_grades: raise ValueError("Grades cannot be empty")
        self.__validate_minerals(mineral_deposit_grades)
        self._grades = mineral_deposit_grades

    @grades.deleter
    def grades(self):
        """delete mineral deposit grades"""
        del self._grades