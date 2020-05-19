from mongoengine.base import EmbeddedDocumentList, LazyReference

from swagger_server.models.array_property_model import ArrayPropertyModel
from swagger_server.models.base_model_kms import KMSModelMixin
from swagger_server.models.db_models.property_help import PropertyHelp
from swagger_server.models.db_models.value_model import EmbeddedValueDocument
from swagger_server.serializer.base_model_serializer import BaseModelSerializer


class ValueSerializer(BaseModelSerializer):
    
    def __init__(self, *args, **kwargs):
        super(ValueSerializer, self).__init__(*args, **kwargs)
    
    def deserialize(self, db_model, exclude=None) -> dict:
        # last added value.
        result = {'value': db_model[-1].value, 'timestamp': db_model[-1].timestamp}
        return result


class ValuePropertyModelSerializer(BaseModelSerializer):
    '''
    for value properties (array, number, boolean, string)
    '''
    
    def __init__(self, *args, **kwargs):
        super(ValuePropertyModelSerializer, self).__init__(*args, **kwargs)
    
    def deserialize(self, db_model, exclude=[]) -> dict:
        
        if type(db_model) == EmbeddedDocumentList:
            result = []
            for p in db_model:
                prop = self.deserialize(p)
                result.append(prop)
            return result
        elif issubclass(db_model._swagger_model, ArrayPropertyModel):
            result = BaseModelSerializer(routing=self.routing).deserialize(db_model, ['value'])
            properties = []
            for p in db_model.value:
                properties.append(PropertyModelSerializer(routing=self.routing).deserialize(p))
            
            result['value'] = properties
            return result
        
        else:
            result = BaseModelSerializer(routing=self.routing).deserialize(db_model)
            return result
    
    def update(self, swagger_model: KMSModelMixin, existing_model, exclude=[]) -> bool:
        
        if issubclass(existing_model._swagger_model, ArrayPropertyModel):
            swagger_model.write_defaults()
            BaseModelSerializer().update(swagger_model, existing_model, exclude=['value'])
            for p_new in swagger_model.value:
                for i in range(len(existing_model.value)):
                    if p_new.value.key == existing_model.value[i].value.key:
                        PropertyModelSerializer().update(p_new, existing_model.value[i])
        else:
            swagger_model.write_defaults()
            
            BaseModelSerializer().update(swagger_model, existing_model)
            value = EmbeddedValueDocument()
            value.value = swagger_model.value
            value.timestamp = swagger_model.timestamp
            value_list = existing_model.value_list
            if isinstance(value_list, LazyReference):
                value_list = value_list.fetch()
            value_list.values.append(value)
            value_list.save()
        return True
    
    def get_history(self, property_db_model, value_field='value', timestamp_field='timestamp', length=None):
        
        if issubclass(property_db_model._swagger_model, ArrayPropertyModel):
            result = self.deserialize(property_db_model, exclude=['value'])
            result['value'] = []
            for p in property_db_model.value:
                _p = PropertyModelSerializer(self.routing).get_history(p, value_field, timestamp_field, length=length)
                result['value'].append(_p)
            return result
        else:
            result = self.deserialize(property_db_model, exclude=['value'])
            history = []
            data = property_db_model.value_list
            if isinstance(data, LazyReference):
                # resolve the reference if it hasn't happend yet
                data = data.fetch()
            values = None
            if length == None:
                values = data.values
            if length != None:
                values = data.values[(-1) * length:]
            for d in values:
                history.append({'x': d.timestamp, 'y': d.value})
            result['value'] = history
            return result


class PropertyModelSerializer(BaseModelSerializer):
    '''
    for properties such as deviceproperties, serviceproperties, etc.
    '''
    
    def __init__(self, *args, **kwargs):
        super(PropertyModelSerializer, self).__init__(*args, **kwargs)
    
    def deserialize(self, db_model, exclude=[]) -> dict:
        
        if type(db_model) == EmbeddedDocumentList:
            result = []
            for p in db_model:
                prop = self.deserialize(p)
                result.append(prop)
            return result
        else:
            # single property (e.g. deviceproperty=
            result = super(PropertyModelSerializer, self).deserialize(db_model, exclude=['value'], serializer_map={
                'value': ValuePropertyModelSerializer})
            
            result.update(result['value'])
            return result
    
    def update(self, swagger_model: KMSModelMixin, existing_model, exclude=[]) -> bool:
        if type(existing_model) == EmbeddedDocumentList:
            for p_new in swagger_model:
                for i in range(len(existing_model)):
                    if p_new.value.key == existing_model[i].value.key:
                        self.update(p_new, existing_model[i])
        else:
            swagger_model.write_defaults()
            
            BaseModelSerializer(routing=self.routing).update(swagger_model, existing_model, exclude=['value'])
            ValuePropertyModelSerializer(routing=self.routing).update(swagger_model.value, existing_model.value)
        
        return True
    
    def _serialize(self, model_klass, p: dict):
        # values:
        value_property_type = PropertyHelp.map_to_property_type(p['type'], value=p['value'])
        value_property = value_property_type.from_dict(p)
        if type(value_property) is ArrayPropertyModel:
            # serialize nested properties if there are json objects in the array. otherwise, it's a list of values
            if len(p['value']) > 0:
                if type(p['value'][0]) is dict:
                    value_property.value = self.serialize(model_klass, p['value'])
                else:
                    value_property.value = p['value']
        property_model = model_klass.from_dict(p)
        property_model.value = value_property
        return property_model
    
    def serialize(self, model_klass, json: []):
        if isinstance(json, list):
            return [self._serialize(model_klass, x) for x in json]
        if isinstance(json, dict):
            return self._serialize(model_klass, json)
    
    def get_history(self, property_db_model, value_field='value', timestamp_field='timestamp', length=None):
        result = None
        if type(property_db_model) == EmbeddedDocumentList:
            result = []
            for p in property_db_model:
                _p = self.get_history(p, length=length)
                result.append(_p)
            return result
        else:
            return ValuePropertyModelSerializer(routing=self.routing).get_history(property_db_model.value,
                                                                                  value_field, timestamp_field,
                                                                                  length=length)
    
    def bulk_update(self, property_db_model, values=[]):
        new_values = []
        for v in values:
            new = EmbeddedValueDocument()
            new.value = v['y']
            # new.timestamp = datetime.datetime.now()
            new.timestamp = v['x']
            new_values.append(new)
        
        value_list = property_db_model.value.value_list
        if isinstance(value_list, LazyReference):
            value_list = value_list.fetch()
        value_list.values.extend(new_values)
        value_list.save()
