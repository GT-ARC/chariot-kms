import time

from mongoengine import LazyReferenceField

from swagger_server.models.base_model_kms import KMSModelMixin
from swagger_server.models.db_models.value_model import EmbeddedValueDocument, ValueDocumentList


def get_time():
    return time.time() * 1000


class KMSValuePropertyModel(KMSModelMixin):
    default = defaults = {'timestamp': (get_time, {})}
    
    # exclude_automated = ['value', 'timestamp']
    
    def update_model_specific_mongo_model(self, attribute_dict):
        attribute_dict = super(KMSValuePropertyModel, self).update_model_specific_mongo_model(attribute_dict)
        attribute_dict['value_list'] = LazyReferenceField(ValueDocumentList)
        return attribute_dict
    
    def write_manual(self, db_model):
        self.write_defaults()
        if db_model.value_list is None:
            value_list = ValueDocumentList()
            value_list = value_list.save()
            db_model.value_list = value_list
        
        document = EmbeddedValueDocument()
        document.timestamp = self.timestamp
        document.value = self.value
        value_list.values.append(document)
        value_list.save()
        return db_model
