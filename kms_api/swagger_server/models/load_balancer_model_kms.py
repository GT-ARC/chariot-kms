from swagger_server.models.base_model_kms import KMSModelMixin


class LoadBalancerModelKMS(KMSModelMixin):
    
    @property
    def url_keyword(self) -> str:
        return 'loadbalancer'
    
    @property
    def url_key(self) -> str:
        return '_id'
