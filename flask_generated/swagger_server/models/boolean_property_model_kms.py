from swagger_server.models.value_property_model import ValuePropertyModel

from swagger_server.models.value_property_model_kms import KMSValuePropertyModel


class KMSBooleanPropertyModel(KMSValuePropertyModel):
    super_db_class = ValuePropertyModel
    pass
