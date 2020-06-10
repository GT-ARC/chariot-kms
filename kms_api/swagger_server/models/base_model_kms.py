import json
import typing

import mongoengine
from bson import ObjectId
from mongoengine import EmbeddedDocumentField, EmbeddedDocumentListField, StringField, IntField, FloatField, \
    BooleanField, ObjectIdField, ListField
from mongoengine.base import BaseField


class KMSModelMixin(object):
    unique_fields = []
    defaults = {}  # dict mapping field -> (function, kwargs)
    exclude_automated = []  # exclude_automated values that need manual handling
    _collection_name = None
    _db_class = None
    super_db_class = None
    mongo_model = None

    def write_defaults(self):
        '''
        Writes default values for the defined attributes.
        @return: None
        '''
        for k, v in self.defaults.items():
            if getattr(self, k) == None:
                func, _kwargs = self.default[k]
                setattr(self, k, func(**_kwargs))

    def write_manual(self, db_model):
        '''
        Customize how the db_model is written. After the db_model is filled, this function is called. Can be used if there are differences between the structure of the swagger and db models
        @param db_model: db model instance
        @return: db model instance
        '''
        return db_model
    
    def get_inheritance(self):
        return True

    def write_mongo_model(self, db_model):
        '''
        Basically a serializer for the swagger_model -> mongo model conversion.
        Recursively going through the swagger definition and filliing the db_model with the swagger_model's values
        @param db_model: db_model instance
        @return: filled db_model
        '''
        self.write_defaults()
    
        for swagg_prop, v in self.swagger_types.items():
            # do not write fields that are a) special b) not there.
            if swagg_prop not in self.exclude_automated and getattr(self, swagg_prop) is not None:
                # check if the value to set is a model. if not, just write the atomic value.
                # if it is, write the embedded model
                db_prop = self.attribute_map[swagg_prop]
                if type(getattr(self.__class__.mongo_model, db_prop)) == EmbeddedDocumentField or type(
                        getattr(self.__class__.mongo_model, db_prop)) == EmbeddedDocumentListField:
                    if type(getattr(self.__class__.mongo_model, db_prop)) == EmbeddedDocumentField:
                        
                        embedded_model = getattr(self.__class__.mongo_model, db_prop).document_type
                        embedded_model = embedded_model()
                        embedded_model = embedded_model.from_json(json.dumps(getattr(self, swagg_prop).to_dict()))
                        setattr(db_model, db_prop, embedded_model)
                    elif type(getattr(self.__class__.mongo_model, db_prop)) == EmbeddedDocumentListField:
                        list = getattr(db_model, db_prop)
                        if getattr(self, swagg_prop) is not None:
                            for item in getattr(self, swagg_prop):  # for each property model (swagger)
                                embedded_model = item.get_mongo_model(embedded=True, inheritance=self.get_inheritance())
                                embedded_model = embedded_model()
                                item.write_mongo_model(embedded_model)
                                list.append(item.fill_db_model(embedded=True))
                
                elif type(getattr(self.__class__.mongo_model, db_prop)) == ListField and \
                        getattr(self, swagg_prop) is not None and \
                        len(getattr(self, swagg_prop)) > 0:
                    getattr(db_model, db_prop).extend(getattr(self, swagg_prop))
                else:
                    setattr(db_model, db_prop, getattr(self, swagg_prop))
        
        db_model = self.write_manual(db_model)
        return db_model

    def fill_db_model(self, embedded=False):
        '''
        fills the db_model with the swagger_model
        @return: a filled db_model instance
        '''
        db_model = self.get_mongo_model(embedded=embedded)
        model = db_model()
        # and write the current state
        model = self.write_mongo_model(model)
        return model

    def write_and_save(self):
        '''
        creates the db_model with the swagger_model and saves it to the db
        @return: saved model
        '''
        model = self.fill_db_model()
        model.save()
        return model

    def get_mongo_model(self, embedded=False, inheritance=False) -> type:
        '''
        python magic. Creates a mongoengine class programatically using type() and set Class.mongo_model if it does not exist
        This function assumes that the input has been validated.
        
        caveat: this only works if the model will always be generated with the same paramters, i.e. embedded and inheritance may not change
        @param embedded: is this model going to be part of another model in mongodb?
        @param inheritance: is this model going to have parent / child relations?
        @return: a new type. A mongoengine model that can be put into the db and can be used to get models from the db.
        '''
        
        if self.__class__.mongo_model is not None:
            return self.__class__.mongo_model
        superclass = self.get_db_model_superclass(embedded=embedded)
        attribute_dict = {}
        for k, v in self.swagger_types.items():
            attribute_dict[self.attribute_map[k]] = self.get_mongo_field_generic(v)
        # add _id field
        attribute_dict['_id'] = ObjectIdField(primary_key=True, default=ObjectId)
        attribute_dict['_swagger_model'] = self.__class__
        attribute_dict = self.update_model_specific_mongo_model(attribute_dict)
        # set the mongodb collection to be used for this model:
    
        attribute_dict['meta'] = {'collection': self.collection_name, 'allow_inheritance': inheritance}
        self.__class__.mongo_model = type(self.db_class, superclass, attribute_dict)
        return self.__class__.mongo_model

    def get_mongo_field_generic(self, swagger_type: type) -> BaseField:
        '''
        
        @param swagger_type: swagger_type from a swagger model's swagger_types
        @return: BaseField or one of its children
        '''
        if swagger_type == str:
            return StringField()
        elif swagger_type == int:
            return IntField()
        elif swagger_type == float:
            return FloatField()
        elif swagger_type == bool:
            return BooleanField()
        elif type(swagger_type) == type(typing.List):
            # atomic type:
            if swagger_type.__args__[0] == str or swagger_type.__args__[0] == int or swagger_type.__args__[0] == float:
                return ListField(self.get_mongo_field_generic(swagger_type.__args__[0]))
            else:
                list_item_type = swagger_type.__args__[0]().get_mongo_model(embedded=True, inheritance=True)
                model = EmbeddedDocumentListField(list_item_type)
                return model
        else:
            model = swagger_type().get_mongo_model(embedded=True)
            return EmbeddedDocumentField(model)

    def update_model_specific_mongo_model(self, attribute_dict: dict) -> dict:
        '''
        updates the mongo model specific to the model.
        For example, the property models should contain a list of value / timestamp pairs
        @return: an updated attribute dict
        '''
    
        # nothing to do here, but is necessary in children
        return attribute_dict

    @property
    def collection_name(self) -> str:
        '''
        Generate and set the name of the collection in mongodb. Store ind self.__class__._collection_name
        @return: The collection name
        '''
        if self.__class__._collection_name is None:
            self.__class__._collection_name = "col_" + str(self.__class__.__name__)
        return self.__class__._collection_name

    @property
    def db_class(self) -> str:
        '''
        Generate and set the name of the mongo model class. Store ind self.__class__._db_class
        usually:
        class Model():
        here:
        class _db_class():
        
        @return: The class name
        '''
        if self.__class__._db_class is None:
            self.__class__._db_class = "db_" + str(self.__class__.__name__)
        return self._db_class
    
    def get_db_model_superclass(self, embedded=False):
        '''
        returns the superclass of the db model to be created.
        @param embedded:
        @return:
        '''
        if self.super_db_class is None:
            if not embedded:
                return (mongoengine.Document,)
            else:
                return (mongoengine.EmbeddedDocument,)
        else:
            klass = self.super_db_class().get_mongo_model(embedded=embedded, inheritance=True)
            klass = (klass,)
            return klass
    
    @property
    def url_keyword(self) -> str:
        '''
        will be prepended to the identifier.
        
        @return: None if the item should not be reachable by url
        '''
        return None
    
    @property
    def url_key(self) -> str:
        '''
        either an atomic property of the model, or (in dot-notation) an atomic property of a property (value.key)
        @return: None if the item should not be reachable by url
        '''
        return None
