# coding: utf-8

"""
    Yagna Activity API

    It conforms with capability level 1 of the [Activity API specification](https://docs.google.com/document/d/1BXaN32ediXdBHljEApmznSfbuudTU8TmvOmHKl0gmQM).  # noqa: E501

    The version of the OpenAPI document: v1
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401


from ya_activity.configuration import Configuration


class CreateActivityAllOf(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'agreement_id': 'str',
        'requestor_pub_key': 'str'
    }

    attribute_map = {
        'agreement_id': 'agreementId',
        'requestor_pub_key': 'requestorPubKey'
    }

    def __init__(self, agreement_id=None, requestor_pub_key=None, local_vars_configuration=None):  # noqa: E501
        """CreateActivityAllOf - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._agreement_id = None
        self._requestor_pub_key = None
        self.discriminator = None

        if agreement_id is not None:
            self.agreement_id = agreement_id
        if requestor_pub_key is not None:
            self.requestor_pub_key = requestor_pub_key

    @property
    def agreement_id(self):
        """Gets the agreement_id of this CreateActivityAllOf.  # noqa: E501


        :return: The agreement_id of this CreateActivityAllOf.  # noqa: E501
        :rtype: str
        """
        return self._agreement_id

    @agreement_id.setter
    def agreement_id(self, agreement_id):
        """Sets the agreement_id of this CreateActivityAllOf.


        :param agreement_id: The agreement_id of this CreateActivityAllOf.  # noqa: E501
        :type: str
        """

        self._agreement_id = agreement_id

    @property
    def requestor_pub_key(self):
        """Gets the requestor_pub_key of this CreateActivityAllOf.  # noqa: E501


        :return: The requestor_pub_key of this CreateActivityAllOf.  # noqa: E501
        :rtype: str
        """
        return self._requestor_pub_key

    @requestor_pub_key.setter
    def requestor_pub_key(self, requestor_pub_key):
        """Sets the requestor_pub_key of this CreateActivityAllOf.


        :param requestor_pub_key: The requestor_pub_key of this CreateActivityAllOf.  # noqa: E501
        :type: str
        """

        self._requestor_pub_key = requestor_pub_key

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in self.openapi_types.items():
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(
                    map(lambda x: x.to_dict() if hasattr(x, "to_dict") else x, value)
                )
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(
                    map(
                        lambda item: (item[0], item[1].to_dict())
                        if hasattr(item[1], "to_dict")
                        else item,
                        value.items(),
                    )
                )
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, CreateActivityAllOf):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CreateActivityAllOf):
            return True

        return self.to_dict() != other.to_dict()
