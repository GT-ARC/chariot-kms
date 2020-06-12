import logging

import connexion
from flask_cors import CORS
from flask_debug import Debug
from flask_mongoengine import MongoEngine

from swagger_server import encoder
from swagger_server.models import ServiceModel, ServicePropertyModel, OperationModel, PositionValue, LocationProperty, \
    IndoorPositionValue, DevicePropertyModel, NumberPropertyModel, BooleanPropertyModel, ArrayPropertyModel, \
    StringPropertyModel, SkillModel
from swagger_server.models.agent_list import AgentList
from swagger_server.models.boolean_constraint_model import BooleanConstraintModel
from swagger_server.models.constraint_model import ConstraintModel
from swagger_server.models.device_model import DeviceModel
from swagger_server.models.load_balancer_model import LoadBalancerModel
from swagger_server.models.monitoring_service_model import MonitoringServiceModel
from swagger_server.models.number_constraint_model import NumberConstraintModel
from swagger_server.models.product_model import ProductModel
from swagger_server.models.production_flow_item import ProductionFlowItem
from swagger_server.models.production_flow_item_property import ProductionFlowItemProperty
from swagger_server.models.production_info_boolean_item import ProductionInfoBooleanItem
from swagger_server.models.production_info_item import ProductionInfoItem
from swagger_server.models.production_info_number_item import ProductionInfoNumberItem
from swagger_server.models.production_info_string_item import ProductionInfoStringItem
from swagger_server.models.string_constraint_model import StringConstraintModel
from swagger_server.models.string_list_property_model import StringListPropertyModel
from swagger_server.models.task_model import TaskModel
from swagger_server.models.task_property_model import TaskPropertyModel
from swagger_server.models.value_property_model import ValuePropertyModel


class ModelLoader(object):
    
    def _import(self):
        '''
        the dynamic class need to be registered with mongoengine. Normally, this happens on import, but we're not
        importing them...
        @return: None
        '''
        
        ValuePropertyModel().get_mongo_model(embedded=True, inheritance=True)
        ArrayPropertyModel().get_mongo_model(embedded=True, inheritance=True)
        StringListPropertyModel().get_mongo_model(embedded=True, inheritance=True)
        BooleanPropertyModel().get_mongo_model(embedded=True, inheritance=True)
        NumberPropertyModel().get_mongo_model(embedded=True, inheritance=True)
        StringPropertyModel().get_mongo_model(embedded=True, inheritance=True)
        DevicePropertyModel().get_mongo_model(embedded=True)
        
        IndoorPositionValue().get_mongo_model(embedded=True)
        LocationProperty().get_mongo_model(embedded=True)
        PositionValue().get_mongo_model(embedded=True)
        
        OperationModel().get_mongo_model(embedded=True)
        
        ServicePropertyModel().get_mongo_model(embedded=True)
        
        DeviceModel().get_mongo_model()
        ServiceModel().get_mongo_model()
        SkillModel().get_mongo_model()
        
        LoadBalancerModel().get_mongo_model(embedded=True)
        AgentList().get_mongo_model(embedded=True)
        MonitoringServiceModel().get_mongo_model()
        
        ConstraintModel().get_mongo_model(embedded=True, inheritance=True)
        NumberConstraintModel().get_mongo_model(embedded=True, inheritance=True)
        BooleanConstraintModel().get_mongo_model(embedded=True, inheritance=True)
        StringConstraintModel().get_mongo_model(embedded=True, inheritance=True)
        
        ProductionInfoStringItem().get_mongo_model(embedded=True, inheritance=True)
        ProductionInfoNumberItem().get_mongo_model(embedded=True, inheritance=True)
        ProductionInfoBooleanItem().get_mongo_model(embedded=True, inheritance=True)
        ProductionInfoItem().get_mongo_model(embedded=True, inheritance=True)
        ProductionFlowItemProperty().get_mongo_model(embedded=True)
        ProductionFlowItem().get_mongo_model(embedded=True)
        ProductModel().get_mongo_model()
        
        TaskPropertyModel().get_mongo_model(embedded=True, inheritance=True)
        TaskModel().get_mongo_model()


def get_app(production=True):
    app = connexion.App(__name__, specification_dir='swagger/')
    app.app.json_encoder = encoder.JSONEncoder

    app.app.config['MONGODB_DB'] = 'admin'
    app.app.config['MONGODB_HOST'] = 'mongo'
    app.app.config['MONGODB_PORT'] = 27017
    app.app.config['MONGODB_USERNAME'] = 'root'
    app.app.config['MONGODB_PASSWORD'] = 'example'
    app.add_api('swagger.yaml', arguments={'title': 'kms'}, pythonic_params=True)
    MongoEngine(app.app)
    CORS(app.app)
    model_loader = ModelLoader()
    model_loader._import()
    log = logging.getLogger('werkzeug')

    if not production:
        Debug(app.app)
        app.app.config['DEBUG'] = True
        log.setLevel(logging.INFO)
    else:
        app.app.config['DEBUG'] = False
        log.setLevel(logging.ERROR)
    
    return app


if __name__ == '__main__':
    # this is only done when running a single instance of the server in devevelopment. Gunicorn deployment does not
    # go here.
    print("in main ######")
    app = get_app(production=False)
    app.run(port=8080, debug=True, threaded=True)
