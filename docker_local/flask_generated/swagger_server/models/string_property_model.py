# coding: utf-8

from __future__ import absolute_import

from swagger_server import util
from swagger_server.models.base_model_ import Model
from swagger_server.models.string_property_model_kms import KMSStringPropertyModel


class StringPropertyModel(Model, KMSStringPropertyModel):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    
    def __init__(self, key: str = None, writable: bool = None, kafka_topic: str = None, uuid: str = None,
                 timestamp: int = None, value: str = None, type: str = None):  # noqa: E501
        """StringPropertyModel - a model defined in Swagger

        :param key: The key of this StringPropertyModel.  # noqa: E501
        :type key: str
        :param writable: The writable of this StringPropertyModel.  # noqa: E501
        :type writable: bool
        :param kafka_topic: The kafka_topic of this StringPropertyModel.  # noqa: E501
        :type kafka_topic: str
        :param uuid: The uuid of this StringPropertyModel.  # noqa: E501
        :type uuid: str
        :param timestamp: The timestamp of this StringPropertyModel.  # noqa: E501
        :type timestamp: int
        :param value: The value of this StringPropertyModel.  # noqa: E501
        :type value: str
        :param type: The type of this StringPropertyModel.  # noqa: E501
        :type type: str
        """
        self.swagger_types = {
            'key': str,
            'writable': bool,
            'kafka_topic': str,
            'uuid': str,
            'timestamp': int,
            'value': str,
            'type': str
        }
        
        self.attribute_map = {
            'key': 'key',
            'writable': 'writable',
            'kafka_topic': 'kafka_topic',
            'uuid': 'uuid',
            'timestamp': 'timestamp',
            'value': 'value',
            'type': 'type'
        }
        self._key = key
        self._writable = writable
        self._kafka_topic = kafka_topic
        self._uuid = uuid
        self._timestamp = timestamp
        self._value = value
        self._type = type
    
    @classmethod
    def from_dict(cls, dikt) -> 'StringPropertyModel':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The StringPropertyModel of this StringPropertyModel.  # noqa: E501
        :rtype: StringPropertyModel
        """
        return util.deserialize_model(dikt, cls)
    
    @property
    def key(self) -> str:
        """Gets the key of this StringPropertyModel.


        :return: The key of this StringPropertyModel.
        :rtype: str
        """
        return self._key
    
    @key.setter
    def key(self, key: str):
        """Sets the key of this StringPropertyModel.


        :param key: The key of this StringPropertyModel.
        :type key: str
        """
        if key is None:
            raise ValueError("Invalid value for `key`, must not be `None`")  # noqa: E501
        
        self._key = key
    
    @property
    def writable(self) -> bool:
        """Gets the writable of this StringPropertyModel.


        :return: The writable of this StringPropertyModel.
        :rtype: bool
        """
        return self._writable
    
    @writable.setter
    def writable(self, writable: bool):
        """Sets the writable of this StringPropertyModel.


        :param writable: The writable of this StringPropertyModel.
        :type writable: bool
        """
        
        self._writable = writable
    
    @property
    def kafka_topic(self) -> str:
        """Gets the kafka_topic of this StringPropertyModel.


        :return: The kafka_topic of this StringPropertyModel.
        :rtype: str
        """
        return self._kafka_topic
    
    @kafka_topic.setter
    def kafka_topic(self, kafka_topic: str):
        """Sets the kafka_topic of this StringPropertyModel.


        :param kafka_topic: The kafka_topic of this StringPropertyModel.
        :type kafka_topic: str
        """
        
        self._kafka_topic = kafka_topic
    
    @property
    def uuid(self) -> str:
        """Gets the uuid of this StringPropertyModel.


        :return: The uuid of this StringPropertyModel.
        :rtype: str
        """
        return self._uuid
    
    @uuid.setter
    def uuid(self, uuid: str):
        """Sets the uuid of this StringPropertyModel.


        :param uuid: The uuid of this StringPropertyModel.
        :type uuid: str
        """
        
        self._uuid = uuid
    
    @property
    def timestamp(self) -> int:
        """Gets the timestamp of this StringPropertyModel.


        :return: The timestamp of this StringPropertyModel.
        :rtype: int
        """
        return self._timestamp
    
    @timestamp.setter
    def timestamp(self, timestamp: int):
        """Sets the timestamp of this StringPropertyModel.


        :param timestamp: The timestamp of this StringPropertyModel.
        :type timestamp: int
        """
        
        self._timestamp = timestamp
    
    @property
    def value(self) -> str:
        """Gets the value of this StringPropertyModel.


        :return: The value of this StringPropertyModel.
        :rtype: str
        """
        return self._value
    
    @value.setter
    def value(self, value: str):
        """Sets the value of this StringPropertyModel.


        :param value: The value of this StringPropertyModel.
        :type value: str
        """
        if value is None:
            raise ValueError("Invalid value for `value`, must not be `None`")  # noqa: E501
        
        self._value = value
    
    @property
    def type(self) -> str:
        """Gets the type of this StringPropertyModel.


        :return: The type of this StringPropertyModel.
        :rtype: str
        """
        return self._type
    
    @type.setter
    def type(self, type: str):
        """Sets the type of this StringPropertyModel.


        :param type: The type of this StringPropertyModel.
        :type type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501
        
        self._type = type
