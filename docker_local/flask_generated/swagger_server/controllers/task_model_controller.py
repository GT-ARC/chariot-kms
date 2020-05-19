from swagger_server.controllers.base_controller import BaseController, kafka_add, kafka_update
from swagger_server.models.task_model import TaskModel  # noqa: E501
from swagger_server.models.task_property_model import TaskPropertyModel
from swagger_server.serializer.model_serializer import ModelSerializer
from swagger_server.serializer.property_model_serializer import PropertyModelSerializer


def delete_task(uuid):  # noqa: E501
    """delete_task

    Delete task # noqa: E501

    :param uuid: 
    :type uuid: str

    :rtype: None
    """
    return BaseController.delete_model(TaskModel, 'uuid', uuid)


def get_all_tasks():  # noqa: E501
    """get a list of all tasks

     # noqa: E501


    :rtype: List[TaskModel]
    """
    return BaseController.get_list_view(TaskModel, ModelSerializer)


def get_task_detail(uuid):  # noqa: E501
    """Task Detail View

     # noqa: E501

    :param uuid: 
    :type uuid: str

    :rtype: TaskModel
    """
    return BaseController.get_detail_view(TaskModel, ModelSerializer, 'uuid', uuid)


def get_task_property_detail(task_uuid, key):  # noqa: E501
    """Get single property of task

     # noqa: E501

    :param task_uuid:
    :type task_uuid: str
    :param key:
    :type key: str

    :rtype: TaskModel
    """
    
    if task_uuid is not None:
        task = BaseController.get_db_model(TaskModel, 'uuid', task_uuid)
        return BaseController.get_nested_list_item_with_route(task, 'properties', 'key', key, ModelSerializer)
    
    return {}, 404


def get_task_property_list(task_uuid):  # noqa: E501
    """Get all properties of task

     # noqa: E501

    :param task_uuid:
    :type task_uuid: str

    :rtype: TaskModel
    """
    if task_uuid is not None:
        task, code = BaseController.get_detail_view(TaskModel, ModelSerializer, 'uuid', task_uuid)
        
        return task['properties'], 200
    
    return {}, 404


@kafka_add(serializer=ModelSerializer, endpoint='skills')
def task_add(body):  # noqa: E501
    """Create task

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: TaskModel
    """
    return BaseController.add_model_with_properties(body, TaskModel, TaskPropertyModel, 'uuid', ModelSerializer)


@kafka_update(serializer=ModelSerializer)
def update_task_model(body, uuid):  # noqa: E501
    """update_task_model

    Update task model # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param uuid: 
    :type uuid: str

    :rtype: TaskModel
    """
    return BaseController.update_model_with_properties(TaskModel, body, TaskPropertyModel, uuid, get_task_detail)


@kafka_update(serializer=PropertyModelSerializer)
def update_task_property(body, task_uuid, key):  # noqa: E501
    """Updates the task property model, use this to add values to single property

     # noqa: E501

    :param body:
    :type body: dict | bytes
    :param task_uuid:
    :type task_uuid: str
    :param key:
    :type key: str

    :rtype: None
    """
    return BaseController.update_model_property(TaskModel, body, TaskPropertyModel, task_uuid, key,
                                                get_task_property_detail)

# TODO add history
