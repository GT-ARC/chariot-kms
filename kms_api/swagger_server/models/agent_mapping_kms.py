from swagger_server.models.base_model_kms import KMSModelMixin


class AgentMappingKMS(KMSModelMixin):
    
    @property
    def url_keyword(self) -> str:
        return 'mappings'
    
    @property
    def url_key(self) -> str:
        return '_id'
