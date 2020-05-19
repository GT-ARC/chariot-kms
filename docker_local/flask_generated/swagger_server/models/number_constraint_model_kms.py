from swagger_server.models.base_model_kms import KMSModelMixin
from swagger_server.models.constraint_model import ConstraintModel


class KMSNumberConstraintModel(KMSModelMixin):
    super_db_class = ConstraintModel
