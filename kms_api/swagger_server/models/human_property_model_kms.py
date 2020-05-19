from swagger_server.models.property_model_mixin import KMSPropertyModelMixin


class KMSHumanPropertyModel(KMSPropertyModelMixin):
    exclude_automated = ['value']
