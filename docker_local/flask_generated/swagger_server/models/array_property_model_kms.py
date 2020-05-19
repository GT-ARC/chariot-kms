from swagger_server.models.value_property_model import ValuePropertyModel
from swagger_server.models.value_property_model_kms import KMSValuePropertyModel


class KMSArrayPropertyModel(KMSValuePropertyModel):
    exclude_automated = []
    super_db_class = ValuePropertyModel
    
    def update_model_specific_mongo_model(self, attribute_dict):
        return attribute_dict
    
    def write_manual(self, db_model):
        return db_model
