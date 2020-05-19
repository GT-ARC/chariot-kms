from swagger_server.models.property_model_mixin import KMSPropertyModelMixin


class KMSSkillPropertyModel(KMSPropertyModelMixin):
    exclude_automated = ['value']
