# coding: utf-8

from __future__ import absolute_import

from swagger_server import util
from swagger_server.models.base_model_ import Model
from swagger_server.models.string_constraint_model_kms import KMSStringConstraintModel


class StringConstraintModel(Model, KMSStringConstraintModel):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    
    def __init__(self, name: str = None, value: str = None):  # noqa: E501
        """StringConstraintModel - a model defined in Swagger

        :param name: The name of this StringConstraintModel.  # noqa: E501
        :type name: str
        :param value: The value of this StringConstraintModel.  # noqa: E501
        :type value: str
        """
        self.swagger_types = {
            'name': str,
            'value': str
        }
        
        self.attribute_map = {
            'name': 'name',
            'value': 'value'
        }
        self._name = name
        self._value = value
    
    @classmethod
    def from_dict(cls, dikt) -> 'StringConstraintModel':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The StringConstraintModel of this StringConstraintModel.  # noqa: E501
        :rtype: StringConstraintModel
        """
        return util.deserialize_model(dikt, cls)
    
    @property
    def name(self) -> str:
        """Gets the name of this StringConstraintModel.


        :return: The name of this StringConstraintModel.
        :rtype: str
        """
        return self._name
    
    @name.setter
    def name(self, name: str):
        """Sets the name of this StringConstraintModel.


        :param name: The name of this StringConstraintModel.
        :type name: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501
        
        self._name = name
    
    @property
    def value(self) -> str:
        """Gets the value of this StringConstraintModel.


        :return: The value of this StringConstraintModel.
        :rtype: str
        """
        return self._value
    
    @value.setter
    def value(self, value: str):
        """Sets the value of this StringConstraintModel.


        :param value: The value of this StringConstraintModel.
        :type value: str
        """
        if value is None:
            raise ValueError("Invalid value for `value`, must not be `None`")  # noqa: E501
        
        self._value = value
