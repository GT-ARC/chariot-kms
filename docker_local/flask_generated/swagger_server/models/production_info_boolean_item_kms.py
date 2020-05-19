from swagger_server.models.base_model_kms import KMSModelMixin
from swagger_server.models.production_info_item import ProductionInfoItem


class KMSProductionInfoBooleanItem(KMSModelMixin):
    super_db_class = ProductionInfoItem
