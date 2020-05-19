from swagger_server.models.base_model_kms import KMSModelMixin


class KMSProductionInfoItem(KMSModelMixin):
    
    def write_manual(self, db_model):
        self.write_defaults()
        db_model.name = self.name
        db_model.value = self.value
        return db_model
