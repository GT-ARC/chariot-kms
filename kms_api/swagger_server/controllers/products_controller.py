import connexion

from swagger_server.controllers.base_controller import BaseController, kafka_add, kafka_update
from swagger_server.controllers.routing import RoutingInformation
from swagger_server.models.product_model import ProductModel  # noqa: E501
from swagger_server.models.production_flow_item import ProductionFlowItem
from swagger_server.models.production_flow_item_property import ProductionFlowItemProperty
from swagger_server.serializer.model_serializer import ModelSerializer
from swagger_server.serializer.product_model_serializer import ProductModelSerializer
from swagger_server.serializer.property_model_serializer import PropertyModelSerializer


def get_all_products():  # noqa: E501
    """Return a list of all products

     # noqa: E501


    :rtype: ProductModel
    """
    return BaseController.get_list_view(ProductModel, ProductModelSerializer)


def get_product_model(uuid):
    return BaseController.get_detail_view(ProductModel, ProductModelSerializer, 'uuid', uuid)


@kafka_add(serializer=ProductModelSerializer, endpoint='products')
def product_create(body):  # noqa: E501
    """Return a list of all products

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: ProductModel
    """
    if connexion.request.is_json:
        if 'uuid' not in body or BaseController.get_db_model(ProductModel, 'uuid', body['uuid']) is not None:
            return "UUID not present or device with uuid exists", 400
        d = ProductModelSerializer().serialize(ProductModel, body)
        model = d.write_and_save()
        
        return get_product_model(model.uuid)
    return "Failed. body: %s" % (body), 500


def delete_product(uuid):
    """
    
    @param uuid: uuid identifying the product model to delete
    @return:
    """
    return BaseController.delete_model(ProductModel, 'uuid', uuid)


@kafka_update(serializer=ProductModelSerializer)
def update_product_model(body, uuid):  # noqa: E501
    """Update product model and also addes values to production flow properties

     # noqa: E501

    :param body:
    :type body: dict | bytes
    :param uuid:
    :type uuid: str

    :rtype: ProductModel
    """
    
    if connexion.request.is_json:
        product_model_new = ProductModelSerializer().serialize(ProductModel, body)
        product_model_old = BaseController.get_db_model(ProductModel, 'uuid', uuid)
        if product_model_old is None:
            return "Not found", 404
        ProductModelSerializer().update(product_model_new, product_model_old)
        
        return get_product_model(uuid)
    return 'not ok', 400


def get_product_history(uuid):  # noqa: E501
    """All recorded values

     # noqa: E501

    :param uuid:
    :type uuid: str

    :rtype: ProductModel
    """
    
    product = BaseController.get_db_model(ProductModel, 'uuid', uuid)
    routing = RoutingInformation.create_root_routing_object()
    result = ProductModelSerializer(routing=routing).get_history(product,
                                                                 {'productionFlow': ModelSerializer,
                                                                  'properties': PropertyModelSerializer})
    
    return result


def get_product_info(uuid):  # noqa: E501
    """get all product info items

     # noqa: E501

    :param uuid:
    :type uuid: str

    :rtype: List
    """
    model = BaseController.get_db_model(ProductModel, 'uuid', uuid)
    if model is not None:
        return model['productInfo'], 200
    else:
        return "Attribute not found", 404


def get_product_info_item(uuid, name):  # noqa: E501
    """get single product info item

     # noqa: E501

    :param uuid:
    :type uuid: str
    :param name:
    :type name: str

    :rtype: ProductionInfoItem
    """
    model = BaseController.get_db_model(ProductModel, 'uuid', uuid)
    result = BaseController.get_list_item_of_db_model(model, 'productInfo', name, 'name')
    if result is not None:
        return result, 200
    else:
        return "Item not found", 404


def get_production_flow(uuid):  # noqa: E501
    """get production flow

     # noqa: E501

    :param uuid:
    :type uuid: str

    :rtype: List
    """
    model = BaseController.get_db_model(ProductModel, 'uuid', uuid)
    result = model['productionFlow']
    if result is not None:
        return result, 200
    return "Not found", 404


def get_production_flow_item(uuid, name):  # noqa: E501
    """get production flow item

     # noqa: E501

    :param uuid:
    :type uuid: str
    :param name:
    :type name: str

    :rtype: ProductionFlowItem
    """
    model = BaseController.get_db_model(ProductModel, 'uuid', uuid)
    result = BaseController.get_list_item_of_db_model(model, 'productionFlow', name, 'name')
    if result is not None:
        return result, 200
    return "Not found", 404


def get_production_flow_item_property(uuid, name, key):  # noqa: E501
    """get production flow item property

     # noqa: E501

    :param uuid:
    :type uuid: str
    :param name:
    :type name: str
    :param key:
    :type key: str

    :rtype: ProductionFlowItemProperty
    """
    flow_item, code = get_production_flow_item(uuid, name)
    if code == 200:
        for p in flow_item['properties']:
            if p.value.key == key:
                return p, 200
    
    return "Not found", 404


def get_production_flow_item_property_history(uuid, name, key):  # noqa: E501
    """get production flow item property history

     # noqa: E501

    :param uuid:
    :type uuid: str
    :param name:
    :type name: str
    :param key:
    :type key: str

    :rtype: ProductionFlowItemProperty
    """
    return 'do some magic!'


@kafka_update(serializer=ModelSerializer)
def update_production_flow_item(body, uuid, name):  # noqa: E501
    """Update production flow item, adds values to properties

     # noqa: E501

    :param body:
    :type body: dict | bytes
    :param uuid:
    :type uuid: str
    :param name:
    :type name: str

    :rtype: ProductionFlowItem
    """
    model = get_product_model(uuid)
    for flow_item_old in model['productionFlow']:
        if flow_item_old.name == name:
            flow_item_new = ModelSerializer().serialize((ProductionFlowItem,
                                                         body,
                                                         ProductionFlowItemProperty))
            ModelSerializer().update(flow_item_new, flow_item_old)
            
            model.save()
            return get_product_model(uuid)
    else:
        return "Not found", 400


@kafka_update(serializer=PropertyModelSerializer)
def update_production_flow_item_property(body, uuid, name, key):  # noqa: E501
    """Update production flow item property, adds values to property

     # noqa: E501

    :param body:
    :type body: dict | bytes
    :param uuid:
    :type uuid: str
    :param name:
    :type name: str
    :param key:
    :type key: str

    :rtype: ProductionFlowItemProperty
    """
    model = get_product_model(uuid)
    for flow_item_old in model['productionFlow']:
        if flow_item_old.name == name:
            for property_old in flow_item_old.properties:
                if property_old.key == key:
                    property_new = PropertyModelSerializer().serialize((ProductionFlowItemProperty, body))
                    PropertyModelSerializer().update(property_new, property_old)
                    
                    model.save()
                    return get_product_model(uuid)
    else:
        return "Not found", 400
