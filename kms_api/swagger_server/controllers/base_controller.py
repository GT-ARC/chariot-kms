import logging
import traceback
from functools import wraps

from swagger_server.controllers.routing import RoutingInformation
from swagger_server.kafka.kafka_producer import LocalKafkaProducer
from swagger_server.models.base_model_ import Model
from swagger_server.serializer.model_serializer import ModelSerializer
from swagger_server.serializer.property_model_serializer import PropertyModelSerializer


def _publish_kafka(model: dict, topic: str) -> None:
    '''
    @param model: Model to push to kafka
    @param topic: Topic to push to
    @return: None
    @raise  ValueError when msg or topic are missing
    '''
    if model is not None and topic is not None:
        LocalKafkaProducer().add_to_queue(model, topic)
    else:
        err = "Msg or topic not given model: %s // topic: %s" % (str(model), str(topic))
        logging.ERROR(err)
        raise ValueError(err)


def publish_kafka(msg, topic=None):
    '''
    
    @param msg: dict that should be sent. Can contain nested dicts with their own kafka topics (i.e. devices that have properties)
    @param topic: if set, forces sending on this topic, otherwise looks for kafka_topic in the model
    @return: None
    '''
    
    if topic is not None:
        _publish_kafka(msg, topic)
        return
    if 'kafka_topic' in msg and type(msg) is dict:
        _publish_kafka(msg, msg['kafka_topic'])
    
    # go into the model and check for nested models that should be send through kakfa. E.g. properties
    # do this only for objects (i.e. dicts):
    if type(msg) is not dict:
        # recursion hook
        return
    for k, v in msg.items():
        if type(v) == dict:
            publish_kafka(v)
        if type(v) == list:
            for item in v:
                publish_kafka(item)


def kafka_update(serializer=None):
    def kafka_update_decorator(func):
        """
        
        @param serializer: must be given if the decorated function does not return a deserialized object, but rather
        a mongo db_model @return: a decorator pushing the result of the function to kafka
        """
        
        @wraps(func)
        def kafka_update_wrapper(*args, **kwargs):
            res, code = func(*args, **kwargs)
            if code >= 300 or code < 200:
                print("Error, not sending through Kafka")
                return res, code
            if isinstance(res, Model):
                ser = serializer().deserialize(res)
                publish_kafka(ser)
            elif type(res) == dict:
                publish_kafka(res)
            
            return res, code
        
        return kafka_update_wrapper
    
    return kafka_update_decorator


def kafka_add(serializer=None, endpoint=""):
    '''
    
    @param serializer:
    @param endpoint: endpoint where this object is added (devices, services, etc.)
    @return:
    '''
    
    def kafka_add_decorator(func):
        @wraps(func)
        def kafka_add_wrapper(*args, **kwargs):
            if serializer is None:
                res, code = func(*args, **kwargs)
                if code >= 300:
                    return res, code
                publish_kafka(res, topic='kms.global.' + endpoint)
                
                return res, code
            else:
                res, code = func(*args, **kwargs)
                if code >= 300:
                    return res, code
                publish_kafka(res, topic='kms.global.' + endpoint)
                return res, code
        
        return kafka_add_wrapper
    
    return kafka_add_decorator


class BaseController(object):
    
    def __init__(self):
        super(BaseController, self).__init__()

    @staticmethod
    def add_model_with_properties(json, swagger_model_class, property_model_class, unique_field, serializer):
        '''
        
        @param json: json to serialize
        @param swagger_model_class: swagger class to use for serialization
        @param property_model_class: the class of properties within the model
        @param unique_field: the identifier field of the model (to check for duplicates)
        @param serializer: the serializer class to use to serialize the model
        
        @return: detail view of the model
        '''
        if unique_field not in json or BaseController.get_db_model(swagger_model_class, unique_field,
                                                                   json[unique_field]) is not None:
            return "UUID not present or device with uuid exists", 400
        swagger_object = serializer().serialize(swagger_model_class, json, property_model_class)
        model = swagger_object.write_and_save()
        return BaseController.get_detail_view(swagger_model_class, serializer, unique_field,
                                              getattr(swagger_object, unique_field))
    
    @staticmethod
    def get_db_model(swagger_class, identifier_field, identifier_value):
        '''
        # retrieves a model from the db.
        @param swagger_class: swagger db_model class to use
        @param identifier_field: field to use as filter (e.g. 'uuid')
        @param identifier_value: value to search for
        @return: a single db object if query returns exactly one result. If no results were found, returns None,
         if more than one result, raises ValueException
        '''
        result = swagger_class().get_mongo_model().objects.filter(__raw__={identifier_field: identifier_value})
        if len(result) == 0:
            return None
        if len(result) > 1:
            raise ValueError("{%s:%s} query returns more than one result" % (identifier_field, identifier_value))
        return result.get()
    
    @staticmethod
    def get_list_item_of_db_model(model, list_attribute, list_filter_value, nested_path):
        '''
        retrieves an item in a list of a db model.
        @param nested_path: attribute path to the field that is applied as filter. e.g. value.key, key, etc.
        @param model: the db_model the list is in
        @param list_attribute: the name of the db_model's attribute that stores the list
        @param list_filter_value: the value to look for
        @return: None if the value could not be found, or the value / object if found.
        '''
        if hasattr(model, list_attribute):
            for item in getattr(model, list_attribute):
                result = item
                path = nested_path.split(".")
                for p in path:
                    item = getattr(item, p)
                
                if item == list_filter_value:
                    return result
        return None
    
    @staticmethod
    def delete_list_item_of_db_model(model, list_attribute, list_filter_value, nested_path):
        '''
        Delete an item in a list on a model
        @param nested_path: attribute path to the field that is applied as filter. e.g. value.key, key, etc.
        @param model: the db_model the list is in
        @param list_attribute: the name of the db_model's attribute that stores the list
        @param list_filter_value: the value to look for
        @return: None if the value could not be found, or the value / object if found.
        '''
        path = nested_path.split(".")
        if hasattr(model, list_attribute):
            list = getattr(model, list_attribute)
            found = -1
            for i in range(0, len(list)):
                item = list[i]
                for p in path:
                    item = getattr(item, p)
                    if item == list_filter_value:
                        result = list.pop(i)
                        model.save()
                        return result, 200
        
        return None, 404
    
    @staticmethod
    def delete_model(swagger_model, identifier_field, identifier_field_value):
        '''
        
        @param swagger_model: db model (db_deviceModel, for example)
        @param identifier_field: the field that uniquely identifies the item to delete (_id, uuid)
        @param identifier_field_value: the value of the identifier field
        @return:
        '''
    
        db_model = BaseController.get_db_model(swagger_model, identifier_field, identifier_field_value)
        if db_model is not None:
            db_model.delete()
            return "OK", 200
        else:
            return "Not found", 404

    @staticmethod
    def get_nested_list_item(db_model, list_name, list_item_identifier_field, list_item_identifier_value):
        '''
        Get item in list on an object. Works on both Swagger/DB Models (in fact, any object works).
        Just makes the code easier to read.
        @param db_model:  db db_model (db_deviceModel, for example), must be instance
        @param list_name: db db_model attribute name with list
        @param list_item_identifier_field: identifier for filtering the list items
        @param list_item_identifier_value: identifier field value to look for
        @return: the item, if found. None if not
        '''
        
        if hasattr(db_model, list_name):
            for item in getattr(db_model, list_name):
                if getattr(item, list_item_identifier_field) == list_item_identifier_value:
                    return item
        return None

    @staticmethod
    def _delete_property_history(property, retain_values=None):
        '''
        Similar to delete_property_history, but working directly on the db model
        @param property: db model of the property
        @param retain_values: number of values that are to be retained (i.e. delete everything but the latest n values)
        @return: None
        '''
        list = property.value.value_list.fetch()
        if retain_values is None:
            list.values = []
        else:
            list.values = list.values[((-1) * retain_values):]
        list.save()
        return

    @staticmethod
    def delete_property_history(swagger_model_klass, uuid, key, retain_values=None):
        '''
        Calls _delete_property_history, but we need the db model first
        @param swagger_model_klass: swagger model holding the property (e.g. a device)
        @param uuid: uuid of the model (e.g. a device)
        @param key: the key of the property
        @param retain_values: number of values that are to be retained (i.e. delete everything but the latest n values)
        @return: HTTP
        '''
        db_model = BaseController.get_db_model(swagger_model_klass, 'uuid', uuid)
        for property in db_model.properties:
            if property.value.key == key:
                try:
                    BaseController._delete_property_history(property, retain_values=retain_values)
                    db_model.save()
                except:
                    return "Not ok", 500
            else:
                return "Property not found", 404
        return "OK", 200

    @staticmethod
    def delete_model_history(swagger_model_klass, uuid, retain_values=None):
        '''
        Delete history of all properties of the model.
        @param swagger_model_klass:  swagger model class of the model we're looking for (e.g. a device)
        @param uuid: uuid of the model
        @param retain_values: number of values that are to be retained (i.e. delete everything but the latest n values)
        @return: HTTP
        '''
    
        db_model = BaseController.get_db_model(swagger_model_klass, 'uuid', uuid)
        for property in db_model.properties:
            BaseController._delete_property_history(property, retain_values=retain_values)
        return "OK", 200
    
    @staticmethod
    def get_list_view(swagger_model_class, serializer):
        '''
        Returns a list of deserialized models. Models of type swagger_model_class are taken from the db and are put
        through serializer.
        @param swagger_model:
        @param serializer:
        @return: list of json objects + code / error + code
        '''
        
        result = []
        models = swagger_model_class().get_mongo_model().objects.all()
        
        try:
            for model in models:
                result.append(serializer(routing=RoutingInformation.create_root_routing_object()).deserialize(model))
            return result, 200
        except Exception as e:
            return "%s" % e, 500
    
    @staticmethod
    def get_detail_view(swagger_model_class, serializer, identifier_field, identifier_value):
        '''
        get a json object for a specific model
        @param swagger_model_class: swagger_model to search for
        @param serializer: serializer class to use to deserialize the found object
        @param identifier_field: identifier to look for
        @param identifier_value: identifier field value to look for
        @return: single json object + code / error + code
        '''
        
        model = BaseController.get_db_model(swagger_model_class, identifier_field, identifier_value)
        
        if model is not None:
            try:
                return serializer(routing=RoutingInformation.create_root_routing_object()).deserialize(model), 200
            except Exception as e:
                return "%s" % e, 500
        else:
            return "Model not found", 404
    
    @staticmethod
    def get_nested_list_item_with_route(db_model, swagger_list_field, swagger_list_item_search_field,
                                        swagger_list_item_search_value, serializer, nested_path=[]):
        '''
        searches a json model for a nested list item
        @param swagger_model:
        @param db_id_field:
        @param db_id_value:
        @param db_list_field:
        @param db_list_item_search_field:
        @param db_list_item_search_value:
        @param nested_path:
        @param serializer:
        @return:
        '''
        model = serializer(routing=RoutingInformation.create_root_routing_object()).deserialize(db_model)
        list = model[swagger_list_field]
        found = None
        for item in list:
            nested = item
            for p in nested_path:
                nested = nested[p]
            if nested[swagger_list_item_search_field] == swagger_list_item_search_value:
                found = item
                break
        return found, 200
    
    @staticmethod
    def update_model_with_properties(model_swagger_klass: type, json, property_swagger_klass: type, uuid, run_after):
        '''
        Updates a model with properties.
        @param model_swagger_klass: Swagger class of the model to be updated (DeviceModel, TaskModel, etc)
        @param json: what the generated controllers call 'body'. A string that contains the data in json format
        @param property_swagger_klass: the property class of the model's properties (i.e. DevicePropertyModel, TaskPropertyMOdel, etc)
        @param uuid: the uuid of the model
        @param run_after: the function that should be called after. The function is invoked with the given uuid. Normally, you'd want to return the updated model detail view.
        
        @return:  An error message if the update fails, the result of the 'run_after' function if not.
        '''
        # serializer
        new_model = ModelSerializer().serialize(model_swagger_klass, json, property_swagger_klass)
        # get from db
        old_model = BaseController.get_db_model(model_swagger_klass, 'uuid', uuid)
        
        if old_model is None:
            return "Model not found", 404
        try:
            ModelSerializer().update(new_model, old_model)
            return run_after(uuid)
        except Exception as e:
            traceback.print_exc()
            return "Update failed: %s" % e, 400
    
    @staticmethod
    def update_model_property(model_swagger_klass: type, json, property_swagger_klass: type, uuid, key, run_after):
        '''
        Updates a model with properties.
        @param model_swagger_klass: Swagger class of the model to be updated (DeviceModel, TaskModel, etc)
        @param json: what the generated controllers call 'body'. A string that contains the data in json format
        @param property_swagger_klass: the property class of the model's properties (i.e. DevicePropertyModel, TaskPropertyMOdel, etc)
        @param uuid: the uuid of the model
        @param key: the key to look for in the list of properties (this works under the assumption that all properties have a 'key' field)
        @param run_after: the function that should be called after. The function is invoked with the given uuid. Normally, you'd want to return the updated model detail view.

        @return:  An error message if the update fails, the result of the 'run_after' function if not.
        '''
        property = PropertyModelSerializer().serialize(property_swagger_klass, json)
        model = BaseController.get_db_model(model_swagger_klass, 'uuid', uuid)
        for p in model.properties:
            if p.value.key == key:
                PropertyModelSerializer().update(property, p)
                model.save()
                return run_after(uuid, key)
        return "Property could not be updated", 400
