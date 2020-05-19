from swagger_server.models.property_model_mixin import KMSPropertyModelMixin


class KMSServicePropertyModel(KMSPropertyModelMixin):
    exclude_automated = ['value']
