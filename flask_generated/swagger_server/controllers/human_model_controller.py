import connexion

from swagger_server.controllers.base_controller import BaseController, kafka_add, kafka_update
from swagger_server.controllers.routing import RoutingInformation
from swagger_server.models.human_model import HumanModel  # noqa: E501
from swagger_server.models.human_property_model import HumanPropertyModel  # noqa: E501
from swagger_server.models.operation_model import OperationModel  # noqa: E501
from swagger_server.serializer.base_model_serializer import BaseModelSerializer
from swagger_server.serializer.model_serializer import ModelSerializer
from swagger_server.serializer.property_model_serializer import PropertyModelSerializer


def get_all_humanmodels():  # noqa: E501
    """Lists all registered humanmodels

     # noqa: E501


    :rtype: HumanModel
    """
    return BaseController.get_list_view(HumanModel, ModelSerializer)


def get_human_operation(uuid, name):  # noqa: E501
    """Returns an operation of humanmodel identified by uuid and name (of operation)

     # noqa: E501

    :param uuid: 
    :type uuid: str
    :param name: 
    :type name: str

    :rtype: OperationModel
    """
    humanmodel = BaseController.get_db_model(HumanModel, 'uuid', uuid)
    operation = BaseController.get_list_item_of_db_model(humanmodel, "operations", name, "name")
    if operation is not None:
        return BaseModelSerializer(routing=RoutingInformation.create_root_routing_object()).deserialize(operation), 200
    return 'do some magic!'


def get_human_operations(uuid):  # noqa: E501
    """Returns all operations

     # noqa: E501

    :param uuid:
    :type uuid: str

    :rtype: OperationModel
    """
    humanmodel, code = get_humanmodel(uuid)
    if code == 200:
        return humanmodel['operations'], 200
    return "error", code


def get_human_property(uuid, key):  # noqa: E501
    """Gets a property identified by {key} of a humanmodel identified by uuid

     # noqa: E501

    :param uuid: 
    :type uuid: str
    :param key: 
    :type key: str

    :rtype: HumanPropertyModel
    """
    req = connexion.request
    if uuid is not None:
        human = BaseController.get_db_model(HumanModel, 'uuid', uuid)
        result, code = BaseController.get_nested_list_item_with_route(human, 'properties', 'key', key, ModelSerializer)
        return result, 200
    
    return {}, 404


def get_humanmodel(uuid):  # noqa: E501
    """Returns specific humanmodel

     # noqa: E501

    :param uuid: 
    :type uuid: str

    :rtype: HumanModel
    """
    
    return BaseController.get_detail_view(HumanModel, ModelSerializer, 'uuid', uuid)


@kafka_update(serializer=ModelSerializer)
def update_human_model(body, uuid):  # noqa: E501
    """Updates the human model, use this to add values

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param uuid: 
    :type uuid: str

    :rtype: None
    """
    return BaseController.update_model_with_properties(HumanModel, body, HumanPropertyModel, uuid, get_humanmodel)


@kafka_update(serializer=PropertyModelSerializer)
def update_human_property(body, uuid, key):  # noqa: E501
    """Updates the property model identified by key of the humanmodel identified by uuid

     # noqa: E501

    :param body:
    :type body: dict | bytes
    :param uuid:
    :type uuid: str
    :param key:
    :type key: str

    :rtype: None
    """
    return BaseController.update_model_property(HumanModel, body, HumanPropertyModel, uuid, key, get_human_property)


@kafka_add(endpoint='humans')
def humanmodel_post(body):  # noqa: E501
    """Adds a new HumanModel

     # noqa: E501

    :param body:
    :type body: dict | bytes

    :rtype: HumanModel
    """
    BaseController.add_model_with_properties(body, HumanModel, HumanPropertyModel, body, ModelSerializer)
    # if connexion.request.is_json:
    #     if 'uuid' not in body or BaseController.get_db_model(HumanModel, 'uuid', body['uuid']) is not None:
    #         return "UUID not present or human with uuid exists", 400
    #     d = ModelSerializer().serialize(HumanModel, body, HumanPropertyModel)
    #     model = d.write_and_save()
    #
    # return get_humanmodel(model.uuid)


def delete_human_model(uuid):
    """
    Deletes HumanModel
    @param uuid: uuid uniqueley identifiying the humanmodel
    @return: 200 if successful
    """
    
    return BaseController.delete_model(HumanModel, 'uuid', uuid)
