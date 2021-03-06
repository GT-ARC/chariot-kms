# coding: utf-8

from __future__ import absolute_import

from swagger_server import util
from swagger_server.models.agent_list import AgentList
from swagger_server.models.base_model_ import Model
from swagger_server.models.load_balancer_model import LoadBalancerModel  # noqa: F401,E501
from swagger_server.models.monitoring_service_model_kms import MonitoringServiceModelKMS


class MonitoringServiceModel(Model, MonitoringServiceModelKMS):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    
    def __init__(self, id: str = None, loadbalancer: LoadBalancerModel = None,
                 agentlist: AgentList = None):  # noqa: E501
        """MonitoringServiceModel - a model defined in Swagger

        :param id: The id of this MonitoringServiceModel.  # noqa: E501
        :type id: str
        :param loadbalancer: The loadbalancer of this MonitoringServiceModel.  # noqa: E501
        :type loadbalancer: LoadBalancerModel
        :param agentlist: The agentlist of this MonitoringServiceModel.  # noqa: E501
        :type agentlist: AgentList
        """
        self.swagger_types = {
            'id': str,
            'loadbalancer': LoadBalancerModel,
            'agentlist': AgentList
        }
        
        self.attribute_map = {
            'id': '_id',
            'loadbalancer': 'loadbalancer',
            'agentlist': 'agentlist'
        }
        self._id = id
        self._loadbalancer = loadbalancer
        self._agentlist = agentlist
    
    @classmethod
    def from_dict(cls, dikt) -> 'MonitoringServiceModel':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The MonitoringServiceModel of this MonitoringServiceModel.  # noqa: E501
        :rtype: MonitoringServiceModel
        """
        return util.deserialize_model(dikt, cls)
    
    @property
    def id(self) -> str:
        """Gets the id of this MonitoringServiceModel.


        :return: The id of this MonitoringServiceModel.
        :rtype: str
        """
        return self._id
    
    @id.setter
    def id(self, id: str):
        """Sets the id of this MonitoringServiceModel.


        :param id: The id of this MonitoringServiceModel.
        :type id: str
        """
        
        self._id = id
    
    @property
    def loadbalancer(self) -> LoadBalancerModel:
        """Gets the loadbalancer of this MonitoringServiceModel.


        :return: The loadbalancer of this MonitoringServiceModel.
        :rtype: LoadBalancerModel
        """
        return self._loadbalancer
    
    @loadbalancer.setter
    def loadbalancer(self, loadbalancer: LoadBalancerModel):
        """Sets the loadbalancer of this MonitoringServiceModel.


        :param loadbalancer: The loadbalancer of this MonitoringServiceModel.
        :type loadbalancer: LoadBalancerModel
        """
        if loadbalancer is None:
            raise ValueError("Invalid value for `loadbalancer`, must not be `None`")  # noqa: E501
        
        self._loadbalancer = loadbalancer
    
    @property
    def agentlist(self) -> AgentList:
        """Gets the agentlist of this MonitoringServiceModel.


        :return: The agentlist of this MonitoringServiceModel.
        :rtype: AgentList
        """
        return self._agentlist
    
    @agentlist.setter
    def agentlist(self, agentlist: AgentList):
        """Sets the agentlist of this MonitoringServiceModel.


        :param agentlist: The agentlist of this MonitoringServiceModel.
        :type agentlist: AgentList
        """
        if agentlist is None:
            raise ValueError("Invalid value for `agentlist`, must not be `None`")  # noqa: E501
        
        self._agentlist = agentlist
