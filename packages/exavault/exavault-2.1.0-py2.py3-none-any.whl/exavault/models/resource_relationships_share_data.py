# coding: utf-8

"""
    ExaVault API

    See our API reference documentation at https://www.exavault.com/developer/api-docs/  # noqa: E501

    OpenAPI spec version: 2.0
    Contact: support@exavault.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class ResourceRelationshipsShareData(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'id': 'int',
        'type': 'str'
    }

    attribute_map = {
        'id': 'id',
        'type': 'type'
    }

    def __init__(self, id=None, type=None):  # noqa: E501
        """ResourceRelationshipsShareData - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._type = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if type is not None:
            self.type = type

    @property
    def id(self):
        """Gets the id of this ResourceRelationshipsShareData.  # noqa: E501


        :return: The id of this ResourceRelationshipsShareData.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ResourceRelationshipsShareData.


        :param id: The id of this ResourceRelationshipsShareData.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def type(self):
        """Gets the type of this ResourceRelationshipsShareData.  # noqa: E501


        :return: The type of this ResourceRelationshipsShareData.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this ResourceRelationshipsShareData.


        :param type: The type of this ResourceRelationshipsShareData.  # noqa: E501
        :type: str
        """

        self._type = type

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(ResourceRelationshipsShareData, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ResourceRelationshipsShareData):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
