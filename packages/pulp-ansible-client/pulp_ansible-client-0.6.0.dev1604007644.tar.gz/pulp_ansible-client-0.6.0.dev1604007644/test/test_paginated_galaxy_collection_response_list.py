# coding: utf-8

"""
    Pulp 3 API

    Fetch, Upload, Organize, and Distribute Software Packages  # noqa: E501

    The version of the OpenAPI document: v3
    Contact: pulp-list@redhat.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import pulpcore.client.pulp_ansible
from pulpcore.client.pulp_ansible.models.paginated_galaxy_collection_response_list import PaginatedGalaxyCollectionResponseList  # noqa: E501
from pulpcore.client.pulp_ansible.rest import ApiException

class TestPaginatedGalaxyCollectionResponseList(unittest.TestCase):
    """PaginatedGalaxyCollectionResponseList unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test PaginatedGalaxyCollectionResponseList
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = pulpcore.client.pulp_ansible.models.paginated_galaxy_collection_response_list.PaginatedGalaxyCollectionResponseList()  # noqa: E501
        if include_optional :
            return PaginatedGalaxyCollectionResponseList(
                count = 123, 
                next = 'http://api.example.org/accounts/?page=4', 
                previous = 'http://api.example.org/accounts/?page=2', 
                results = [
                    pulpcore.client.pulp_ansible.models.galaxy_collection_response.GalaxyCollectionResponse(
                        id = '0', 
                        name = '0', 
                        namespace = pulpcore.client.pulp_ansible.models.namespace.namespace(), 
                        href = '0', 
                        versions_url = '0', 
                        created = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        modified = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        latest_version = pulpcore.client.pulp_ansible.models.latest_version.latest_version(), )
                    ]
            )
        else :
            return PaginatedGalaxyCollectionResponseList(
        )

    def testPaginatedGalaxyCollectionResponseList(self):
        """Test PaginatedGalaxyCollectionResponseList"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
