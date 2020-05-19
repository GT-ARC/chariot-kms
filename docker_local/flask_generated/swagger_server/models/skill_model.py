# coding: utf-8

from __future__ import absolute_import

from typing import List  # noqa: F401

from swagger_server import util
from swagger_server.models.base_model_ import Model
from swagger_server.models.skill_model_kms import KMSSkillModel
from swagger_server.models.skill_property_model import SkillPropertyModel  # noqa: F401,E501


class SkillModel(Model, KMSSkillModel):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    
    def __init__(self, object_type: str = None, name: str = None, uuid: str = None, kafka_topic: str = None,
                 id: str = None, properties: List[SkillPropertyModel] = None):  # noqa: E501
        """SkillModel - a model defined in Swagger

        :param object_type: The object_type of this SkillModel.  # noqa: E501
        :type object_type: str
        :param name: The name of this SkillModel.  # noqa: E501
        :type name: str
        :param uuid: The uuid of this SkillModel.  # noqa: E501
        :type uuid: str
        :param kafka_topic: The kafka_topic of this SkillModel.  # noqa: E501
        :type kafka_topic: str
        :param id: The id of this SkillModel.  # noqa: E501
        :type id: str
        :param properties: The properties of this SkillModel.  # noqa: E501
        :type properties: List[SkillPropertyModel]
        """
        self.swagger_types = {
            'object_type': str,
            'name': str,
            'uuid': str,
            'kafka_topic': str,
            'id': str,
            'properties': List[SkillPropertyModel]
        }
        
        self.attribute_map = {
            'object_type': 'objectType',
            'name': 'name',
            'uuid': 'uuid',
            'kafka_topic': 'kafka_topic',
            'id': '_id',
            'properties': 'properties'
        }
        self._object_type = object_type
        self._name = name
        self._uuid = uuid
        self._kafka_topic = kafka_topic
        self._id = id
        self._properties = properties
    
    @classmethod
    def from_dict(cls, dikt) -> 'SkillModel':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The SkillModel of this SkillModel.  # noqa: E501
        :rtype: SkillModel
        """
        return util.deserialize_model(dikt, cls)
    
    @property
    def object_type(self) -> str:
        """Gets the object_type of this SkillModel.


        :return: The object_type of this SkillModel.
        :rtype: str
        """
        return self._object_type
    
    @object_type.setter
    def object_type(self, object_type: str):
        """Sets the object_type of this SkillModel.


        :param object_type: The object_type of this SkillModel.
        :type object_type: str
        """
        allowed_values = ["actuator", "sensor", "human", "service", "skill", "task", "action", "healthdata",
                          "humanrole", "message", "permission", "preference", "property"]  # noqa: E501
        if object_type not in allowed_values:
            raise ValueError(
                "Invalid value for `object_type` ({0}), must be one of {1}"
                    .format(object_type, allowed_values)
            )
        
        self._object_type = object_type
    
    @property
    def name(self) -> str:
        """Gets the name of this SkillModel.

        []  # noqa: E501

        :return: The name of this SkillModel.
        :rtype: str
        """
        return self._name
    
    @name.setter
    def name(self, name: str):
        """Sets the name of this SkillModel.

        []  # noqa: E501

        :param name: The name of this SkillModel.
        :type name: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501
        
        self._name = name
    
    @property
    def uuid(self) -> str:
        """Gets the uuid of this SkillModel.

        []  # noqa: E501

        :return: The uuid of this SkillModel.
        :rtype: str
        """
        return self._uuid
    
    @uuid.setter
    def uuid(self, uuid: str):
        """Sets the uuid of this SkillModel.

        []  # noqa: E501

        :param uuid: The uuid of this SkillModel.
        :type uuid: str
        """
        if uuid is None:
            raise ValueError("Invalid value for `uuid`, must not be `None`")  # noqa: E501
        
        self._uuid = uuid
    
    @property
    def kafka_topic(self) -> str:
        """Gets the kafka_topic of this SkillModel.

        []  # noqa: E501

        :return: The kafka_topic of this SkillModel.
        :rtype: str
        """
        return self._kafka_topic
    
    @kafka_topic.setter
    def kafka_topic(self, kafka_topic: str):
        """Sets the kafka_topic of this SkillModel.

        []  # noqa: E501

        :param kafka_topic: The kafka_topic of this SkillModel.
        :type kafka_topic: str
        """
        
        self._kafka_topic = kafka_topic
    
    @property
    def id(self) -> str:
        """Gets the id of this SkillModel.

        []  # noqa: E501

        :return: The id of this SkillModel.
        :rtype: str
        """
        return self._id
    
    @id.setter
    def id(self, id: str):
        """Sets the id of this SkillModel.

        []  # noqa: E501

        :param id: The id of this SkillModel.
        :type id: str
        """
        
        self._id = id
    
    @property
    def properties(self) -> List[SkillPropertyModel]:
        """Gets the properties of this SkillModel.


        :return: The properties of this SkillModel.
        :rtype: List[SkillPropertyModel]
        """
        return self._properties
    
    @properties.setter
    def properties(self, properties: List[SkillPropertyModel]):
        """Sets the properties of this SkillModel.


        :param properties: The properties of this SkillModel.
        :type properties: List[SkillPropertyModel]
        """
        
        self._properties = properties
