import connexion

from swagger_server.controllers.base_controller import kafka_update, kafka_add
from swagger_server.controllers.routing import RoutingInformation
from swagger_server.models.agent_mapping import AgentMapping
from swagger_server.models.load_balancer_model import LoadBalancerModel
from swagger_server.models.monitoring_service_model import MonitoringServiceModel  # noqa: E501
from swagger_server.serializer.base_model_serializer import BaseModelSerializer


def _get_monitoringservice(msid):
    result = MonitoringServiceModel().get_mongo_model().objects.filter(pk=msid)
    if len(result) == 0:
        return None
    return result.get()


def get_all_monitoringservice():  # noqa: E501
    """Lists all items

     # noqa: E501


    :rtype: MonitoringServiceModel
    """
    serializer = BaseModelSerializer
    result = MonitoringServiceModel().get_mongo_model().objects.all()
    serialized_result = []
    for model in result:
        serialized_result.append(serializer(routing=RoutingInformation.create_root_routing_object()).deserialize(model))
    return serialized_result, 200


@kafka_add(endpoint='monitoringservice')
def monitoring_service_post(body):  # noqa: E501
    """Adds a new MonitoringService

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: MonitoringServiceModel
    """
    if connexion.request.is_json:
        body = MonitoringServiceModel.from_dict(connexion.request.get_json())  # noqa: E501
        result = body.write_and_save()
        return BaseModelSerializer(routing=RoutingInformation.create_root_routing_object()).deserialize(result), 201


@kafka_update(serializer=BaseModelSerializer)
def agentlist_add(body, msid):  # noqa: E501
    """Add to the agentlist

     # noqa: E501

    :param body:
    :type body: dict | bytes
    :param msid:
    :type msid: str

    :rtype: MonitoringServiceModel
    """
    if connexion.request.is_json:
        ms = _get_monitoringservice(msid)
        if ms is None:
            return 'Model not found. Check msid parameter', 400
        agent = AgentMapping.from_dict(connexion.request.get_json())
        agent = agent.fill_db_model()
        ms.agentlist.mappings.append(agent)
        ms.save()
        return BaseModelSerializer(routing=RoutingInformation.create_root_routing_object()).deserialize(ms), 201
    return 'not ok', 500


@kafka_update(BaseModelSerializer)
def update_loadbalancer(body, msid, lbid):  # noqa: E501
    """Update the loadbalancer

     # noqa: E501

    :param body:
    :type body: dict | bytes
    :param msid:
    :type msid: str
    :param lbid:
    :type lbid: str

    :rtype: MonitoringServiceModel
    """
    if connexion.request.is_json:
        body = LoadBalancerModel.from_dict(connexion.request.get_json())  # noqa: E501
        ms = _get_monitoringservice(msid)
        BaseModelSerializer().update(body, ms.loadbalancer)
        ms.save()
        return BaseModelSerializer(routing=RoutingInformation.create_root_routing_object()).deserialize(ms), 200


def get_monitoringservice(msid):  # noqa: E501
    """Get specific MS

     # noqa: E501

    :param msid:
    :type msid: str

    :rtype: MonitoringServiceModel
    """
    ms = _get_monitoringservice(msid)
    if ms is not None:
        return BaseModelSerializer(routing=RoutingInformation.create_root_routing_object()).deserialize(ms), 200
    return 'Not found', 404


@kafka_update(BaseModelSerializer)
def delete_monitoring_service(msid):  # noqa: E501
    """Delete a monitoring service

     # noqa: E501

    :param msid:
    :type msid: str

    :rtype: None
    """
    ms = _get_monitoringservice(msid)
    if ms is not None:
        ms.delete()
        return "Deleted", 201
    return 'Not found', 404


@kafka_update(BaseModelSerializer)
def agentlist_delete_agent(msid, agentlistid, mapping_id):  # noqa: E501
    """Delete an agent mapping from an agentlist

     # noqa: E501

    :param msid:
    :type msid: str
    :param agid:
    :type agid: str

    :rtype: MonitoringServiceModel
    """
    ms = _get_monitoringservice(msid)
    if ms is not None:
        for mapping in ms.agentlist.mappings:
            if str(mapping._id) == str(mapping_id):
                ms.agentlist.mappings.filter(_id=mapping_id).delete()
                ms.save()
                return BaseModelSerializer(routing=RoutingInformation.create_root_routing_object()).deserialize(ms), 200
    
    return 'Not found', 404


def get_ms_agentlist(msid, agentlistid):  # noqa: E501
    """returns the agentlist object of the monitoring service object

     # noqa: E501

    :param msid:
    :type msid: str
    :param agentlistid:
    :type agentlistid: str

    :rtype: AgentList
    """
    ms, code = get_monitoringservice(msid)
    if code < 300:
        return ms['agentlist'], 200
    return 'Not found', 404


def get_ms_mapping(msid, agentlistid, mapping_id):  # noqa: E501
    """Get a mapping object

     # noqa: E501

    :param msid:
    :type msid: str
    :param agentlistid:
    :type agentlistid: str
    :param mapping_id:
    :type mapping_id: str

    :rtype: AgentMapping
    """
    agentlist, code = get_ms_agentlist(msid, agentlistid)
    if code < 300:
        for mapping in agentlist['mappings']:
            if mapping['_id'] == mapping_id:
                return mapping, 200
    return 'Not found', 404


def get_loadbalancer(msid, lbid):  # noqa: E501
    """Returns the loadbalancer object

     # noqa: E501

    :param msid:
    :type msid: str
    :param lbid:
    :type lbid: str

    :rtype: LoadBalancerModel
    """
    ms, code = get_monitoringservice(msid)
    if code < 300:
        return ms['loadbalancer'], 200
    return 'Not found', 404
