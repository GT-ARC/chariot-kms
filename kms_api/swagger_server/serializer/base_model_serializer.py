import json
import typing

from bson import ObjectId
from mongoengine.base import EmbeddedDocumentList, BaseDocument

from swagger_server.controllers.routing import RoutingInformation
from swagger_server.models.base_model_ import Model
from swagger_server.models.base_model_kms import KMSModelMixin


class BaseModelSerializer(object):
    '''
    Base Serializer for Models.
    '''
    
    def __init__(self, routing: RoutingInformation = None):
        '''
        @param routing: A routing object containing the routes to the current level of the db_model
        @param url_base: a url path that leads to the parent resource
        '''
        super(BaseModelSerializer, self).__init__()
        self.routing = routing
    

    
    def deserialize(self, db_model, exclude=[], serializer_map: dict = {}) -> dict:
        '''
        DB Model -> Swagger Model.
        Recursively deserializes attributes of db_model using the stored swagger_model's attribute_map
        @param db_model: mongoengine db_model
        @param exclude: a list of fields that are present in the swagger_types of the swagger models, that should be ignored by the serializer.
        @param serializer_map: a mapping of attributes -> serializer classes. If you want a specific serializer for an attribute, use this.
        
        @return: dictionary that is parsable by the swagger_model.from_dict() functions
        '''
        result = {}
        # some of the nested objects are not required. Don't try to deserialize those objects
        if db_model is None:
            return None
        
        attribute_map = db_model._swagger_model().attribute_map
        exclude.append('kafka_topic')
        exclude.append('url')
        
        self.update_routing(db_model._swagger_model(), db_model, result)
        
        # deserialize
        for swagg_prop, t in db_model._swagger_model().swagger_types.items():
            # print("Desierializing %s %s" % (str(swagg_prop), str(t)))
            # k is the attribute, v is the type
            if swagg_prop not in exclude and (
                    hasattr(db_model, swagg_prop) or hasattr(db_model, attribute_map[swagg_prop])) \
                    and swagg_prop not in serializer_map:
                db_prop = attribute_map[swagg_prop]
                if type(t) == type(typing.List):
                    list = []
                    for item in getattr(db_model, db_prop):
                        if type(item) == str or type(item) == int:
                            list.append(item)
                        else:
                            list.append(self.deserialize(item))
                    result[db_prop] = list
                elif issubclass(t, Model):
                    result[db_prop] = BaseModelSerializer(routing=self.routing).deserialize(
                        getattr(db_model, db_prop))
                elif isinstance(getattr(db_model, db_prop), ObjectId):
                    result[db_prop] = str(getattr(db_model, db_prop))
                else:
                    result[db_prop] = getattr(db_model, db_prop)
        for att, serializer in serializer_map.items():
            if hasattr(db_model, att):
                if type(getattr(db_model, att)) is EmbeddedDocumentList:
                    result[att] = [serializer(routing=self.routing).deserialize(item) for item in
                                   getattr(db_model, att)]
                else:
                    result[att] = serializer(routing=self.routing).deserialize(getattr(db_model, att))
        self.routing.up()
        return result
    
    def update(self, swagger_model: KMSModelMixin, existing_model, exclude=[]) -> bool:
        '''
        
        @param swagger_model: new db_model
        @param existing_model: existing db_model parsed from db
        @param exclude: list of fields that should be excluded
        @return: boolean value success / no success
        '''
        for swagg_prop, t in swagger_model.swagger_types.items():
            db_prop = swagger_model.attribute_map[swagg_prop]
            if swagg_prop not in exclude and hasattr(swagger_model, swagg_prop) and hasattr(existing_model, db_prop):
                if issubclass(t, Model):
                    self.update(getattr(swagger_model, swagg_prop),
                                getattr(existing_model, db_prop))
                elif isinstance(getattr(existing_model, db_prop), ObjectId):
                    continue
                
                else:
                    setattr(existing_model,
                            db_prop,
                            getattr(swagger_model, swagg_prop))
        return True
    
    def update_attribute(self, db_model, swagger_model: Model, attribute_name, byte_value):
        '''
        update specific attribute of a model.
        @param db_model: db model instance
        @param swagger_model: swagger model instance
        @param attribute_name: name of the attribute to update
        @param byte_value: the value to put. will be typecasted to whatever the swagger model says it should be.
        @return: boolean success or no
        '''
        if attribute_name in swagger_model.swagger_types:
            value = byte_value.decode('utf-8')
            mongo_value = None
            if value.startswith('{') and value.endswith('}'):
                mongo_value = swagger_model.swagger_types[attribute_name].from_dict(json.loads(value))
            else:
                mongo_value = swagger_model.swagger_types[attribute_name](value)
            try:
                if not isinstance(mongo_value, Model):
                    setattr(db_model, swagger_model.attribute_map[attribute_name], mongo_value)
                else:
                    self.update(mongo_value, getattr(db_model, attribute_name))
                if db_model._is_document:
                    db_model.save()
            except Exception as e:
                raise
            return True
        return False
    
    def serialize(self, model_klass: type, json: dict) -> Model:
        '''
        
        @param model_klass: db_model class that should be used to serialize the data
        @param json: json containing the data to serialize
        @return: a db_model
        '''
        result = model_klass.from_dict(json)
        return result
    
    def update_routing(self, _swagger_model: Model, db_model: BaseDocument, deserialized: dict) -> None:
        '''
        Updates the routing information object with current path
        @param _swagger_model: the model that should be appended to the path
        @param db_model: the db model that should be appended to the path
        @param deserialized: deserilized json. url + kafka topic will be set on this
        @return: None
        '''
        key = _swagger_model.url_key
        result = ""
        if key is None:
            result = ""
            self.routing.add(result)
            return
        else:
            
            path = _swagger_model.url_key.split(".")
            url_key_value = db_model
            for p in path:
                url_key_value = getattr(url_key_value, p)
            result = ("%s/%s/" % (_swagger_model.url_keyword, url_key_value))
            self.routing.add(result)
            self.routing.urlize(deserialized)
            return
    
    def get_history(self, db_model, serializer_map={}):
        """

        @param db_model: the model to generate the history of @param serializer_map: a map mapping attribute ->
        serializer class. for these attributes, serilizer().get_history(model[attribute]) will be called @return:
        """
        # result = self.deserialize(db_model, exclude=list(serializer_map.keys()))
        # for attribute, serializer in serializer_map.items():
        #     if hasattr(db_model, attribute):
        #         v = db_model[attribute]
        #         if type(v) is list or type(v) is EmbeddedDocumentList:
        #             result['attribute'] = [serializer(self.routing).get_history(x, serializer_map=serializer_map) for x in v]
        #         else:
        #             result['attribute'] = serializer(self.routing).get_history(v, serializer_map=serializer_map)
        #
        # return result
        
        # TODO
