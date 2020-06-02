This page describes how to add, handle, and extend a model to the KMS API.

In the end, the following model will be ready to be used:

```
{
    "objectType": "vehicle",
    "uuid": "{{current_uuid}}",
    "name": "new_vehicle",
    "properties": [
        {
            "key": "property_name",
            "type": "string",
            "value": "this is the value",
            "timestamp": 1
        },
        {
            "key": "numberproperty",
            "type": "number",
            "value": 1,
            "timestamp": 1
        },
        {
            "key": "booleanproperty",
            "type": "boolean",
            "value": true,
            "timestamp": 1
        },
        {
            "key": "stringlist",
            "type": "array",
            "value": [
                "a",
                "b"
            ],
            "timestamp": 1
        },
        {
            "key": "compoundproperty",
            "type": "array",
            "value": [
                {
                    "key": "property_name",
                    "type": "string",
                    "value": "this is the value",
                    "timestamp": 1
                },
                {
                    "key": "numberproperty",
                    "type": "number",
                    "value": 1,
                    "timestamp": 1
                }
            ],
            "writable": false,
            "timestamp": 1
        }
    ]
}
```

The model describes a vehicle, which has a set of properties. This follows the same structure as the existing models, and is straight-forward to implement. 

First, go into the swagger.yml to add the new model under schemas and define the _Vehicle_ schema. 
There are predefined Mixin schemas defined, that define basic fields for models, such as _objectType_ or _uuid_. To make the example above work, a minimum inheritance definition must include _BaseModel_:

```
Vehicle:
  type: object
  allOf:
    - $ref: '#/components/schemas/BaseModel'
```  

If you look at the defintion of _BaseModel_, you'll find that the schema's defintion of properties does not contain the model's list of properties. Thus, it must defined in the _Vehicle_ schema like this: 

```

Vehicle:
  type: object
  allOf:
    - $ref: '#/components/schemas/BaseModel'
  properties:
    properties:
      type: array
      items:
        $ref: '#/components/schemas/SimplePropertyModel'
```

The basic representation of a property is described in the SimplePropertyModel, allowing to add properties with key, value, type, and timestamp. A descritption how to extend this model is below. 

To make the model's _properties_ attribute required (the parser throws and error if its missing in requests), add it to the required list:

```

Vehicle:
  type: object
  allOf:
    - $ref: '#/components/schemas/BaseModel'
  required:
    - properties
  properties:
    properties:
      type: array
      items:
        $ref: '#/components/schemas/SimplePropertyModel'
```

That's it for the defintion of the schema. Definitions of paths and operations does not require any special cases to be observerd to make generated code work, refer to the OpenApi docs for steps to define paths. 


# Generate and integrate code. 

Go the the directory of the swagger.yaml and run the following cli command to generate the code:

`swagger-codegen generate -i swagger.yaml -o generated_files -l python-flask`

Generated code files are in the ./generated_files folder. Copy the generatedf file for the vehicle model from the ./generated_files/swagger_server/models folder to the ../models/ folder. In this case, there should be a _vehicle.py_ file. 
To add KMS functionality (mostly the database representation) to the model, create a python file next to the vehicle.py file and name it vehicle_kms.py. 

Add the following code to  vehicle_kms.py:
```
from swagger_server.models.base_model_kms import KMSModelMixin
class KMSVehicle(KMSModelMixin):
    pass
```

In the vehicle.py file, add the KMSVehicle class as mixin to the Vehicle class: 

```
...
from swagger_server.models.vehicle_kms import KMSVehicle
class Vehicle(Model, KMSVehicle):
...
```

This includes code in the vehicle model, that allows KMS to generate the MongoEngine model during runtime. Existing models are generated when the server starts. To add vehicle to the list of created models, add it in main.py, at the end of the _import() method of ModelLoader:

```
def _import(self):
  ...
  VehicleModel().get_mongo_model()
```

This is necessary to add the mongo model to the MongoEngine repository, which would normally happen on import of a defined MongoEngine model. Since the mongo engine model classes here are generated in code, we need to add them in code, which is done here.

# Extend Models:

There are a few examples of models with different definitions in the swagger.yaml. If any schema is updated, run the generator again copy the generated models to the soruce folder. Add the defined KMS mixins (KMSVehicle) to the model classes (class Vehicle). 

# Extend properties
To extend the property class, a new property class must be defined. 

Add a new property to the sagger.yaml: 

``` 
    VehiclePropertyModel:
      oneOf:
        - $ref: '#/components/schemas/BooleanPropertyModel'
        - $ref: '#/components/schemas/NumberPropertyModel'
        - $ref: '#/components/schemas/StringPropertyModel'
        - $ref: '#/components/schemas/ArrayPropertyModel'
        - $ref: '#/components/schemas/StringListPropertyModel'
      properties:
        public:
          type: boolean
```

This extends the SimplePropertyModel with the property _public_ 

Change the schema defintion of the Vehicle model: 

```

Vehicle:
  type: object
  allOf:
    - $ref: '#/components/schemas/BaseModel'
  required:
    - properties
  properties:
    properties:
      type: array
      items:
        $ref: '#/components/schemas/VehiclePropertyModel'
```

Generate code, and copy both the vehicle.py and the vehicle_property_model.py to the source folder, following the same steps as above. 

Add a KMS Mixin for the new property (vehicle_property_model_kms.py) with the following code: 

```
from swagger_server.models.property_model_mixin import KMSPropertyModelMixin
class KMSVehiclePropertyMixin(KMSPropertyModelMixin):
    exclude_automated = ['value']
```

and change the class definition of the VehicleProperty class: 

```

class VehiclePropertyModel(Model, KMSVehicleProperty):
```

