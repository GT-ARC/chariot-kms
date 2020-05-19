import uuid

from swagger_server.models.base_model_kms import KMSModelMixin


class KMSHumanModel(KMSModelMixin):
    @property
    def url_keyword(self) -> str:
        return 'humans'
    
    @property
    def url_key(self) -> str:
        return 'uuid'
    
    defaults = {'uuid': (uuid.uuid4, {})}
