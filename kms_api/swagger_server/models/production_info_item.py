# coding: utf-8

from __future__ import absolute_import

from swagger_server import util
from swagger_server.models.base_model_ import Model
from swagger_server.models.production_info_item_kms import KMSProductionInfoItem


class ProductionInfoItem(Model, KMSProductionInfoItem):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    
    def __init__(self, name: str = None):  # noqa: E501
        """ProductionInfoItem - a model defined in Swagger

        :param name: The name of this ProductionInfoItem.  # noqa: E501
        :type name: str
        """
        self.swagger_types = {
            'name': str
        }
        
        self.attribute_map = {
            'name': 'name'
        }
        self._name = name
    
    @classmethod
    def from_dict(cls, dikt) -> 'ProductionInfoItem':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ProductionInfoItem of this ProductionInfoItem.  # noqa: E501
        :rtype: ProductionInfoItem
        """
        return util.deserialize_model(dikt, cls)
    
    @property
    def name(self) -> str:
        """Gets the name of this ProductionInfoItem.


        :return: The name of this ProductionInfoItem.
        :rtype: str
        """
        return self._name
    
    @name.setter
    def name(self, name: str):
        """Sets the name of this ProductionInfoItem.


        :param name: The name of this ProductionInfoItem.
        :type name: str
        """
        
        self._name = name
