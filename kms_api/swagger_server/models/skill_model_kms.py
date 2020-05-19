import uuid

from swagger_server.models.base_model_kms import KMSModelMixin


class KMSSkillModel(KMSModelMixin):
    defaults = {'uuid': (uuid.uuid4, {})}
    
    @property
    def url_key(self) -> str:
        return 'uuid'
    
    @property
    def url_keyword(self) -> str:
        return 'skills'
