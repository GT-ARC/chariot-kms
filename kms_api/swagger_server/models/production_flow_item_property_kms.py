from swagger_server.models.property_model_mixin import KMSPropertyModelMixin


class KMSProductionFlowItemProperty(KMSPropertyModelMixin):
    exclude_automated = ['value']
