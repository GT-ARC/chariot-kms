# coding: utf-8

from __future__ import absolute_import

from swagger_server import util
from swagger_server.models.base_model_ import Model


class GroupMixin(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    
    def __init__(self, groupId: str = None):  # noqa: E501
        """GroupMixin - a model defined in Swagger

        :param groupId: The groupId of this GroupMixin.  # noqa: E501
        :type groupId: str
        """
        self.swagger_types = {
            'groupId': str
        }
        
        self.attribute_map = {
            'groupId': 'groupId'
        }
        self._groupId = groupId
    
    @classmethod
    def from_dict(cls, dikt) -> 'GroupMixin':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The GroupMixin of this GroupMixin.  # noqa: E501
        :rtype: GroupMixin
        """
        return util.deserialize_model(dikt, cls)
    
    @property
    def groupId(self) -> str:
        """Gets the groupId of this GroupMixin.


        :return: The groupId of this GroupMixin.
        :rtype: str
        """
        return self._groupId
    
    @groupId.setter
    def groupId(self, groupId: str):
        """Sets the groupId of this GroupMixin.


        :param groupId: The groupId of this GroupMixin.
        :type groupId: str
        """
        if groupId is None:
            raise ValueError("Invalid value for `groupId`, must not be `None`")  # noqa: E501
        
        self._groupId = groupId
