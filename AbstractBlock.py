import abc
from abc import ABC, abstractmethod

class AbstractBlock(ABC):
    @abc.abstractproperty
    def id(self):
        """Get block id"""
        pass

    @abc.abstractproperty
    def x_coordinate(self):
        """Get block x coordinate"""
        pass

    @abc.abstractproperty
    def y_coordinate(self):
        """Get block y coordinate"""
        pass

    @abc.abstractproperty
    def z_coordinate(self):
        """Get block z coordinate"""
        pass

    @abc.abstractproperty
    def weight(self):
        """Get block weight"""
        pass

    @abc.abstractproperty
    def grades(self):
        """Get block grades"""
        pass
