import connexion

from swagger_server.controllers.base_controller import kafka_add, kafka_update, BaseController
from swagger_server.controllers.routing import RoutingInformation
from swagger_server.models import ServicePropertyModel
from swagger_server.models.service_model import ServiceModel  # noqa: E501
from swagger_server.serializer.model_serializer import ModelSerializer
from swagger_server.serializer.property_model_serializer import PropertyModelSerializer


def get_service_history(service_uuid):  # noqa: E501
    """List of the service&#x27;s properties&#x27; histories

     # noqa: E501

    :param service_uuid:
    :type service_uuid: str

    :rtype: ServiceModel
    #TODO refactor
    """
    service = BaseController.get_db_model(ServiceModel, 'uuid', service_uuid)
    routing = RoutingInformation.create_root_routing_object()
    serializer = ModelSerializer(routing=routing)
    result = serializer.deserialize(service, exclude=['properties'])
    routing.new_root(result['url'], result['kafka_topic'])
    p_histories = PropertyModelSerializer(serializer.routing).get_history(service.properties)
    for p_result in result['properties']:
        for p_history in p_histories:
            if p_result['key'] == p_history['key']:
                p_result.update(p_history)
    
    return result


def delete_service(service_uuid):  # noqa: E501
    """Deletes the service model identified by service_id

     # noqa: E501

    :param service_id:
    :type service_id: str

    :rtype: None
    """
    return BaseController.delete_model(ServiceModel, 'uuid', service_uuid)


def delete_service_property(service_uuid, key):  # noqa: E501
    """Delete a service property

     # noqa: E501

    :param service_uuid:
    :type service_uuid: str
    :param key:
    :type key: str

    :rtype: ServiceModel
    #TODO refactor
    """
    
    service = BaseController.get_db_model(ServiceModel, 'uuid', service_uuid)
    result = BaseController.delete_list_item_of_db_model(service, 'properties', key, 'value.key')
    return result, 200


def get_all_services():  # noqa: E501
    """Lists all registered services

     # noqa: E501


    :rtype: ServiceModel
    """
    return BaseController.get_list_view(ServiceModel, ModelSerializer)


def get_service(service_uuid):  # noqa: E501
    """Gets a service by its ID

     # noqa: E501

    :param service_id:
    :type service_id: str

    :rtype: ServiceModel
    """
    return BaseController.get_detail_view(ServiceModel, ModelSerializer, 'uuid', service_uuid)


@kafka_add()
def services_post(body):  # noqa: E501
    """Adds a new ServiceModel

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: ServiceModel
    """
    return BaseController.add_model_with_properties(body, ServiceModel, ServicePropertyModel, 'uuid', ModelSerializer)


@kafka_update(serializer=ModelSerializer)
def update_service(body, service_uuid):  # noqa: E501
    """Updates the service model, use this to add values

     # noqa: E501

    :param body:
    :type body: dict | bytes
    :param service_id:
    :type service_id: str

    :rtype: None
    
    """
    return BaseController.update_model_with_properties(ServiceModel, body, ServicePropertyModel, service_uuid,
                                                       get_service)


def get_service_properties(service_uuid):  # noqa: E501
    """List of the service&#x27;s properties

     # noqa: E501

    :param service_uuid:
    :type service_uuid: str

    :rtype: ServicePropertyModel
    """
    service_model, code = BaseController.get_detail_view(ServiceModel, ModelSerializer, 'uuid', service_uuid)
    if code == 200:
        return service_model['properties'], 200
    
    return 'service model not found', 404


def get_service_property(service_uuid, key):  # noqa: E501
    """Returns a single Service Property

     # noqa: E501

    :param service_uuid:
    :type service_uuid: str
    :param key:
    :type key: str

    :rtype: ServicePropertyModel
    """
    req = connexion.request
    if service_uuid is not None:
        service = BaseController.get_db_model(ServiceModel, 'uuid', service_uuid)
        return BaseController.get_nested_list_item_with_route(service, 'properties', 'key', key,
                                                              ModelSerializer)
    
    return {}, 404


def get_service_property_history(service_uuid, key):  # noqa: E501
    """List of the service&#x27;s properties history

     # noqa: E501

    :param service_uuid:
    :type service_uuid: str
    :param key:
    :type key: str

    :rtype: ServiceModel
    """
    service = BaseController.get_db_model(ServiceModel, 'uuid', service_uuid)
    property = BaseController.get_list_item_of_db_model(service, 'properties', key, nested_path="value.key")
    result = PropertyModelSerializer(routing=RoutingInformation.create_root_routing_object()).get_history(property)
    return result


@kafka_update(serializer=ModelSerializer)
def service_property_add(body, service_uuid):  # noqa: E501
    """Add property to service model

     # noqa: E501

    :param body:
    :type body: dict | bytes
    :param service_uuid:
    :type service_uuid: str

    :rtype: ServiceModel
    #TODO refactor
    """
    if connexion.request.is_json:
        property = PropertyModelSerializer().serialize(ServicePropertyModel, json=body)
        service, code = BaseController.get_db_model(ServiceModel, 'uuid', service_uuid)
        if service is not None:
            for p in service.properties:
                if p.value.key == property.value.key:
                    return "Duplicate key", 404
        service.properties.append(property.fill_db_model())
        service.save()
        return ModelSerializer(routing=RoutingInformation.create_root_routing_object()).deserialize(service), 201


@kafka_update(serializer=PropertyModelSerializer)
def update_service_property(body, service_uuid, key):  # noqa: E501
    """Updates the property model identified by key of the service identified by service_uuid

     # noqa: E501

    :param body:
    :type body: dict | bytes
    :param service_uuid:
    :type service_uuid: str
    :param key:
    :type key: str

    :rtype: None
    """
    
    return BaseController.update_model_property(ServiceModel, body, ServicePropertyModel, service_uuid, key,
                                                get_service_property)
