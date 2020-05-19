# coding: utf-8

from __future__ import absolute_import

from flask import json

from swagger_server.models.device_model import DeviceModel  # noqa: E501
from swagger_server.models.device_property_model import DevicePropertyModel  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDeviceModelController(BaseTestCase):
    """DeviceModelController integration test stubs"""
    
    def test_delete_device(self):
        """Test case for delete_device

        Deletes the device model identified by device_id
        """
        response = self.client.open(
            '/v1/devices/{device_id}'.format(device_id='device_id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
    
    def test_device_nested_property_bulk_update(self):
        """Test case for device_nested_property_bulk_update

        Bulk update of nested property
        """
        body = None
        response = self.client.open(
            '/v1/devices/{device_id}/properties/{key1}/properties/{key2}/bulk_update'.format(
                device_id='device_id_example', key1='key1_example', key2='key2_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
    
    def test_device_property_bulk_update(self):
        """Test case for device_property_bulk_update

        Bulk update of property values
        """
        body = None
        response = self.client.open(
            '/v1/devices/{device_id}/properties/{key}/bulk_update'.format(device_id='device_id_example',
                                                                          key='key_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
    
    def test_devices_post(self):
        """Test case for devices_post

        Adds a new DeviceModel
        """
        body = DeviceModel()
        response = self.client.open(
            '/v1/devices',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
    
    def test_get_all_devices(self):
        """Test case for get_all_devices

        Lists all registered devices (objectType is actuator, sensor)
        """
        response = self.client.open(
            '/v1/devices',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
    
    def test_get_device(self):
        """Test case for get_device

        Gets a device by its ID
        """
        response = self.client.open(
            '/v1/devices/{device_id}'.format(device_id='device_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
    
    def test_get_device_history(self):
        """Test case for get_device_history

        All recorded values for this device
        """
        response = self.client.open(
            '/v1/devices/{device_id}/history'.format(device_id='device_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
    
    def test_get_device_nested_property(self):
        """Test case for get_device_nested_property

        Gets a property identified by {key} of a device identified by {id}
        """
        response = self.client.open(
            '/v1/devices/{device_id}/properties/{key1}/properties/{key2}'.format(device_id='device_id_example',
                                                                                 key1='key1_example',
                                                                                 key2='key2_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
    
    def test_get_device_property(self):
        """Test case for get_device_property

        Gets a property identified by {key} of a device identified by {id}
        """
        response = self.client.open(
            '/v1/devices/{device_id}/properties/{key}'.format(device_id='device_id_example', key='key_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
    
    def test_get_device_property_history(self):
        """Test case for get_device_property_history

        All recorded values for this device
        """
        response = self.client.open(
            '/v1/devices/{device_id}/properties/{key}/history'.format(device_id='device_id_example', key='key_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
    
    def test_update_device(self):
        """Test case for update_device

        Updates the device model, use this to add values
        """
        body = DeviceModel()
        response = self.client.open(
            '/v1/devices/{device_id}'.format(device_id='device_id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
    
    def test_update_device_property(self):
        """Test case for update_device_property

        Updates the property model identified by key of the device identified by device_id
        """
        body = DevicePropertyModel()
        response = self.client.open(
            '/v1/devices/{device_id}/properties/{key}'.format(device_id='device_id_example', key='key_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
    
    def test_update_nested_device_property(self):
        """Test case for update_nested_device_property

        Updates the nested property identified by key2 of property model identified by key1 of the device identified by device_id
        """
        body = DevicePropertyModel()
        response = self.client.open(
            '/v1/devices/{device_id}/properties/{key1}/properties/{key2}'.format(device_id='device_id_example',
                                                                                 key1='key1_example',
                                                                                 key2='key2_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    
    unittest.main()
