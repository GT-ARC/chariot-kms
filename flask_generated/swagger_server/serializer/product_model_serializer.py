from swagger_server.models.boolean_constraint_model import BooleanConstraintModel

from swagger_server.models.constraint_model import ConstraintModel
from swagger_server.models.number_constraint_model import NumberConstraintModel

from swagger_server.models.production_flow_item import ProductionFlowItem

from swagger_server.models.production_flow_item_property import ProductionFlowItemProperty
from swagger_server.models.production_info_boolean_item import ProductionInfoBooleanItem
from swagger_server.models.production_info_item import ProductionInfoItem
from swagger_server.models.production_info_number_item import ProductionInfoNumberItem
from swagger_server.models.production_info_string_item import ProductionInfoStringItem
from swagger_server.models.string_constraint_model import StringConstraintModel
from swagger_server.serializer.base_model_serializer import BaseModelSerializer
from swagger_server.serializer.model_serializer import ModelSerializer


class ProductModelSerializer(BaseModelSerializer):
    
    def __init__(self, *args, **kwargs):
        super(ProductModelSerializer, self).__init__(*args, **kwargs)
    
    def serialize(self, model_klass, json, property_klass=None):
        production_flow_data = json.pop('productionFlow')
        production_information_data = json.pop("productInfo")
        constraints = json.pop('constraints')
        result = super(self.__class__, self).serialize(model_klass, json)
        production_flow_ser = []
        for production_flow_item_raw in production_flow_data:
            production_flow_ser.append(ModelSerializer().serialize(ProductionFlowItem,
                                                                   production_flow_item_raw,
                                                                   ProductionFlowItemProperty))
        production_info_ser = []
        for production_info_item_raw in production_information_data:
            production_info_ser.append(
                ProductionInfoSerializer().serialize(ProductionInfoItem, production_info_item_raw))
        constraints_ser = []
        for constraint_raw in constraints:
            constraints_ser.append(ConstraintModelSerializer().serialize(ConstraintModel, constraint_raw))
        result.production_flow = production_flow_ser
        result.product_info = production_info_ser
        result.constraints = constraints_ser
        return result
    
    def deserialize(self, db_model, exclude=[]) -> dict:
        exclude.append('production_flow')
        result = super(ProductModelSerializer, self).deserialize(db_model, exclude,
                                                                 serializer_map={'productionFlow': ModelSerializer})
        
        return result


class ConstraintModelSerializer(BaseModelSerializer):
    def __init__(self):
        super(ConstraintModelSerializer, self).__init__()
    
    def serialize(self, model_klass, json: dict):
        type = self.model_decider(json['value'])
        result = type.from_dict(json)
        return result
    
    def model_decider(self, value):
        if type(value) is str:
            return StringConstraintModel
        if type(value) is int or type(value) is float:
            return NumberConstraintModel
        if type(value) is bool:
            return BooleanConstraintModel
        return None


class ProductionInfoSerializer(BaseModelSerializer):
    
    def __init__(self, *args, **kwargs):
        super(ProductionInfoSerializer, self).__init__(*args, **kwargs)
    
    def serialize(self, model_klass, json: dict):
        type = self.model_decider(json['value'])
        result = type.from_dict(json)
        return result
    
    def model_decider(self, value):
        if type(value) is str:
            return ProductionInfoStringItem
        if type(value) is int or type(value) is float:
            return ProductionInfoNumberItem
        if type(value) is bool:
            return ProductionInfoBooleanItem
        return None
