from swagger_server.models.property_model_mixin import KMSPropertyModelMixin


class KMSTaskPropertyModel(KMSPropertyModelMixin):
    exclude_automated = ['value']
