import uuid
from typing import List

import connexion

from swagger_server.controllers.base_controller import kafka_update, kafka_add, BaseController
from swagger_server.controllers.routing import RoutingInformation
from swagger_server.models import DevicePropertyModel
from swagger_server.models.device_model import DeviceModel  # noqa: E501
from swagger_server.serializer.base_model_serializer import BaseModelSerializer
from swagger_server.serializer.model_serializer import ModelSerializer
from swagger_server.serializer.property_model_serializer import PropertyModelSerializer


def _get_device_property(device_uuid: uuid.uuid4, key: []):
    result = None
    device = BaseController.get_db_model(DeviceModel, 'uuid', device_uuid)
    
    if device:
        for p in device.properties:
            if p.value.key == key[0]:
                if len(key) == 1:
                    result = p
                    return result
                if len(key) == 2:
                    for _p in p.value:
                        if _p.value.key == key[1]:
                            result = _p
                            return result
    return result


def delete_device(device_uuid):  # noqa: E501
    """Deletes the device db_model identified by device_uuid

     # noqa: E501

    :param device_uuid:
    :type device_uuid: str

    :rtype: None
    """
    
    return BaseController.delete_model(DeviceModel, 'uuid', device_uuid)


@kafka_add(serializer=ModelSerializer, endpoint='devices')
def devices_post(body):  # noqa: E501
    """Adds a new DeviceModel

     # noqa: E501
    :param body:
    
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        if 'uuid' not in body or BaseController.get_db_model(DeviceModel, 'uuid', body['uuid']) is not None:
            return "UUID not present or device with uuid exists", 400
        d = ModelSerializer().serialize(DeviceModel, body, DevicePropertyModel)
        model = d.write_and_save()
        
        return get_device(model.uuid)
    return "Failed. body: %s" % (body), 500


def get_all_devices():  # noqa: E501
    """Lists all registered devices (objectType is actuator, sensor)

     # noqa: E501


    :rtype: DeviceModel
    """
    return BaseController.get_list_view(DeviceModel, ModelSerializer)


def get_device(device_uuid):  # noqa: E501
    """Gets a device by its ID

     # noqa: E501
delete_property_history
    :param device_uuid:
    :type device_uuid: str
    """
    return BaseController.get_detail_view(DeviceModel, ModelSerializer, 'uuid', device_uuid)


def get_device_history(device_uuid, length=None, clear=None):  # noqa: E501
    """All recorded values for this device
     # noqa: E501
    :param device_uuid:
    :type device_uuid: str
    :param length: optional value to limit the number of values returned (per property)
    :type length: int
    :param clear: true if historical data should be cleared. add length for number of values that should be retained.
    :type clear: bool

    :rtype: DeviceModel
    """
    if not clear:
        # device = _get_device_model(device_uuid)
        device = BaseController.get_db_model(DeviceModel, 'uuid', device_uuid)
        if device is None:
            return "Not found", 404
        routing = RoutingInformation.create_root_routing_object()
        serializer = ModelSerializer(routing=routing)
        result = serializer.deserialize(device, exclude=['properties'])
        routing.new_root(result['url'], result['kafka_topic'])
        p_histories = PropertyModelSerializer(serializer.routing).get_history(device.properties, length=length)
        for p_result in result['properties']:
            for p_history in p_histories:
                if p_result['key'] == p_history['key']:
                    p_result.update(p_history)
        
        return result, 200
    else:
        return BaseController.delete_model_history(DeviceModel, device_uuid, retain_values=length)


def get_device_property(device_uuid: uuid.uuid4, key):  # noqa: E501
    """Gets a property identified by {key} of a device identified by {id}

     # noqa: E501

    :param id:
    :type id: str
    :param key:
    :type key: str

    :rtype: List
    """
    req = connexion.request
    if device_uuid is not None:
        device = BaseController.get_db_model(DeviceModel, 'uuid', device_uuid)
        result, code = BaseController.get_nested_list_item_with_route(device, 'properties', 'key', key, ModelSerializer)
        return result, 200
    
    return {}, 404


def get_device_property_history(device_uuid, key, length=None, clear=False):  # noqa: E501
    """All recorded values for this device

     # noqa: E501

    :param device_uuid:
    :type device_uuid: str
    :param key:
    :type key: str
    :param length: optional value to limit the number of values returned (per property)
    :type length: int
    :param clear: true if historical data should be cleared. add length for number of values that should be retained.
    :type clear: bool

    :rtype: DeviceModel
    """
    # property = _get_device_property(device_uuid, key=[key, ])
    device = BaseController.get_db_model(DeviceModel, 'uuid', device_uuid)
    if device is None:
        return "Not found", 404
    property = BaseController.get_list_item_of_db_model(device, 'properties', key, nested_path='value.key')

    if not clear:
        result = PropertyModelSerializer(routing=RoutingInformation.create_root_routing_object()).get_history(property,
                                                                                                              length=length)
        if result is not None:
            return result, 200
    else:
        return BaseController.delete_property_history(DeviceModel, device_uuid, key, retain_values=length)

    return "Error", 404


def get_device_nested_property(device_uuid: uuid.uuid4, key1, key2):  # noqa: E501
    serializer = PropertyModelSerializer
    if key2 == "all":
        return get_device_property(device_uuid, key1)
    else:
        p = _get_device_property(device_uuid, [key1, key2])
        result = serializer(routing=RoutingInformation.create_root_routing_object()).deserialize(p)
        return [result, ], 200
    
    return "Error", 500


@kafka_update(serializer=ModelSerializer)
def update_device(body, device_uuid):  # noqa: E501
    """Updates the device db_model, use this to add values

     # noqa: E501

    :param body:
    :type body: dict | bytes
    :param id:
    :type id: str

    :rtype: None
    """
    return BaseController.update_model_with_properties(DeviceModel, body, DevicePropertyModel, device_uuid, get_device)


@kafka_update(serializer=PropertyModelSerializer)
def update_device_property(body, device_uuid, key):  # noqa: E501
    """Updates the property db_model identified by key of the device identified by id

     # noqa: E501

    :param body:
    :type body: dict | bytes
    :param id:
    :type id: str
    :param key:
    :type key: str

    :rtype: None
    """
    return BaseController.update_model_property(DeviceModel, body, DevicePropertyModel, device_uuid, key,
                                                get_device_property)


@kafka_update(serializer=ModelSerializer)
def update_nested_device_property(body, device_uuid, key1, key2):  # noqa: E501
    """Updates the nested property identified by key2 of property db_model identified by key1 of the device identified by id

     # noqa: E501

    :param body:
    :type body: dict | bytes
    :param id:
    :type id: str
    :param key1:
    :type key1: str
    :param key2:
    :type key2: str

    :rtype: None
    """
    if connexion.request.is_json:
        json = connexion.request.get_json()
        json = [json]
        property = PropertyModelSerializer().serialize(DevicePropertyModel, body)[0]
        device = BaseController.get_db_model(DeviceModel, 'uuid', device_uuid)
        for p1 in device.properties:
            if p1.value.key == key1:
                for p2 in p1.value.value:
                    if p2.value.key == key2:
                        PropertyModelSerializer().update(property, p2)
        device.save()
        return get_device_nested_property(device_uuid, key1, key2)
    return 'not ok', 404


@kafka_update(serializer=ModelSerializer)
def device_nested_property_bulk_update(body, device_uuid, key1, key2):  # noqa: E501
    """Bulk update of nested property

     # noqa: E501

    :param body:
    :type body: dict | bytes
    :param device_uuid:
    :type device_uuid: str
    :param key1:
    :type key1: str
    :param key2:
    :type key2: str

    :rtype: None
    """
    if connexion.request.is_json:
        body = connexion.request.get_json()  # noqa: E501
        device = BaseController.get_db_model(DeviceModel, 'uuid', device_uuid)
        for p1 in device.properties:
            if p1.value.key == key1:
                for p2 in p1.value.value:
                    if p2.value.key == key2:
                        PropertyModelSerializer().bulk_update(p2, body)
                        break
        device.save()
        return 'OK', 200
    return 'not ok', 404


@kafka_update(serializer=ModelSerializer)
def device_property_bulk_update(body, device_uuid, key):  # noqa: E501
    """Bulk update of property values

     # noqa: E501

    :param body:
    :type body: dict | bytes
    :param device_uuid:
    :type device_uuid: str
    :param key:
    :type key: str

    :rtype: None
    """
    
    if connexion.request.is_json:
        body = connexion.request.get_json()  # noqa: E501
        device = BaseController.get_db_model(DeviceModel, 'uuid', device_uuid)
        for p in device.properties:
            if p.value.key == key:
                PropertyModelSerializer().bulk_update(p, body)
                
                device.save()
                return 'OK', 200
    return 'not ok', 500


def get_device_attribute(device_uuid, attribute_name):  # noqa: E501
    """Get the attribute identified by attribute_name of this device

     # noqa: E501

    :param device_uuid:
    :type device_uuid: str
    :param attribute_name:
    :type attribute_name: str

    :rtype: object
    """
    device, code = get_device(device_uuid)
    if code >= 300:
        return device, code
    else:
        if attribute_name not in device:
            return "attribute %s not found on device %s" % (attribute_name, device), 404
        else:
            return device[attribute_name], 200


@kafka_update(serializer=ModelSerializer)
def set_device_attribute(device_uuid, attribute_name, body=None):  # noqa: E501
    """Set the attribute identified by attribute_name of this device

     # noqa: E501

    :param device_uuid:
    :type device_uuid: str
    :param attribute_name:
    :type attribute_name: str
    :param body:
    :type body: dict | bytes

    :rtype: DeviceModel
    """
    device = BaseController.get_db_model(DeviceModel, 'uuid', device_uuid)
    if not device:
        return "Device not found", 404
    swagger_model = device._swagger_model()
    try:
        result = ModelSerializer().update_attribute(device, swagger_model, attribute_name, body)
        if not result:
            return "Update failed", 404
    except Exception as e:
        return str(e), 500
    return get_device(device_uuid)


def get_device_property_attribute(device_uuid, key, attribute_name):  # noqa: E501
    """Get attribute_name of property of device

     # noqa: E501

    :param device_uuid:
    :type device_uuid: str
    :param key:
    :type key: str
    :param attribute_name:
    :type attribute_name: str

    :rtype: DevicePropertyModel
    """
    property = get_device_property(device_uuid, key)
    if property is {} or property is None:
        return "Property not found", 404
    if attribute_name not in property:
        return "Attribute %s not found on property %s" % (attribute_name, property)
    
    return property[attribute_name]


@kafka_update(serializer=ModelSerializer)
def set_device_property_attribute(device_uuid, key, attribute_name, body=None):  # noqa: E501
    """Get attribute_name of property of device

     # noqa: E501

    :param device_uuid:
    :type device_uuid: str
    :param key:
    :type key: str
    :param attribute_name:
    :type attribute_name: str
    :param body:
    :type body: dict | bytes

    :rtype: DevicePropertyModel
    """
    device = BaseController.get_db_model(DeviceModel, 'uuid', device_uuid)
    property = BaseController.get_list_item_of_db_model(device, 'properties', key, nested_path='value.key')
    try:
        result = PropertyModelSerializer().update_attribute(property, property._swagger_model(), attribute_name, body)
        device.save()
        if not result:
            return "Update failed", 500
    
    except Exception as e:
        return str(e), 500
    return get_device(device_uuid)


def get_device_location_attribute(device_uuid, attribute_name):  # noqa: E501
    """Get location of device

     # noqa: E501

    :param device_uuid:
    :type device_uuid: str
    :param attribute_name:
    :type attribute_name: str

    :rtype: object
    """
    device, code = get_device(device_uuid)
    if device['location'] is not None:
        if hasattr(device['location'], attribute_name):
            return device['location'][attribute_name], 200
    return 'not ok', 404


@kafka_update(serializer=ModelSerializer)
def set_device_location_attribute(body, device_uuid, attribute_name):  # noqa: E501
    """Set the attribute identified by attribute_name of this device location

     # noqa: E501

    :param body: A single value to set. Allowed are only string, number, boolean, and json objects. Lists are not supported.
    :type body: dict | bytes
    :param device_uuid:
    :type device_uuid: str
    :param attribute_name:
    :type attribute_name: str

    :rtype: InlineResponse200
    """
    device = BaseController.get_db_model(DeviceModel, 'uuid', device_uuid)
    location = device.location
    try:
        result = BaseModelSerializer().update_attribute(location, location._swagger_model(), attribute_name, body)
        device.save()
        if not result:
            return "Update failed", 500
    
    except Exception as e:
        return str(e), 500
    return get_device(device_uuid)
