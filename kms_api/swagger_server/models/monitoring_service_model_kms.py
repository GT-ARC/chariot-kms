from swagger_server.models.base_model_kms import KMSModelMixin


class MonitoringServiceModelKMS(KMSModelMixin):
    
    @property
    def url_keyword(self) -> str:
        '''
        will be prepended to the identifier.

        @return: None if the item should not be reachable by url
        '''
        return 'monitoringservice'
    
    @property
    def url_key(self) -> str:
        '''
        either an atomic property of the model, or (in dot-notation) an atomic property of a property (value.key)
        @return: None if the item should not be reachable by url
        '''
        return '_id'
