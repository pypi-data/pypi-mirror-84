# coding: utf-8

"""
    Yagna Market API

     ## Yagna Market The Yagna Market is a core component of the Yagna Network, which enables computational Offers and Demands circulation. The Market is open for all entities willing to buy computations (Demands) or monetize computational resources (Offers). ## Yagna Market API The Yagna Market API is the entry to the Yagna Market through which Requestors and Providers can publish their Demands and Offers respectively, find matching counterparty, conduct negotiations and make an agreement.  This version of Market API conforms with capability level 1 of the <a href=\"https://docs.google.com/document/d/1Zny_vfgWV-hcsKS7P-Kdr3Fb0dwfl-6T_cYKVQ9mkNg\"> Market API specification</a>.  Market API contains two roles: Requestors and Providers which are symmetrical most of the time (excluding agreement phase).   # noqa: E501

    The version of the OpenAPI document: 1.6.0
    Generated by: https://openapi-generator.tech
"""


import unittest
import datetime

import ya_market
from ya_market.models.event import Event  # noqa: E501
from ya_market.rest import ApiException


class TestEvent(unittest.TestCase):
    """Event unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test Event
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = ya_market.models.event.Event()  # noqa: E501
        if include_optional:
            return Event(
                event_type="0",
                event_date=datetime.datetime.strptime(
                    "2013-10-20 19:20:30.00", "%Y-%m-%d %H:%M:%S.%f"
                ),
            )
        else:
            return Event(
                event_type="0",
                event_date=datetime.datetime.strptime(
                    "2013-10-20 19:20:30.00", "%Y-%m-%d %H:%M:%S.%f"
                ),
            )

    def testEvent(self):
        """Test Event"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()
