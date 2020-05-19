from swagger_server.models.array_property_model import ArrayPropertyModel

from swagger_server.models.boolean_property_model import BooleanPropertyModel
from swagger_server.models.number_property_model import NumberPropertyModel
from swagger_server.models.string_list_property_model import StringListPropertyModel
from swagger_server.models.string_property_model import StringPropertyModel


class PropertyHelp(object):
    
    @classmethod
    def map_to_property_type(cls, _type, value=None):
        
        if _type == "array":
            if len(value) > 0:
                if type(value[0]) == str:
                    return StringListPropertyModel
            return ArrayPropertyModel
        elif _type == "string":
            return StringPropertyModel
        elif _type == "boolean":
            return BooleanPropertyModel
        elif _type == "number":
            return NumberPropertyModel
    
    @classmethod
    def nested_properties_from_dict(cls, properties_list_of_dicts, set_on_model, set_to_attr):
        properties = []
        for p in properties_list_of_dicts:
            property_type = PropertyHelp.map_to_property_type(p['_type'])
            property = property_type.from_dict(p)
            if type(property) is ArrayPropertyModel:
                cls.nested_properties_from_dict(p['value'], property, 'value')
            properties.append(property)
        setattr(set_on_model, set_to_attr, properties)
