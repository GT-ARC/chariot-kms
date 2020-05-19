import connexion

from swagger_server.controllers.base_controller import kafka_add, kafka_update, BaseController
from swagger_server.models.skill_model import SkillModel  # noqa: E501
from swagger_server.models.skill_property_model import SkillPropertyModel
from swagger_server.serializer.model_serializer import ModelSerializer
from swagger_server.serializer.property_model_serializer import PropertyModelSerializer


def delete_skill(skill_uuid):  # noqa: E501
    """Deletes the skill model identified by skill_uuid

     # noqa: E501

    :param skill_uuid: 
    :type skill_uuid: str

    :rtype: None
    """
    return BaseController.delete_model(SkillModel, 'uuid', skill_uuid)


def get_all_skills():  # noqa: E501
    """Lists all registered skills

     # noqa: E501


    :rtype: SkillModel
    """
    return BaseController.get_list_view(SkillModel, ModelSerializer)


def get_skill(skill_uuid):  # noqa: E501
    """Gets a skill by its uuid

     # noqa: E501

    :param skill_uuid: 
    :type skill_uuid: str

    :rtype: SkillModel
    """
    return BaseController.get_detail_view(SkillModel, ModelSerializer, 'uuid', skill_uuid)


def get_skill_property_detail(skill_uuid, key):  # noqa: E501
    """Get single property of skill

     # noqa: E501

    :param skill_uuid:
    :type skill_uuid: str
    :param key:
    :type key: str

    :rtype: SkillModel
    """
    req = connexion.request
    if skill_uuid is not None:
        skill = BaseController.get_db_model(SkillModel, 'uuid', skill_uuid)
        return BaseController.get_nested_list_item_with_route(skill, 'properties', 'key', key, ModelSerializer)
    
    return {}, 404


def get_skill_property_list(skill_uuid):  # noqa: E501
    """Get all properties of skill

     # noqa: E501

    :param skill_uuid:
    :type skill_uuid: str

    :rtype: SkillModel
    """
    if skill_uuid is not None:
        skill, code = BaseController.get_detail_view(SkillModel, ModelSerializer, 'uuid', skill_uuid)
        
        return skill['properties'], 200
    
    return {}, 404


@kafka_add(serializer=ModelSerializer, endpoint='skills')
def skills_post(body):  # noqa: E501
    """Adds a new SkillModel

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: SkillModel
    """
    return BaseController.add_model_with_properties(body, SkillModel, SkillPropertyModel, 'uuid', ModelSerializer)


@kafka_update(serializer=ModelSerializer)
def update_skill(body, skill_uuid):  # noqa: E501
    """Updates the skill model, use this to add values

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param skill_uuid: 
    :type skill_uuid: str

    :rtype: None
    """
    return BaseController.update_model_with_properties(SkillModel, body, SkillPropertyModel, skill_uuid, get_skill)


@kafka_update(serializer=PropertyModelSerializer)
def update_skill_property(body, skill_uuid, key):  # noqa: E501
    """Updates the skill property model, use this to add values to single property

     # noqa: E501

    :param body:
    :type body: dict | bytes
    :param skill_uuid:
    :type skill_uuid: str
    :param key:
    :type key: str

    :rtype: None
    """
    return BaseController.update_model_property(SkillModel, body, SkillPropertyModel, skill_uuid, key,
                                                get_skill_property_detail)
# TODO add history
