from swagger_server.models.base_model_kms import KMSModelMixin
from swagger_server.models.constraint_model import ConstraintModel


class KMSBooleanConstraintModel(KMSModelMixin):
    super_db_class = ConstraintModel
