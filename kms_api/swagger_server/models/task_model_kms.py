from swagger_server.models.base_model_kms import KMSModelMixin


class KMSTaskModel(KMSModelMixin):
    
    @property
    def url_key(self) -> str:
        return 'uuid'
    
    @property
    def url_keyword(self) -> str:
        return 'tasks'
