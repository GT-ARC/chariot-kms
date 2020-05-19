# coding: utf-8

from __future__ import absolute_import

from swagger_server import util
from swagger_server.models.base_model_ import Model


class BasePropertyModel(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    
    def __init__(self, key: str = None, writable: bool = None, kafka_topic: str = None, uuid: str = None,
                 timestamp: int = None):  # noqa: E501
        """BasePropertyModel - a model defined in Swagger

        :param key: The key of this BasePropertyModel.  # noqa: E501
        :type key: str
        :param writable: The writable of this BasePropertyModel.  # noqa: E501
        :type writable: bool
        :param kafka_topic: The kafka_topic of this BasePropertyModel.  # noqa: E501
        :type kafka_topic: str
        :param uuid: The uuid of this BasePropertyModel.  # noqa: E501
        :type uuid: str
        :param timestamp: The timestamp of this BasePropertyModel.  # noqa: E501
        :type timestamp: int
        """
        self.swagger_types = {
            'key': str,
            'writable': bool,
            'kafka_topic': str,
            'uuid': str,
            'timestamp': int
        }
        
        self.attribute_map = {
            'key': 'key',
            'writable': 'writable',
            'kafka_topic': 'kafka_topic',
            'uuid': 'uuid',
            'timestamp': 'timestamp'
        }
        self._key = key
        self._writable = writable
        self._kafka_topic = kafka_topic
        self._uuid = uuid
        self._timestamp = timestamp
    
    @classmethod
    def from_dict(cls, dikt) -> 'BasePropertyModel':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The BasePropertyModel of this BasePropertyModel.  # noqa: E501
        :rtype: BasePropertyModel
        """
        return util.deserialize_model(dikt, cls)
    
    @property
    def key(self) -> str:
        """Gets the key of this BasePropertyModel.


        :return: The key of this BasePropertyModel.
        :rtype: str
        """
        return self._key
    
    @key.setter
    def key(self, key: str):
        """Sets the key of this BasePropertyModel.


        :param key: The key of this BasePropertyModel.
        :type key: str
        """
        if key is None:
            raise ValueError("Invalid value for `key`, must not be `None`")  # noqa: E501
        
        self._key = key
    
    @property
    def writable(self) -> bool:
        """Gets the writable of this BasePropertyModel.


        :return: The writable of this BasePropertyModel.
        :rtype: bool
        """
        return self._writable
    
    @writable.setter
    def writable(self, writable: bool):
        """Sets the writable of this BasePropertyModel.


        :param writable: The writable of this BasePropertyModel.
        :type writable: bool
        """
        
        self._writable = writable
    
    @property
    def kafka_topic(self) -> str:
        """Gets the kafka_topic of this BasePropertyModel.


        :return: The kafka_topic of this BasePropertyModel.
        :rtype: str
        """
        return self._kafka_topic
    
    @kafka_topic.setter
    def kafka_topic(self, kafka_topic: str):
        """Sets the kafka_topic of this BasePropertyModel.


        :param kafka_topic: The kafka_topic of this BasePropertyModel.
        :type kafka_topic: str
        """
        
        self._kafka_topic = kafka_topic
    
    @property
    def uuid(self) -> str:
        """Gets the uuid of this BasePropertyModel.


        :return: The uuid of this BasePropertyModel.
        :rtype: str
        """
        return self._uuid
    
    @uuid.setter
    def uuid(self, uuid: str):
        """Sets the uuid of this BasePropertyModel.


        :param uuid: The uuid of this BasePropertyModel.
        :type uuid: str
        """
        
        self._uuid = uuid
    
    @property
    def timestamp(self) -> int:
        """Gets the timestamp of this BasePropertyModel.


        :return: The timestamp of this BasePropertyModel.
        :rtype: int
        """
        return self._timestamp
    
    @timestamp.setter
    def timestamp(self, timestamp: int):
        """Sets the timestamp of this BasePropertyModel.


        :param timestamp: The timestamp of this BasePropertyModel.
        :type timestamp: int
        """
        
        self._timestamp = timestamp
