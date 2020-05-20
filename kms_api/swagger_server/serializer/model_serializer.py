from swagger_server.models.base_model_kms import KMSModelMixin
from swagger_server.serializer.base_model_serializer import BaseModelSerializer
from swagger_server.serializer.property_model_serializer import PropertyModelSerializer


class ModelSerializer(BaseModelSerializer):
    
    def __init__(self, *args, **kwargs):
        super(ModelSerializer, self).__init__(*args, **kwargs)
    
    def deserialize(self, db_model, exclude=[]) -> dict:
        print("Desierlializing %s " % (type(db_model)))
        exclude.append('properties')
        result = super(ModelSerializer, self).deserialize(db_model, exclude,
                                                          serializer_map={'properties': PropertyModelSerializer})
        
        return result
    
    def update(self, swagger_model: KMSModelMixin, existing_model, exclude=[]) -> bool:
        exclude.append('properties')
        BaseModelSerializer().update(swagger_model, existing_model, exclude)
        PropertyModelSerializer().update(swagger_model.properties, existing_model.properties)
        existing_model.save()
        
        return True
    
    def serialize(self, model_klass, json, property_klass=None):
        properties_data = json.pop('properties')
        result = super(self.__class__, self).serialize(model_klass, json)
        result.properties = PropertyModelSerializer().serialize(property_klass, properties_data)
        return result
