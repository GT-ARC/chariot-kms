from mongoengine import EmbeddedDocumentField

from swagger_server.models.base_model_kms import KMSModelMixin
from swagger_server.models.value_property_model import ValuePropertyModel


class KMSPropertyModelMixin(KMSModelMixin):
    
    @property
    def url_keyword(self) -> str:
        return 'properties'
    
    @property
    def url_key(self) -> str:
        return 'value.key'
    
    def update_model_specific_mongo_model(self, attribute_dict):
        attribute_dict = super(KMSPropertyModelMixin, self).update_model_specific_mongo_model(attribute_dict)
        # add .value for the list of value properties
        m = ValuePropertyModel().get_mongo_model(embedded=True, inheritance=True)
        m = EmbeddedDocumentField(m)
        attribute_dict['value'] = m
        return attribute_dict
    
    def write_manual(self, db_model):
        db_model.value = self.value.fill_db_model(embedded=True)
        
        return db_model
    
    def get_inheritance(self):
        return False
