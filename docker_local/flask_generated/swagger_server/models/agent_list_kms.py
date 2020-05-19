from swagger_server.models.base_model_kms import KMSModelMixin


class AgentListKMS(KMSModelMixin):
    
    @property
    def url_keyword(self) -> str:
        return 'agentlist'
    
    @property
    def url_key(self) -> str:
        return '_id'
