# coding: utf-8

from __future__ import absolute_import

from flask import json

from swagger_server.models.service_model import ServiceModel  # noqa: E501
from swagger_server.test import BaseTestCase


class TestServiceModelController(BaseTestCase):
    """ServiceModelController integration test stubs"""
    
    def test_delete_service(self):
        """Test case for delete_service

        Deletes the service model identified by service_id
        """
        response = self.client.open(
            '/v1/services/{service_id}'.format(service_id='service_id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
    
    def test_get_all_services(self):
        """Test case for get_all_services

        Lists all registered services
        """
        response = self.client.open(
            '/v1/services',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
    
    def test_get_service(self):
        """Test case for get_service

        Gets a service by its ID
        """
        response = self.client.open(
            '/v1/services/{service_id}'.format(service_id='service_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
    
    def test_services_post(self):
        """Test case for services_post

        Adds a new ServiceModel
        """
        body = ServiceModel()
        response = self.client.open(
            '/v1/services',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
    
    def test_update_service(self):
        """Test case for update_service

        Updates the service model, use this to add values
        """
        body = ServiceModel()
        response = self.client.open(
            '/v1/services/{service_id}'.format(service_id='service_id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    
    unittest.main()
