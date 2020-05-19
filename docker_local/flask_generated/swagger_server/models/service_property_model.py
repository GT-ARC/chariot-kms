# coding: utf-8

from __future__ import absolute_import

from typing import List

from swagger_server import util
from swagger_server.models.base_model_ import Model
from swagger_server.models.service_property_model_kms import KMSServicePropertyModel


class ServicePropertyModel(Model, KMSServicePropertyModel):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    
    def __init__(self, related_to: List[str] = None, operation: str = None):  # noqa: E501
        """ServicePropertyModel - a model defined in Swagger

        :param related_to: The related_to of this ServicePropertyModel.  # noqa: E501
        :type related_to: List[str]
        :param operation: The operation of this ServicePropertyModel.  # noqa: E501
        :type operation: str
        """
        self.swagger_types = {
            'related_to': List[str],
            'operation': str
        }
        
        self.attribute_map = {
            'related_to': 'relatedTo',
            'operation': 'operation'
        }
        self._related_to = related_to
        self._operation = operation
    
    @classmethod
    def from_dict(cls, dikt) -> 'ServicePropertyModel':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ServicePropertyModel of this ServicePropertyModel.  # noqa: E501
        :rtype: ServicePropertyModel
        """
        return util.deserialize_model(dikt, cls)
    
    @property
    def related_to(self) -> List[str]:
        """Gets the related_to of this ServicePropertyModel.


        :return: The related_to of this ServicePropertyModel.
        :rtype: List[str]
        """
        return self._related_to
    
    @related_to.setter
    def related_to(self, related_to: List[str]):
        """Sets the related_to of this ServicePropertyModel.


        :param related_to: The related_to of this ServicePropertyModel.
        :type related_to: List[str]
        """
        if related_to is None:
            raise ValueError("Invalid value for `related_to`, must not be `None`")  # noqa: E501
        
        self._related_to = related_to
    
    @property
    def operation(self) -> str:
        """Gets the operation of this ServicePropertyModel.


        :return: The operation of this ServicePropertyModel.
        :rtype: str
        """
        return self._operation
    
    @operation.setter
    def operation(self, operation: str):
        """Sets the operation of this ServicePropertyModel.


        :param operation: The operation of this ServicePropertyModel.
        :type operation: str
        """
        if operation is None:
            raise ValueError("Invalid value for `operation`, must not be `None`")  # noqa: E501
        
        self._operation = operation
