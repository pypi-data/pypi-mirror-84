# coding: utf-8

"""
    Yagna Activity API

    It conforms with capability level 1 of the [Activity API specification](https://docs.google.com/document/d/1BXaN32ediXdBHljEApmznSfbuudTU8TmvOmHKl0gmQM).  # noqa: E501

    The version of the OpenAPI document: v1
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import ya_activity
from ya_activity.models.credentials import Credentials  # noqa: E501
from ya_activity.rest import ApiException

class TestCredentials(unittest.TestCase):
    """Credentials unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test Credentials
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = ya_activity.models.credentials.Credentials()  # noqa: E501
        if include_optional :
            return Credentials(
                sgx = ya_activity.models.sgx_credentials.SgxCredentials(
                    enclave_pub_key = '0', 
                    requestor_pub_key = '0', 
                    payload_hash = '0', 
                    ias_report = '0', 
                    ias_sig = '0', )
            )
        else :
            return Credentials(
                sgx = ya_activity.models.sgx_credentials.SgxCredentials(
                    enclave_pub_key = '0', 
                    requestor_pub_key = '0', 
                    payload_hash = '0', 
                    ias_report = '0', 
                    ias_sig = '0', ),
        )

    def testCredentials(self):
        """Test Credentials"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
