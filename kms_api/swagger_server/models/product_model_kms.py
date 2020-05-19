import uuid

from swagger_server.models.base_model_kms import KMSModelMixin


class KMSProductModel(KMSModelMixin):
    
    @property
    def url_keyword(self) -> str:
        return 'products'
    
    @property
    def url_key(self) -> str:
        return 'uuid'
    
    defaults = {'uuid': (uuid.uuid4, {})}
