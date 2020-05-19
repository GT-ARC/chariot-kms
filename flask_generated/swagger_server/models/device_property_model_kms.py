from swagger_server.models.property_model_mixin import KMSPropertyModelMixin


class KMSDevicePropertyModel(KMSPropertyModelMixin):
    exclude_automated = ['value']
